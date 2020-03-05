"""Draytek Web Admin - Model: SNMP."""

# pylint: disable=attribute-defined-outside-init

from draytekwebadmin.utils import (
    valid_ipv4_address,
    valid_ipv4_subnet,
    valid_ipv6_address,
    valid_ipv6_prefix,
    valid_community_string,
    bool_or_none,
)
from draytekwebadmin.const import (
    SNMPV3_AUTH_ALGO,
    SNMPV3_PRIV_ALGP,
    MAX_COMMUNITY_STRING_LENGTH,
    SNMP_TRAP_TIMEOUT_MAX,
    SNMP_TRAP_TIMEOUT_MIN,
)


class SNMP:
    """SNMP Base Class."""

    def __init__(self, enable_agent=None, enable_v3_agent=None):
        """SNMP base class.

        :param enable_agent: (bool)Enable or Disable SNMP v1/v2 agent
        :param enable_v3_agent: (bool) Enable or Disable SNMP v3 agent
        """
        self.enable_agent = enable_agent
        self.enable_v3_agent = enable_v3_agent

    def __setattr__(self, name, value):
        if name in ["enable_agent", "enable_v3_agent"]:
            value = bool_or_none(value)
        super(SNMP, self).__setattr__(name, value)


class SNMPv3(SNMP):
    """SNMPv3 Object."""

    def __init__(
        self,
        enable_v3_agent=None,
        usm_user=None,
        auth_algorithm=None,
        auth_password=None,
        priv_algorithm=None,
        priv_password=None,
    ):
        """SNMPv3 - derived from SNMP base class.

        :param enable_agent: (bool) Enable or Disable SNMPv3 agent. Note SNMPv1v2 Agent must be enabled first.
        :param usm_user: (str)SNMPv3 User Name
        :param auth_algorithm: (str) Authentication Algorithm: No Auth, MD5 or SHA
        :param auth_password: (str) Authentication Password
        :param priv_algorithm: (str) Privacy Algorithm: No Priv, DES or AES
        :param priv_password: (str) Privacy Password
        """
        super().__init__(enable_agent=True, enable_v3_agent=True)
        self.enable_v3_agent = enable_v3_agent
        self.usm_user = usm_user
        self.auth_algorithm = auth_algorithm
        self.auth_password = auth_password
        self.priv_algorithm = priv_algorithm
        self.priv_password = priv_password

    def __setattr__(self, name, value):
        if name in ("auth_password", "priv_password"):
            if value is not None:
                if len(set(value)) == 1:  # All the same character
                    # Don't store. If all the same character. Likely all * as password field
                    value = None
        if name == "auth_algorithm":
            if value is not None and value not in SNMPV3_AUTH_ALGO:
                raise ValueError(
                    f"Unsupported SNMPv3 Authentication Algorithm: {value}"
                )
        if name == "priv_algorithm":
            if value is not None and value not in SNMPV3_PRIV_ALGP:
                raise ValueError(f"Unsupported SNMPv3 Privacy Algorithm: {value}")
        super(SNMPv3, self).__setattr__(name, value)


class SNMPv1v2(SNMP):
    """SNMPv1v2 Base Class."""

    def __init__(self, enable_agent=None, get_community=None, set_community=None):
        """SNMPv1v2 class - derived from SNMP base class.

        :param enable_agent: (bool) Enable or Disable SNMP agent
        :param get_community: (str) Public or read only SNMP community string
        :param set_community: (str) Private or read/write SNMP community string
        """
        super().__init__(enable_agent=True)
        self.enable_agent = enable_agent
        self.get_community = get_community
        self.set_community = set_community

    def __setattr__(self, name, value):
        if name in ["get_community", "set_community"]:
            if not valid_community_string(value):
                raise ValueError(
                    f"Community string - Exceeds maximum length ({MAX_COMMUNITY_STRING_LENGTH} characters)"
                )
        super(SNMPv1v2, self).__setattr__(name, value)


class SNMPIPv4(SNMPv1v2):
    """SNMPIPv4 Object."""

    def __init__(
        self,
        enable_agent=None,
        get_community=None,
        set_community=None,
        manager_host_1=None,
        manager_host_2=None,
        manager_host_3=None,
        manager_host_subnet_1=None,
        manager_host_subnet_2=None,
        manager_host_subnet_3=None,
    ):
        """SNMPIPv4 - derived from SNMPv1v2 base class.

        :param enable_agent: (bool) Enable or Disable SNMP agent
        :param get_community: (str) Public or read only SNMP community string
        :param set_community: (str) Private or read/write SNMP community string
        :param manager_host_1: (str) (IPv4 address) IP address of management host
        :param manager_host_2: (str) (IPv4 address) IP address of management host
        :param manager_host_3: (str) (IPv4 address) IP address of management host
        :param manager_host_subnet_1: (str) Subnet Mast and Network (CIDR) e.g. "255.255.255.0 /24"
        :param manager_host_subnet_2: (str) Subnet Mast and Network (CIDR) e.g. "255.255.255.0 /24"
        :param manager_host_subnet_3: (str) Subnet Mast and Network (CIDR) e.g. "255.255.255.0 /24"
        """
        super().__init__(enable_agent, get_community, set_community)
        self.manager_host_1 = manager_host_1
        self.manager_host_2 = manager_host_2
        self.manager_host_3 = manager_host_3
        self.manager_host_subnet_1 = manager_host_subnet_1
        self.manager_host_subnet_2 = manager_host_subnet_2
        self.manager_host_subnet_3 = manager_host_subnet_3

    def __setattr__(self, name, value):
        if name in ["manager_host_1", "manager_host_2", "manager_host_3"]:
            if not valid_ipv4_address(value):
                raise ValueError(f"Invalid IPv4 Address: {value}")
        if name in [
            "manager_host_subnet_1",
            "manager_host_subnet_2",
            "manager_host_subnet_3",
        ]:
            if not valid_ipv4_subnet(value):
                raise ValueError(f"Invalid Subnet: {value}")
        super(SNMPIPv4, self).__setattr__(name, value)


class SNMPIPv6(SNMPv1v2):
    """SNMPIPv6 Object."""

    def __init__(
        self,
        enable_agent=None,
        get_community=None,
        set_community=None,
        manager_host_1=None,
        manager_host_2=None,
        manager_host_3=None,
        manager_host_prelen_1=None,
        manager_host_prelen_2=None,
        manager_host_prelen_3=None,
    ):
        """SNMPIPv6 - derived from SNMPv1v2 base class.

        :param enable_agent: (bool) Enable or Disable SNMP agent
        :param get_community: (str) Public or read only SNMP community string
        :param set_community: (str) Private or read/write SNMP community string
        :param manager_host_1: (str) (IPv6 address) IP address of management host
        :param manager_host_2: (str) (IPv6 address) IP address of management host
        :param manager_host_3: (str) (IPv6 address) IP address of management host
        :param manager_host_prelen_1: (int) IPv6 prefix length
        :param manager_host_prelen_2: (int) IPv6 prefix length
        :param manager_host_prelen_3: (int) IPv6 prefix length
        """
        super().__init__(enable_agent, get_community, set_community)
        self.manager_host_1 = manager_host_1
        self.manager_host_2 = manager_host_2
        self.manager_host_3 = manager_host_3
        self.manager_host_prelen_1 = manager_host_prelen_1
        self.manager_host_prelen_2 = manager_host_prelen_2
        self.manager_host_prelen_3 = manager_host_prelen_3

    def __setattr__(self, name, value):
        if name in ["manager_host_1", "manager_host_2", "manager_host_3"]:
            if not valid_ipv6_address(value):
                raise ValueError(f"Invalid IPv6 Address: {value}")
        if name in [
            "manager_host_prelen_1",
            "manager_host_prelen_2",
            "manager_host_prelen_3",
        ]:
            if value in (0, "0", ""):
                value = None  # Zero is the default prefix when no address is set.
            if not valid_ipv6_prefix(value):
                raise ValueError(f"Invalid IPv6 Prefix Length: {value}")
        super(SNMPIPv6, self).__setattr__(name, value)


class SNMPTrap:
    """SNMPTrap Base class."""

    def __init__(self, community=None, timeout=None):  # noqa: D403
        """SNMPTrap class.

        :param community: (str) SNMP community string for TRAP messages
        :param timeout: (int) How many seconds the device should wait for a response from a trap message,
                        before deciding to try again or fail.
        """
        self.community = community
        self.timeout = timeout

    def __setattr__(self, name, value):
        if name == "community":
            if not valid_community_string(value):
                raise ValueError(
                    f"Trap Community string - Exceeds maximum length "
                    f"({MAX_COMMUNITY_STRING_LENGTH} characters)"
                )
        if name == "timeout":
            if value is not None:
                if (
                    int(value) > SNMP_TRAP_TIMEOUT_MAX
                    or int(value) < SNMP_TRAP_TIMEOUT_MIN
                ):
                    raise ValueError(
                        f"Trap Timeout - Supported range "
                        f"{SNMP_TRAP_TIMEOUT_MIN}-{SNMP_TRAP_TIMEOUT_MAX}"
                    )
        super(SNMPTrap, self).__setattr__(name, value)


class SNMPTrapIPv4(SNMPTrap):
    """SNMPTrapIPv4 Object."""

    def __init__(self, community=None, timeout=None, host_1=None, host_2=None):
        """SNMPTrapIPv4 - derived from SNMPTrap base class.

        :param community: (str) SNMP community string for TRAP messages
        :param timeout: (int) How many seconds the device should wait for a response from a trap message,
                        before deciding to try again or fail.
        :param host_1: (str) (IPv4 address) IP address of trap destination host
        :param host_2: (str) (IPv4 address) IP address of trap destination host
        """
        super().__init__(community, timeout)
        self.host_1 = host_1
        self.host_2 = host_2

    def __setattr__(self, name, value):
        if name in ["host_1", "host_2"]:
            if not valid_ipv4_address(value):
                raise ValueError(f"Invalid IPv4 Address: {value}")
        super(SNMPTrapIPv4, self).__setattr__(name, value)


class SNMPTrapIPv6(SNMPTrap):
    """SNMPTrapIPv6 Object."""

    def __init__(self, community=None, timeout=None, host_1=None, host_2=None):
        """SNMPTrapIPv6 - derived from SNMPTrap base class.

        :param community: (str) SNMP community string for TRAP messages
        :param timeout: (int) How many seconds the device should wait for a response from a trap message,
                        before deciding to try again or fail.
        :param host_1: (str) (IPv6 address) IP address of trap destination host
        :param host_2: (str) (IPv6 address) IP address of trap destination host
        """
        super().__init__(community, timeout)
        self.host_1 = host_1
        self.host_2 = host_2

    def __setattr__(self, name, value):
        if name in ["host_1", "host_2"]:
            if not valid_ipv6_address(value):
                raise ValueError(f"Invalid IPv6 Address: {value}")
        super(SNMPTrapIPv6, self).__setattr__(name, value)
