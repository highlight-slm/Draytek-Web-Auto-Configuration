import unittest
from unittest.mock import patch
from pathlib import Path

from draytekwebadmin.firmware import Firmware


class TestFirmware(unittest.TestCase):
    def setUp(self):
        self.firmware_file_name = r"c:\test path\file name.test"

    def tearDown(self):
        pass

    def test_empty(self):
        empty = Firmware()
        self.assertIsNone(empty.filepath)
        self.assertIsNone(empty.model)
        self.assertIsNone(empty.firmware_current)
        self.assertIsNone(empty.firmware_current)
        self.assertIsNone(empty.modem_firmware_current)
        self.assertIsNone(empty.modem_firmware_target)

    @patch("pathlib.Path.exists", return_value=True)
    def test_valid(self, mock_path_exists):
        self.assertEqual("My Model Name", Firmware(model="My Model Name").model)
        self.assertEqual(
            "1.2.3.4", Firmware(firmware_current="1.2.3.4").firmware_current
        )
        self.assertEqual("5.6.7.8", Firmware(firmware_target="5.6.7.8").firmware_target)
        self.assertEqual(
            "ABC12345",
            Firmware(modem_firmware_current="ABC12345").modem_firmware_current,
        )
        self.assertEqual(
            "XYZ6789", Firmware(modem_firmware_target="XYZ6789").modem_firmware_target
        )
        self.assertEqual(
            Path(self.firmware_file_name),
            Firmware(filepath=self.firmware_file_name).filepath,
        )
        self.assertTrue(mock_path_exists.called)

    @patch("pathlib.Path.exists", return_value=False)
    def test_validation(self, mock_path_exists):
        with self.assertRaises(ValueError) as cm:
            self.assertTrue(Firmware(filepath=self.firmware_file_name))
        self.assertTrue(mock_path_exists.called)
        self.assertEqual("Firmware: File Not Found!", str(cm.exception).rstrip())

    def test_Router_Firmware_Upgradeable(self):
        self.assertTrue(
            Firmware.router_firmware_upgradable(
                Firmware(firmware_current="1.2.3.4", firmware_target="4.5.6.6")
            )
        )
        self.assertFalse(
            Firmware.router_firmware_upgradable(
                Firmware(firmware_current="1.2.3.4", firmware_target="1.2.3.4")
            )
        )

    def test_Modem_Firmware_Upgradeable(self):
        self.assertTrue(
            Firmware.modem_firmware_upgradable(
                Firmware(
                    modem_firmware_current="ABC1234", modem_firmware_target="XYZ5678"
                )
            )
        )
        self.assertFalse(
            Firmware.modem_firmware_upgradable(
                Firmware(
                    modem_firmware_current="ABC1234", modem_firmware_target="ABC1234"
                )
            )
        )
