import unittest

from draytekwebadmin import DrayTekWebAdmin


class TestDraytek(unittest.TestCase):
    def test_empty(self):
        default = DrayTekWebAdmin()
        self.assertEqual(None, default.hostname)
        self.assertEqual("admin", default.username)
        self.assertEqual(None, default.password)
        self.assertEqual(443, default.port)
        self.assertTrue(default.use_https)
        self.assertFalse(default.reboot_required)

    def test_default(self):
        default = DrayTekWebAdmin(
            hostname="myhost", username="user123", password="secret"
        )
        self.assertEqual("myhost", default.hostname)
        self.assertEqual("user123", default.username)
        self.assertEqual("secret", default.password)
        self.assertEqual(443, default.port)
        self.assertTrue(default.use_https)
        self.assertEqual("https://myhost:443", default.url)
        self.assertFalse(default.reboot_required)

    def test_valid(self):
        valid = DrayTekWebAdmin(
            hostname="192.168.0.1",
            username="user123",
            password="secret",
            port=80,
            use_https=False,
        )
        self.assertEqual("http://192.168.0.1:80", valid.url)
        self.assertFalse(valid.use_https)

    def test_port_validation(self):
        port_test = DrayTekWebAdmin(
            hostname="myhost", username="user123", password="secret", port="8080"
        )
        self.assertEqual("https://myhost:8080", port_test.url)
        with self.assertRaises(ValueError):
            port_test.port = 100000
        with self.assertRaises(ValueError):
            port_test.port = "Not a Port Number"

    def test_hostname_validation(self):
        good_names = [
            "192.168.0.1",
            "fdfe:5d4d:384d:1:d8df:ed2:eafa:70af",
            "router.domain.com",
            "router",
        ]
        bad_names = [
            "192.168.100.500",
            "fdfe:5d4d:384d:1:d8df:ed2:eafa:70af:1abc",
            "--not-a-domain.com",
        ]
        host_test = DrayTekWebAdmin(
            hostname="myhost", username="user123", password="secret"
        )

        for hostname in good_names:
            host_test.hostname = hostname
            self.assertEqual(hostname, host_test.hostname)
        for hostname in bad_names:
            with self.assertRaises(ValueError) as cm:
                host_test.hostname = hostname
            self.assertEqual(
                f"Invalid hostname: {hostname}", str(cm.exception).rstrip()
            )

    # TODO: Fix up mocking with Toolium tests
    # @patch(
    #     "draytekwebadmin.draytek.LoginPage.login_error",
    #     autospec=True,
    #     return_value=False,
    # )
    # @patch("draytekwebadmin.draytek.load_driver", autospec=True)
    # def test_start_session_successful(self, mock_load_driver, mock_login_error):
    #     connection = DrayTekWebAdmin(
    #         hostname="myhost", username="user123", password="secret", port="8080"
    #     )
    #     connection.start_session()
    #     self.assertTrue(mock_load_driver.called)
    #     self.assertTrue(mock_login_error.called)
    #     self.assertTrue(connection.loggedin)

    # TODO: Fix up mocking with Toolium tests
    # @patch(
    #     "draytekwebadmin.draytek.LoginPage.login_error",
    #     autospec=True,
    #     return_value=True,
    # )
    # @patch("draytekwebadmin.draytek.load_driver", autospec=True)
    # def test_start_session_login_error(self, mock_load_driver, mock_login_error):
    #     connection = DrayTekWebAdmin(
    #         hostname="myhost", username="user123", password="secret", port="8080"
    #     )
    #     with self.assertRaises(RuntimeError):
    #         connection.start_session()
    #     self.assertTrue(mock_load_driver.called)
    #     self.assertTrue(mock_login_error.called)
    #     self.assertFalse(connection.loggedin)

    # TODO: Fix up mocking with Toolium tests
    # @patch(
    #     "draytekwebadmin.draytek.load_driver",
    #     autospec=True,
    #     side_effect=Exception("Test"),
    # )
    # def test_start_session_driver_error(self, mock_load_driver):
    #     connection = DrayTekWebAdmin(
    #         hostname="myhost", username="user123", password="secret", port="8080"
    #     )
    #     with self.assertRaises(RuntimeError) as cm:
    #         connection.start_session()
    #     self.assertEqual(
    #         "Unable to navigate to DrayTek Web Administration Console",
    #         str(cm.exception).rstrip(),
    #     )
    #     self.assertTrue(mock_load_driver.called)
    #     self.assertFalse(connection.loggedin)

    def test_read_settings(self):
        pass

    def test_write_settings(self):
        pass

    # TODO: Fix up mocking with Toolium tests
    # @patch(
    #     "draytekwebadmin.draytek.LoginPage.login_error",
    #     autospec=True,
    #     return_value=False,
    # )
    # @patch("draytekwebadmin.draytek.load_driver", autospec=True)
    # def test_reboot(self, mock_load_driver, mock_login_error):
    #     connection = DrayTekWebAdmin(
    #         hostname="myhost", username="user123", password="secret", port="8080"
    #     )
    #     connection.reboot_required = True
    #     connection.reboot()
    #     self.assertTrue(mock_load_driver.called)
    #     self.assertFalse(connection.reboot_required)

    def test_upgrade_preview(self):
        pass

    def test_upgrade(self):
        pass
