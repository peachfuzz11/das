import datetime
import os
import unittest
from pathlib import Path

from das.das_file import DASFile


class TestLoad(unittest.TestCase):
    BASE_DIR = Path(__file__).resolve().parent.parent
    DATA_DIR = os.path.join(BASE_DIR, "data", "20250224")
    SINGLE = os.path.join(DATA_DIR, "181227.hdf5")

    def test_init(self):
        das_file = DASFile(self.SINGLE)
        self.assertEqual(das_file.filepath, self.SINGLE)

    def test_timestamp(self):
        das_file = DASFile(self.SINGLE)
        with das_file as f:
            meta = f.get_metadata()
        ts = meta["timestamp"]
        self.assertEqual(ts.replace(microsecond=0),
                         datetime.datetime(2025, 2, 24, 18, 12, 27, tzinfo=datetime.timezone.utc))

    def test_read_data_fails_no_enter(self):
        err = None
        try:
            das_file = DASFile(self.SINGLE)
            das_file.get_metadata()
        except RuntimeError as e:
            err = e
        self.assertIsNotNone(err)

    def test_read_data(self):
        err = None
        try:
            das_file = DASFile(self.SINGLE)
            with das_file as f:
                f.get_metadata()
        except RuntimeError as e:
            err = e
        self.assertIsNone(err)
