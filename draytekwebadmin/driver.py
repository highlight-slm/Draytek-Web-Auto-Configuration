"""Draytek Web Admin - Selenium Web Driver selector."""

import logging
from selenium import webdriver
from selenium.common.exceptions import WebDriverException

LOGGER = logging.getLogger("root")


def load_driver(browser_name="", headless=False):
    """Create a Selenium WebDriver instance. Will attempt to auto-detect if browserName not set.

    Args:
        browserName: Browser Name [FireFox, Chrome, IE, Edge] (case insensitive)
        headless: (optional) Set to True to run without the web page being visible (Default: False)

    Returns:
        webdriver: Selenium WebDriver instance

    """
    LOGGER.info(
        f"Loading Webdriver - BrowserName: {browser_name} - Headless: {headless}"
    )
    if browser_name.upper() == "FIREFOX":
        return load_firefox(headless)
    if browser_name.upper() == "CHROME":
        return load_chrome(headless)
    if browser_name.upper() == "EDGE":
        return load_edge()
    if browser_name:
        raise Exception(
            f"Unable to start Selenium Webdriver for browser: {browser_name}"
        )

    # Browser not specified, first one that works will be returned.
    LOGGER.debug(
        "Loading Webdriver - BrowserName not specified, attempting each supported browser"
    )
    try:
        return load_firefox(headless)
    except WebDriverException:
        try:
            return load_chrome(headless)
        except WebDriverException:
            try:
                return load_edge()
            except WebDriverException as error:
                raise Exception(f"Unable to find suitable browser. Error {error}")


def unload_driver(driver):
    """Shutdown given webdriver instance.

    Args:
        driver (selenium.webdriver): The running webdriver instance

    """
    driver.quit()


def load_firefox(headless):
    """Create Firefox Selenium WebDriver.

    Args:
        headless: Set to True to run without the web page being visble

    Returns:
        webdriver: FireFox Selenium WebDriver instance

    """
    LOGGER.info("Loading Webdriver - Firefox")
    options = webdriver.FirefoxOptions()
    options.headless = headless
    driver = webdriver.Firefox(firefox_options=options)
    driver.maximize_window()
    return driver


def load_chrome(headless):
    """Create Chrome Selenium WebDriver.

    Args:
        headless: Set to True to run without the web page being visible

    Returns:
        webdriver: Chrome Selenium WebDriver instance

    """
    LOGGER.info("Loading Webdriver - Chrome")
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    options.headless = headless
    return webdriver.Chrome(chrome_options=options)


def load_edge():
    """Create Edge Selenium WebDriver.

    Args:
        None

    Returns:
        webdriver: Edge Selenium WebDriver instance

    """
    LOGGER.info("Loading Webdriver - Edge")
    return webdriver.Edge()
