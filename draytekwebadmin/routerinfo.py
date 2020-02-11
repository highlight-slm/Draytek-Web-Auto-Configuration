"""Draytek Web Admin - Model: Router Info."""


class RouterInfo:
    """RouterInfo Object."""

    def __init__(self, model=None, router_name=None, firmware=None, dsl_version=None):
        """Create a new RouterInfo object."""
        self.model = model
        self.router_name = router_name
        self.firmware = firmware
        self.dsl_version = dsl_version
