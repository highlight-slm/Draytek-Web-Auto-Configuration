import unittest

from draytekwebadmin.utils import (
    valid_ipv4_address,
    valid_community_string,
    valid_ipv4_subnet,
    valid_ipv6_address,
    valid_ipv6_prefix,
    valid_hostname,
    bool_or_none,
    int_or_none,
    port_or_none,
)


class TestUtils(unittest.TestCase):
    def test_valid_hostname(self):
        good_names = ["my.domain.com", "this.host.domain.com", "1hostname.tld.co.uk"]
        bad_names = [
            "this is not valid!",
            "thisnameisverylongandlongerthanisallowedbyrfc952whichstatesthemaximumtobe63.name.com",
            ".name.com",
            "my.name.com/",
            "http://my.name.com/",
            "192.168.0.1",
            r"///\\\///***",
        ]
        long_name = "x" * 256

        for hostname in good_names:
            self.assertTrue(valid_hostname(hostname), f"Hostname: {hostname}")
        for hostname in bad_names:
            self.assertFalse(valid_hostname(hostname), f"Hostname: {hostname}")
        self.assertFalse(valid_hostname(None))
        self.assertFalse(valid_hostname(long_name))

    def test_validIPv4Address(self):
        self.assertTrue(valid_ipv4_address(None))
        self.assertTrue(valid_ipv4_address(""))
        self.assertTrue(valid_ipv4_address("192.168.0.1"))

        self.assertFalse(valid_ipv4_address("fdfe:5d4d:384d:1:d8df:ed2:eafa:70af"))
        self.assertFalse(valid_ipv4_address("192.168.0.300"))
        self.assertFalse(valid_ipv4_address("Hello"))

    def test_validIPv6Address(self):
        self.assertTrue(valid_ipv6_address(None))
        self.assertTrue(valid_ipv6_address(""))
        self.assertTrue(valid_ipv6_address("fdfe:5d4d:384d:1:d8df:ed2:eafa:70af"))

        self.assertFalse(valid_ipv6_address("192.168.0.1"))
        self.assertFalse(valid_ipv6_address("fdfe:5d4d:384d:1:d8df:ed2:eafa:70af:1abc"))
        self.assertFalse(valid_ipv6_address("fdfe:5d4d:384d:1"))
        self.assertFalse(valid_ipv6_address("Hello"))

    def test_validCommunityString(self):
        self.assertTrue(valid_community_string(None))
        self.assertTrue(valid_community_string(""))
        self.assertTrue(valid_community_string("MyCommunity"))

        self.assertFalse(valid_community_string("This is a Very Long community String"))

    def test_validIPv4Subnet(self):
        self.assertTrue(valid_ipv4_subnet(None))
        self.assertTrue(valid_ipv4_subnet(""))
        self.assertTrue(valid_ipv4_subnet("255.255.252.0 / 22"))
        self.assertTrue(valid_ipv4_subnet("255.255.254.0 / 23"))
        self.assertTrue(valid_ipv4_subnet("255.255.255.0 / 24"))
        self.assertTrue(valid_ipv4_subnet("255.255.255.0 / 32"))

        self.assertFalse(valid_ipv4_subnet("255.255.128.0 / 17"))
        self.assertFalse(valid_ipv4_subnet("255.255.255.0 / 33"))
        self.assertFalse(valid_ipv4_subnet("255.255.256.0 / 32"))

        with self.assertRaises(ValueError):
            valid_ipv4_subnet("NotASubnet")

    def test_validIPv6PreFixLength(self):
        self.assertTrue(valid_ipv6_prefix(None))
        self.assertTrue(valid_ipv6_prefix(1))
        self.assertTrue(valid_ipv6_prefix(2))
        self.assertTrue(valid_ipv6_prefix(64))
        self.assertTrue(valid_ipv6_prefix(128))
        self.assertTrue(valid_ipv6_prefix("128"))

        self.assertFalse(valid_ipv6_prefix(0))
        self.assertFalse(valid_ipv6_prefix("0"))
        self.assertFalse(valid_ipv6_prefix(-1))
        self.assertFalse(valid_ipv6_prefix(129))

        with self.assertRaises(ValueError):
            valid_ipv6_prefix("NotANumber")

    def test_boolOrNone(self):
        self.assertIsNone(bool_or_none(None))
        self.assertTrue(bool_or_none(True))
        self.assertFalse(bool_or_none(False))
        self.assertTrue(bool_or_none(1))
        self.assertFalse(bool_or_none(0))
        self.assertTrue(bool_or_none("1"))
        self.assertTrue(bool_or_none("True"))
        self.assertFalse(bool_or_none("False"))
        self.assertFalse(bool_or_none(3))

    def test_intOrNone(self):
        self.assertIsNone(int_or_none(None))
        self.assertIsNone(int_or_none(""))
        self.assertEqual(100, int_or_none(100))
        self.assertEqual(999, int_or_none("999"))
        self.assertEqual(1, int_or_none(True))
        self.assertEqual(0, int_or_none(False))
        self.assertEqual(99, int_or_none(99.99))
        self.assertEqual(-100, int_or_none(-100))
        with self.assertRaises(ValueError):
            self.assertTrue(int_or_none("192.168.0.1"))
        with self.assertRaises(ValueError):
            self.assertTrue(int_or_none("this are words"))

    def test_portOrNone(self):
        self.assertEqual(8080, port_or_none(8080))
        with self.assertRaises(ValueError):
            self.assertTrue(port_or_none(9999999))
