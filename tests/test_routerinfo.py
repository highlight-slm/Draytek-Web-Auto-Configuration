import unittest

from draytekwebadmin.routerinfo import RouterInfo


class TestRouterInfo(unittest.TestCase):
    def test_empty(self):
        empty = RouterInfo()
        self.assertIsNone(empty.model)
        self.assertIsNone(empty.router_name)
        self.assertIsNone(empty.firmware)
        self.assertIsNone(empty.dsl_version)

    def test_valid(self):
        self.assertEqual("DrayTek V1234", RouterInfo(model="DrayTek V1234").model)
        self.assertEqual("My Router", RouterInfo(router_name="My Router").router_name)
        self.assertEqual("1.2.3.4ABC", RouterInfo(firmware="1.2.3.4ABC").firmware)
        self.assertEqual("ABC1234", RouterInfo(dsl_version="ABC1234").dsl_version)
