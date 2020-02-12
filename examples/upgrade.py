"""Example: draytekwebadmin mass upgrade router firmware from a CSV file"""

import argparse
import csv
import logging

from draytekwebadmin import DrayTekWebAdmin, Firmware

LOGGER = logging.getLogger("root")
FORMAT = "[%(levelname)s] %(message)s"
logging.basicConfig(format=FORMAT)
LOGGER.setLevel(logging.INFO)


def _get_parser():
    """Parse command line arguments.

    Args:
        None

    Returns:
        parser: argparse object

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
        "--not-headless",
        dest="headless",
        action="store_false",
        default=True,
        help="Show the browser session, do not run headless",
    )
    return parser


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


def upgrade_router(router, headless=True, upgrade=False):
    """ Upgrade firmware on Draytek Router

    Args:
        router: row from CSV with settings for a single router
        headless: display of browser session when interacting with router
        upgrade: Perform firmware upgrade, otherwise preview only

    Returns:
        None

    """
    webadmin_session = None
    upgrade_required = False

    try:
        settings = extract_settings(router)

        webadmin_session = settings["connection"]
        webadmin_session.headless = headless

        preview = webadmin_session.upgrade_preview(
            Firmware(filepath=settings["firmware"].filepath)
        )
        if preview.router_firmware_upgradable():
            upgrade_required = True
            LOGGER.info(
                f"Router: {webadmin_session.hostname} "
                f"Firmware upgrade available "
                f"form: {preview.firmware_current} "
                f"to {preview.firmware_target}"
            )
        if preview.modem_firmware_upgradable():
            upgrade_required = True
            LOGGER.info(
                f"Router: {webadmin_session.hostname} "
                f"Modem Firmware upgrade available "
                f"from: {preview.modem_firmware_current} "
                f"to {preview.modem_firmware_target}"
            )

        if upgrade_required:
            if upgrade:
                LOGGER.info(f"Router {webadmin_session.hostname} - Upgrading Router")
                webadmin_session.upgrade(preview)  # Reuse the Preview (Firmware) object
            else:
                LOGGER.info(
                    f"Router {webadmin_session.hostname} - Upgrade required. Not appllied. Re-run with --upgrade argument"
                )
        else:
            LOGGER.info(f"Router {webadmin_session.hostname} - Firmware up-to-date")

    except RuntimeError as exception:
        LOGGER.critical(exception)
    finally:
        if webadmin_session is not None:
            webadmin_session.close_session()


def extract_settings(router_settings, separator="|"):
    """Extracts connection settings and firmware details from csv.
       Logs errors if unexpected modulenames found in header.

    Args:
        router: row from CSV with settings for a single router
        separator: character used to separate modules from fields (default '|')

    Returns:
        settings: dictionary of dictionaries containing extracted data from csv

    """
    connection = DrayTekWebAdmin()
    router_firmware = Firmware()
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

    Args:
        output_file: filename to save template as

    Returns:
        None

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
                upgrade_router(
                    router=router, headless=args.headless, upgrade=args.upgrade
                )
        except FileNotFoundError:
            LOGGER.critical(f"Input file not found: {args.inputfile}")
        # TODO:
        # Parallel execution

    else:
        parser.print_help()


if __name__ == "__main__":
    main()
