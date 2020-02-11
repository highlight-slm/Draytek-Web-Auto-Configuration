"""Draytek Web Admin - Reboot System Page."""

from selenium.webdriver.common.by import By
from page_elements import Element

from draytekwebadmin.pages.basepage import BasePage
from draytekwebadmin.pages.menu_navigator import MenuNavigator


class RebootSystemPage(BasePage):
    """Selenium Page Object Model: RebootSystemPage."""

    # Page Elements
    current_settings_radio = Element(
        By.XPATH, "//input[@name='sReboot' and @type='radio' and @value='Current']"
    )
    factory_settings_radio = Element(
        By.XPATH, "//input[@name='sReboot' and @type='radio' and @value='Default']"
    )
    reboot_now_button = Element(By.NAME, "submitbnt")

    # TODO (#4074): Add Support for scheduling a reboot

    def open_page(self):
        """Navigate menus to open SNMP configuration page.

        Args: None

        Returns: None

        """
        menu = MenuNavigator(self.driver)
        menu.open_sysmain_reboot_system()

    def reboot(self):
        """Trigger router reboot with current configuration.

        Args: None

        Returns: None

        """
        self.open_page()
        self.current_settings_radio.click()
        self.reboot_now_button.click()

    def reboot_reset_to_factory_configuration(self):
        """***CAUTION*** Trigger router reboot back to factory default configuration.

        Args: None

        Returns: None

        """
        self.open_page()
        self.factory_settings_radio.click()
        self.reboot_now_button.click()
