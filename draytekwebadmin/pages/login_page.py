"""Draytek Web Admin - Login Page."""
from selenium.webdriver.common.by import By
from toolium.pageelements import InputText, Button, Text
from draytekwebadmin.pages.basepageobject import BasePageObject


class LoginPage(BasePageObject):
    """Selenium Page Object Model: LoginPage."""

    # Page Elements
    username = InputText(By.NAME, "sUserName", wait=True)
    password = InputText(By.NAME, "sSysPass", wait=True)
    login_button = Button(By.NAME, "btnOk", wait=True)
    login_error_message = Text(By.ID, "errmsg")

    def login(self, username, passsword):
        """Submit login details to Web Admin login page.

        :param username: The username
        :param password: The password
        """
        self.set_element_value(self.username, username)
        self.set_element_value(self.password, passsword)
        self.login_button.click()

    def login_error(self):
        """Check for presence of login error text.

        :returns: True if error displayed, False otherwise
        """
        if self.login_error_message.is_visible():
            return True
        return False

    def error_message(self):
        """Return error message displayed on login page.

        :returns: Error message string
        """
        if self.login_error_message.is_visible():
            message = self.read_element_value(self.login_error_message.web_element)
        else:
            message = "No Error message returned - Login Failed"
        return message
