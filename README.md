# DrayTek-Web-Auto-Configuration

[![Build Status](https://travis-ci.org/highlight-slm/Draytek-Web-Auto-Configuration.svg?branch=master)](https://travis-ci.org/highlight-slm/Draytek-Web-Auto-Configuration/) [![Coverage Status](https://coveralls.io/repos/github/highlight-slm/Draytek-Web-Auto-Configuration/badge.svg?branch=master)](https://coveralls.io/github/highlight-slm/Draytek-Web-Auto-Configuration?branch=master)

Some customers may have rolled out large number of DrayTek routers with only Web Management enabled. This makes rolling out changes to a large number of devices a tedious, manual, slow and error prone activity. Whilst DrayTek routers support TR069 to provide centralised management via an ACS, often this isn't used.

This library creates a Selenium WebDriver based API for accessing and configuring all the pages available via the web administration console.
Example utilities are provided which demonstrate how the library can be used to automate mass configuration changes.

## Capabilities

The following capabilities are currently implemented:

- Reading and writing all Management settings (_System Maintenance >> Management_)
- Reading and writing SNMP settings (_System Maintenance >> SNMP_)
- Router firmware upgrade (_System Maintenance >> Firmware Upgrade_)
  - Uploading a firmware file
  - Previewing the file to determine if an upgrade is needed
  - Performing an upgrade and rebooting
- Router Reboot (immediately, using current configuration)

## Tested Devices

The following devices and firmware versions have been tested. It is likely that other models and firmware versions will just work. However, some may require some changes. Please feel free to raise an issue, though without access to the device we may need to collaborate to get it working, or you can submit a PR.

| Model        | Firmware Versions       | Supplementary Notes |
|:-------------|-------------------------|---------------------|
| Vigor 2860   | 3.8.9.4_BT - 3.8.9.7_BT |                     |
| Vigor 2860Ln | 3.8.9.4_BT - 3.8.9.7_BT |                     |

## Requirements

This utility uses Python with Selenium Web Driver (using [Toolium](https://github.com/Telefonica/toolium) as a wrapper) in order to interact with the DrayTek Web Management console. To run this utility you will need to install:

- [Python 3.6 (or later)](https://www.python.org/downloads/)
- Install driver for required web browser. The path to the driver needs to be defined in `conf\properties.cfg`.
  - Chrome - requires [ChromeDriver](http://chromedriver.chromium.org/)
  - Firefox - requires [GeckoDriver](https://github.com/mozilla/geckodriver/releases)
- Clone [this](https://github.com/highlight-slm/Draytek-Web-Auto-Configuration) repository

From within cloned directory:

- Install requirements: `pip install --user -r requirements.txt`
- Install this module: `pip install --user .`

## Example Implementations

### Read Router Settings

This example reads the configuration of router and outputs the settings to a CSV file.
The supported command line arguments can be displayed by running: `python read_settings.py -h`

```text
usage: read_settings.py [-h] -a ADDRESS [-u USER] -p PASSWORD [-o OUTPUT] [-c CONFIG] [--browser BROWSER] [--headless] [--search_driver] [--implicit_wait IMPLICIT_WAIT] [--explicit_wait EXPLICIT_WAIT] [--debug]

Read DrayTek router settings. Saving the result to a CSV file.

optional arguments:
  -h, --help            show this help message and exit
  -a ADDRESS, --address ADDRESS
                        Router address e.g. https://192.168.0.1:8080
  -u USER, --user USER  Router administrator user name (default: admin)
  -p PASSWORD, --password PASSWORD
                        Router administrator password
  -o OUTPUT, --output OUTPUT
                        Output data file (default: draytek-out.csv)
  -c CONFIG, --config CONFIG
                        Location of configuration file directory e.g. -c c:\draytekwebadmin\conf
  --browser BROWSER     Browser name [chrome|firefox] overrides configuration file
  --headless            Run session headless (without GUI). Overrides configuration file
  --search_driver       Searches for browser driver in current directory, under conf or driver. Overrides configuration file
  --implicit_wait IMPLICIT_WAIT
                        WebDriver implicit wait time (secs). Overrides configuration file
  --explicit_wait EXPLICIT_WAIT
                        WebDriver explicit wait time (secs). Overrides configuration file
  --debug               Errors will attempt to capture Web page
```

### Write Router Settings

This example configures multiple routers specified in a CSV file.
The support command line arguments can be displayed by running: `python write_sesttings.py`

Using the -t option a template CSV file will be generated.

```text
usage: write_settings.py [-h] [-t TEMPLATE] [-w] [--no-reboot] [-c CONFIG] [--browser BROWSER] [--headless] [--search_driver] [--implicit_wait IMPLICIT_WAIT] [--explicit_wait EXPLICIT_WAIT] [--debug] [inputfile]

Write DrayTek router settings from a source CSV file.

positional arguments:
  inputfile             Input CSV. Each router and config should be on it's own row

optional arguments:
  -h, --help            show this help message and exit
  -t TEMPLATE, --template TEMPLATE
                        Generate blank template CSV e.g. -t template.csv
  -w, --whatif          Show what changes would be made, does not make any change to current configuration
  --no-reboot           Do not reboot routers after configuration change, even if required
  -c CONFIG, --config CONFIG
                        Location of configuration file directory e.g. -c c:\draytekwebadmin\conf
  --browser BROWSER     Browser name [chrome|firefox] overrides configuration file
  --headless            Run session headless (without GUI). Overrides configuration file
  --search_driver       Searches for browser driver in current directory, under conf or driver. Overrides configuration file
  --implicit_wait IMPLICIT_WAIT
                        WebDriver implicit wait time (secs). Overrides configuration file
  --explicit_wait EXPLICIT_WAIT
                        WebDriver explicit wait time (secs). Overrides configuration file
  --debug               Errors will attempt to capture Web page
```

### Upgrade Router Firmware

Apply firmware updates to multiple routers specified in a CSV file. File can contain multiple routers, models, versions.

Usage:

- Generate input file template: `upgrade.py -t upgrade-template.csv`
- Preview upgrade: `upgrade.py upgrade.csv`
- Apply firmware updates: `upgrade.py -u upgrade.csv`
  - Example [upgrade.csv](https://raw.githubusercontent.com/highlight-slm/Draytek-Web-Auto-Configuration/master/examples/upgrade.csv)

```text
usage: upgrade.py [-h] [-t TEMPLATE] [-u] [-c CONFIG] [--browser BROWSER] [--headless] [--search_driver] [--implicit_wait IMPLICIT_WAIT] [--explicit_wait EXPLICIT_WAIT] [--debug] [inputfile]

Upgrade Draytek Router firmware from a source CSV file

positional arguments:
  inputfile             Input CSV. Each router and config should be on it's own row

optional arguments:
  -h, --help            show this help message and exit
  -t TEMPLATE, --template TEMPLATE
                        Generate blank template CSV e.g. -t template.csv
  -u, --upgrade         Perform firmware upgrade (inc reboot), preview only
  -c CONFIG, --config CONFIG
                        Location of configuration file directory e.g. -c c:\draytekwebadmin\conf
  --browser BROWSER     Browser name [chrome|firefox] overrides configuration file
  --headless            Run session headless (without GUI). Overrides configuration file
  --search_driver       Searches for browser driver in current directory, under conf or driver. Overrides configuration file
  --implicit_wait IMPLICIT_WAIT
                        WebDriver implicit wait time (secs). Overrides configuration file
  --explicit_wait EXPLICIT_WAIT
                        WebDriver explicit wait time (secs). Overrides configuration file
  --debug               Errors will attempt to capture Web page
```

## Development & Unit Testing

If you are looking to contribute/extend this project. You will need to install additional requirements:

- For testing, linting and code coverage: `pip install -r requirements_test.txt`
- For development, ensuring tests are run before committing code: `pip install -r requirements_dev.txt`
- Setup git pre-commit hook: `pre-commit install`

## Contributors

This project is inspired by the work performed by two work experience students during their week at Highlight.

- [Martin Rowan](https://www.linkedin.com/in/martinrowan/)
- Work experience students from the [Royal Grammar School Guildford](https://www.linkedin.com/school/royal-grammar-school-guildford/):
  - [Jackie Zhang](https://www.linkedin.com/in/jackie-zhang-70a79218a/)
  - [Anish Goel](https://www.linkedin.com/in/anish-goel-0500ab183/)
