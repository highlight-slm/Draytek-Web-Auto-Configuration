"""Draytek Web Admin - Web API Library."""

import logging

from draytekwebadmin.driver import load_driver, unload_driver
from draytekwebadmin.pages import (
    LoginPage,
    SNMPpage,
    RebootSystemPage,
    ManagementPage,
    FirmwareUpgradePage,
    DashboardPage,
)
from draytekwebadmin.utils import (
    bool_or_none,
    port_or_none,
    valid_hostname,
    valid_ipv4_address,
    valid_ipv6_address,
)

LOGGER = logging.getLogger("root")
LOGGER.setLevel(logging.INFO)


class DrayTekWebAdmin:
    """DrayTek web based administration console."""

    def __init__(
        self,
        hostname=None,
        username="admin",
        password=None,
        port=443,
        use_https=True,
        browsername="",
        headless=False,
    ):
        """
        Create a web session to the web administration console.

        Args:
            hostname: IP address or DNS name of Web admin interface on the router
            port: (optional) Port running the web admin console (Default: 443)
            username: Web admin account username (default: admin)
            password: Password for admin account
            use_https: (optional) Use https instead of http (Default: True)
            browsername: (optional) Name of browser to attempt to use, will attempt to auto-detect if blank
            headless: (optional) Use a headless browser session if possible (Default: False)

        """
        self.hostname = hostname
        self.port = port
        self.username = username
        self.password = password
        self.use_https = use_https
        self.browsername = browsername
        self.headless = headless
        self.loggedin = False
        self.reboot_required = False
        self.routerinfo = None
        self._driver = None
        self._url = None

    def __setattr__(self, name, value):
        if name == "hostname":
            if not (
                valid_hostname(value)
                or valid_ipv4_address(value)
                or valid_ipv6_address(value)
            ):
                raise ValueError(f"Invalid hostname: {value}")
        if name in ["use_https", "headless", "loggedin", "reboot_required"]:
            value = bool_or_none(value)
        elif name == "port":
            value = port_or_none(value)
        super(DrayTekWebAdmin, self).__setattr__(name, value)

    @property
    def driver(self):
        """Return current webdriver instance, creating if needed.

        Args: None

        Returns:WebDriver instance

        """
        if self._driver is None:
            try:
                LOGGER.info("Creating WebDriver and opening session")
                self._driver = load_driver(self.browsername, self.headless)
                self._driver.get(self.url)
                LOGGER.info("Connected to Router")
            except Exception:
                self.close_session()
                raise RuntimeError(
                    "Unable to navigate to DrayTek Web Administration Console"
                )
        return self._driver

    @property
    def url(self):
        """Construct the url for the Web Administration Console.

        Args: None

        Returns:
            url: Formatted URL string for Web Administaton Console

        """
        LOGGER.info("Building URL for Management Console")
        web_protocol = "https"
        if not self.use_https:
            web_protocol = "http"
            LOGGER.warning(
                "Using HTTP connnection is insecure, please reconfigure your system to use HTTPS."
            )
        self._url = f"{web_protocol}://{self.hostname}:{self.port}"
        return self._url

    def start_session(self):
        """Start selenium webdriver session.

           Logs user in, if not already logged in.
           Collects basic RouterInfo

        Args: None

        Returns:
            None or Exception

        """
        if not self.loggedin:
            self.login()
            self.routerinfo = DashboardPage(self.driver).routerinfo()
            LOGGER.info(
                f"Connected to: {self.hostname} - {self.routerinfo.router_name} - "
                f"{self.routerinfo.model} - {self.routerinfo.firmware}"
            )

    def close_session(self):
        """Close selenium webdriver session.

        Args: None

        Returns:
            None or Exception

        """
        if self._driver:
            unload_driver(self.driver)

    def login(self):
        """Login to the DrayTek Web Administration Console. If login successful then loggedin property set to True.

        Args: None

        Returns:
            None or Exception

        """
        LOGGER.info("Opening Login Page.")
        loginpage = LoginPage(self.driver)
        loginpage.login(self.username, self.password)
        if loginpage.login_error():
            # TODO (#4414): Need to fix
            # If remote WAN access is disabled, page is still accessible, but can't login and no error is reported
            message = loginpage.error_message()
            LOGGER.error(f"Login Failed - Error: {message}")
            raise RuntimeError(message)
        self.loggedin = True
        LOGGER.info("Successful Login.")

    def read_settings(self, settings):
        """Read Router Settings for a specified type.

        Args:
            settings: Object of the type of settings requested

        Returns:
            object: of Type requested with the current settings

        """
        name = settings.__name__
        self.start_session()
        LOGGER.info(f"Reading {name} Settings.")
        if name == "SNMPIPv4":
            return SNMPpage(self.driver).read_snmp_ipv4_settings()
        # if name == "SNMPIPv6":
        #     return SNMPpage(self.driver).read_SNMPIPv6_settings()
        if name == "InternetAccessControl":
            return ManagementPage(self.driver).read_internet_access_control_settings()
        raise TypeError(f"Unexpected object type: {name}")

    def write_settings(self, settings):
        """Apply Router Settings for a specified type. Update property if changes require a device reboot.

        Args:
            settings: Object cointaining the settings to apply

        Returns:
            reboot required: True if changes resulted in a reboot being required

        """
        reboot_req = False
        name = type(settings).__name__

        self.start_session()
        LOGGER.info(f"Applying new {name} Settings.")

        if name == "SNMPIPv4":
            reboot_req = SNMPpage(self.driver).write_snmp_ipv4_settings(settings)
            # return SNMPpage(self.driver).write_SNMPIPv4_settings(settings)
        # elif name == "SNMPIPv6":
        #     reboot_req = SNMPpage(self.driver).write_SNMPIPv6_settings(settings)
        elif name == "InternetAccessControl":
            reboot_req = ManagementPage(
                self.driver
            ).write_internet_access_control_settings(settings)
        else:
            raise TypeError(f"Unexpected object type: {name}")

        if reboot_req:
            self.reboot_required = True
        return reboot_req

    def reboot(self):
        """Reboot Router - System Maintenance >> Reboot System.

        Args: None

        Returns: None

        """
        self.start_session()
        LOGGER.info("Rebooting Router.")
        RebootSystemPage(self.driver).reboot()
        self.reboot_required = False

    def upgrade_preview(self, firmware):
        """Preview firmware upgrade - System Maintenance >> Firmware Upgrade.

        Args:
            firmware: Firmware object containing full file path for new firmware

        Returns:
            Firmware object: Properties set for based on the previewing the firmware

        """
        if firmware.filepath is None:
            return ValueError("Firmware filepath not set")
        self.start_session()
        LOGGER.info("Opening firmware page for preview")
        new_firmware = FirmwareUpgradePage(self.driver).new_firmware_preview(firmware)
        # Patch in the current firmware version which oddly isn't shown on the preview page
        new_firmware.firmware_current = self.routerinfo.firmware
        return new_firmware

    def upgrade(self, firmware):
        """Upgrade firmware - System Maintenance >> Firmware Upgrade.

        Args:
            firmware: Firmware object containing full file path for new firmware

        Returns:
            Upgrading: (bool) True if firmware is being updated and router rebooted

        """
        if firmware.filepath is None:
            return ValueError("Firmware filepath not set")
        self.start_session()
        LOGGER.info("Opening firmware page for upgrade")
        upgrading = FirmwareUpgradePage(self.driver).new_firmware_install(firmware)
        if upgrading:
            LOGGER.info("Upgraded firmware and rebooted")
            return True
        return False
