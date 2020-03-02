"""Draytek Web Admin - SNMP Page."""
from selenium.webdriver.common.by import By

from toolium.pageelements import InputText, Button, Select, Checkbox

from draytekwebadmin.snmp import SNMPIPv4, SNMPIPv6, SNMPTrapIPv4, SNMPTrapIPv6, SNMPv3
from draytekwebadmin.pages.menu_navigator import MenuNavigator
from draytekwebadmin.pages.basepageobject import BasePageObject


class SNMPpage(BasePageObject):
    """Selenium Page Object Model: SNMPpage."""

    # Page Elements
    snmp_agent_enable = Checkbox(By.NAME, "SNMPAgentEn")
    get_community = InputText(By.NAME, "SNMPGetCom")
    set_community = InputText(By.NAME, "SNMPSetCom")

    manager_host_v4_index_1 = InputText(By.NAME, "SNMPMngHostIP0")
    manager_host_v4_index_2 = InputText(By.NAME, "SNMPMngHostIP1")
    manager_host_v4_index_3 = InputText(By.NAME, "SNMPMngHostIP2")
    manager_host_v4_subnet_index_1 = Select(By.NAME, "SNMPMngHostMask0")
    manager_host_v4_subnet_index_2 = Select(By.NAME, "SNMPMngHostMask1")
    manager_host_v4_subnet_index_3 = Select(By.NAME, "SNMPMngHostMask2")

    manager_host_v6_index_1 = InputText(By.NAME, "SNMPMngHostIP_V60")
    manager_host_v6_index_2 = InputText(By.NAME, "SNMPMngHostIP_V61")
    manager_host_v6_index_3 = InputText(By.NAME, "SNMPMngHostIP_V62")
    manager_host_v6_prelen_index_1 = Select(By.NAME, "SNMPMngHostPreLen_V60")
    manager_host_v6_prelen_index_2 = Select(By.NAME, "SNMPMngHostPreLen_V61")
    manager_host_v6_prelen_index_3 = Select(By.NAME, "SNMPMngHostPreLen_V62")

    trap_community = InputText(By.NAME, "SNMPTrapCom")
    trap_timeout = InputText(By.NAME, "SNMPTrapTimeOut")

    trap_host_v4_index_1 = InputText(By.NAME, "SNMPNotiHostIP0")
    trap_host_v4_index_2 = InputText(By.NAME, "SNMPNotiHostIP1")

    trap_host_v6_index_1 = InputText(By.NAME, "SNMPNotiHostIP_V60")
    trap_host_v6_index_2 = InputText(By.NAME, "SNMPNotiHostIP_V61")

    snmpv3_agent_enable = Checkbox(By.NAME, "SNMPV3En")
    snmpv3_usm_user = InputText(By.NAME, "SNMPUSMUser")
    snmpv3_auth_algo = Select(By.NAME, "SNMPAuthProto")
    snmpv3_auth_password = InputText(By.NAME, "SNMPAuthPwd")
    snmpv3_priv_algo = Select(By.NAME, "SNMPPrivProto")
    snmpv3_priv_password = InputText(By.NAME, "SNMPPrivPwd")

    ok_button = Button(By.NAME, "snmp_btnOk")

    def open_page(self):
        """Navigate menus to open SNMP configuration page."""
        menu = MenuNavigator(self.driver_wrapper)
        menu.open_sysmain_snmp()

    def check_reboot(self):
        """Check if reboot page is displayed, if so set flag to indicate a reboot is required.

        :returns: True if reboot page found. False otherwise
        """
        return MenuNavigator(self.driver_wrapper).is_reboot_system_displayed()

    def read_snmp_ipv4_settings(self):
        """Return the current SNMPIPv4 setting.

        :returns SNMPIPv4 object
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

        :param settings: SNMPIPv4 object
        :returns reboot required (bool) - Indicating if settings change requires a reboot
        """
        self.open_page()
        # TODO (#4424): If agent isn't enabled you can't set any of the sub-settings. Warn?
        if settings.enable_agent is not None:
            self.set_element_value(self.snmp_agent_enable, settings.enable_agent)
        if settings.get_community is not None:
            self.set_element_value(self.get_community, settings.get_community)
        if settings.set_community is not None:
            self.set_element_value(self.set_community, settings.set_community)
        if settings.manager_host_1 is not None:
            self.set_element_value(
                self.manager_host_v4_index_1, settings.manager_host_1
            )
        if settings.manager_host_2 is not None:
            self.set_element_value(
                self.manager_host_v4_index_2, settings.manager_host_2
            )
        if settings.manager_host_3 is not None:
            self.set_element_value(
                self.manager_host_v4_index_3, settings.manager_host_3
            )
        if settings.manager_host_subnet_1 is not None:
            self.set_element_value(
                self.manager_host_v4_subnet_index_1, settings.manager_host_subnet_1
            )
        if settings.manager_host_subnet_2 is not None:
            self.set_element_value(
                self.manager_host_v4_subnet_index_2, settings.manager_host_subnet_2
            )
        if settings.manager_host_subnet_3 is not None:
            self.set_element_value(
                self.manager_host_v4_subnet_index_3, settings.manager_host_subnet_3
            )
        self.ok_button.click()
        return self.check_reboot()

    def read_snmp_ipv6_settings(self):
        """Return the current SNMPIPv6 settings.

        :returns SNMPIPv6 object
        """
        # TODO (#4425): Implement
        raise NotImplementedError

    def write_snmp_ipv6_settings(self, settings: SNMPIPv6):
        """Populate the SNMPIPv6 settings.

        :param settings: SNMPIPv6 object
        :returns: reboot required (bool) - Indicating if settings change requires a reboot
        """
        # TODO (#4425): Implement
        raise NotImplementedError

    def read_snmp_ipv4_trap_setting(self):
        """Return the current SNMPIPv4 Trap settings.

        :returns: SNMPIPv4Trap object
        """
        # TODO (#4425): Implement
        raise NotImplementedError

    def write_snmp_ipv4_trap_settings(self, settings: SNMPTrapIPv4):
        """Populate the SNMPIPv4 Trap settings.

        :param settings: SNMPIPv4Trap object
        :returns: reboot required (bool) - Indicating if settings change requires a reboot
        """
        # TODO (#4425): Implement
        raise NotImplementedError

    def read_snmp_ipv6_trap_setting(self):
        """Return the current SNMPIPv6 Trap settings.

        :returns: SNMPIPv6Trap object
        """
        # TODO (#4425): Implement
        raise NotImplementedError

    def write_snmp_ipv6_trap_settings(self, settings: SNMPTrapIPv6):
        """Populate the SNMPIPv6 Trap settings.

        :param settings: SNMPIPv6Trap object
        :returns: reboot required (bool) - Indicating if settings change requires a reboot
        """
        # TODO (#4425): Implement
        raise NotImplementedError

    def read_snmp_v3_settings(self):
        """Return the current SNMPv3 settings.

        :returns: SNMPv3 object
        """
        # TODO (#4425): Implement
        raise NotImplementedError

    def write_snmp_v3_settings(self, setting: SNMPv3):
        """Populate the SNMPv3 settings.

        :param settings: SNMPv3 object
        :returns: reboot required (bool) - Indicating if settings change requires a reboot
        """
        # Note: To enable SNMPv3 agent, you also have to enable the SNMPv1v2 agent.
        # Which also needs v1v2 community strings, manager hosts etc.
        # TODO (#4425): Implement
        raise NotImplementedError
