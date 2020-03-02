"""Draytek Web Admin - Dashboard Page."""

# pylint: disable=broad-except

from selenium.webdriver.common.by import By

from toolium.pageelements import Text

from draytekwebadmin.routerinfo import RouterInfo
from draytekwebadmin.pages.basepageobject import BasePageObject


class DashboardPage(BasePageObject):
    """Selenium Page Object Model: DashboardPage."""

    # Page Elements
    # Frames
    frame_header = "header"
    frame_main = "main"

    # System Information Table
    model_name = Text(
        By.CSS_SELECTOR,
        "#blksysinfo > table:nth-child(1) > tbody:nth-child(1) > tr:nth-child(2) > td:nth-child(2)",
    )
    router_name = Text(
        By.CSS_SELECTOR,
        "#blksysinfo > table:nth-child(1) > tbody:nth-child(1) > tr:nth-child(3) > td:nth-child(2)",
    )
    fw_version = Text(
        By.CSS_SELECTOR,
        "#blksysinfo > table:nth-child(1) > tbody:nth-child(1) > tr:nth-child(4) > td:nth-child(2)",
    )
    dsl_version = Text(
        By.CSS_SELECTOR,
        "#blksysinfo > table:nth-child(1) > tbody:nth-child(1) > tr:nth-child(5) > td:nth-child(3)",
    )

    def routerinfo(self):
        """Get the router info via the table on the dashboard or try and use the Javascript variables in the header.

        :returns: RouterInfo object
        """
        router = {
            "router_name": None,
            "firmware": None,
            "model": None,
            "dsl_version": None,
        }
        # try:
        # Initial read via JavaScript Header variables
        self.driver.switch_to.default_content()
        self.driver.switch_to.frame(self.frame_header)
        try:
            router["router_name"] = self.driver.execute_script("return sSysName")
        except Exception:
            pass
        try:
            router["firmware"] = self.driver.execute_script("return sSysVer")
        except Exception:
            pass
        try:
            router["model"] = self.driver.execute_script("return sFwNameLeading")
        except Exception:
            pass
        # except NoSuchElementException:
        #     pass

        # Read the values from the dashboard table and replace initial JavaScript values
        self.driver.switch_to.default_content()
        self.driver.switch_to.frame(self.frame_main)
        # TODO (#4418): Need to replace try/catch around each call with a different approach.
        #       Needs to be potentially implemented over all files.
        if self.model_name.is_visible():
            router["model"] = self.read_element_value(self.model_name)
        if self.router_name.is_visible():
            router["router_name"] = self.read_element_value(self.router_name)
        if self.fw_version.is_visible():
            router["firmware"] = self.read_element_value(self.fw_version)
        if self.dsl_version.is_visible():
            router["dsl_version"] = self.read_element_value(self.dsl_version)

        return RouterInfo(
            model=router["model"],
            router_name=router["router_name"],
            firmware=router["firmware"],
            dsl_version=router["dsl_version"],
        )
