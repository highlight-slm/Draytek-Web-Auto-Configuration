"""Draytek Web Admin - SNMP Page."""

from selenium.webdriver.common.by import By
from page_elements import Element, InputField, CheckBox, SelectBox

from draytekwebadmin.snmp import SNMPIPv4, SNMPIPv6, SNMPTrapIPv4, SNMPTrapIPv6, SNMPv3
from draytekwebadmin.pages.basepage import BasePage
from draytekwebadmin.pages.menu_navigator import MenuNavigator


class SNMPpage(BasePage):
    """Selenium Page Object Model: SNMPpage."""

    # Page Elements
    snmp_agent_enable = CheckBox(By.NAME, "SNMPAgentEn")
    get_community = InputField(By.NAME, "SNMPGetCom")
    set_community = InputField(By.NAME, "SNMPSetCom")

    manager_host_v4_index_1 = InputField(By.NAME, "SNMPMngHostIP0")
    manager_host_v4_index_2 = InputField(By.NAME, "SNMPMngHostIP1")
    manager_host_v4_index_3 = InputField(By.NAME, "SNMPMngHostIP2")
    manager_host_v4_subnet_index_1 = SelectBox(By.NAME, "SNMPMngHostMask0")
    manager_host_v4_subnet_index_2 = SelectBox(By.NAME, "SNMPMngHostMask1")
    manager_host_v4_subnet_index_3 = SelectBox(By.NAME, "SNMPMngHostMask2")

    manager_host_v6_index_1 = InputField(By.NAME, "SNMPMngHostIP_V60")
    manager_host_v6_index_2 = InputField(By.NAME, "SNMPMngHostIP_V61")
    manager_host_v6_index_3 = InputField(By.NAME, "SNMPMngHostIP_V62")
    manager_host_v6_prelen_index_1 = SelectBox(By.NAME, "SNMPMngHostPreLen_V60")
    manager_host_v6_prelen_index_2 = SelectBox(By.NAME, "SNMPMngHostPreLen_V61")
    manager_host_v6_prelen_index_3 = SelectBox(By.NAME, "SNMPMngHostPreLen_V62")

    trap_community = InputField(By.NAME, "SNMPTrapCom")
    trap_timeout = InputField(By.NAME, "SNMPTrapTimeOut")

    trap_host_v4_index_1 = InputField(By.NAME, "SNMPNotiHostIP0")
    trap_host_v4_index_2 = InputField(By.NAME, "SNMPNotiHostIP1")

    trap_host_v6_index_1 = InputField(By.NAME, "SNMPNotiHostIP_V60")
    trap_host_v6_index_2 = InputField(By.NAME, "SNMPNotiHostIP_V61")

    snmpv3_agent_enable = CheckBox(By.NAME, "SNMPV3En")
    snmpv3_usm_user = InputField(By.NAME, "SNMPUSMUser")
    snmpv3_auth_algo = SelectBox(By.NAME, "SNMPAuthProto")
    snmpv3_auth_password = InputField(By.NAME, "SNMPAuthPwd")
    snmpv3_priv_algo = SelectBox(By.NAME, "SNMPPrivProto")
    snmpv3_priv_password = InputField(By.NAME, "SNMPPrivPwd")

    ok_button = Element(By.NAME, "snmp_btnOk")

    def open_page(self):
        """Navigate menus to open SNMP configuration page.

        Args: None

        Returns: None

        """
        menu = MenuNavigator(self.driver)
        menu.open_sysmain_snmp()

    def check_reboot(self):
        """Check if reboot page is displayed, if so set flag to indicate a reboot is required.

        Args: None

        Returns:
            bool: True if reboot page found. False otherwise

        """
        return MenuNavigator(self.driver).is_reboot_system_displayed()

    def read_snmp_ipv4_settings(self):
        """Return the current SNMPIPv4 setting.

        Args: None

        Returns:
            settings: SNMPIPv4 object

        """
        self.open_page()
        return SNMPIPv4(
            enable_agent=self.read_element_value(self.snmp_agent_enable),
            get_community=self.read_element_value(self.get_community),
            set_community=self.read_element_value(self.set_community),
            manager_host_1=self.read_element_value(self.manager_host_v4_index_1),
            manager_host_subnet_1=self.read_element_value(
                self.manager_host_v4_subnet_index_1
            ),
            manager_host_2=self.read_element_value(self.manager_host_v4_index_2),
            manager_host_subnet_2=self.read_element_value(
                self.manager_host_v4_subnet_index_2
            ),
            manager_host_3=self.read_element_value(self.manager_host_v4_index_3),
            manager_host_subnet_3=self.read_element_value(
                self.manager_host_v4_subnet_index_3
            ),
        )

    def write_snmp_ipv4_settings(self, settings: SNMPIPv4):
        """Populate the SNMPIPv4 settings.

        Args:
            settings: SNMPIPv4 object

        Returns:
            reboot required (bool): Indicating if settings change requires a reboot

        """
        self.open_page()
        # TODO (#4424): If agent isn't enabled you can't set any of the sub-settings. Warn?
        if settings.enable_agent is not None:
            self.snmp_agent_enable = settings.enable_agent
        if settings.get_community is not None:
            self.get_community = settings.get_community
        if settings.set_community is not None:
            self.set_community = settings.set_community
        if settings.manager_host_1 is not None:
            self.manager_host_v4_index_1 = settings.manager_host_1
        if settings.manager_host_2 is not None:
            self.manager_host_v4_index_2 = settings.manager_host_2
        if settings.manager_host_3 is not None:
            self.manager_host_v4_index_3 = settings.manager_host_3
        if settings.manager_host_subnet_1 is not None:
            self.manager_host_v4_subnet_index_1 = settings.manager_host_subnet_1
        if settings.manager_host_subnet_2 is not None:
            self.manager_host_v4_subnet_index_2 = settings.manager_host_subnet_2
        if settings.manager_host_subnet_3 is not None:
            self.manager_host_v4_subnet_index_3 = settings.manager_host_subnet_3
        self.ok_button.click()
        return self.check_reboot()

    def read_snmp_ipv6_settings(self):
        """Return the current SNMPIPv6 settings.

        Args: None

        Returns:
            settings: SNMPIPv6 object

        """
        # TODO (#4425): Implement
        raise NotImplementedError

    def write_snmp_ipv6_settings(self, settings: SNMPIPv6):
        """Populate the SNMPIPv6 settings.

        Args:
            settings: SNMPIPv6 object

        Returns:
            reboot required (bool):  Indicating if settings change requires a reboot

        """
        # TODO (#4425): Implement
        raise NotImplementedError

    def read_snmp_ipv4_trap_setting(self):
        """Return the current SNMPIPv4 Trap settings.

        Args: None

        Returns:
            settings: SNMPIPv4Trap object

        """
        # TODO (#4425): Implement
        raise NotImplementedError

    def write_snmp_ipv4_trap_settings(self, settings: SNMPTrapIPv4):
        """Populate the SNMPIPv4 Trap settings.

        Args:
            settings: SNMPIPv4Trap object

        Returns:
            reboot required (bool): Indicating if settings change requires a reboot

        """
        # TODO (#4425): Implement
        raise NotImplementedError

    def read_snmp_ipv6_trap_setting(self):
        """Return the current SNMPIPv6 Trap settings.

        Args: None

        Returns:
            settings: SNMPIPv6Trap object

        """
        # TODO (#4425): Implement
        raise NotImplementedError

    def write_snmp_ipv6_trap_settings(self, settings: SNMPTrapIPv6):
        """Populate the SNMPIPv6 Trap settings.

        Args:
            settings: SNMPIPv6Trap object

        Returns:
            reboot required (bool): Indicating if settings change requires a reboot

        """
        # TODO (#4425): Implement
        raise NotImplementedError

    def read_snmp_v3_settings(self):
        """Return the current SNMPv3 settings.

        Args: None

        Returns:
            settings: SNMPv3 object

        """
        # TODO (#4425): Implement
        raise NotImplementedError

    def write_snmp_v3_settings(self, setting: SNMPv3):
        """Populate the SNMPv3 settings.

        Args:
            settings: SNMPv3 object

        Returns:
            reboot required (bool): Indicating if settings change requires a reboot

        """
        # Note: To enable SNMPv3 agent, you also have to enable the SNMPv1v2 agent.
        # Which also needs v1v2 community strings, manager hosts etc.
        # TODO (#4425): Implement
        raise NotImplementedError
