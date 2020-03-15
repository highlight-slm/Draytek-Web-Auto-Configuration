"""Draytek Web Admin - Toolium Session."""
from os import getcwd, environ
from pathlib import Path
import logging


from toolium import test_cases
from draytekwebadmin.utils import bool_or_none, int_or_none

LOGGER = logging.getLogger("root")


class TooliumSession(test_cases.SeleniumTestCase):
    """Toolium Session."""

    def setUp(
        self,
        config_dir=None,
        browser=None,
        search_driver=None,
        headless=None,
        implicit_wait=None,
        explicit_wait=None,
    ):
        """Override setUp function to enable config file directory to be configured.

        :param config_dir: path to config file location
        :param browser: browser name [chrome|firefox] overriding configuration file setting
        :param search_browser_driver: Attempt to locate browser driver in current working directory
        :param headless: Boolean flag to run the session headless, overriding configuration file setting
        :param implicit_wait: wait time in seconds, overriding configuration file setting
        :param explicit_wait: wait time in seconds, overriding configuration file setting
        """
        self.config_files.set_config_properties_filenames(
            "properties.cfg", "local-properties.cfg"
        )
        configuration_dir = self._locate_config_dir(config_dir)
        if configuration_dir:
            self.config_files.set_config_directory(str(configuration_dir))
        if browser:
            self._override_browser_type(browser)
        if search_driver:
            self._locate_browser_driver()
        if headless:
            self._override_headless(headless)
        if implicit_wait:
            self._override_implicit_wait(implicit_wait)
        if explicit_wait:
            self._override_explcit_wait(explicit_wait)
        super(TooliumSession, self).setUp()

    def _locate_config_dir(self, config_dir=None):
        """Attempt to locate configuration files for Toolium.

        :return: File path to valid configuration directory (as str) or None otherwise
        """
        conf_dir = None
        if config_dir:
            conf_dir = self._validate_config_dir(config_dir)
        if not conf_dir:
            conf_dir = self._validate_config_dir(Path(getcwd(), "conf"))
            if not conf_dir:
                conf_dir = self._validate_config_dir(
                    Path(getcwd(), "draytekwebadmin", "conf")
                )
        return conf_dir

    @staticmethod
    def _validate_config_dir(config_directory):
        """Validate configuration file location.

        :param config_directory: Full file path for configuration file to use
        :return: validated config file path (as str)
        """
        conf_dir_str = str(config_directory)
        return conf_dir_str if Path(str(conf_dir_str)).exists() else None

    @staticmethod
    def _override_browser_type(browser):
        """Override configuration file setting for browser type.

        :param browser: browser name [chrome|firefox]
        """
        browser = str(browser).lower()
        if browser in ["chrome", "firefox"]:
            environ["Driver_type"] = browser

    @staticmethod
    def _locate_browser_driver():
        """Search local directory for browser drivers. Override configuration file."""
        # Search for Chrome Driver (chromedriver.exe)
        chrome_driver = Path(getcwd(), "chromedriver.exe")
        if chrome_driver.exists():
            environ["Driver_chrome_driver_path"] = str(chrome_driver)
        else:
            chrome_driver = Path(getcwd(), "conf", "chromedriver.exe")
            if chrome_driver.exists():
                environ["Driver_chrome_driver_path"] = str(chrome_driver)
            else:
                chrome_driver = Path(getcwd(), "driver", "chromedriver.exe")
                if chrome_driver.exists():
                    environ["Driver_chrome_driver_path"] = str(chrome_driver)

        # Search for Firefox Driver (geckodriver.exe)
        firefox_driver = Path(getcwd(), "geckodriver.exe")
        if firefox_driver.exists():
            environ["Driver_gecko_driver_path"] = str(firefox_driver)
        else:
            firefox_driver = Path(getcwd(), "conf", "geckodriver.exe")
            if firefox_driver.exists():
                environ["Driver_gecko_driver_path"] = str(firefox_driver)
            else:
                firefox_driver = Path(getcwd(), "driver", "geckodriver.exe")
                if firefox_driver.exists():
                    environ["Driver_gecko_driver_path"] = str(firefox_driver)

    @staticmethod
    def _override_headless(headless):
        """Override configuration file setting for headless session state.

        :param headless: Boolean flag to run the session headless
        """
        if bool_or_none(headless):
            environ["Driver_headless"] = str(bool_or_none(headless))

    @staticmethod
    def _override_implicit_wait(wait):
        """Override configuration file setting for Implicitly Wait.

        :param wait: time in seconds
        """
        if int_or_none(wait):
            environ["Driver_implicitly_wait"] = str(wait)

    @staticmethod
    def _override_explcit_wait(wait):
        """Override configuration file setting for Explicitly Wait.

        :param wait: time in seconds
        """
        if int_or_none(wait):
            environ["Driver_explicitly_wait"] = str(wait)
