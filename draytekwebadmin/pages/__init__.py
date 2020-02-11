"""Selenium Page Objects for Draytek Web Admin."""
from draytekwebadmin.pages.basepage import BasePage
from draytekwebadmin.pages.menu_navigator import MenuNavigator
from draytekwebadmin.pages.login_page import LoginPage
from draytekwebadmin.pages.management_page import ManagementPage
from draytekwebadmin.pages.snmp_page import SNMPpage
from draytekwebadmin.pages.reboot_system_page import RebootSystemPage
from draytekwebadmin.pages.firmware_upgrade_page import FirmwareUpgradePage
from draytekwebadmin.pages.dashboard_page import DashboardPage

__all__ = [
    "BasePage",
    "MenuNavigator",
    "LoginPage",
    "ManagementPage",
    "SNMPpage",
    "RebootSystemPage",
    "FirmwareUpgradePage",
    "DashboardPage",
]
