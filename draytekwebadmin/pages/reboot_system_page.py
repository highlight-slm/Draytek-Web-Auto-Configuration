"""Draytek Web Admin - Reboot System Page."""

from selenium.webdriver.common.by import By
from toolium.pageelements import Button, InputRadio

from draytekwebadmin.pages.menu_navigator import MenuNavigator
from draytekwebadmin.pages.basepageobject import BasePageObject


class RebootSystemPage(BasePageObject):
    """Selenium Page Object Model: RebootSystemPage."""

    # Page Elements
    current_settings_radio = InputRadio(
        By.XPATH, "//input[@name='sReboot' and @type='radio' and @value='Current']"
    )
    factory_settings_radio = InputRadio(
        By.XPATH, "//input[@name='sReboot' and @type='radio' and @value='Default']"
    )
    reboot_now_button = Button(By.NAME, "submitbnt")

    # TODO (#4074): Add Support for scheduling a reboot

    def open_page(self):
        """Navigate menus to open SNMP configuration page.

        Args: None

        Returns: None

        """
        menu = MenuNavigator(self.driver_wrapper)
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
