"""Example: draytekwebadmin write settings to router from a CSV file"""

import argparse
import csv
import logging
from urllib.parse import urlparse

from draytekwebadmin import DrayTekWebAdmin, SNMPIPv4, InternetAccessControl

LOGGER = logging.getLogger("root")
FORMAT = "[%(levelname)s] %(message)s"
logging.basicConfig(format=FORMAT)
LOGGER.setLevel(logging.WARNING)


def _get_parser():
    """Parse command line arguments.

    Args:
        None

    Returns:
        parser: argparse object

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
        "--not-headless",
        dest="headless",
        action="store_false",
        default=True,
        help="Show the browser session, do not run headless",
    )
    parser.add_argument(
        "--no-reboot",
        dest="reboot",
        action="store_false",
        default=True,
        help="Do not reboot routers after configuration change, even if required",
    )
    return parser


def parse_address_url_to_host(address):
    """Convert URL to host, port and use HTTPs flag

    Args:
        address: URL for Webadmin console

    Returns:
        host, port, useHTTPs tuple

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

    Args:
        filename: output filename for csv

    Returns:
        dict_list: dictionary of csv contents

    """
    with open(csvfilename, newline="") as csvfile:
        reader = csv.DictReader(csvfile)
        dict_list = []
        for line in reader:
            dict_list.append(line)
    return dict_list


def diff(current, new):
    """ Compare two sets of router module settings

    Args:
        current: current router settings
        new: router settings to be applied

    Returns:
        List of strings showing differences

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
                differences.append(
                    f"{key}: CURRENT = {dict_current[key]} | NEW = {dict_new[key]}"
                )
    return differences


def configure_router(router, allow_reboot, headless=True, whatif=False):
    """ Apply router configuration specified

    Args:
        router: row from CSV with settings for a single router
        allow_reboot: reboot router if required after config change
        headless: display of browser session when interacting with router
        whatif: Compares settings does not write changes to router

    Returns:
        None

    """
    webadmin_session = None
    reboot_required = False

    try:
        settings = extract_settings(router)

        webadmin_session = settings["connection"]
        webadmin_session.headless = headless
        # Not strictly needed, since configuring modules will trigger connect.
        # But this way we can ensure we ensure we can connect ourside the for loop.
        webadmin_session.start_session()
        for modulename in settings:
            LOGGER.debug(f"Processing modulename: {modulename}")
            if modulename not in ("connection", "info"):  # Ignore these
                newsettings = settings[modulename]
                LOGGER.info(
                    f"Module: {modulename} of type {type(newsettings)} found. Applying settings"
                )
                if whatif:
                    current = webadmin_session.read_settings(type(settings[modulename]))
                    differences = diff(current, newsettings)
                    for change in differences:
                        print(
                            f"[WhatIf] {webadmin_session.hostname} : {modulename} - {change}"
                        )
                else:
                    reboot_requested = webadmin_session.write_settings(newsettings)
                    if reboot_requested:
                        reboot_required = True
        if reboot_required:
            LOGGER.info("Router Reboot required to apply configuration changes")
            if allow_reboot:
                LOGGER.info(f"Rebooting Router: {webadmin_session.hostname}")
                webadmin_session.reboot_router()
            else:
                print(
                    f"Reboot required to complete configuration of {webadmin_session.hostname}"
                )
        else:
            print(f"Router: {webadmin_session.hostname} - Reconfiguration completed")
        # TODO: Have a list of completed devices, and ones with pending reboots, report sucess or fail?

    except RuntimeError as exception:
        LOGGER.critical(exception)
    finally:
        if webadmin_session is not None:
            webadmin_session.close_session()


def extract_settings(router_settings, separator="|"):
    """Extracts settings from csv file into dictionaries. Logs errors if unexpected modulenames found in header.

    Args:
        router: row from CSV with settings for a single router
        separator: character used to separate modules from fields (default '|')

    Returns:
        settings: dictionary of dictionaries containing extracted data from csv

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

    Args:
        output_file: filename to save template as

    Returns:
        None

    """
    raise NotImplementedError


def main():
    """Main. Called when program called directly from the command line.

    Args:
        None

    Returns:
        None

    """
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
                configure_router(
                    router=router,
                    allow_reboot=args.reboot,
                    headless=args.headless,
                    whatif=args.whatif,
                )
        except FileNotFoundError:
            LOGGER.critical(f"Input file not found: {args.inputfile}")
        # TODO:
        # Parallel execution

    else:
        parser.print_help()


if __name__ == "__main__":
    main()
