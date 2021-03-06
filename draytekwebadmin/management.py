"""Draytek Web Admin - Model: Management."""

# pylint: disable=attribute-defined-outside-init, invalid-name

from draytekwebadmin.utils import bool_or_none, int_or_none, port_or_none
from draytekwebadmin.const import (
    BRUTE_FORCE_MAX_LOGIN_FAILURES,
    BRUTE_FORCE_MAX_PENALITY,
)


class Management:
    """Management object."""

    def __init__(
        self, router_name=None, disable_auto_logout=None, enable_validation_code=None
    ):
        """Create a new Management object."""
        self.router_name = router_name
        self.disable_auto_logout = disable_auto_logout
        self.enable_validation_code = enable_validation_code

    def __setattr__(self, name, value):
        if name in ("disable_auto_logout", "enable_validation_code"):
            value = bool_or_none(value)
        super(Management, self).__setattr__(name, value)


class InternetAccessControl:
    """Internet Access Control Object."""

    def __init__(
        self,
        internet_management=None,
        domain_name_allowed=None,
        ftp_server=None,
        http_server=None,
        enforce_https_access=None,
        https_server=None,
        telnet_server=None,
        tr069_server=None,
        ssh_server=None,
        snmp_server=None,
        disable_ping_from_internet=None,
    ):
        """Create a new InternetAccessControl object."""
        self.internet_management = internet_management
        self.domain_name_allowed = domain_name_allowed
        self.ftp_server = ftp_server
        self.http_server = http_server
        self.enforce_https_access = enforce_https_access
        self.https_server = https_server
        self.telnet_server = telnet_server
        self.tr069_server = tr069_server
        self.ssh_server = ssh_server
        self.snmp_server = snmp_server
        self.disable_ping_from_internet = disable_ping_from_internet

    def __setattr__(self, name, value):
        if name != "domain_name_allowed":
            value = bool_or_none(value)
        super(InternetAccessControl, self).__setattr__(name, value)


class AccessList:
    """AccessList Object."""

    def __init__(
        self,
        list_1_ip_object_index=None,
        list_2_ip_object_index=None,
        list_3_ip_object_index=None,
        list_4_ip_object_index=None,
        list_5_ip_object_index=None,
        list_6_ip_object_index=None,
        list_7_ip_object_index=None,
        list_8_ip_object_index=None,
        list_9_ip_object_index=None,
        list_10_ip_object_index=None,
    ):
        """Create a new AccessList object."""
        # TODO (4416): Should the be in a dictionary/list?
        self.list_1_ip_object_index = list_1_ip_object_index
        self.list_2_ip_object_index = list_2_ip_object_index
        self.list_3_ip_object_index = list_3_ip_object_index
        self.list_4_ip_object_index = list_4_ip_object_index
        self.list_5_ip_object_index = list_5_ip_object_index
        self.list_6_ip_object_index = list_6_ip_object_index
        self.list_7_ip_object_index = list_7_ip_object_index
        self.list_8_ip_object_index = list_8_ip_object_index
        self.list_9_ip_object_index = list_9_ip_object_index
        self.list_10_ip_object_index = list_10_ip_object_index


class ManagementPort:
    """ManagementPort Object."""

    def __init__(
        self,
        user_defined_ports=None,
        telnet_port=None,
        http_port=None,
        https_port=None,
        ftp_port=None,
        tr069_port=None,
        ssh_port=None,
    ):
        """Create a new ManagementPort object."""
        self.user_defined_ports = user_defined_ports
        self.telnet_port = telnet_port
        self.http_port = http_port
        self.https_port = https_port
        self.ftp_port = ftp_port
        self.tr069_port = tr069_port
        self.ssh_port = ssh_port

    def __setattr__(self, name, value):
        if name == "user_defined_ports":
            value = bool_or_none(value)
        else:
            value = port_or_none(value)
        super(ManagementPort, self).__setattr__(name, value)


class BruteForceProtection:
    """BruteForceProtection Object."""

    def __init__(
        self,
        enable=None,
        ftp_server=None,
        http_server=None,
        https_server=None,
        telnet_server=None,
        tr069_server=None,
        ssh_server=None,
        max_login_failures=None,
        penalty_period=None,
    ):
        """Create a new BruteForceProtection object."""
        self.enable = enable
        self.ftp_server = ftp_server
        self.http_server = http_server
        self.https_server = https_server
        self.telnet_server = telnet_server
        self.tr069_server = tr069_server
        self.ssh_server = ssh_server
        self.max_login_failures = max_login_failures
        self.penalty_period = penalty_period

    def __setattr__(self, name, value):
        if name == "max_login_failures":
            value = int_or_none(value)
            if value is not None and value > BRUTE_FORCE_MAX_LOGIN_FAILURES:
                raise ValueError(
                    f"{value} Exceeds Max login failures: {BRUTE_FORCE_MAX_LOGIN_FAILURES}"
                )
        elif name == "penalty_period":
            value = int_or_none(value)
            if value is not None and value > BRUTE_FORCE_MAX_PENALITY:
                raise ValueError(
                    f"{value} Exceeds Max penalty: {BRUTE_FORCE_MAX_PENALITY} seconds"
                )
        else:
            value = bool_or_none(value)
        super(BruteForceProtection, self).__setattr__(name, value)


class Encryption:
    """Encryption Object."""

    def __init__(self, tls_1_2=None, tls_1_1=None, tls_1_0=None, ssl_3_0=None):
        """Create a new Encryption object."""
        self.tls_1_2 = tls_1_2
        self.tls_1_1 = tls_1_1
        self.tls_1_0 = tls_1_0
        self.ssl_3_0 = ssl_3_0

    def __setattr__(self, name, value):
        value = bool_or_none(value)
        super(Encryption, self).__setattr__(name, value)


class CVM_AccessControl:
    """CWM_AccessControl Object."""

    def __init__(self, enable=None, ssl_enable=None, port=None, ssl_port=None):
        """Create a new CWM_AccessControl object."""
        self.enable = enable
        self.ssl_enable = ssl_enable
        self.port = port
        self.ssl_port = ssl_port

    def __setattr__(self, name, value):
        if name in ("enable", "ssl_enable"):
            value = bool_or_none(value)
        else:
            value = port_or_none(value)
        super(CVM_AccessControl, self).__setattr__(name, value)


class AP_Management:
    """AP_Management Object."""

    def __init__(self, enable=None):
        """Create a new AP_Management object."""
        self.enable = enable

    def __setattr__(self, name, value):
        value = bool_or_none(value)
        super(AP_Management, self).__setattr__(name, value)


class DeviceManagement:
    """DeviceManagement object."""

    def __init__(self, enable=None, respond_to_external_device=None):
        """Create a new DeviceManagement object."""
        self.enable = enable
        self.respond_to_external_device = respond_to_external_device

    def __setattr__(self, name, value):
        value = bool_or_none(value)
        super(DeviceManagement, self).__setattr__(name, value)


class IPv6Management:
    """IPv6Management object."""

    def __init__(
        self,
        internet_management=None,
        telnet_server=None,
        http_server=None,
        https_server=None,
        ssh_server=None,
        snmp_server=None,
        disable_ping_from_internet=None,
        access_index_1=None,
        access_index_2=None,
        access_index_3=None,
        access_index_4=None,
        access_index_5=None,
        access_index_6=None,
        access_index_7=None,
        access_index_8=None,
        access_index_9=None,
        access_index_10=None,
    ):
        """Create a new IPv6Management object."""
        self.internet_management = internet_management
        self.telnet_server = telnet_server
        self.http_server = http_server
        self.https_server = https_server
        self.ssh_server = ssh_server
        self.snmp_server = snmp_server
        self.disable_ping_from_internet = disable_ping_from_internet
        self.access_index_1 = access_index_1
        self.access_index_2 = access_index_2
        self.access_index_3 = access_index_3
        self.access_index_4 = access_index_4
        self.access_index_5 = access_index_5
        self.access_index_6 = access_index_6
        self.access_index_7 = access_index_7
        self.access_index_8 = access_index_8
        self.access_index_9 = access_index_9
        self.access_index_10 = access_index_10

    def __setattr__(self, name, value):
        if name in (
            "internet_management",
            "telnet_server",
            "http_server",
            "https_server",
            "ssh_server",
            "snmp_server",
            "disable_ping_from_internet",
        ):
            value = bool_or_none(value)
        else:
            value = int_or_none(value)
        super(IPv6Management, self).__setattr__(name, value)


class LAN_Access:
    """LAN_Access object."""

    def __init__(
        self,
        enable=None,
        ftp_server=None,
        http_server=None,
        enforce_https_access=None,
        https_server=None,
        telnet_server=None,
        tr069_server=None,
        ssh_server=None,
        lan_1_access=None,
        lan_1_use_index=None,
        lan_1_index=None,
        lan_2_access=None,
        lan_2_use_index=None,
        lan_2_index=None,
        lan_3_access=None,
        lan_3_use_index=None,
        lan_3_index=None,
        lan_4_access=None,
        lan_4_use_index=None,
        lan_4_index=None,
        lan_5_access=None,
        lan_5_use_index=None,
        lan_5_index=None,
        lan_6_access=None,
        lan_6_use_index=None,
        lan_6_index=None,
        dmz_access=None,
        lan_ip_routed_access=None,
        lan_ip_routed_use_index=None,
        lan_ip_routed_index=None,
    ):
        """Create a new LAN_Access object."""
        self.enable = enable
        self.ftp_server = ftp_server
        self.http_server = http_server
        self.enforce_https_access = enforce_https_access
        self.https_server = https_server
        self.telnet_server = telnet_server
        self.tr069_server = tr069_server
        self.ssh_server = ssh_server
        self.lan_1_access = lan_1_access
        self.lan_1_use_index = lan_1_use_index
        self.lan_1_index = lan_1_index
        self.lan_2_access = lan_2_access
        self.lan_2_use_index = lan_2_use_index
        self.lan_2_index = lan_2_index
        self.lan_3_access = lan_3_access
        self.lan_3_use_index = lan_3_use_index
        self.lan_3_index = lan_3_index
        self.lan_4_access = lan_4_access
        self.lan_4_use_index = lan_4_use_index
        self.lan_4_index = lan_4_index
        self.lan_5_access = lan_5_access
        self.lan_5_use_index = lan_5_use_index
        self.lan_5_index = lan_5_index
        self.lan_6_access = lan_6_access
        self.lan_6_use_index = lan_6_use_index
        self.lan_6_index = lan_6_index
        self.dmz_access = dmz_access
        self.lan_ip_routed_access = lan_ip_routed_access
        self.lan_ip_routed_use_index = lan_ip_routed_use_index
        self.lan_ip_routed_index = lan_ip_routed_index

    def __setattr__(self, name, value):
        if name in (
            "lan_1_index",
            "lan_2_index",
            "lan_3_index",
            "lan_4_index",
            "lan_5_index",
            "lan_6_index",
            "lan_ip_routed_index",
        ):
            value = int_or_none(value)
        else:
            value = bool_or_none(value)
        super(LAN_Access, self).__setattr__(name, value)
