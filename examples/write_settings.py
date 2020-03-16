"""Example: draytekwebadmin write settings to router from a CSV file"""

import argparse
import csv
import logging
import time
from urllib.parse import urlparse
from pathlib import Path

from tabulate import tabulate

from draytekwebadmin import (
    DrayTekWebAdmin,
    SNMPIPv4,
    SNMPIPv6,
    SNMPTrapIPv4,
    SNMPTrapIPv6,
    SNMPv3,
    InternetAccessControl,
    AccessList,
    ManagementPort,
    BruteForceProtection,
    Encryption,
    CVM_AccessControl,
    DeviceManagement,
    AP_Management,
    LAN_Access,
    IPv6Management,
)

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
        "-c",
        "--config",
        type=dir_path,
        help=r"Location of configuration file directory e.g. -c c:\draytekwebadmin\conf",
    )
    parser.add_argument(
        "--browser",
        type=str,
        help="Browser name [chrome|firefox] overrides configuration file",
    )
    parser.add_argument(
        "--headless",
        action="store_true",
        help="Run session headless (without GUI). Overrides configuration file",
    )
    parser.add_argument(
        "--search_driver",
        action="store_true",
        help="Searches for browser driver in current directory, under conf or driver. Overrides configuration file",
    )
    parser.add_argument(
        "--implicit_wait",
        type=int,
        help="WebDriver implicit wait time (secs). Overrides configuration file",
    )
    parser.add_argument(
        "--explicit_wait",
        type=int,
        help="WebDriver explicit wait time (secs). Overrides configuration file",
    )
    parser.add_argument(
        "--debug",
        action="store_true",
        default=False,
        help="Errors will attempt to capture Web page",
    )
    return parser


def dir_path(string):
    if Path.exists(Path(string)):
        return string
    else:
        raise NotADirectoryError(string)


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


def configure_router(router, allow_reboot, test_settings):
    """ Apply router configuration specified

    :param router: row from CSV with settings for a single router
    :param allow_reboot: reboot router if required after config change
    :param test_settings: collection of test settings
    :return: webadmin_session
    :return: Configuration status message
    """
    webadmin_session = None
    reboot_required = False
    router_configure_status = ""

    try:
        settings = extract_settings(router)

        webadmin_session = settings["connection"]
        webadmin_session.config_dir = test_settings.config_dir
        webadmin_session.browser = test_settings.browser
        webadmin_session.headless = test_settings.headless
        webadmin_session.search_driver = test_settings.search_driver
        webadmin_session.implicit_wait_time = test_settings.implicit_wait_time
        webadmin_session.explcit_wait_time = test_settings.explicit_wait_time
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
                    if test_settings.what_if:
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
            if test_settings.debug:
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
    snmpipv6 = SNMPIPv6()
    snmp_trap_ipv4 = SNMPTrapIPv4()
    snmp_trap_ipv6 = SNMPTrapIPv6()
    snmpv3 = SNMPv3()
    iac = InternetAccessControl()
    access_list = AccessList()
    management_port = ManagementPort()
    brute_force = BruteForceProtection()
    encryption = Encryption()
    cvm_access = CVM_AccessControl()
    device_management = DeviceManagement()
    ap_management = AP_Management()
    lan_access = LAN_Access()
    ipv6_management = IPv6Management()
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
            elif modulename == type(snmpipv6).__name__.lower():
                if hasattr(snmpipv6, fieldname):
                    setattr(snmpipv6, fieldname, router_settings.get(key))
                else:
                    invalid = True
            elif modulename == type(snmp_trap_ipv4).__name__.lower():
                if hasattr(snmp_trap_ipv4, fieldname):
                    setattr(snmp_trap_ipv4, fieldname, router_settings.get(key))
                else:
                    invalid = True
            elif modulename == type(snmp_trap_ipv6).__name__.lower():
                if hasattr(snmp_trap_ipv6, fieldname):
                    setattr(snmp_trap_ipv6, fieldname, router_settings.get(key))
                else:
                    invalid = True
            elif modulename == type(snmpv3).__name__.lower():
                if hasattr(snmpv3, fieldname):
                    setattr(snmpv3, fieldname, router_settings.get(key))
                else:
                    invalid = True
            elif modulename == type(iac).__name__.lower():
                if hasattr(iac, fieldname):
                    setattr(iac, fieldname, router_settings.get(key))
                else:
                    invalid = True
            elif modulename == type(access_list).__name__.lower():
                if hasattr(access_list, fieldname):
                    setattr(access_list, fieldname, router_settings.get(key))
                else:
                    invalid = True
            elif modulename == type(management_port).__name__.lower():
                if hasattr(management_port, fieldname):
                    setattr(management_port, fieldname, router_settings.get(key))
                else:
                    invalid = True
            elif modulename == type(brute_force).__name__.lower():
                if hasattr(brute_force, fieldname):
                    setattr(brute_force, fieldname, router_settings.get(key))
                else:
                    invalid = True
            elif modulename == type(encryption).__name__.lower():
                if hasattr(encryption, fieldname):
                    setattr(encryption, fieldname, router_settings.get(key))
                else:
                    invalid = True
            elif modulename == type(cvm_access).__name__.lower():
                if hasattr(cvm_access, fieldname):
                    setattr(cvm_access, fieldname, router_settings.get(key))
                else:
                    invalid = True
            elif modulename == type(device_management).__name__.lower():
                if hasattr(device_management, fieldname):
                    setattr(device_management, fieldname, router_settings.get(key))
                else:
                    invalid = True
            elif modulename == type(ap_management).__name__.lower():
                if hasattr(ap_management, fieldname):
                    setattr(ap_management, fieldname, router_settings.get(key))
                else:
                    invalid = True
            elif modulename == type(lan_access).__name__.lower():
                if hasattr(lan_access, fieldname):
                    setattr(lan_access, fieldname, router_settings.get(key))
                else:
                    invalid = True
            elif modulename == type(ipv6_management).__name__.lower():
                if hasattr(ipv6_management, fieldname):
                    setattr(ipv6_management, fieldname, router_settings.get(key))
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
    settings["snmpipv6"] = snmpipv6
    settings["snmp_trap_ipv4"] = snmp_trap_ipv4
    settings["snmp_trap_ipv6"] = snmp_trap_ipv6
    settings["snmpv3"] = snmpv3
    settings["iac"] = iac
    settings["access_list"] = access_list
    settings["management_port"] = management_port
    settings["brute_force"] = brute_force
    settings["encryption"] = encryption
    settings["cvm_access"] = cvm_access
    settings["device_management"] = device_management
    settings["ap_management"] = ap_management
    settings["lan_access"] = lan_access
    settings["ipv6_managament"] = ipv6_management
    return settings


def create_template_csv(output_file):
    """Create a template CSV with just the data headers

    :param output_file: filename to save template as
    """
    raise NotImplementedError


def result_row_builder(session, status, router_name=None):
    """Generate data for results table
        :param session: Draytekwebadmin session object
        :param status: Status from performing write operations
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


class TestSettings:
    """Test Environment Settings"""

    def __init__(
        self,
        what_if=None,
        config_dir=None,
        browser=None,
        headless=None,
        search_driver=None,
        implicit_wait_time=None,
        explicit_wait_time=None,
        debug=False,
    ):
        """"Test Environment settings.

        :param what_if: Flag to indicate settings should not be applied, changes shown
        :param config_dir: Path to toolium configuration file
        :param browser: browser name to override configuration file
        :param headless: headless session, to override configuration file
        :param search_driver: search local directories for browser driver executables
        :param implicit_wait_time: WebDriver implicit wait time, override configuration file
        :param explicit_wait_time: WebDriver explicit wait time, override configuration file
        :param debug: flag to trigger debug behaviours
        """
        self.what_if = what_if
        self.config_dir = config_dir
        self.browser = browser
        self.headless = headless
        self.search_driver = search_driver
        self.implicit_wait_time = implicit_wait_time
        self.explicit_wait_time = explicit_wait_time
        self.debug = debug


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
            test_settings = TestSettings(
                what_if=args.whatif,
                config_dir=args.config,
                browser=args.browser,
                headless=args.headless,
                search_driver=args.search_driver,
                implicit_wait_time=args.implicit_wait,
                explicit_wait_time=args.explicit_wait,
                debug=args.debug,
            )
            datasource = read_csv(args.inputfile)

            # For each row attempt to configure router
            for router in datasource:
                (session, status) = configure_router(
                    router=router,
                    allow_reboot=args.reboot,
                    test_settings=test_settings,
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
