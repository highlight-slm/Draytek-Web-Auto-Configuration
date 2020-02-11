"""Draytek Web Admin - Base Page for Selenium Page Objects."""


class BasePage:
    """Base class to initialize the base page that will be called from all pages."""

    def __init__(self, driver):
        """Create a BasePage using Selenium WebDriver.

        Args:
            driver: Selenium Webdriver

        """
        self.driver = driver

    @staticmethod
    def read_element_value(element):
        """Read element value if enabled, else return None.

        Args:
            element: WebDriver element

        Returns: Element value or None if disabled

        """
        if element.is_enabled():
            return element.value()
        return None

    @staticmethod
    def read_element_text(element):
        """Read element Text property if enabled, else return None.

        Args:
            element: WebDriver element

        Returns: Element text value (leading and trailing spaces removed) or None if disabled

        """
        if element.is_enabled():
            return element.text.strip()
        return None


# TODO (#4417): Ideally create method in base class for writing elements, after checking if not None.
#       Initial attempts have not been successful
