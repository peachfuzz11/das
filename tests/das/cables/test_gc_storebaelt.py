import glob
import os
import unittest
from pathlib import Path

from das.cables.gc_storebaelt import GCStorebaelt


class TestGCStorebaelt(unittest.TestCase):
    CABLE = GCStorebaelt()

    BASE_DIR = Path(__file__).resolve().parent.parent.parent
    DATA_DIR = os.path.join(BASE_DIR, "data", "20250224")
    SINGLE = os.path.join(DATA_DIR, "181227.hdf5")
    MANY = glob.glob(os.path.join(DATA_DIR, "*.hdf5"))

    def test_gc_storebaelt_read_resource(self):
        self.assertIsNotNone(self.CABLE.geojson)

    def test_read_files(self):
        ds = self.CABLE.read_files(self.MANY)
