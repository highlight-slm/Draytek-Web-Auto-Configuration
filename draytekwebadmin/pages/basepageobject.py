"""Draytek Web Admin - BasePage."""
from toolium.pageobjects.page_object import PageObject


class BasePageObject(PageObject):
    """Selenium Page Object Model from Toolium. BasePage class."""

    @staticmethod
    def read_element_value(element):
        """Read element value from various properties based on element type.

        :param element: Web Element
        :returns: element value
        """
        if element.web_element.is_enabled():
            if (type(element).__name__ == "InputText") or (
                type(element).__name__ == "Text"
            ):
                return element.text.strip()
            if (type(element).__name__ == "Checkbox") or (
                type(element).__name__ == "InputRadio"
            ):
                return element.is_selected()
            if type(element).__name__ == "Select":
                return element.option()
            raise TypeError(f"read_element_value: Unhandled element type: {type(element).__name__}")
        return None

    @staticmethod
    def set_element_value(element, value):
        """Set element to specified value based on element type.

        :param element: Web Element
        :param value: Value to be set against element
        """
        if element.web_element.is_enabled():
            if type(element).__name__ == "InputText":
                element.clear()
                element.text = value
                return
            if type(element).__name__ == "Checkbox":
                if value:
                    element.check()
                elif not None:
                    element.uncheck()
                return
            if type(element).__name__ == "InputRadio":
                if value:
                    element.check()
                return
            if type(element).__name__ == "Select":
                element.option = value
                return
            raise TypeError(f"write_element_value: Unhandled element type: {type(element).__name__}")
