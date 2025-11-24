import datetime
import math
import os

import h5py


class DASFile:
    def __init__(self, filepath):
        self._filepath = filepath
        self._file = None

    def __enter__(self):
        self._file = h5py.File(self.filepath, "r")
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._file.close()
        self._file = None

    def get_timestamp(self) -> datetime.datetime:
        date = os.path.basename(os.path.dirname(self.filepath))
        time = os.path.splitext(os.path.basename(self.filepath))[0]
        timestamp_str = date + time
        return datetime.datetime.strptime(timestamp_str, "%Y%m%d%H%M%S")

    @property
    def filepath(self):
        return self._filepath

    def get_data(self):
        if self._file is None:
            raise RuntimeError()
        return self._file["data"][:]

    def get_metadata(self):
        if self._file is None:
            raise RuntimeError()
        file = self._file
        metadata = {
            "x": file["cableSpec"]["sensorDistances"][:],
            "dt": file["header"]["dt"][()],
            "dx": file["header"]["dx"][()],
            "n": file["cableSpec"]["refractiveIndexes"][()],
            "GL": file["header"]["gaugeLength"][()],
            "nx": len(file["header"]["channels"][()]),
        }
        metadata["scale"] = (2 * math.pi) / 2 ** 16 * (1550.12 * 1e-9) / (
                0.78 * 4 * math.pi * metadata["n"] * metadata["GL"])
        return metadata
