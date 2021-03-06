"""Example: draytekwebadmin mass upgrade router firmware from a CSV file"""

import argparse
import csv
import logging
import time
from os import getcwd
from pathlib import Path

from tabulate import tabulate

from draytekwebadmin import DrayTekWebAdmin, Firmware

LOGGER = logging.getLogger("root")
FORMAT = "[%(levelname)s] %(message)s"
logging.basicConfig(format=FORMAT)
LOGGER.setLevel(logging.ERROR)


def _get_parser():
    """Parse command line arguments.

    :returns: argparse object
    """
    parser = argparse.ArgumentParser(
        description="Upgrade Draytek Router firmware from a source CSV file"
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
        "-u",
        "--upgrade",
        action="store_true",
        default=False,
        help="Perform firmware upgrade (inc reboot), preview only",
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


def read_csv(csvfilename):
    """Read data from CSV file into dictionary

    :param filename: output filename for csv
    :returns: dictionary of csv contents
    """
    with open(csvfilename, newline="") as csvfile:
        reader = csv.DictReader(csvfile)
        dict_list = []
        for line in reader:
            dict_list.append(line)
    return dict_list


def check_upgrade_router(router, test_settings):
    """Check Upgrade firmware on Draytek Router

    :param router: row from CSV with settings for a single router
    :param test_settings: collection of test settings
    :returns: DraytekWebAdmin Session object
    :returns: DraytekWebAdmin Firmware object
    """
    webadmin_session = None
    preview = None

    try:
        settings = extract_settings(router, test_settings.config_dir)

        webadmin_session = settings["connection"]
        webadmin_session.browser = test_settings.browser
        webadmin_session.headless = test_settings.headless
        webadmin_session.search_driver = test_settings.search_driver
        webadmin_session.implicit_wait_time = test_settings.implicit_wait_time
        webadmin_session.explcit_wait_time = test_settings.explicit_wait_time
        preview = webadmin_session.upgrade_preview(
            Firmware(filepath=settings["firmware"].filepath)
        )
        return webadmin_session, preview

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
                    f"draytek_upgrade_debug-{hostname}-{timestamp}.html", "w+"
                )
                debugfile.write(page_source)
                debugfile.close()
            else:
                webadmin_session.close_session()
            return webadmin_session, preview
        return None, None


def extract_settings(router_settings, config_dir=None, delimiter="|"):
    """Extracts connection settings and firmware details from csv.
       Logs errors if unexpected modulenames found in header.

    :param router: row from CSV with settings for a single router
    :param config_dir: path to configuration file for toolium
    :param delimiter: character used to separate modules from fields (default '|')
    :returns: dictionary of dictionaries containing extracted data from csv
    """
    if not config_dir:
        LOGGER.debug("Config directory not specified. Attempt to use cwd \\ conf")
        config_dir = Path(getcwd(), "conf")
    if Path.exists(Path(config_dir)):
        LOGGER.info(f"Setting configuration Directory to: {config_dir}")
        config_dir = str(Path(config_dir))
    else:
        config_dir = None

    connection = DrayTekWebAdmin(config_dir=config_dir)
    router_firmware = Firmware()
    invalid = False
    try:
        for key in router_settings.keys():
            modulename, fieldname = key.split(sep=delimiter)
            modulename = modulename.lower()
            if modulename == type(connection).__name__.lower():
                if hasattr(connection, fieldname):
                    setattr(connection, fieldname, router_settings.get(key))
                else:
                    invalid = True
            elif modulename == type(router_firmware).__name__.lower():
                if hasattr(router_firmware, fieldname):
                    setattr(router_firmware, fieldname, router_settings.get(key))
                else:
                    invalid = True
            if invalid:
                LOGGER.error(f"Ignoring unexpected field: {modulename}|{fieldname}")
                invalid = False
    except AttributeError as e:
        LOGGER.error(f"Error parsing CSV contents. {e}")
    settings = dict()
    settings["connection"] = connection
    settings["firmware"] = router_firmware
    return settings


def create_template_csv(output_file):
    """Create a template CSV with just the data headers

    :param output_file: filename to save template as
    """
    LOGGER.info(f"Outputfile {output_file}")
    # Get connection properties to save to CSV useful for later scripted changes
    wanted_session_properties = [
        "DrayTekWebAdmin|url",
        "DrayTekWebAdmin|hostname",
        "DrayTekWebAdmin|port",
        "DrayTekWebAdmin|use_https",
        "DrayTekWebAdmin|username",
        "DrayTekWebAdmin|password",
    ]
    wanted_firmware_properties = ["Firmware|filepath"]

    connection_info = {element: None for element in wanted_session_properties}
    firmware_info = {element: None for element in wanted_firmware_properties}

    data = {**connection_info, **firmware_info}

    with open(output_file, "w", newline="") as outfile:
        csvfile = csv.DictWriter(outfile, data.keys(), dialect="excel")
        csvfile.writeheader()


def upgrade_router(router, test_settings):
    """Upgrade router firmware, or preview potential upgrade

    :param router: connection information from csv input file
    :param test_settings: collection of test settings
    :return: webadmin_session
    :return: router firmware object
    :return: Upgrade status message
    :return: Upgrade required Boolean
    """

    session = None
    router_firmware = None
    upgrade_status_message = None
    upgrade_required = False
    try:
        (session, router_firmware) = check_upgrade_router(
            router=router, test_settings=test_settings
        )
        if (session) and (router_firmware):  # Both values not None
            if (router_firmware.router_firmware_upgradable()) or (
                router_firmware.modem_firmware_upgradable()
            ):
                if test_settings.upgrade:
                    upgrade_status_message = "UPGRADED!"
                    LOGGER.info(f"Router {session.hostname} - Upgrading Router")
                    session.upgrade(router_firmware)
                else:
                    upgrade_required = True
                    upgrade_status_message = "Upgrade Required"
            else:
                upgrade_status_message = "N/A"
                LOGGER.info(f"Router {session.hostname} - Firmware up-to-date")
        else:
            upgrade_status_message = "ERROR: Unable to access Firmware information"
            LOGGER.info(
                f"Router {session.hostname} - Unable to access Firmware information"
            )
        return session, router_firmware, upgrade_status_message, upgrade_required
    finally:
        return session, router_firmware, upgrade_status_message, upgrade_required


def result_row_builder(session, status, firmware=None, router_name=None):
    """Generate data for results table

        :param session: Draytekwebadmin session object
        :param status: Status from performing write operations
        :param firmware: Draytekwebadmin firmware object
        :param router_name: (optional): Router name from source CSV file, for if connection fails
        :return: row list of fields
    """
    row = [""]
    if (session) and (firmware) and (len(status) > 0):
        row = [
            session.hostname,
            session.routerinfo.model,
            session.routerinfo.router_name,
            firmware.firmware_current,
            firmware.modem_firmware_current.split()[0],
            firmware.firmware_target,
            firmware.modem_firmware_target.split()[0],
            status,
        ]
    elif (session) and (len(status) > 0):
        row = [session.hostname, "", "", "", "", "", "", status]
    elif session:
        row = [session.hostname, "", "", "", "", "", "", "ERROR!"]
    elif router_name:
        row = [router_name, "", "", "", "", "", "", "ERROR!"]
    else:
        row = ["Unknown", "", "", "", "", "", "", "ERROR!"]
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
        upgrade=None,
        config_dir=None,
        browser=None,
        headless=None,
        search_driver=None,
        implicit_wait_time=None,
        explicit_wait_time=None,
        debug=False,
    ):
        """"Test Environment settings.

        :param upgrade: Flag to upgrade should not be attempted or just previewed
        :param config_dir: Path to toolium configuration file
        :param browser: browser name to override configuration file
        :param headless: headless session, to override configuration file
        :param search_driver: search local directories for browser driver executables
        :param implicit_wait_time: WebDriver implicit wait time, override configuration file
        :param explicit_wait_time: WebDriver explicit wait time, override configuration file
        :param debug: flag to trigger debug behaviours
        """
        self.upgrade = upgrade
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
    results = results_table(
        headers=[
            "Index",
            "Router",
            "Model",
            "Name",
            "Current Firmware",
            "Current Modem Firmware",
            "Target Firmware",
            "Target Modem Firmware",
            "Status",
        ]
    )
    upgrade_pending_count = 0
    session = None
    argv = None
    parser = _get_parser()
    args = parser.parse_args(argv)
    try:
        if args.template:
            create_template_csv(args.template)
        elif args.inputfile:
            test_settings = TestSettings(
                upgrade=args.upgrade,
                config_dir=args.config,
                browser=args.browser,
                headless=args.headless,
                search_driver=args.search_driver,
                implicit_wait_time=args.implicit_wait,
                explicit_wait_time=args.explicit_wait,
                debug=args.debug,
            )
            datasource = read_csv(args.inputfile)
            for router in datasource:
                (session, firmware, status, upgrade_required) = upgrade_router(
                    router=router, test_settings=test_settings
                )
                if upgrade_required:
                    upgrade_pending_count += 1

                results.add_row(result_row_builder(session, status, firmware))
                results.print()
                session.close_session()
            if upgrade_pending_count > 0:
                print("\nUpgrades required! Re-run with --upgrade (or -u) argument")

        else:
            parser.print_help()
    except OSError as os_err:
        LOGGER.critical(f"OSError: {os_err}")
    except Exception as e:
        if session:
            results.add_row(
                result_row_builder(session=session, status=status, router_name=router)
            )
        LOGGER.critical(f"Error: {e}")


if __name__ == "__main__":
    main()
