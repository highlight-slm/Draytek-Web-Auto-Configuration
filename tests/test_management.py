import unittest

from draytekwebadmin.management import (
    Management,
    InternetAccessControl,
    AccessList,
    ManagementPort,
    BruteForceProtection,
    Encryption,
    CVM_AccessControl,
    AP_Management,
    DeviceManagement,
)


class TestManagement(unittest.TestCase):
    def test_empty(self):
        empty = Management()
        self.assertIsNone(empty.router_name)
        self.assertIsNone(empty.disable_auto_logout)
        self.assertIsNone(empty.enable_validation_code)

    def test_valid(self):
        self.assertEqual("Test Name", Management(router_name="Test Name").router_name)
        self.assertTrue(Management(disable_auto_logout=True).disable_auto_logout)
        self.assertTrue(Management(enable_validation_code=True).enable_validation_code)

    def test_validation(self):
        self.assertTrue(Management(disable_auto_logout="true").disable_auto_logout)
        self.assertTrue(Management(enable_validation_code=1).enable_validation_code)
        self.assertFalse(
            Management(disable_auto_logout="something").disable_auto_logout
        )


class TestManagementInternetAccessControl(unittest.TestCase):
    def test_empty(self):
        empty = InternetAccessControl()
        self.assertIsNone(empty.internet_management)
        self.assertIsNone(empty.domain_name_allowed)
        self.assertIsNone(empty.ftp_server)
        self.assertIsNone(empty.http_server)
        self.assertIsNone(empty.enforce_https_access)
        self.assertIsNone(empty.https_server)
        self.assertIsNone(empty.telnet_server)
        self.assertIsNone(empty.tr069_server)
        self.assertIsNone(empty.ssh_server)
        self.assertIsNone(empty.snmp_server)
        self.assertIsNone(empty.disable_ping_from_internet)

    def test_valid(self):
        self.assertTrue(
            InternetAccessControl(internet_management=True).internet_management
        )
        self.assertEqual(
            "a.b.com",
            InternetAccessControl(domain_name_allowed="a.b.com").domain_name_allowed,
        )
        self.assertTrue(InternetAccessControl(ftp_server=True).ftp_server)
        self.assertTrue(InternetAccessControl(http_server=True).http_server)
        self.assertTrue(
            InternetAccessControl(enforce_https_access=True).enforce_https_access
        )
        self.assertTrue(InternetAccessControl(https_server=True).https_server)
        self.assertTrue(InternetAccessControl(telnet_server=True).telnet_server)
        self.assertTrue(InternetAccessControl(tr069_server=True).tr069_server)
        self.assertTrue(InternetAccessControl(ssh_server=True).ssh_server)
        self.assertTrue(InternetAccessControl(snmp_server=True).snmp_server)
        self.assertTrue(
            InternetAccessControl(
                disable_ping_from_internet=True
            ).disable_ping_from_internet
        )

    def test_validation(self):
        self.assertTrue(InternetAccessControl(ftp_server="True").ftp_server)
        self.assertTrue(InternetAccessControl(http_server="Y").http_server)
        self.assertTrue(
            InternetAccessControl(enforce_https_access="1").enforce_https_access
        )
        self.assertTrue(
            InternetAccessControl(enforce_https_access=1).enforce_https_access
        )
        self.assertFalse(InternetAccessControl(snmp_server="Blah").snmp_server)


class TestmanagementAccessList(unittest.TestCase):
    def test_empty(self):
        empty = AccessList()
        self.assertIsNone(empty.list_1_ip_object_index)
        self.assertIsNone(empty.list_2_ip_object_index)
        self.assertIsNone(empty.list_3_ip_object_index)
        self.assertIsNone(empty.list_4_ip_object_index)
        self.assertIsNone(empty.list_5_ip_object_index)
        self.assertIsNone(empty.list_6_ip_object_index)
        self.assertIsNone(empty.list_7_ip_object_index)
        self.assertIsNone(empty.list_8_ip_object_index)
        self.assertIsNone(empty.list_9_ip_object_index)
        self.assertIsNone(empty.list_10_ip_object_index)

    def test_valid(self):
        self.assertEqual(1, AccessList(list_1_ip_object_index=1).list_1_ip_object_index)
        self.assertEqual(2, AccessList(list_2_ip_object_index=2).list_2_ip_object_index)
        self.assertEqual(3, AccessList(list_3_ip_object_index=3).list_3_ip_object_index)
        self.assertEqual(4, AccessList(list_4_ip_object_index=4).list_4_ip_object_index)
        self.assertEqual(5, AccessList(list_5_ip_object_index=5).list_5_ip_object_index)
        self.assertEqual(6, AccessList(list_6_ip_object_index=6).list_6_ip_object_index)
        self.assertEqual(7, AccessList(list_7_ip_object_index=7).list_7_ip_object_index)
        self.assertEqual(8, AccessList(list_8_ip_object_index=8).list_8_ip_object_index)
        self.assertEqual(9, AccessList(list_9_ip_object_index=9).list_9_ip_object_index)
        self.assertEqual(
            99, AccessList(list_10_ip_object_index=99).list_10_ip_object_index
        )


class TestManagementManagementPort(unittest.TestCase):
    def test_empty(self):
        empty = ManagementPort()
        self.assertIsNone(empty.user_defined_ports)
        self.assertIsNone(empty.telnet_port)
        self.assertIsNone(empty.http_port)
        self.assertIsNone(empty.https_port)
        self.assertIsNone(empty.ftp_port)
        self.assertIsNone(empty.tr069_port)
        self.assertIsNone(empty.ssh_port)

    def test_valid(self):
        self.assertTrue(ManagementPort(user_defined_ports=True).user_defined_ports)
        self.assertEqual(8023, ManagementPort(telnet_port=8023).telnet_port)
        self.assertEqual(8080, ManagementPort(http_port=8080).http_port)
        self.assertEqual(1443, ManagementPort(https_port=1443).https_port)
        self.assertEqual(8021, ManagementPort(ftp_port=8021).ftp_port)
        self.assertEqual(18069, ManagementPort(tr069_port=18069).tr069_port)
        self.assertEqual(8022, ManagementPort(ssh_port=8022).ssh_port)

    def test_validation(self):
        self.assertTrue(ManagementPort(user_defined_ports="true").user_defined_ports)
        self.assertFalse(ManagementPort(user_defined_ports="False").user_defined_ports)
        self.assertEqual(1234, ManagementPort(telnet_port="1234").telnet_port)
        self.assertEqual(6789, ManagementPort(http_port=6789.5).http_port)
        self.assertEqual(1, ManagementPort(https_port=True).https_port)
        self.assertEqual(0, ManagementPort(ftp_port=False).ftp_port)
        self.assertEqual(1, ManagementPort(tr069_port="1").tr069_port)
        with self.assertRaises(ValueError):
            self.assertTrue(ManagementPort(ssh_port="hello world").ssh_port)
        with self.assertRaises(ValueError):
            self.assertTrue(ManagementPort(tr069_port="655999").tr069_port)


class TestManagementBruceForceProtection(unittest.TestCase):
    def test_empty(self):
        empty = BruteForceProtection()
        self.assertIsNone(empty.enable)
        self.assertIsNone(empty.ftp_server)
        self.assertIsNone(empty.http_server)
        self.assertIsNone(empty.https_server)
        self.assertIsNone(empty.telnet_server)
        self.assertIsNone(empty.tr069_server)
        self.assertIsNone(empty.ssh_server)
        self.assertIsNone(empty.max_login_failures)
        self.assertIsNone(empty.penalty_period)

    def test_valid(self):
        self.assertTrue(BruteForceProtection(enable=True).enable)
        self.assertTrue(BruteForceProtection(ftp_server=True).ftp_server)
        self.assertTrue(BruteForceProtection(http_server=True).http_server)
        self.assertTrue(BruteForceProtection(https_server=True).https_server)
        self.assertTrue(BruteForceProtection(telnet_server=True).telnet_server)
        self.assertTrue(BruteForceProtection(tr069_server=True).tr069_server)
        self.assertTrue(BruteForceProtection(ssh_server=True).ssh_server)
        self.assertEqual(
            5, BruteForceProtection(max_login_failures=5).max_login_failures
        )
        self.assertEqual(60, BruteForceProtection(penalty_period=60).penalty_period)

    def test_validation(self):
        self.assertTrue(BruteForceProtection(ftp_server="true").ftp_server)
        self.assertFalse(BruteForceProtection(http_server="false").http_server)
        self.assertFalse(BruteForceProtection(http_server=99).http_server)
        with self.assertRaises(ValueError):
            self.assertTrue(BruteForceProtection(max_login_failures=1000))
        with self.assertRaises(ValueError):
            self.assertTrue(BruteForceProtection(penalty_period=99999999999))


class TestManagementEncryption(unittest.TestCase):
    def test_empty(self):
        empty = Encryption()
        self.assertIsNone(empty.tls_1_2)
        self.assertIsNone(empty.tls_1_1)
        self.assertIsNone(empty.tls_1_0)
        self.assertIsNone(empty.ssl_3_0)

    def test_valid(self):
        self.assertTrue(Encryption(tls_1_2=True).tls_1_2)
        self.assertTrue(Encryption(tls_1_1=True).tls_1_1)
        self.assertTrue(Encryption(tls_1_0=True).tls_1_0)
        self.assertTrue(Encryption(ssl_3_0=True).ssl_3_0)

    def test_validation(self):
        self.assertTrue(Encryption(ssl_3_0="True").ssl_3_0)
        self.assertFalse(Encryption(tls_1_1="Not a Boolean").tls_1_1)
        self.assertTrue(Encryption(tls_1_0=1).tls_1_0)


class TestManagementCVMAccessControl(unittest.TestCase):
    def test_empty(self):
        empty = CVM_AccessControl()
        self.assertIsNone(empty.enable)
        self.assertIsNone(empty.ssl_enable)
        self.assertIsNone(empty.port)
        self.assertIsNone(empty.ssl_port)

    def test_valid(self):
        self.assertTrue(CVM_AccessControl(enable=True).enable)
        self.assertFalse(CVM_AccessControl(enable=False).enable)
        self.assertTrue(CVM_AccessControl(ssl_enable=True).ssl_enable)
        self.assertEqual(1234, CVM_AccessControl(port=1234).port)
        self.assertEqual(5678, CVM_AccessControl(ssl_port=5678).ssl_port)

    def test_validation(self):
        self.assertFalse(CVM_AccessControl(enable="fred").enable)
        self.assertFalse(CVM_AccessControl(ssl_enable="fred").ssl_enable)
        self.assertEqual(1212, CVM_AccessControl(port="1212").port)
        with self.assertRaises(ValueError):
            self.assertTrue(CVM_AccessControl(ssl_port=999999).ssl_port)


class TestManagementAPManagement(unittest.TestCase):
    def test_empty(self):
        empty = AP_Management()
        self.assertIsNone(empty.enable)

    def test_valid(self):
        self.assertTrue(AP_Management(enable=True).enable)
        self.assertFalse(AP_Management(enable=False).enable)

    def test_validation(self):
        self.assertTrue(AP_Management(enable="True").enable)
        self.assertTrue(AP_Management(enable="1").enable)
        self.assertTrue(AP_Management(enable=1).enable)
        self.assertFalse(AP_Management(enable="not a bool").enable)


class TestManagementDeviceManagement(unittest.TestCase):
    def test_empty(self):
        empty = DeviceManagement()
        self.assertIsNone(empty.enable)
        self.assertIsNone(empty.respond_to_external_device)

    def test_valid(self):
        self.assertTrue(DeviceManagement(enable=True).enable)
        self.assertTrue(
            DeviceManagement(respond_to_external_device=True).respond_to_external_device
        )

    def test_validation(self):
        self.assertTrue(DeviceManagement(enable=1).enable)
        self.assertFalse(
            DeviceManagement(respond_to_external_device=0).respond_to_external_device
        )
