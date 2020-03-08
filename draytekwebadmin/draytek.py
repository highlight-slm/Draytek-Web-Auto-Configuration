"""Draytek Web Admin - Web API Library."""

import logging

from draytekwebadmin.driver import TooliumSession
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
LOGGER.setLevel(logging.ERROR)


class DrayTekWebAdmin:
    """DrayTek web based administration console."""

    def __init__(
        self,
        hostname=None,
        username="admin",
        password=None,
        port=443,
        use_https=True,
        config_dir=None,
    ):
        """Create a web session to the web administration console.

        :param hostname: IP address or DNS name of Web admin interface on the router
        :param port: (optional) Port running the web admin console (Default: 443)
        :param username: Web admin account username (default: admin)
        :param password: Password for admin account
        :param use_https: (optional) Use https instead of http (Default: True)
        :param config_dir: (optional) Path to toolium configuration files
        """
        self.hostname = hostname
        self.port = port
        self.username = username
        self.password = password
        self.use_https = use_https
        self.config_dir = config_dir
        self.loggedin = False
        self.reboot_required = False
        self.routerinfo = None
        self._url = None
        self._session = None

    def __setattr__(self, name, value):
        if name == "hostname":
            if not (
                valid_hostname(value)
                or valid_ipv4_address(value)
                or valid_ipv6_address(value)
            ):
                raise ValueError(f"Invalid hostname: {value}")
        if name in ["use_https", "loggedin", "reboot_required"]:
            value = bool_or_none(value)
        elif name == "port":
            value = port_or_none(value)
        super(DrayTekWebAdmin, self).__setattr__(name, value)

    @property
    def session(self):
        """Return toolium session instance, creating if needed.

        :returns: toolium session
        """
        if self._session is None:
            try:
                LOGGER.info("Creating and opening session")
                self._session = TooliumSession()
                self._session.setUp(configuration_directory=self.config_dir)
                self._session.driver.get(self.url)
                LOGGER.info(f"Connected to: {self.url} - {self._session.driver.title}")
            except Exception:
                self.close_session()
                raise RuntimeError(
                    "Unable to navigate to DrayTek Web Administration Console"
                )
        return self._session

    @property
    def url(self):
        """Construct the url for the Web Administration Console.

        :returns: Formatted URL string for Web Administration Console
        """
        LOGGER.info("Building URL for Management Console")
        web_protocol = "https"
        if not self.use_https:
            web_protocol = "http"
            LOGGER.warning(
                "Using HTTP connection is insecure, please reconfigure your system to use HTTPS."
            )
        self._url = f"{web_protocol}://{self.hostname}:{self.port}"
        return self._url

    def start_session(self):
        """Start selenium webdriver session via toolium.

        Logs user in, if not already logged in.
        Collects basic RouterInfo
        """
        if not self.loggedin:
            self.login()
            self.routerinfo = DashboardPage(
                driver_wrapper=self.session.driver_wrapper
            ).routerinfo()
            LOGGER.info(
                f"Connected to: {self.hostname} - {self.routerinfo.router_name} - "
                f"{self.routerinfo.model} - {self.routerinfo.firmware}"
            )

    def close_session(self):
        """Close selenium webdriver session."""
        if self._session:
            self._session.tearDown()

    def login(self):
        """Login to the DrayTek Web Administration Console. If login successful then loggedin property set to True."""
        LOGGER.info("Opening Login Page.")
        loginpage = LoginPage(
            driver_wrapper=self.session.driver_wrapper
        ).wait_until_loaded()
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

        :param settings: Object of the type of settings requested
        :returns: object: of Type requested with the current settings
        """
        name = settings.__name__
        self.start_session()
        LOGGER.info(f"Reading {name} Settings.")
        if name == "SNMPIPv4":
            return SNMPpage(
                driver_wrapper=self.session.driver_wrapper
            ).read_snmp_ipv4_settings()
        if name == "SNMPIPv6":
            return SNMPpage(
                driver_wrapper=self.session.driver_wrapper
            ).read_snmp_ipv6_settings()
        if name == "SNMPTrapIPv4":
            return SNMPpage(
                driver_wrapper=self.session.driver_wrapper
            ).read_snmp_ipv4_trap_setting()
        if name == "SNMPTrapIPv6":
            return SNMPpage(
                driver_wrapper=self.session.driver_wrapper
            ).read_snmp_ipv6_trap_setting()
        if name == "SNMPv3":
            return SNMPpage(
                driver_wrapper=self.session.driver_wrapper
            ).read_snmp_v3_settings()
        if name == "Management":
            return ManagementPage(
                driver_wrapper=self.session.driver_wrapper
            ).read_management_settings()
        if name == "InternetAccessControl":
            return ManagementPage(
                driver_wrapper=self.session.driver_wrapper
            ).read_internet_access_control_settings()
        if name == "AccessList":
            return ManagementPage(
                driver_wrapper=self.session.driver_wrapper
            ).read_access_list_settings()
        if name == "ManagementPort":
            return ManagementPage(
                driver_wrapper=self.session.driver_wrapper
            ).read_management_port_settings()
        if name == "Encryption":
            return ManagementPage(
                driver_wrapper=self.session.driver_wrapper
            ).read_encryption_settings()
        if name == "BruteForceProtection":
            return ManagementPage(
                driver_wrapper=self.session.driver_wrapper
            ).read_brute_force_protection_settings()
        if name == "CVM_AccessControl":
            return ManagementPage(
                driver_wrapper=self.session.driver_wrapper
            ).read_cvm_access_control_settings()
        if name == "AP_Management":
            return ManagementPage(
                driver_wrapper=self.session.driver_wrapper
            ).read_ap_management_settings()
        if name == "DeviceManagement":
            return ManagementPage(
                driver_wrapper=self.session.driver_wrapper
            ).read_device_management_settings()
        if name == "LAN_Access":
            return ManagementPage(
                driver_wrapper=self.session.driver_wrapper
            ).read_lan_access_settings()
        raise TypeError(f"Unexpected object type: {name}")

    def write_settings(self, settings):
        """Apply Router Settings for a specified type. Update property if changes require a device reboot.

        :param settings: Object containing the settings to apply
        :returns: True if changes resulted in a reboot being required
        """
        reboot_req = False
        name = type(settings).__name__

        self.start_session()
        LOGGER.info(f"Applying new {name} Settings.")

        if name == "SNMPIPv4":
            reboot_req = SNMPpage(
                driver_wrapper=self.session.driver_wrapper
            ).write_snmp_ipv4_settings(settings)
        elif name == "SNMPIPv6":
            reboot_req = SNMPpage(
                driver_wrapper=self.session.driver_wrapper
            ).write_snmp_ipv6_settings(settings)
        elif name == "SNMPTrapIPv4":
            reboot_req = SNMPpage(
                driver_wrapper=self.session.driver_wrapper
            ).write_snmp_ipv4_trap_settings(settings)
        elif name == "SNMPTrapIPv6":
            reboot_req = SNMPpage(
                driver_wrapper=self.session.driver_wrapper
            ).write_snmp_ipv6_trap_settings(settings)
        elif name == "SNMPv3":
            reboot_req = SNMPpage(
                driver_wrapper=self.session.driver_wrapper
            ).write_snmp_v3_settings(settings)
        elif name == "Management":
            reboot_req = ManagementPage(
                driver_wrapper=self.session.driver_wrapper
            ).write_management_settings(settings)
        elif name == "InternetAccessControl":
            reboot_req = ManagementPage(
                driver_wrapper=self.session.driver_wrapper
            ).write_internet_access_control_settings(settings)
        elif name == "AccessList":
            reboot_req = ManagementPage(
                driver_wrapper=self.session.driver_wrapper
            ).write_access_list_settings(settings)
        elif name == "ManagementPort":
            reboot_req = ManagementPage(
                driver_wrapper=self.session.driver_wrapper
            ).write_management_port_settings(settings)
        elif name == "BruteForceProtection":
            reboot_req = ManagementPage(
                driver_wrapper=self.session.driver_wrapper
            ).write_brute_force_protection_settings(settings)
        elif name == "Encryption":
            reboot_req = ManagementPage(
                driver_wrapper=self.session.driver_wrapper
            ).write_encryption_settings(settings)
        elif name == "CVM_AccessControl":
            reboot_req = ManagementPage(
                driver_wrapper=self.session.driver_wrapper
            ).write_cvm_access_control_settings(settings)
        elif name == "AP_Management":
            reboot_req = ManagementPage(
                driver_wrapper=self.session.driver_wrapper
            ).write_ap_management_settings(settings)
        elif name == "DeviceManagement":
            reboot_req = ManagementPage(
                driver_wrapper=self.session.driver_wrapper
            ).write_device_management_settings(settings)
        elif name == "LAN_Access":
            reboot_req = ManagementPage(
                driver_wrapper=self.session.driver_wrapper
            ).write_lan_access_settings(settings)
        else:
            raise TypeError(f"Unexpected object type: {name}")

        if reboot_req:
            self.reboot_required = True
        return reboot_req

    def reboot(self):
        """Reboot Router - System Maintenance >> Reboot System."""
        self.start_session()
        LOGGER.info("Rebooting Router.")
        RebootSystemPage(driver_wrapper=self.session.driver_wrapper).reboot()
        self.reboot_required = False

    def upgrade_preview(self, firmware):
        """Preview firmware upgrade - System Maintenance >> Firmware Upgrade.

        :param firmware: Firmware object containing full file path for new firmware
        :returns: Firmware object: Properties set for based on the previewing the firmware
        """
        if firmware.filepath is None:
            return ValueError("Firmware filepath not set")
        self.start_session()
        LOGGER.info("Opening firmware page for preview")
        new_firmware = FirmwareUpgradePage(
            driver_wrapper=self.session.driver_wrapper
        ).new_firmware_preview(firmware)
        # Patch in the current firmware version which oddly isn't shown on the preview page
        new_firmware.firmware_current = self.routerinfo.firmware
        return new_firmware

    def upgrade(self, firmware):
        """Upgrade firmware - System Maintenance >> Firmware Upgrade.

        :param firmware: Firmware object containing full file path for new firmware
        :returns: (bool) True if firmware is being updated and router rebooted
        """
        if firmware.filepath is None:
            return ValueError("Firmware filepath not set")
        self.start_session()
        LOGGER.info("Opening firmware page for upgrade")
        upgrading = FirmwareUpgradePage(
            driver_wrapper=self.session.driver_wrapper
        ).new_firmware_install(firmware)
        if upgrading:
            LOGGER.info("Upgraded firmware and rebooted")
            return True
        return False
