"""Example: draytekwebadmin write settings to router from a CSV file"""

import argparse
import csv
import logging
import time
from urllib.parse import urlparse

from tabulate import tabulate

from draytekwebadmin import DrayTekWebAdmin, SNMPIPv4, InternetAccessControl

LOGGER = logging.getLogger("root")
FORMAT = "[%(levelname)s] %(message)s"
logging.basicConfig(format=FORMAT)
LOGGER.setLevel(logging.ERROR)


def _get_parser():
    """Parse command line arguments.

    :returns: argparse object
    """
    parser = argparse.ArgumentParser(
        description="Write DrayTek router settings from a source CSV file."
    )
    parser.add_argument(
        "inputfile",
        nargs="?",
        type=str,
        help="Input CSV. Each router and config should be on it's own row",
    )
    parser.add_argument(
        "-t",
        "--template",
        type=str,
        help="Generate blank template CSV e.g. -t template.csv",
    )
    parser.add_argument(
        "-w",
        "--whatif",
        action="store_true",
        default=False,
        help="Show what changes would be made, does not make any change to current configuration",
    )
    parser.add_argument(
        "--no-reboot",
        dest="reboot",
        action="store_false",
        default=True,
        help="Do not reboot routers after configuration change, even if required",
    )
    parser.add_argument(
        "-d",
        "--debug",
        action="store_true",
        default=False,
        help="Errors will attempt to capture Web page",
    )
    return parser


def parse_address_url_to_host(address):
    """Convert URL to host, port and use HTTPs flag

    :param address: URL for Webadmin console
    :returns: host, port, useHTTPs tuple
    """
    url = urlparse(address)
    port = url.port
    https = True
    if url.scheme == "http":
        https = False
        if url.port is None:
            port = 80
    if url.scheme == "https" and url.port is None:
        port = 443
    return url.hostname, port, https


def read_csv(csvfilename):
    """Read data from CSV file into dictionary

    :param filename: output filename for csv
    :returns: dict_list - dictionary of csv contents
    """
    with open(csvfilename, newline="") as csvfile:
        reader = csv.DictReader(csvfile)
        dict_list = []
        for line in reader:
            dict_list.append(line)
    return dict_list


def diff(current, new):
    """ Compare two sets of router module settings

    :param current: current router settings
    :param new: router settings to be applied
    :returns: List of strings showing differences
    """
    differences = []
    # Convert to dictionary
    dict_current = vars(current)
    dict_new = vars(new)
    if dict_current == dict_new:
        LOGGER.debug(f"Dictionaries are the same")
    else:
        different_keys = set(dict_current.keys()) ^ set(dict_new.keys())
        common_keys = set(dict_current.keys()) - (
            set(dict_current.keys()) - set(dict_new.keys())
        )
        if different_keys:
            differences.append(f"Unexpected keys: {different_keys}")
        for key in common_keys:
            if dict_current[key] != dict_new[key]:
                # None is the same as False and an empty value, so exclude from differences as should be falsey
                if (dict_current[key]) or (dict_new[key]):
                    differences.append(
                        f"{key}: CURRENT = {dict_current[key]} | NEW = {dict_new[key]}"
                    )
    return differences


def configure_router(router, allow_reboot, whatif=False, debug=False):
    """ Apply router configuration specified

    :param router: row from CSV with settings for a single router
    :param allow_reboot: reboot router if required after config change
    :param whatif: Compares settings does not write changes to router
    :param debug: write a debug files of the page source on exception
    :return: webadmin_session
    :return: Configuration status message
    """
    webadmin_session = None
    reboot_required = False
    router_configure_status = ""

    try:
        settings = extract_settings(router)

        webadmin_session = settings["connection"]
        # Not strictly needed, since configuring modules will trigger connect.
        # But this way we can ensure we ensure we can connect outside the for loop.
        webadmin_session.start_session()
        for modulename in settings:
            LOGGER.debug(f"Processing modulename: {modulename}")
            if modulename not in ("connection", "info"):  # Ignore these
                newsettings = settings[modulename]
                LOGGER.info(
                    f"Module: {modulename} of type {type(newsettings)} found. Applying settings"
                )
                current = webadmin_session.read_settings(type(settings[modulename]))
                differences = diff(current, newsettings)
                if len(differences) > 0:
                    if whatif:
                        for change in differences:
                            router_configure_status = (
                                "WhatIf Mode - Changes not applied"
                            )
                            print(
                                f"[WhatIf] {webadmin_session.hostname} : {modulename} - {change}"
                            )
                    else:
                        reboot_requested = webadmin_session.write_settings(newsettings)
                        router_configure_status = "Updated"
                        if reboot_requested:
                            reboot_required = True
                else:
                    router_configure_status = "No changes required"
        if reboot_required:
            LOGGER.info("Router Reboot required to apply configuration changes")
            if allow_reboot:
                LOGGER.info(f"Rebooting Router: {webadmin_session.hostname}")
                webadmin_session.reboot_router()
                router_configure_status = "Updated & router restarted"
            else:
                router_configure_status = "Updated. REBOOT REQUIRED"
                print(
                    f"Reboot required to complete configuration of {webadmin_session.hostname}"
                )
        else:
            print(f"Router: {webadmin_session.hostname} - Reconfiguration completed")

        return webadmin_session, router_configure_status

    except Exception as exception:
        LOGGER.critical(exception)
        if webadmin_session is not None:
            if debug:
                timestamp = time.strftime("%Y%m%d-%H%M%S")
                # Collect the information from the session object and close it before attempting file access in case that fails
                # This avoids having another try/except/finally block within this error handling routine.
                hostname = webadmin_session.hostname
                page_source = webadmin_session.session.driver.page_source
                webadmin_session.close_session()

                debugfile = open(
                    f"draytek_write_settings_debug-{hostname}-{timestamp}.html", "w+"
                )
                debugfile.write(page_source)
                debugfile.close()
        return webadmin_session, router_configure_status


def extract_settings(router_settings, separator="|"):
    """Extracts settings from csv file into dictionaries. Logs errors if unexpected modulenames found in header.

    :param router: row from CSV with settings for a single router
    :param separator: character used to separate modules from fields (default '|')
    :returns: settings - dictionary of dictionaries containing extracted data from csv
    """
    connection = DrayTekWebAdmin()
    info = {}
    snmpipv4 = SNMPIPv4()
    iac = InternetAccessControl()
    invalid = False
    try:
        for key in router_settings.keys():
            modulename, fieldname = key.split(sep=separator)
            modulename = modulename.lower()
            if modulename == type(connection).__name__.lower():
                if hasattr(connection, fieldname):
                    setattr(connection, fieldname, router_settings.get(key))
                else:
                    invalid = True
            elif modulename == "routerinfo":
                info[fieldname] = router_settings.get(key)
            elif modulename == type(snmpipv4).__name__.lower():
                if hasattr(snmpipv4, fieldname):
                    setattr(snmpipv4, fieldname, router_settings.get(key))
                else:
                    invalid = True
            elif modulename == type(iac).__name__.lower():
                if hasattr(iac, fieldname):
                    setattr(iac, fieldname, router_settings.get(key))
                else:
                    invalid = True
            if invalid:
                LOGGER.error(f"Ignoring unexpected field: {modulename}|{fieldname}")
                invalid = False
    except AttributeError as e:
        LOGGER.error(f"Error parsing CSV contents. {e}")
    settings = dict()
    settings["connection"] = connection
    settings["info"] = info
    settings["snmpipv4"] = snmpipv4
    settings["iac"] = iac
    return settings


def create_template_csv(output_file):
    """Create a template CSV with just the data headers

    :param output_file: filename to save template as
    """
    raise NotImplementedError


def result_row_builder(session, status, router_name=None):
    """Generate data for results table
        :param session: Draytekwebadmin session object
        :param status: Status from perfoming write operations
        :param router_name: (optional): Router name from source CSV file, for if connection fails
        :return: row list of fields
    """
    row = [""]
    if (session) and (len(status) > 0):
        row = [
            session.hostname,
            session.routerinfo.model,
            session.routerinfo.router_name,
            status,
        ]
    elif session:
        if session.routerinfo:
            row = [
                session.hostname,
                session.routerinfo.model,
                session.routerinfo.router_name,
                "ERROR in WebSession",
            ]
        else:
            row = [session.hostname, "", "", "ERROR - Unable to Login"]
    elif (router_name) and (len(status) > 0):
        row = [router_name, "", "", status]
    elif len(status) > 0:
        row = ["Unknown", "", "", status]
    elif router_name:
        row = [router_name, "", "", "ERROR!"]
    else:
        row = ["Unknown", "", "", "ERROR!"]
    return row


class results_table:
    """Results Table."""

    def __init__(self, headers):
        """Create a table for showing results."""

        self._table = [""]
        self.headers = headers

    def add_row(self, row):
        """Add a row to the results table.

        :param row: list of result fields
        """
        self._table.append(row)

    def print(self):
        """Print the results table with headers."""
        print(tabulate(self._table, headers=self.headers, showindex=True))


def main():
    """Main. Called when program called directly from the command line.

    """
    results = results_table(headers=["Index", "Router", "Model", "Name", "Status"])
    session = None
    argv = None
    parser = _get_parser()
    args = parser.parse_args(argv)
    if args.template:
        create_template_csv(args.template)
    elif args.inputfile:
        try:
            datasource = read_csv(args.inputfile)

            # For each row attempt to configure router
            for router in datasource:
                (session, status) = configure_router(
                    router=router,
                    allow_reboot=args.reboot,
                    whatif=args.whatif,
                    debug=args.debug,
                )
                results.add_row(result_row_builder(session, status))
                results.print()
                session.close_session()
        except FileNotFoundError:
            LOGGER.critical(f"Input file not found: {args.inputfile}")
        except Exception as e:
            if session:
                results.add_row(result_row_builder(session, status, router))
            LOGGER.critical(f"Error: {e}")
        finally:
            if session is not None:
                session.close_session()
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
