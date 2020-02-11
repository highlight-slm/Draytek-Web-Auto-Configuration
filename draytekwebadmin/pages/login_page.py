"""Draytek Web Admin - Login Page."""

from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from page_elements import Element, InputField

from draytekwebadmin.pages.basepage import BasePage


class LoginPage(BasePage):
    """Selenium Page Object Model: LoginPage."""

    # Page Elements
    username = InputField(By.NAME, "sUserName")
    password = InputField(By.NAME, "sSysPass")
    login_button = Element(By.NAME, "btnOk")
    login_error_message = Element(By.ID, "errmsg")

    def login(self, username, passsword):
        """Submit login details to Web Admin login page.

        Args:
            username: The username
            password: The password

        Returns: None

        """
        self.username = username
        self.password = passsword
        self.login_button.click()

    def login_error(self):
        """Check for presence of login error text.

        Args: None

        Returns:
            bool: True if error displayed, False otherwise

        """
        try:
            self.login_error_message.is_displayed()  # Error message shown
            self.username.is_displayed()  # We can still see the logon screen
        except NoSuchElementException:
            return False
        return True

    def error_message(self):
        """Return error message displayed on login page.

        Args: None

        Returns:
            message: Error message string

        """
        try:
            message = self.login_error_message.text
        except NoSuchElementException:
            message = "No Error message returned - Login Failed"
        return message
