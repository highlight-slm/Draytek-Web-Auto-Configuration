"""Draytek Web Admin - Firmware Upgrade Page."""

from selenium.webdriver.common.by import By
from toolium.pageelements import Button, Text

from draytekwebadmin.firmware import Firmware
from draytekwebadmin.pages.menu_navigator import MenuNavigator
from draytekwebadmin.pages.basepageobject import BasePageObject


class FirmwareUpgradePage(BasePageObject):
    """Selenium Page Object Model: FirmwareUpgradePage."""

    # Page Elements
    choose_firmware_button = Button(By.ID, "fw_file")
    firmware_path_form_element = Button(
        By.CSS_SELECTOR, "input[type='file']"
    )  # Might not be needed
    upgrade_button = Button(
        By.XPATH, "//input[@name='attach' and @type='button' and @value='Upgrade']"
    )
    preview_button = Button(By.NAME, "btnpreview")
    post_upgrade_restart_button = Button(
        By.XPATH, "//input[@type='button' and @value='Restart']"
    )

    preview_close_button = Button(By.NAME, "btnClose")
    preview_model = Text(By.ID, "smodelName")
    preview_firmware_version = Text(By.ID, "sfwversion")
    preview_modem_version = Text(By.ID, "scurmdmver")
    preview_current_modem_version = Text(By.ID, "snewmdmver")

    def open_page(self):
        """Navigate menus to open Firmware Upgrade page.

        Args: None

        Returns: None

        """
        menu = MenuNavigator(self.driver_wrapper)
        menu.open_sysmain_firmware_upgrade()

    def new_firmware_preview(self, file: Firmware):
        """Preview firmware upgrade information for supplied firmware file.

        Args:
            file: Full file name and path to router firmware

        Returns:
            Firmware object: Firmware object populated with settings retrieved from previewing the firmware

        """
        if file.filepath is None:
            raise ValueError("Firmware Preview requires a path to the a firmware file")

        self.open_page()

        self.choose_firmware_button.web_element.send_keys(str(file.filepath))
        self.preview_button.click()
        preview_firmware = Firmware(
            filepath=str(file.filepath),
            model=self.read_element_value(self.preview_model),
            firmware_target=self.read_element_value(self.preview_firmware_version),
            modem_firmware_current=self.read_element_value(
                self.preview_current_modem_version
            ),
            modem_firmware_target=self.read_element_value(self.preview_modem_version),
        )
        self.preview_close_button.click()

        # TODO (#4412): Handle incompatible firmware provided to preview. Raise exception?

        return preview_firmware

    def new_firmware_install(self, file: Firmware):
        """Install firmware using the file specified.

        Args:
            file: Full file name and path to router firmware

        Returns:
            success: True if upgrade successful

        """
        self.open_page()
        self.choose_firmware_button.web_element.send_keys(str(file.filepath))
        self.upgrade_button.click()
        self.driver.switch_to.alert.accept()
        self.post_upgrade_restart_button.click()
        self.driver.switch_to.alert.accept()
        # TODO (#4413): Handle firmware install failures and return false or raise exceptions?
        return True
