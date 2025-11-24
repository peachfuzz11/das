import glob
import os
import unittest
from pathlib import Path

from das import read_files, read_folder


class TestDASArray(unittest.TestCase):
    BASE_DIR = Path(__file__).resolve().parent.parent
    DATA_DIR = os.path.join(BASE_DIR, "data", "20250224")
    SINGLE = os.path.join(DATA_DIR, "181227.hdf5")
    MANY = glob.glob(os.path.join(DATA_DIR, "*.hdf5"))

    def test_read_single(self):
        arr = read_files([self.SINGLE])
        self.assertIsNotNone(arr)

    def test_read_many(self):
        arr = read_files(self.MANY)
        self.assertIsNotNone(arr)

    def test_read_folder(self):
        arr = read_folder(self.DATA_DIR)
        self.assertIsNotNone(arr)
