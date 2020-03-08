"""Example: draytekwebadmin read settings to CSV file"""

import argparse
import csv
import logging
import time
from urllib.parse import urlparse

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


def read_data(session):
    """Read router configuration

    :param session: draytekwebadmin session object
    :returns: data - Dictionary of all collected values
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
    snmp_ipv6 = vars(session.read_settings(SNMPIPv6))
    snmp_trap_ipv4 = vars(session.read_settings(SNMPTrapIPv4))
    snmp_trap_ipv6 = vars(session.read_settings(SNMPTrapIPv6))
    snmpv3 = vars(session.read_settings(SNMPv3))
    internet_access = vars(session.read_settings(InternetAccessControl))
    access_list = vars(session.read_settings(AccessList))
    management_port = vars(session.read_settings(ManagementPort))
    brute_force = vars(session.read_settings(BruteForceProtection))
    encryption = vars(session.read_settings(Encryption))
    cvm_access = vars(session.read_settings(CVM_AccessControl))
    device_management = vars(session.read_settings(DeviceManagement))
    ap_management = vars(session.read_settings(AP_Management))
    lan_access = vars(session.read_settings(LAN_Access))

    # Rename the dictionary keys to include the object model name
    sep = "|"
    connection_info = prefixKeys(connection_info, DrayTekWebAdmin.__name__, sep)
    router_info = prefixKeys(router_info, session.routerinfo.__class__.__name__, sep)
    snmp_ipv4 = prefixKeys(snmp_ipv4, SNMPIPv4.__name__, sep)
    snmp_ipv6 = prefixKeys(snmp_ipv6, SNMPIPv6.__name__, sep)
    snmp_trap_ipv4 = prefixKeys(snmp_trap_ipv4, SNMPTrapIPv4.__name__, sep)
    snmp_trap_ipv6 = prefixKeys(snmp_trap_ipv6, SNMPTrapIPv6.__name__, sep)
    snmpv3 = prefixKeys(snmpv3, SNMPv3.__name__, sep)
    internet_access = prefixKeys(internet_access, InternetAccessControl.__name__, sep)
    access_list = prefixKeys(access_list, AccessList.__name__, sep)
    management_port = prefixKeys(management_port, ManagementPort.__name__, sep)
    brute_force = prefixKeys(brute_force, BruteForceProtection.__name__, sep)
    encryption = prefixKeys(encryption, Encryption.__name__, sep)
    cvm_access = prefixKeys(cvm_access, CVM_AccessControl.__name__, sep)
    device_management = prefixKeys(device_management, DeviceManagement.__name__, sep)
    ap_management = prefixKeys(ap_management, AP_Management.__name__, sep)
    lan_access = prefixKeys(lan_access, LAN_Access.__name__, sep)

    # Merge the data sources into a single dictionary
    data = {
        **connection_info,
        **router_info,
        **snmp_ipv4,
        **snmp_ipv6,
        **snmp_trap_ipv4,
        **snmp_trap_ipv6,
        **snmpv3,
        **internet_access,
        **access_list,
        **management_port,
        **brute_force,
        **encryption,
        **cvm_access,
        **device_management,
        **ap_management,
        **lan_access,
    }
    return data


def prefixKeys(data, prefix, separator):
    """Prefix dictionary keys

    :param data: dictionary of data
    :param prefix: value to prefix keys with
    :param separator: character between prefix and original key name
    :returns: prefixed - dictionary with updated key names
    """
    prefixed = {}
    if type(data) is dict:
        for key in data.keys():
            newKeyName = f"{prefix}{separator}{key}"
            prefixed[newKeyName] = data[key]
    return prefixed


def save_to_csv(data, filename):
    """Save data to CSV file

    :param data: dictionary of data to be saved
    :param filename: output filename for csv
    """
    with open(filename, "w", newline="") as outfile:
        csvfile = csv.DictWriter(outfile, data.keys(), dialect="excel")
        csvfile.writeheader()
        csvfile.writerow(data)


def main():
    """Main. Called when program called directly from the command line.

    """
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
        )
        webadmin_session.start_session()
        dataset = read_data(webadmin_session)
        save_to_csv(dataset, args.output)
    except Exception as exception:
        LOGGER.critical(exception)
        if webadmin_session is not None:
            if args.debug:
                timestamp = time.strftime("%Y%m%d-%H%M%S")
                # Collect the information from the session object and close it before attempting file access in case that fails
                # This avoids having another try/except/finally block within this error handling routine.
                hostname = webadmin_session.hostname
                page_source = webadmin_session.session.driver.page_source
                webadmin_session.close_session()

                debugfile = open(
                    f"draytek_read_settings_debug-{hostname}-{timestamp}.html", "w+"
                )
                debugfile.write(page_source)
                debugfile.close()
    finally:
        if webadmin_session is not None:
            webadmin_session.close_session()


if __name__ == "__main__":
    main()
