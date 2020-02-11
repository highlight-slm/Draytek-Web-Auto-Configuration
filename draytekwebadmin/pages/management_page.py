"""Draytek Web Admin - Management Page."""

from selenium.webdriver.common.by import By
from page_elements import CheckBox, Element, InputField

from draytekwebadmin.management import (
    AccessList,
    AP_Management,
    BruteForceProtection,
    CVM_AccessControl,
    DeviceManagement,
    InternetAccessControl,
    Management,
    ManagementPort,
    Encryption,
)
from draytekwebadmin.pages.basepage import BasePage
from draytekwebadmin.pages.menu_navigator import MenuNavigator


class ManagementPage(BasePage):
    """Selenium Page Object Model: ManagementPage."""

    # Page Elements
    management_setup_tab = Element(By.ID, "tab1")
    lan_access_setup_tab = Element(By.ID, "tab3")
    ok_button = Element(By.CLASS_NAME, "btnw")

    # TAB: Management Setup
    router_name = InputField(By.NAME, "sRouterName")
    disable_auto_logout = CheckBox(By.NAME, "sDeflogoff")
    enable_validation_code = CheckBox(By.NAME, "sValidatedCode")

    # Internet Access Control
    enable_internet_access = CheckBox(By.NAME, "sRMC")
    domain_name_allowed = InputField(By.NAME, "sSysAllDomain")
    ftp = CheckBox(By.NAME, "sRMCFtp")
    http = CheckBox(By.NAME, "sRMCHttp")
    enforce_https_access = CheckBox(By.NAME, "iRMCHsfrc")
    https = CheckBox(By.NAME, "sRMCHttps")
    telnet = CheckBox(By.NAME, "sRMCTelnet")
    tr069 = CheckBox(By.NAME, "sRMCTr069")
    ssh = CheckBox(By.NAME, "sRMCSsh")
    snmp = CheckBox(By.NAME, "sRMCSnmp")
    disable_ping_from_internet = CheckBox(By.NAME, "sWPing")

    # Access List from the Internet
    access_index_1 = InputField(By.NAME, "index1")
    access_index_2 = InputField(By.NAME, "index2")
    access_index_3 = InputField(By.NAME, "index3")
    access_index_4 = InputField(By.NAME, "index4")
    access_index_5 = InputField(By.NAME, "index5")
    access_index_6 = InputField(By.NAME, "index6")
    access_index_7 = InputField(By.NAME, "index7")
    access_index_8 = InputField(By.NAME, "index8")
    access_index_9 = InputField(By.NAME, "index9")
    access_index_10 = InputField(By.NAME, "index10")

    # Management Port Setup
    user_defined_ports_radio = Element(
        By.XPATH,
        "//input[@name='ConfigPort' and @type='radio' and @value='UserDefine']",
    )
    default_ports_radio = Element(
        By.XPATH, "//input[@name='ConfigPort' and @type='radio' and @value='Default']"
    )
    telnet_port = InputField(By.NAME, "TelnetPort")
    http_port = InputField(By.NAME, "HttpPort")
    https_port = InputField(By.NAME, "HttpsPort")
    ftp_port = InputField(By.NAME, "txtFtpPort")
    tr069_port = InputField(By.NAME, "txtTr069Port")
    ssh_port = InputField(By.NAME, "txtSshPort")

    # Bruce Force Protection
    enable_brute_force_login_protection = CheckBox(By.NAME, "iBrEn")
    bf_ftp = CheckBox(By.NAME, "iBrFtp")
    bf_http = CheckBox(By.NAME, "iBrHttp")
    bf_https = CheckBox(By.NAME, "iBrHttps")
    bf_telnet = CheckBox(By.NAME, "iBrTelnet")
    bf_tr069 = CheckBox(By.NAME, "iBrTr069")
    bf_ssh = CheckBox(By.NAME, "iBrSsh")
    bf_max_login_failures = InputField(By.NAME, "iLoginFailures")
    bf_penality_period = InputField(By.NAME, "iPenaltyPeriod")

    # TLS/SSL Encryption Setup
    enc_tls12 = CheckBox(By.NAME, "enTLSv1_2")
    enc_tls11 = CheckBox(By.NAME, "enTLSv1_1")
    enc_tls10 = CheckBox(By.NAME, "enTLSv1")
    enc_ssl30 = CheckBox(By.NAME, "enSSLv3")

    # CVM Access Control
    cvm_port_enable = CheckBox(By.NAME, "CvmHttpEnb")
    cvm_port = InputField(By.NAME, "CvmHttpPort")
    cvm_ssl_port_enable = CheckBox(By.NAME, "CvmHttpsEnb")
    cvm_ssl_port = InputField(By.NAME, "CvmHttpsPort")

    # AP Management
    ap_management = CheckBox(By.NAME, "ApmEn")

    # Device Management
    device_management = CheckBox(By.NAME, "chkDevMng")
    device_management_respond_external = CheckBox(By.NAME, "")

    # TAB: LAN Access Setup
    allow_management_from_lan = CheckBox(By.NAME, "sMngtfrmLanEn1")
    lan_ftp = CheckBox(By.NAME, "iMngtlanftp1")
    lan_http = CheckBox(By.NAME, "iMngtlanHttp1")
    lan_enforce_https_access = CheckBox(By.NAME, "iMngtHsfrc1")
    lan_https = CheckBox(By.NAME, "iMngtlanHttps1")
    lan_telnet = CheckBox(By.NAME, "iMngtlanTelnet1")
    lan_tr069 = CheckBox(By.NAME, "iMngtlanTr0691")
    lan_ssh = CheckBox(By.NAME, "iMngtlanSsh1")
    subnet_lan_1 = CheckBox(By.NAME, "iMngtlanacc0")
    subnet_lan_1_use_index = CheckBox(By.NAME, "iMngObjen0")
    subnet_lan_1_index = InputField(By.NAME, "iMngObjidx0")
    subnet_lan_2 = CheckBox(By.NAME, "iMngtlanacc1")
    subnet_lan_2_use_index = CheckBox(By.NAME, "iMngObjen1")
    subnet_lan_2_index = InputField(By.NAME, "iMngObjidx1")
    subnet_lan_3 = CheckBox(By.NAME, "iMngtlanacc2")
    subnet_lan_3_use_index = CheckBox(By.NAME, "iMngObjen2")
    subnet_lan_3_index = InputField(By.NAME, "iMngObjidx2")
    subnet_lan_4 = CheckBox(By.NAME, "iMngtlanacc3")
    subnet_lan_4_use_index = CheckBox(By.NAME, "iMngObjen3")
    subnet_lan_4_index = InputField(By.NAME, "iMngObjidx3")
    subnet_lan_5 = CheckBox(By.NAME, "iMngtlanacc4")
    subnet_lan_5_use_index = CheckBox(By.NAME, "iMngObjen4")
    subnet_lan_5_index = InputField(By.NAME, "iMngObjidx4")
    subnet_lan_6 = CheckBox(By.NAME, "iMngtlanacc5")
    subnet_lan_6_use_index = CheckBox(By.NAME, "iMngObjen5")
    subnet_lan_6_index = InputField(By.NAME, "iMngObjidx5")
    subnet_lan_dmz = CheckBox(By.NAME, "iMngObjendmz")
    subnet_lan_ip_routed = CheckBox(By.NAME, "iMngtlanSub1")
    subnet_lan_ip_routed_use_index = CheckBox(By.NAME, "iMngObjensub")
    subnet_lan_ip_routed_index = InputField(By.NAME, "iMngObjidxsub")

    def open_page(self):
        """Navigate menus to open SNMP configuration page.

        Args: None

        Returns: None

        """
        menu = MenuNavigator(self.driver)
        menu.open_sysmain_management()

    def check_reboot(self):
        """Check if reboot page is displayed, if so set flag to indicate a reboot is required.

        Args: None

        Returns:
            bool: True if reboot page found. False otherwise

        """
        return MenuNavigator(self.driver).is_reboot_system_displayed()

    def read_management_settings(self):
        """Return the current Management settings.

        Args: None

        Returns:
            settings: Management object

        """
        self.open_page()
        return Management(
            router_name=self.read_element_value(self.router_name),
            disable_auto_logout=self.read_element_value(self.disable_auto_logout),
            enable_validation_code=self.read_element_value(self.enable_validation_code),
        )

    def write_management_settings(self, settings: Management):
        """Populate the Management setting.

        Args:
            settings: Management object

        Returns: None

        """
        self.open_page()
        if settings.router_name is not None:
            self.router_name = settings.router_name
        if settings.disable_auto_logout is not None:
            self.disable_auto_logout = settings.disable_auto_logout
        if settings.enable_validation_code is not None:
            self.enable_validation_code = settings.enable_validation_code
        self.ok_button.click()
        return self.check_reboot()

    def read_internet_access_control_settings(self):
        """Return the current InternetAccessControl settings.

        Args: None

        Returns:
            settings: InternetAccessControl object

        """
        self.open_page()
        return InternetAccessControl(
            internet_management=self.read_element_value(self.enable_internet_access),
            domain_name_allowed=self.read_element_value(self.domain_name_allowed),
            ftp_server=self.read_element_value(self.ftp),
            http_server=self.read_element_value(self.http),
            enforce_https_access=self.read_element_value(self.enforce_https_access),
            https_server=self.read_element_value(self.https),
            telnet_server=self.read_element_value(self.telnet),
            tr069_server=self.read_element_value(self.tr069),
            ssh_server=self.read_element_value(self.ssh),
            snmp_server=self.read_element_value(self.snmp),
            disable_ping_from_internet=self.read_element_value(
                self.disable_ping_from_internet
            ),
        )

    def write_internet_access_control_settings(self, settings: InternetAccessControl):
        """Populate the InternetAccessControl setting.

        Args:
            settings: InternetAccessControl object

        Returns: None

        """
        self.open_page()
        if settings.internet_management is not None:
            self.enable_internet_access = settings.internet_management
        if settings.domain_name_allowed is not None:
            if self.domain_name_allowed.is_enabled():
                self.domain_name_allowed = settings.domain_name_allowed
        if settings.ftp_server is not None:
            self.ftp = settings.ftp_server
        if settings.http_server is not None:
            self.http = settings.http_server
        if settings.enforce_https_access is not None:
            self.enforce_https_access = settings.enforce_https_access
        if settings.https_server is not None:
            self.https = settings.https_server
        if settings.telnet_server is not None:
            self.telnet = settings.telnet_server
        if settings.tr069_server is not None:
            self.tr069 = settings.tr069_server
        if settings.ssh_server is not None:
            self.ssh = settings.ssh_server
        if settings.snmp_server is not None:
            self.snmp = settings.snmp_server
        if settings.disable_ping_from_internet is not None:
            self.disable_ping_from_internet = settings.disable_ping_from_internet
        self.ok_button.click()
        return self.check_reboot()

    def read_access_list_settings(self):
        """Return the current AccessList settings.

        Args: None

        Returns:
            settings: AccessList object

        """
        # TODO (#4421): Implement
        raise NotImplementedError

    def write_access_list_settings(self, settings: AccessList):
        """Populate the AccessList setting.

        Args:
            settings: AccessList object

        Returns: None

        """
        # TODO (#4421): Implement
        raise NotImplementedError

    def read_management_port_settings(self):
        """Return the current ManagementPort settings.

        Args: None

        Returns:
            settings: ManagementPort object

        """
        # TODO (#4421): Implement
        raise NotImplementedError

    def write_management_port_settings(self, settings: ManagementPort):
        """Populate the ManagementPort setting.

        Args:
            settings: ManagementPort object

        Returns: None

        """
        # TODO (#4421): Implement
        raise NotImplementedError

    def read_brute_force_protection_settings(self):
        """Return the current BruteForceProtection settings.

        Args: None

        Returns:
            settings: BruteForceProtection object

        """
        # TODO (#4421): Implement
        raise NotImplementedError

    def write_brute_force_protection_settings(self, settings: BruteForceProtection):
        """Populate the BruteForceProtection setting.

        Args:
            settings: BruteForceProtection object

        Returns: None

        """
        # TODO (#4421): Implement
        raise NotImplementedError

    def read_encryption_settings(self):
        """Return the current Encryption settings.

        Args: None

        Returns:
            settings: Encryption object

        """
        # TODO (#4421): Implement
        raise NotImplementedError

    def write_encryption_settings(self, settings: Encryption):
        """Populate the Encryption setting.

        Args:
            settings: Encryption object

        Returns: None

        """
        # TODO (#4421): Implement
        raise NotImplementedError

    def read_cvm_access_control_settings(self):
        """Return the current CVM_AccessControl settings.

        Args: None

        Returns:
            settings: CVM_AccessControl object

        """
        # TODO (#4421): Implement
        raise NotImplementedError

    def write_cvm_access_control_settings(self, settings: CVM_AccessControl):
        """Populate the CVM_AccessControl setting.

        Args:
            settings: CVM_AccessControl object

        Returns: None

        """
        # TODO (#4421): Implement
        raise NotImplementedError

    def read_ap_management_settings(self):
        """Return the current AP_Management settings.

        Args: None

        Returns:
            settings: AP_Management object

        """
        # TODO (#4421): Implement
        raise NotImplementedError

    def write_ap_management_settings(self, settings: AP_Management):
        """Populate the AP_Management setting.

        Args:
            settings: AP_Management object

        Returns: None

        """
        # TODO (#4421): Implement
        raise NotImplementedError

    def read_device_management_settings(self):
        """Return the current DeviceManagement settings.

        Args: None

        Returns:
            settings: DeviceManagement object

        """
        # TODO (#4421): Implement
        raise NotImplementedError

    def write_device_management_settings(self, settings: DeviceManagement):
        """Populate the DeviceManagement setting.

        Args:
            settings: DeviceManagement object

        Returns: None

        """
        # TODO (#4421): Implement
        raise NotImplementedError


# TODO: LAN Tab classes not created.
