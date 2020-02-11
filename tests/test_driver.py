import unittest
from unittest.mock import patch
from selenium.common.exceptions import WebDriverException

from draytekwebadmin.driver import load_driver, unload_driver


class TestDriver(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    @patch("selenium.webdriver.FirefoxOptions", autospec=True)
    @patch("selenium.webdriver.Firefox", autospec=True)
    def test_Load_Driver_Named_Firefox(self, mock_firefox, mock_FirefoxOptions):
        load_driver(browser_name="firefox")
        self.assertTrue(mock_firefox.called)
        self.assertTrue(mock_FirefoxOptions.called)
        self.assertTrue(mock_firefox().maximize_window.called)
        self.assertFalse(mock_FirefoxOptions().headless)

    @patch("selenium.webdriver.FirefoxOptions", autospec=True)
    @patch("selenium.webdriver.Firefox", autospec=True)
    def test_Load_Driver_Named_Firefox_Headless(
        self, mock_firefox, mock_FirefoxOptions
    ):
        load_driver(browser_name="firefox", headless=True)
        self.assertTrue(mock_firefox.called)
        self.assertTrue(mock_FirefoxOptions.called)
        self.assertTrue(mock_FirefoxOptions().headless)

    @patch("selenium.webdriver.ChromeOptions", autospec=True)
    @patch("selenium.webdriver.Chrome", autospec=True)
    def test_Load_Driver_Named_Chrome(self, mock_chrome, mock_ChromeOptions):
        load_driver(browser_name="chrome")
        self.assertTrue(mock_chrome.called)
        self.assertTrue(mock_ChromeOptions.called)
        self.assertFalse(mock_ChromeOptions().headless)

    @patch("selenium.webdriver.ChromeOptions", autospec=True)
    @patch("selenium.webdriver.Chrome", autospec=True)
    def test_Load_Driver_Named_Chrome_Headless(self, mock_chrome, mock_ChromeOptions):
        load_driver(browser_name="chrome", headless=True)
        self.assertTrue(mock_chrome.called)
        self.assertTrue(mock_ChromeOptions.called)
        self.assertTrue(mock_ChromeOptions().headless)

    @patch("selenium.webdriver.Edge", autospec=True)
    def test_Load_Driver_Named_Edge(self, mock_edge):
        load_driver(browser_name="edge")
        self.assertTrue(mock_edge.called)

    @patch("draytekwebadmin.driver.load_firefox", autospec=True)
    def test_Load_Driver_Unspecified_Browser(self, mock_load_firefox):
        load_driver()
        self.assertTrue(mock_load_firefox.called)

    def test_Load_Driver_Unsupported_Browser(self):
        with self.assertRaises(Exception):
            load_driver(browser_name="NonExistent Browser")

    @patch("draytekwebadmin.driver.load_firefox", side_effect=WebDriverException())
    @patch("draytekwebadmin.driver.load_chrome", side_effect=WebDriverException())
    @patch("draytekwebadmin.driver.load_edge", side_effect=WebDriverException())
    def test_Load_Driver_FallThrough(self, mock_edge, mock_chrome, mock_firefox):
        with self.assertRaises(Exception) as cm:
            load_driver()
        self.assertEqual(
            "Unable to find suitable browser. Error Message: None",
            str(cm.exception).rstrip(),
        )

    @patch("selenium.webdriver.firefox")
    def test_Unload_Driver(self, mock_firefox):
        unload_driver(mock_firefox())
        self.assertTrue(mock_firefox().quit.called)
