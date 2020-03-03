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
        "-d",
        "--debug",
        action="store_true",
        default=False,
        help="Errors will attempt to capture Web page",
    )
    parser.add_argument(
        "-c",
        "--config",
        type=dir_path,
        help=r"Location of configuration file directory e.g. -c c:\upgrade\conf",
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


def check_upgrade_router(router, config_dir=None, debug=False):
    """Check Upgrade firmware on Draytek Router

    :param router: row from CSV with settings for a single router
    :param config_dir: path to configuration file for toolium
    :param debug: write a debug files of the page source on exception
    :returns: DraytekWebAdmin Session object
    :returns: DraytekWebAdmin Firmware object
    """
    webadmin_session = None

    try:
        settings = extract_settings(router, config_dir)

        webadmin_session = settings["connection"]
        preview = webadmin_session.upgrade_preview(
            Firmware(filepath=settings["firmware"].filepath)
        )
        return webadmin_session, preview

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
                    f"draytek_upgrade_debug-{hostname}-{timestamp}.html", "w+"
                )
                debugfile.write(page_source)
                debugfile.close()
            else:
                webadmin_session.close_session()
            return webadmin_session, None
        return None, None


def extract_settings(router_settings, config_dir=None, delimiter="|"):
    """Extracts connection settings and firmware details from csv.
       Logs errors if unexpected modulenames found in header.

    :param router: row from CSV with settings for a single router
    :param config_dir: path to configuration file for toolium
    :param delimiter: character used to separate modules from fields (default '|')
    :returns: dictionary of dictionaries containing extracted data from csv
    """
    # TODO: Not working yet, check if this needs to be called earlier in this function on in prior function.
    # Ensure it does get passed into the Draytek Library
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


def upgrade_router(router_data, upgrade, config_dir, debug=False):
    """Upgrade router firmware, or preview potential upgrade

    :param router_data: connection information from csv input file
    :param upgrade: Flag to allow upgrade to run, preview otherwise
    :param config_dir: path to configuration file for toolium
    :param debug: write a debug files of the page source on exception
    """
    table_headers = [
        "Router",
        "Model",
        "Name",
        "Current Firmware",
        "Current Modem Firmware",
        "Target Firmware",
        "Target Modem Firmware",
        "Upgrade",
    ]
    table = [""]
    upgrade_required_count = 0
    session = None
    try:
        for router in router_data:
            upgrade_state = None
            session, router_firmware = check_upgrade_router(
                router=router, config_dir=config_dir, debug=debug
            )
            if (session) and (router_firmware):  # Both values not None
                if (router_firmware.router_firmware_upgradable()) or (
                    router_firmware.modem_firmware_upgradable()
                ):
                    if upgrade:
                        upgrade_state = "UPGRADED!"
                        LOGGER.info(f"Router {session.hostname} - Upgrading Router")
                        session.upgrade(router_firmware)
                    else:
                        upgrade_required_count += 1
                        upgrade_state = "REQUIRED"
                else:
                    upgrade_state = "N/A"
                    LOGGER.info(f"Router {session.hostname} - Firmware up-to-date")
                row = [
                    session.hostname,
                    session.routerinfo.model,
                    session.routerinfo.router_name,
                    router_firmware.firmware_current,
                    router_firmware.modem_firmware_current.split()[0],
                    router_firmware.firmware_target,
                    router_firmware.modem_firmware_target.split()[0],
                    upgrade_state,
                ]
            else:
                upgrade_state = "ERROR!"
                LOGGER.info(
                    f"Router {session.hostname} - Unable to access Firmware information"
                )
                row = [session.hostname, "", "", "", "", "", "", upgrade_state]
            table.append(row)
            print(tabulate(table, headers=table_headers))
        if upgrade_required_count > 0:
            print("\nUpgrades required! Re-run with --upgrade (or -u) argument")
        session.close_session()
        session = None  # Clear session before next loop
    finally:
        if session is not None:
            session.close_session()


def main():
    """Main. Called when program called directly from the command line.
    """
    argv = None
    parser = _get_parser()
    args = parser.parse_args(argv)
    try:
        if args.template:
            create_template_csv(args.template)
        elif args.inputfile:
            datasource = read_csv(args.inputfile)
            upgrade_router(
                router_data=datasource,
                upgrade=args.upgrade,
                config_dir=args.config,
                debug=args.debug,
            )
        else:
            parser.print_help()
    except OSError as os_err:
        LOGGER.critical(f"OSError: {os_err}")


if __name__ == "__main__":
    main()
