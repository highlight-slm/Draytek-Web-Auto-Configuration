"""Utility functions for DrayTek Web Admin."""

import ipaddress
import logging
import re

from draytekwebadmin.const import (
    IPV4_SUBNET_MAX,
    IPV4_SUBNET_MIN,
    MAX_COMMUNITY_STRING_LENGTH,
    IPV6_PREFIX_MAX,
    IPV6_PREFIX_MIN,
    MAX_PORT,
    HOSTNAME_REGEX,
)

LOGGER = logging.getLogger("root")


def valid_hostname(hostname):
    """Check if name passed is a valid DNS host name.

    Args:
        hostname (str): Host name or FQDN

    Returns:
        bool: True if valid or None, false otherwise

    """
    if hostname is not None and len(hostname) < 255:
        if not hostname.split(".")[-1].isdigit():  # This is just a number
            return bool(re.match(HOSTNAME_REGEX, hostname))
    return False


def valid_ipv4_address(address):
    """Check if address passed is a valid IPv4 address.

    Args:
        ip (str): IP Address

    Returns:
        bool: True if valid or None, false otherwise

    """
    if not address:  # None or Empty string
        return True
    try:
        ipaddress.IPv4Address(address)
        return True
    except ipaddress.AddressValueError as error_code:
        LOGGER.debug(f"IP Address validation failed, error: {error_code}")
        return False


def valid_ipv6_address(address):
    """Check if address passed is a valid IPv6 address.

    Args:
        ip (str): IP Address

    Returns:
        bool: True if valid or None, false otherwise

    """
    if not address:  # None or Empty string
        return True
    try:
        ipaddress.IPv6Address(address)
        return True
    except ipaddress.AddressValueError as error_code:
        LOGGER.debug(f"IP Address validation failed, error: {error_code}")
        return False


def valid_community_string(community):
    """Check if community string is valid.

    Args:
        community (str): SNMP community string

    Returns:
        bool: True if valid or None, false otherwise

    """
    if not community:  # None or Empty string
        return True
    if len(community) <= MAX_COMMUNITY_STRING_LENGTH:
        return True
    return False


def valid_ipv4_subnet(subnet):
    """Check if subnet passed is a valid IPv4 subnet for Draytek.

    :param subnet: IPv4 subnet string
    :returns: True if valid or None, false otherwise
    """
    if not subnet:  # None or Empty string
        return True
    try:
        if (
            int(subnet.split("/")[1].strip()) <= IPV4_SUBNET_MAX
            and int(subnet.split("/")[1].strip()) >= IPV4_SUBNET_MIN
        ):
            if valid_ipv4_address(subnet.split("/")[0].strip()):
                return True
        return False
    except (IndexError, ValueError) as error:
        raise ValueError(error)


def valid_ipv6_prefix(prefix):
    """Check if prefix passed is a valid IPv6 prefix length.

    :param prefix: IPv6 Prefix length
    :returns: True if valid or None, false otherwise
    """
    if prefix is None:
        return True
    if int(prefix) <= IPV6_PREFIX_MAX and int(prefix) >= IPV6_PREFIX_MIN:
        return True
    return False


def bool_or_none(value):
    """Return boolean equivalent or None for a given value.

    :param value: value to be parsed
    returns: None if value=None, else True if truthy or False otherwise
    """
    if value is None:
        return None
    return str(value).lower() in ["true", "1", "y", "yes", "on"]


def int_or_none(value):
    """Return integer equivalent or None for a given value.

    :param value: value to be parsed
    :returns: None if value=None else int(value)
    """
    if value is None:
        return None
    return int(value)


def port_or_none(value):
    """Return integer port number or None for a given value.

    :param value: value to be parsed
    :returns: Valid port number, None if value=None else int(value)
    """
    port = int_or_none(value)
    if port is not None and port > MAX_PORT:
        raise ValueError(f"Port exceeds maximum port number {MAX_PORT}")
    return port
