"""Draytek Web Admin - Management Page."""

from selenium.webdriver.common.by import By
from toolium.pageelements import InputText, Button, Checkbox, Link, InputRadio
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
from draytekwebadmin.pages.menu_navigator import MenuNavigator
from draytekwebadmin.pages.basepageobject import BasePageObject


class ManagementPage(BasePageObject):
    """Selenium Page Object Model: ManagementPage."""

    # Page Elements
    management_setup_tab = Link(By.ID, "tab1")
    lan_access_setup_tab = Link(By.ID, "tab3")
    ok_button = Button(By.CLASS_NAME, "btnw")

    # TAB: Management Setup
    router_name = InputText(By.NAME, "sRouterName")
    disable_auto_logout = Checkbox(By.NAME, "sDeflogoff")
    enable_validation_code = Checkbox(By.NAME, "sValidatedCode")

    # Internet Access Control
    enable_internet_access = Checkbox(By.NAME, "sRMC")
    domain_name_allowed = InputText(By.NAME, "sSysAllDomain")
    ftp = Checkbox(By.NAME, "sRMCFtp")
    http = Checkbox(By.NAME, "sRMCHttp")
    enforce_https_access = Checkbox(By.NAME, "iRMCHsfrc")
    https = Checkbox(By.NAME, "sRMCHttps")
    telnet = Checkbox(By.NAME, "sRMCTelnet")
    tr069 = Checkbox(By.NAME, "sRMCTr069")
    ssh = Checkbox(By.NAME, "sRMCSsh")
    snmp = Checkbox(By.NAME, "sRMCSnmp")
    disable_ping_from_internet = Checkbox(By.NAME, "sWPing")

    # Access List from the Internet
    access_index_1 = InputText(By.NAME, "index1")
    access_index_2 = InputText(By.NAME, "index2")
    access_index_3 = InputText(By.NAME, "index3")
    access_index_4 = InputText(By.NAME, "index4")
    access_index_5 = InputText(By.NAME, "index5")
    access_index_6 = InputText(By.NAME, "index6")
    access_index_7 = InputText(By.NAME, "index7")
    access_index_8 = InputText(By.NAME, "index8")
    access_index_9 = InputText(By.NAME, "index9")
    access_index_10 = InputText(By.NAME, "index10")

    # Management Port Setup
    user_defined_ports_radio = InputRadio(
        By.XPATH,
        "//input[@name='ConfigPort' and @type='radio' and @value='UserDefine']",
    )
    default_ports_radio = InputRadio(
        By.XPATH, "//input[@name='ConfigPort' and @type='radio' and @value='Default']"
    )
    telnet_port = InputText(By.NAME, "TelnetPort")
    http_port = InputText(By.NAME, "HttpPort")
    https_port = InputText(By.NAME, "HttpsPort")
    ftp_port = InputText(By.NAME, "txtFtpPort")
    tr069_port = InputText(By.NAME, "txtTr069Port")
    ssh_port = InputText(By.NAME, "txtSshPort")

    # Bruce Force Protection
    bf_enable = Checkbox(By.NAME, "iBrEn")
    bf_ftp = Checkbox(By.NAME, "iBrFtp")
    bf_http = Checkbox(By.NAME, "iBrHttp")
    bf_https = Checkbox(By.NAME, "iBrHttps")
    bf_telnet = Checkbox(By.NAME, "iBrTelnet")
    bf_tr069 = Checkbox(By.NAME, "iBrTr069")
    bf_ssh = Checkbox(By.NAME, "iBrSsh")
    bf_max_login_failures = InputText(By.NAME, "iLoginFailures")
    bf_penality_period = InputText(By.NAME, "iPenaltyPeriod")

    # TLS/SSL Encryption Setup
    enc_tls12 = Checkbox(By.NAME, "enTLSv1_2")
    enc_tls11 = Checkbox(By.NAME, "enTLSv1_1")
    enc_tls10 = Checkbox(By.NAME, "enTLSv1")
    enc_ssl30 = Checkbox(By.NAME, "enSSLv3")

    # CVM Access Control
    cvm_port_enable = Checkbox(By.NAME, "CvmHttpEnb")
    cvm_port = InputText(By.NAME, "CvmHttpPort")
    cvm_ssl_port_enable = Checkbox(By.NAME, "CvmHttpsEnb")
    cvm_ssl_port = InputText(By.NAME, "CvmHttpsPort")

    # AP Management
    ap_management = Checkbox(By.NAME, "ApmEn")

    # Device Management
    device_management = Checkbox(By.NAME, "chkDevMng")
    device_management_respond_external = Checkbox(By.NAME, "NoRsp2ExDev")

    # TAB: LAN Access Setup
    allow_management_from_lan = Checkbox(By.NAME, "sMngtfrmLanEn1")
    lan_ftp = Checkbox(By.NAME, "iMngtlanftp1")
    lan_http = Checkbox(By.NAME, "iMngtlanHttp1")
    lan_enforce_https_access = Checkbox(By.NAME, "iMngtHsfrc1")
    lan_https = Checkbox(By.NAME, "iMngtlanHttps1")
    lan_telnet = Checkbox(By.NAME, "iMngtlanTelnet1")
    lan_tr069 = Checkbox(By.NAME, "iMngtlanTr0691")
    lan_ssh = Checkbox(By.NAME, "iMngtlanSsh1")
    subnet_lan_1 = Checkbox(By.NAME, "iMngtlanacc0")
    subnet_lan_1_use_index = Checkbox(By.NAME, "iMngObjen0")
    subnet_lan_1_index = InputText(By.NAME, "iMngObjidx0")
    subnet_lan_2 = Checkbox(By.NAME, "iMngtlanacc1")
    subnet_lan_2_use_index = Checkbox(By.NAME, "iMngObjen1")
    subnet_lan_2_index = InputText(By.NAME, "iMngObjidx1")
    subnet_lan_3 = Checkbox(By.NAME, "iMngtlanacc2")
    subnet_lan_3_use_index = Checkbox(By.NAME, "iMngObjen2")
    subnet_lan_3_index = InputText(By.NAME, "iMngObjidx2")
    subnet_lan_4 = Checkbox(By.NAME, "iMngtlanacc3")
    subnet_lan_4_use_index = Checkbox(By.NAME, "iMngObjen3")
    subnet_lan_4_index = InputText(By.NAME, "iMngObjidx3")
    subnet_lan_5 = Checkbox(By.NAME, "iMngtlanacc4")
    subnet_lan_5_use_index = Checkbox(By.NAME, "iMngObjen4")
    subnet_lan_5_index = InputText(By.NAME, "iMngObjidx4")
    subnet_lan_6 = Checkbox(By.NAME, "iMngtlanacc5")
    subnet_lan_6_use_index = Checkbox(By.NAME, "iMngObjen5")
    subnet_lan_6_index = InputText(By.NAME, "iMngObjidx5")
    subnet_lan_dmz = Checkbox(By.NAME, "iMngObjendmz")
    subnet_lan_ip_routed = Checkbox(By.NAME, "iMngtlanSub1")
    subnet_lan_ip_routed_use_index = Checkbox(By.NAME, "iMngObjensub")
    subnet_lan_ip_routed_index = InputText(By.NAME, "iMngObjidxsub")

    def open_page(self):
        """Navigate menus to open SNMP configuration page."""
        menu = MenuNavigator(self.driver_wrapper)
        menu.open_sysmain_management()

    def check_reboot(self):
        """Check if reboot page is displayed, if so set flag to indicate a reboot is required.

        :returns: True if reboot page found. False otherwise
        """
        return MenuNavigator(self.driver_wrapper).is_reboot_system_displayed()

    def read_management_settings(self):
        """Return the current Management settings.

        :returns: Management object

        """
        self.open_page()
        return Management(
            router_name=self.read_element_value(self.router_name),
            disable_auto_logout=self.read_element_value(self.disable_auto_logout),
            enable_validation_code=self.read_element_value(self.enable_validation_code),
        )

    def write_management_settings(self, settings: Management):
        """Populate the Management setting.

        :param settings: Management object
        """
        self.open_page()
        self.set_element_value(self.router_name, settings.router_name)
        self.set_element_value(self.disable_auto_logout, settings.disable_auto_logout)
        self.set_element_value(
            self.enable_validation_code, settings.enable_validation_code
        )
        self.ok_button.click()
        return self.check_reboot()

    def read_internet_access_control_settings(self):
        """Return the current InternetAccessControl settings.

        :returns: InternetAccessControl object
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

        :param settings: InternetAccessControl object
        """
        self.open_page()
        self.set_element_value(
            self.enable_internet_access, settings.internet_management
        )
        self.set_element_value(self.domain_name_allowed, settings.domain_name_allowed)
        self.set_element_value(self.ftp, settings.ftp_server)
        self.set_element_value(self.http, settings.http_server)
        self.set_element_value(self.enforce_https_access, settings.enforce_https_access)
        self.set_element_value(self.https, settings.https_server)
        self.set_element_value(self.telnet, settings.telnet_server)
        self.set_element_value(self.tr069, settings.tr069_server)
        self.set_element_value(self.ssh, settings.ssh_server)
        self.set_element_value(self.snmp, settings.snmp_server)
        self.set_element_value(
            self.disable_ping_from_internet, settings.disable_ping_from_internet
        )
        self.ok_button.click()
        return self.check_reboot()

    def read_access_list_settings(self):
        """Return the current AccessList settings.

        :returns: AccessList object
        """
        self.open_page()
        return AccessList(
            list_1_ip_object_index=self.read_element_value(self.access_index_1),
            list_2_ip_object_index=self.read_element_value(self.access_index_2),
            list_3_ip_object_index=self.read_element_value(self.access_index_3),
            list_4_ip_object_index=self.read_element_value(self.access_index_4),
            list_5_ip_object_index=self.read_element_value(self.access_index_5),
            list_6_ip_object_index=self.read_element_value(self.access_index_6),
            list_7_ip_object_index=self.read_element_value(self.access_index_7),
            list_8_ip_object_index=self.read_element_value(self.access_index_8),
            list_9_ip_object_index=self.read_element_value(self.access_index_9),
            list_10_ip_object_index=self.read_element_value(self.access_index_10),
        )

    def write_access_list_settings(self, settings: AccessList):
        """Populate the AccessList setting.

        :param settings: AccessList object
        """
        self.open_page()
        self.set_element_value(self.access_index_1, settings.list_1_ip_object_index)
        self.set_element_value(self.access_index_2, settings.list_2_ip_object_index)
        self.set_element_value(self.access_index_3, settings.list_3_ip_object_index)
        self.set_element_value(self.access_index_4, settings.list_4_ip_object_index)
        self.set_element_value(self.access_index_5, settings.list_5_ip_object_index)
        self.set_element_value(self.access_index_6, settings.list_6_ip_object_index)
        self.set_element_value(self.access_index_7, settings.list_7_ip_object_index)
        self.set_element_value(self.access_index_8, settings.list_8_ip_object_index)
        self.set_element_value(self.access_index_9, settings.list_9_ip_object_index)
        self.set_element_value(self.access_index_10, settings.list_10_ip_object_index)
        self.ok_button.click()
        return self.check_reboot()

    def read_management_port_settings(self):
        """Return the current ManagementPort settings.

        :returns: ManagementPort object
        """
        self.open_page()
        return ManagementPort(
            user_defined_ports=self.read_element_value(self.user_defined_ports_radio),
            telnet_port=self.read_element_value(self.telnet_port),
            http_port=self.read_element_value(self.http_port),
            https_port=self.read_element_value(self.https_port),
            ftp_port=self.read_element_value(self.ftp_port),
            tr069_port=self.read_element_value(self.tr069_port),
            ssh_port=self.read_element_value(self.ssh_port),
        )

    def write_management_port_settings(self, settings: ManagementPort):
        """Populate the ManagementPort setting.

        :param settings: ManagementPort object
        """
        self.open_page()
        if settings.user_defined_ports:
            self.set_element_value(
                self.user_defined_ports_radio, settings.user_defined_ports
            )
            self.set_element_value(self.telnet_port, settings.telnet_port)
            self.set_element_value(self.http_port, settings.http_port)
            self.set_element_value(self.https_port, settings.https_port)
            self.set_element_value(self.ftp_port, settings.ftp_port)
            self.set_element_value(self.tr069_port, settings.tr069_port)
            self.set_element_value(self.ssh_port, settings.ssh_port)
        else:
            self.set_element_value(self.default_ports_radio, True)
        self.ok_button.click()
        return self.check_reboot()

    def read_brute_force_protection_settings(self):
        """Return the current BruteForceProtection settings.

        :returns: BruteForceProtection object
        """
        self.open_page()
        return BruteForceProtection(
            enable=self.read_element_value(self.bf_enable),
            ftp_server=self.read_element_value(self.bf_ftp),
            http_server=self.read_element_value(self.bf_http),
            https_server=self.read_element_value(self.bf_https),
            telnet_server=self.read_element_value(self.bf_telnet),
            tr069_server=self.read_element_value(self.bf_tr069),
            ssh_server=self.read_element_value(self.bf_ssh),
            max_login_failures=self.read_element_value(self.bf_max_login_failures),
            penalty_period=self.read_element_value(self.bf_penality_period),
        )

    def write_brute_force_protection_settings(self, settings: BruteForceProtection):
        """Populate the BruteForceProtection setting.

        :param settings: BruteForceProtection object
        """
        self.open_page()
        self.set_element_value(self.bf_enable, settings.enable)
        self.set_element_value(self.bf_ftp, settings.ftp_server)
        self.set_element_value(self.bf_http, settings.http_server)
        self.set_element_value(self.bf_https, settings.https_server)
        self.set_element_value(self.bf_telnet, settings.telnet_server)
        self.set_element_value(self.bf_tr069, settings.tr069_server)
        self.set_element_value(self.bf_ssh, settings.ssh_server)
        self.set_element_value(self.bf_max_login_failures, settings.max_login_failures)
        self.set_element_value(self.bf_penality_period, settings.penalty_period)
        self.ok_button.click()
        return self.check_reboot()

    def read_encryption_settings(self):
        """Return the current Encryption settings.

        :returns: Encryption object
        """
        self.open_page()
        return Encryption(
            tls_1_2=self.read_element_value(self.enc_tls12),
            tls_1_1=self.read_element_value(self.enc_tls11),
            tls_1_0=self.read_element_value(self.enc_tls10),
            ssl_3_0=self.read_element_value(self.enc_ssl30),
        )

    def write_encryption_settings(self, settings: Encryption):
        """Populate the Encryption setting.

        :param settings: Encryption object
        """
        self.open_page()
        self.set_element_value(self.enc_tls12, settings.tls_1_2)
        self.set_element_value(self.enc_tls11, settings.tls_1_1)
        self.set_element_value(self.enc_tls10, settings.tls_1_0)
        self.set_element_value(self.enc_ssl30, settings.ssl_3_0)
        self.ok_button.click()
        return self.check_reboot()

    def read_cvm_access_control_settings(self):
        """Return the current CVM_AccessControl settings.

        :returns: CVM_AccessControl object
        """
        self.open_page()
        return CVM_AccessControl(
            enable=self.read_element_value(self.cvm_port_enable),
            ssl_enable=self.read_element_value(self.cvm_ssl_port_enable),
            port=self.read_element_value(self.cvm_port),
            ssl_port=self.read_element_value(self.cvm_ssl_port),
        )

    def write_cvm_access_control_settings(self, settings: CVM_AccessControl):
        """Populate the CVM_AccessControl setting.

        :param settings: CVM_AccessControl object
        """
        self.open_page()
        self.set_element_value(self.cvm_port_enable, settings.enable)
        self.set_element_value(self.cvm_ssl_port_enable, settings.ssl_enable)
        self.set_element_value(self.cvm_port, settings.port)
        self.set_element_value(self.cvm_ssl_port, settings.ssl_port)
        self.ok_button.click()
        return self.check_reboot()

    def read_ap_management_settings(self):
        """Return the current AP_Management settings.

        :returns: AP_Management object
        """
        self.open_page()
        return AP_Management(enable=self.read_element_value(self.ap_management),)

    def write_ap_management_settings(self, settings: AP_Management):
        """Populate the AP_Management setting.

        :param settings: AP_Management object
        """
        self.open_page()
        self.set_element_value(self.ap_management, settings.enable)
        self.ok_button.click()
        return self.check_reboot()

    def read_device_management_settings(self):
        """Return the current DeviceManagement settings.

        :returns: DeviceManagement object
        """
        self.open_page()
        return DeviceManagement(
            enable=self.read_element_value(self.device_management),
            respond_to_external_device=self.read_element_value(
                self.device_management_respond_external
            ),
        )

    def write_device_management_settings(self, settings: DeviceManagement):
        """Populate the DeviceManagement setting.

        :param settings: DeviceManagement object
        """
        self.open_page()
        self.set_element_value(self.device_management, settings.enable)
        self.set_element_value(
            self.device_management_respond_external, settings.respond_to_external_device
        )
        self.ok_button.click()
        return self.check_reboot()


# TODO: LAN Tab classes not created.
