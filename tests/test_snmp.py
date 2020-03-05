import unittest

from draytekwebadmin.snmp import (
    SNMP,
    SNMPv3,
    SNMPIPv4,
    SNMPIPv6,
    SNMPTrapIPv4,
    SNMPTrapIPv6,
)


class TestSNMP(unittest.TestCase):
    def test_empty(self):
        empty = SNMP()
        self.assertIsNone(empty.enable_agent)
        self.assertIsNone(empty.enable_v3_agent)

    def test_valid(self):
        self.assertTrue(SNMP(enable_agent=True).enable_agent)
        self.assertTrue(SNMP(enable_v3_agent=True).enable_v3_agent)

    def test_validation(self):
        self.assertTrue(SNMP(enable_agent="true").enable_agent)
        self.assertTrue(SNMP(enable_v3_agent=1).enable_v3_agent)
        self.assertFalse(SNMP(enable_agent="not true").enable_agent)
        self.assertFalse(SNMP(enable_v3_agent=3).enable_v3_agent)


class TestSNMPv3(unittest.TestCase):
    def test_empty(self):
        empty = SNMPv3()
        self.assertTrue(empty.enable_agent)
        self.assertIsNone(empty.enable_v3_agent)
        self.assertIsNone(empty.usm_user)
        self.assertIsNone(empty.auth_algorithm)
        self.assertIsNone(empty.auth_password)
        self.assertIsNone(empty.priv_algorithm)
        self.assertIsNone(empty.priv_password)

    def test_valid(self):
        self.assertTrue(SNMPv3(enable_v3_agent=True).enable_v3_agent)
        self.assertEqual("my user", SNMPv3(usm_user="my user").usm_user)
        self.assertEqual("No Auth", SNMPv3(auth_algorithm="No Auth").auth_algorithm)
        self.assertEqual("MD5", SNMPv3(auth_algorithm="MD5").auth_algorithm)
        self.assertEqual("SHA", SNMPv3(auth_algorithm="SHA").auth_algorithm)
        self.assertEqual("secret", SNMPv3(auth_password="secret").auth_password)
        self.assertEqual("No Priv", SNMPv3(priv_algorithm="No Priv").priv_algorithm)
        self.assertEqual("DES", SNMPv3(priv_algorithm="DES").priv_algorithm)
        self.assertEqual("AES", SNMPv3(priv_algorithm="AES").priv_algorithm)
        self.assertEqual(
            "another secret", SNMPv3(priv_password="another secret").priv_password
        )

    def test_validation(self):
        with self.assertRaises(ValueError):
            SNMPv3(auth_algorithm="BLAH")
        with self.assertRaises(ValueError):
            SNMPv3(priv_algorithm="AES4096")


class TestSNMPIPv4(unittest.TestCase):
    def test_empty(self):
        empty = SNMPIPv4()
        self.assertIsNone(empty.enable_agent)
        self.assertIsNone(empty.get_community)
        self.assertIsNone(empty.set_community)
        self.assertIsNone(empty.manager_host_1)
        self.assertIsNone(empty.manager_host_2)
        self.assertIsNone(empty.manager_host_3)
        self.assertIsNone(empty.manager_host_subnet_1)
        self.assertIsNone(empty.manager_host_subnet_2)
        self.assertIsNone(empty.manager_host_subnet_3)

    def test_valid(self):
        self.assertTrue(SNMPIPv4(enable_agent=True).enable_agent)
        self.assertEqual("public", SNMPIPv4(get_community="public").get_community)
        self.assertEqual("private", SNMPIPv4(set_community="private").set_community)
        self.assertEqual(
            "192.168.0.1", SNMPIPv4(manager_host_1="192.168.0.1").manager_host_1
        )
        self.assertEqual(
            "255.255.255.255 / 32",
            SNMPIPv4(
                manager_host_subnet_2="255.255.255.255 / 32"
            ).manager_host_subnet_2,
        )

    def test_validation(self):
        with self.assertRaises(ValueError):
            SNMPIPv4(get_community="a very long string longer than is permitted")
        with self.assertRaises(ValueError):
            SNMPIPv4(
                set_community="a very long private string longer than is permitted"
            )
        with self.assertRaises(ValueError):
            SNMPIPv4(manager_host_3="google.com")
        with self.assertRaises(ValueError):
            SNMPIPv4(manager_host_subnet_1="255.255.0.0 / 16")


class TestSNMPIPv6(unittest.TestCase):
    def test_empty(self):
        empty = SNMPIPv6()
        self.assertIsNone(empty.enable_agent)
        self.assertIsNone(empty.get_community)
        self.assertIsNone(empty.set_community)
        self.assertIsNone(empty.manager_host_1)
        self.assertIsNone(empty.manager_host_2)
        self.assertIsNone(empty.manager_host_3)
        self.assertIsNone(empty.manager_host_prelen_1)
        self.assertIsNone(empty.manager_host_prelen_2)
        self.assertIsNone(empty.manager_host_prelen_3)

    def test_valid(self):
        self.assertTrue(SNMPIPv6(enable_agent=True).enable_agent)
        self.assertEqual("public", SNMPIPv6(get_community="public").get_community)
        self.assertEqual("private", SNMPIPv6(set_community="private").set_community)
        self.assertEqual(
            "fdfe:5d4d:384d:1:78fb:64c0:767b:9ed9",
            SNMPIPv6(
                manager_host_1="fdfe:5d4d:384d:1:78fb:64c0:767b:9ed9"
            ).manager_host_1,
        )
        self.assertEqual(1, SNMPIPv6(manager_host_prelen_1=1).manager_host_prelen_1)
        self.assertEqual(None, SNMPIPv6(manager_host_prelen_1="").manager_host_prelen_1)

    def test_validation(self):
        with self.assertRaises(ValueError):
            SNMPIPv6(get_community="a very long string longer than is permitted")
        with self.assertRaises(ValueError):
            SNMPIPv6(
                set_community="a very long private string longer than is permitted"
            )
        with self.assertRaises(ValueError):
            SNMPIPv6(manager_host_1="192.168.0.1")
        with self.assertRaises(ValueError):
            SNMPIPv6(manager_host_2="google.co.uk")
        with self.assertRaises(ValueError):
            SNMPIPv6(manager_host_prelen_3=256)


class TestSNMPTrapIPv4(unittest.TestCase):
    def test_empty(self):
        empty = SNMPTrapIPv4()
        self.assertIsNone(empty.community)
        self.assertIsNone(empty.timeout)
        self.assertIsNone(empty.host_1)
        self.assertIsNone(empty.host_2)

    def test_valid(self):
        self.assertEqual(
            "trap community", SNMPTrapIPv4(community="trap community").community
        )
        self.assertEqual(60, SNMPTrapIPv4(timeout=60).timeout)
        self.assertEqual("192.168.100.1", SNMPTrapIPv4(host_1="192.168.100.1").host_1)
        self.assertEqual("192.168.100.2", SNMPTrapIPv4(host_2="192.168.100.2").host_2)

    def test_validation(self):
        with self.assertRaises(ValueError):
            SNMPTrapIPv4(community="a very long string which is too long to be allowed")
        with self.assertRaises(ValueError):
            SNMPTrapIPv4(timeout=10000)
        with self.assertRaises(ValueError):
            SNMPTrapIPv4(host_1="my.domain.com")
        with self.assertRaises(ValueError):
            SNMPTrapIPv4(host_1="fdfe:5d4d:384d:1:d8df:ed2:eafa:70af")
        with self.assertRaises(ValueError):
            SNMPTrapIPv4(host_2="fdfe:5d4d:384d:1:d8df:ed2:eafa:70af")


class TestSNMPTrapIPv6(unittest.TestCase):
    def test_empty(self):
        empty = SNMPTrapIPv6()
        self.assertIsNone(empty.community)
        self.assertIsNone(empty.timeout)
        self.assertIsNone(empty.host_1)
        self.assertIsNone(empty.host_2)

    def test_valid(self):
        self.assertEqual(
            "trap community", SNMPTrapIPv6(community="trap community").community
        )
        self.assertEqual(60, SNMPTrapIPv6(timeout=60).timeout)
        self.assertEqual(
            "fdfe:5d4d:384d:1:78fb:64c0:767b:9ed9",
            SNMPTrapIPv6(host_1="fdfe:5d4d:384d:1:78fb:64c0:767b:9ed9").host_1,
        )
        self.assertEqual(
            "fdfe:5d4d:384d:1:d8df:ed2:eafa:70af",
            SNMPTrapIPv6(host_2="fdfe:5d4d:384d:1:d8df:ed2:eafa:70af").host_2,
        )

    def test_validation(self):
        with self.assertRaises(ValueError):
            SNMPTrapIPv6(community="a very long string which is too long to be allowed")
        with self.assertRaises(ValueError):
            SNMPTrapIPv6(timeout=10000)
        with self.assertRaises(ValueError):
            SNMPTrapIPv6(host_1="my.domain.com")
        with self.assertRaises(ValueError):
            SNMPTrapIPv6(host_1="192.168.100.100")
        with self.assertRaises(ValueError):
            SNMPTrapIPv6(host_2="192.168.100.100")
