"""Draytek Web Admin - Menu Navigation."""

from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from page_elements import Element

from draytekwebadmin.pages.basepage import BasePage


class MenuNavigator(BasePage):
    """Selenium Page Object Model: Menu Navigation."""

    # Page Elements
    # Frames
    frame_main = Element(By.NAME, "main")
    frame_menu = Element(By.NAME, "menu")
    frame_cfgMain = Element(By.NAME, "cfgMain")

    # Menu Items
    menu_system_maintenance = Element(By.LINK_TEXT, "System Maintenance")
    menu_snmp = Element(By.LINK_TEXT, "SNMP")
    menu_management = Element(By.LINK_TEXT, "Management")
    menu_reboot_system = Element(By.LINK_TEXT, "Reboot System")
    menu_firmware_upgrade = Element(By.LINK_TEXT, "Firmware Upgrade")

    # Reboot Page Radio button
    reboot_radio = Element(By.NAME, "sReboot")

    def open_sysmain_snmp(self):
        """Navigate the menus to open the SNMP configuration panel.

        Args: None

        """
        self.driver.switch_to.default_content()
        self.driver.switch_to.frame(self.frame_menu)
        try:
            self.menu_snmp.is_displayed()
        except NoSuchElementException:
            self.menu_system_maintenance.click()
        self.menu_snmp.click()
        self.driver.switch_to.default_content()
        self.driver.switch_to.frame(self.frame_main)

    def open_sysmain_management(self):
        """Navigate the menus to open the SNMP configuration panel.

        Args: None

        """
        self.driver.switch_to.default_content()
        self.driver.switch_to.frame(self.frame_menu)
        try:
            self.menu_management.is_displayed()
        except NoSuchElementException:
            self.menu_system_maintenance.click()
        self.menu_management.click()
        self.driver.switch_to.default_content()
        self.driver.switch_to.frame(self.frame_main)

    def open_sysmain_reboot_system(self):
        """Navigate the menus to open the Reboot System panel.

        Args: None

        """
        self.driver.switch_to.default_content()
        self.driver.switch_to.frame(self.frame_menu)
        try:
            self.menu_reboot_system.is_displayed()
        except NoSuchElementException:
            self.menu_system_maintenance.click()
        self.menu_reboot_system.click()
        self.driver.switch_to.default_content()
        self.driver.switch_to.frame(self.frame_main)

    def open_sysmain_firmware_upgrade(self):
        """Navigate the menus to open the Reboot System panel.

        Args: None

        """
        self.driver.switch_to.default_content()
        self.driver.switch_to.frame(self.frame_menu)
        try:
            self.menu_firmware_upgrade.is_displayed()
        except NoSuchElementException:
            self.menu_system_maintenance.click()
        self.menu_firmware_upgrade.click()
        self.driver.switch_to.default_content()
        self.driver.switch_to.frame(self.frame_main)
        self.driver.switch_to.frame(self.frame_cfgMain)

    def is_reboot_system_displayed(self):
        # TODO (#4423): This feels like the wrong place for this. But is common to other pages.
        """Check if reboot system page is displayed.

        Args: None

        Return:
            bool: True if reboot page is displayed, False otherwise

        """
        self.driver.switch_to.default_content()
        self.driver.switch_to.frame(self.frame_main)
        try:
            self.reboot_radio.is_displayed()
            return True
        except NoSuchElementException:
            return False
