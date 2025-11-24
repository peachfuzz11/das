import unittest

from das.cables.gc_storebaelt import GCStorebaelt


class TestGCStorebaelt(unittest.TestCase):


    def test_gc_storebaelt_read_resource(self):
        cable = GCStorebaelt()
        self.assertIsNotNone(cable.geojson)