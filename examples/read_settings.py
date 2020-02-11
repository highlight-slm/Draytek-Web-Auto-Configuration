"""Example: draytekwebadmin read settings to CSV file"""

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
        description="Read DrayTek router settings. Saving the result to a CSV file."
    )
    parser.add_argument(
        "-a",
        "--address",
        type=str,
        help="Router address e.g. https://192.168.0.1:8080",
        required=True,
    )
    parser.add_argument(
        "-u",
        "--user",
        type=str,
        default="admin",
        help="Router administrator user name (default: admin)",
    )
    parser.add_argument(
        "-p",
        "--password",
        type=str,
        help="Router administrator password",
        required=True,
    )
    parser.add_argument(
        "-o",
        "--output",
        type=str,
        default="draytek-out.csv",
        help="Output data file (default: draytek-out.csv)",
    )
    parser.add_argument(
        "--not-headless",
        dest="headless",
        action="store_false",
        default=True,
        help="Show the browser session, do not run headless",
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


def read_data(session):
    """Read router configuration

    Args:
        session: draytekwebadmin session object

    Returns:
        data: Dictionary of all collected values

    """
    # Get connection properties to save to CSV useful for later scripted changes
    wanted_session_properties = [
        "url",
        "hostname",
        "port",
        "use_https",
        "username",
        "password",
    ]
    connection = vars(session)
    connection_info = dict(
        (k, connection[k]) for k in wanted_session_properties if k in connection
    )

    router_info = vars(session.routerinfo)  # Read router info
    snmp_ipv4 = vars(session.read_settings(SNMPIPv4))
    internet_access = vars(session.read_settings(InternetAccessControl))

    # Rename the dictionary keys to include the object model name
    sep = "|"
    connection_info = prefixKeys(connection_info, DrayTekWebAdmin.__name__, sep)
    router_info = prefixKeys(router_info, session.routerinfo.__class__.__name__, sep)
    snmp_ipv4 = prefixKeys(snmp_ipv4, SNMPIPv4.__name__, sep)
    internet_access = prefixKeys(internet_access, InternetAccessControl.__name__, sep)

    # Merge the data sources into a single dictionary
    data = {**connection_info, **router_info, **snmp_ipv4, **internet_access}
    return data


def prefixKeys(data, prefix, separator):
    """Prefix dictionary keys

    Args:
        data: dictionary of data
        prefix: value to prefix keys with
        separator: character between prefix and original key name

    Returns:
        prefixed: dictionary with updated key names

    """
    prefixed = {}
    if type(data) is dict:
        for key in data.keys():
            newKeyName = f"{prefix}{separator}{key}"
            prefixed[newKeyName] = data[key]
    return prefixed


def save_to_csv(data, filename):
    """Save data to CSV file

    Args:
        data: dictionary of data to be saved
        filename: output filename for csv

    Returns:
        None

    """
    with open(filename, "w", newline="") as outfile:
        csvfile = csv.DictWriter(outfile, data.keys(), dialect="excel")
        csvfile.writeheader()
        csvfile.writerow(data)


def main():
    """Main. Called when program called directly from the command line.

    Args:
        None

    Returns:
        None

    """
    #
    # TODO: Read connection info from file to allow bulk read of settings
    #       output filename to include date and time?
    #

    argv = None
    parser = _get_parser()
    args = parser.parse_args(argv)
    host, port, https = parse_address_url_to_host(args.address)
    webadmin_session = None
    try:
        webadmin_session = DrayTekWebAdmin(
            hostname=host,
            port=port,
            use_https=https,
            username=args.user,
            password=args.password,
            headless=args.headless,
        )
        webadmin_session.start_session()
        dataset = read_data(webadmin_session)
        save_to_csv(dataset, args.output)
    except RuntimeError as exception:
        LOGGER.critical(exception)
    finally:
        if webadmin_session is not None:
            webadmin_session.close_session()


if __name__ == "__main__":
    main()
