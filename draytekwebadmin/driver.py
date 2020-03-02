"""Draytek Web Admin - Toolium Session."""
from os import getcwd
from pathlib import Path
import logging


from toolium import test_cases

LOGGER = logging.getLogger("root")


class TooliumSession(test_cases.SeleniumTestCase):
    """Toolium Session."""

    def setUp(self, configuration_directory=None):
        """Override setUp function to enable config file directory to be configured.

        :param configuration_directory: path to config file location
        """
        self.config_files.set_config_properties_filenames(
            "properties.cfg", "local-properties.cfg"
        )
        if configuration_directory:
            self.config_files.set_config_directory(str(configuration_directory))
        else:
            conf_dir = Path(getcwd(), "conf")
            if not Path.exists(conf_dir):
                conf_dir = Path(getcwd(), "draytekwebadmin", "conf")
            if Path.exists(conf_dir):
                self.config_files.set_config_directory(str(conf_dir))
        super(TooliumSession, self).setUp()
