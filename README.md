# DrayTek-Web-Auto-Configuration

[![Build Status](https://travis-ci.org/highlight-slm/Draytek-Web-Auto-Configuration.svg?branch=master)](https://travis-ci.org/highlight-slm/Draytek-Web-Auto-Configuration/) [![Coverage Status](https://coveralls.io/repos/github/highlight-slm/Draytek-Web-Auto-Configuration/badge.svg?branch=master)](https://coveralls.io/github/highlight-slm/Draytek-Web-Auto-Configuration?branch=master)

Some customers may have rolled out large number of DrayTek routers with only Web Management enabled. This makes rolling out changes to a large number of devices a tedious, manual, slow and error prone activity. Whilst DrayTek routers support TR069 to provide centralised management via an ACS, often this isn't used.

This library creates a Selenium WebDriver based API for accessing and configuring all the pages available via the web administration console.
Example utilities are provided which demonstrate how the library can be used to automate mass configuration changes.

## Capabilities

The following capabilities are currently implemented:

- Reading and writing Internet Access Control settings (_System Maintenance >> Management >> Internet Access Control_)
  - Enabling/Disabling remote management via the WAN interface
  - Restricting remote access to a defined domain name
  - Enabling/Disabling specific protocols are exposed via the WAN
- Reading and writing SNMPv2 settings (_System Maintenance >> SNMP_)
  - Enabling SNMP Agent
  - Setting the Community strings
  - Setting the allowed Management Host IPs (IPv4)
- Router firmware upgrade (_System Maintenance >> Firmware Upgrade_)
  - Uploading a firmware file
  - Previewing the file to determine if an upgrade is needed
  - Performing an upgrade and rebooting
- Router Reboot (immediately, using current configuration)

Note full data models have been created for the SNMP and Management pages. Enabling anyone to contribute further to add the extra settings they need to configure.

## Tested Devices

The following devices and firmware versions have been tested. It is likely that other models and firmware versions will just work. However, some may require some changes. Please feel free to raise an issue, though without access to the device we may need to collaborate to get it working, or you can submit a PR.

| Model        | Firmware Versions       | Supplementary Notes |
|:-------------|-------------------------|---------------------|
| Vigor 2860   | 3.8.9.4_BT - 3.8.9.7_BT |                     |
| Vigor 2860Ln | 3.8.9.4_BT - 3.8.9.7_BT |                     |

## Requirements

This utility uses Python with Selenium Web Driver in order to interact with the DrayTek Web Management console. In order to run this utility you will need to install:

- Python 3.6 (or later)
- Python binding for [Selenium](https://pypi.org/project/selenium/)

To install requirements: `pip install -r requirements.txt`

### Supported Browsers

Depending on which Web Browser you have installed you will need the appropriate driver, placing the executable in the same directory as this library. Note that the drivers are linked to the specific browser version, please check and install the correct version.

- Chrome - requires [ChromeDriver](http://chromedriver.chromium.org/)
- Firefox - requires [GeckoDriver](https://github.com/mozilla/geckodriver/releases)

## Example Implementations

### Read and Write Router Settings

Configure multiple routers specified in a CSV file

Usage: TODO

Read settings from routers and save to CSV: `examples/read_settings.py`
Write new settings to router: `examples/write_settings.py`

### Upgrade Router Firmware

Apply firmware updates to multiple routers specified in a CSV file. File can contain multiple routers, models, versions.

Usage:
 - Generate input file template: `upgrade.py -t upgrade-template.csv`
 - Preview upgrade: `upgrade.py upgrade.csv`
 - Apply firmware updates: `upgrade.py -u upgrade.csv`
   - Example [upgrade.csv](https://raw.githubusercontent.com/highlight-slm/Draytek-Web-Auto-Configuration/master/examples/upgrade.csv)

See: `examples/upgrade.py`

## Development & Unit Testing

If you are looking to contribute/extend this project. You will need to install additional requirements:

- For testing, linting and code coverage: `pip install -r requirements_test.txt`
- For development, ensuring tests are run before committing code: `pip install -r requirements_dev.txt`

## Contributors

This project is inspired by the work performed by two work experience students during their week at Highlight.

- [Martin Rowan](https://www.linkedin.com/in/martinrowan/)
- Work experience students from the [Royal Grammar School Guildford](https://www.linkedin.com/school/royal-grammar-school-guildford/):
  - [Jackie Zhang](https://www.linkedin.com/in/jackie-zhang-70a79218a/)
  - [Anish Goel](https://www.linkedin.com/in/anish-goel-0500ab183/)
