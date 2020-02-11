"""Draytek Web Admin - Model: Firmware."""

# pylint: disable=attribute-defined-outside-init

from pathlib import Path


class Firmware:
    """Firmware object."""

    def __init__(
        self,
        filepath=None,
        model=None,
        firmware_current=None,
        firmware_target=None,
        modem_firmware_current=None,
        modem_firmware_target=None,
    ):
        """Create a new Firmware object."""
        self.filepath = filepath
        self.model = model
        self.firmware_current = firmware_current
        self.firmware_target = firmware_target
        self.modem_firmware_current = modem_firmware_current
        self.modem_firmware_target = modem_firmware_target

    @property
    def filepath(self):
        """str: Full path to firmware file."""
        return self._filepath

    @filepath.setter
    def filepath(self, filepath):
        if filepath is not None:
            file = Path(filepath)
            if file.exists():
                self._filepath = Path(filepath)
            else:
                raise ValueError("Firmware: File Not Found!")
        else:
            self._filepath = None

    def router_firmware_upgradable(self):
        """bool: True if firmware_current is not the same as firmware_target."""
        if self.firmware_current != self.firmware_target:
            return True
        return False

    def modem_firmware_upgradable(self):
        """bool: True if modem_firmware_current is not the same as modem_firmware_target."""
        if self.modem_firmware_current != self.modem_firmware_target:
            return True
        return False
