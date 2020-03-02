"""Draytek Web Admin - Menu Navigation."""

from selenium.webdriver.common.by import By

from toolium.pageelements import InputRadio, Link
from draytekwebadmin.pages.basepageobject import BasePageObject


class MenuNavigator(BasePageObject):
    """Selenium Page Object Model: Menu Navigation."""

    # Page Elements
    # Frames
    frame_main = "main"
    frame_menu = "menu"
    frame_cfgMain = "cfgMain"

    # Menu Items
    menu_system_maintenance = Link(By.LINK_TEXT, "System Maintenance", wait=True)
    menu_snmp = Link(By.LINK_TEXT, "SNMP")
    menu_management = Link(By.LINK_TEXT, "Management")
    menu_reboot_system = Link(By.LINK_TEXT, "Reboot System")
    menu_firmware_upgrade = Link(By.LINK_TEXT, "Firmware Upgrade")

    # Reboot Page Radio button
    reboot_radio = InputRadio(By.NAME, "sReboot")

    def open_sysmain_snmp(self):
        """Navigate the menus to open the SNMP configuration panel."""
        self.driver.switch_to.default_content()
        self.driver.switch_to.frame(self.frame_menu)
        if not self.menu_snmp.is_visible():
            self.menu_system_maintenance.click()
        self.menu_snmp.click()
        self.driver.switch_to.default_content()
        self.driver.switch_to.frame(self.frame_main)

    def open_sysmain_management(self):
        """Navigate the menus to open the SNMP configuration panel."""
        self.driver.switch_to.default_content()
        self.driver.switch_to.frame(self.frame_menu)
        if not self.menu_management.is_visible():
            self.menu_system_maintenance.click()
        self.menu_management.click()
        self.driver.switch_to.default_content()
        self.driver.switch_to.frame(self.frame_main)

    def open_sysmain_reboot_system(self):
        """Navigate the menus to open the Reboot System panel."""
        self.driver.switch_to.default_content()
        self.driver.switch_to.frame(self.frame_menu)
        if not self.menu_reboot_system.is_visible():
            self.menu_system_maintenance.click()
        self.menu_reboot_system.click()
        self.driver.switch_to.default_content()
        self.driver.switch_to.frame(self.frame_main)

    def open_sysmain_firmware_upgrade(self):
        """Navigate the menus to open the Reboot System panel."""
        self.driver.switch_to.default_content()
        self.driver.switch_to.frame(self.frame_menu)
        if not self.menu_firmware_upgrade.is_visible():
            self.menu_system_maintenance.click()
        self.menu_firmware_upgrade.click()
        self.driver.switch_to.default_content()
        self.driver.switch_to.frame(self.frame_main)
        self.driver.switch_to.frame(self.frame_cfgMain)

    def is_reboot_system_displayed(self):
        # TODO (#4423): This feels like the wrong place for this. But is common to other pages.
        """Check if reboot system page is displayed.

        :returns: True if reboot page is displayed, False otherwise
        """
        self.driver.switch_to.default_content()
        self.driver.switch_to.frame(self.frame_main)
        return self.reboot_radio.is_visible()
