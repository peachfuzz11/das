import abc
import json
import os
import typing

import numpy
import xarray

from das import read_folder, read_files


class Cable(abc.ABC):
    CABLE_RESOURCE = None

    def __init__(self):
        json_path = os.path.join(os.path.dirname(__file__), "resources", self.CABLE_RESOURCE)
        with open(json_path, "r", encoding="utf-8") as f:
            self._geojson = json.load(f)

    @property
    def geojson(self):
        return self._geojson

    def read_folder(self, folder_path) -> xarray.Dataset:
        ds = read_folder(folder_path)
        ds = self._add_cable_info(ds)
        return ds

    def read_files(self, files: typing.List[str]) -> xarray.Dataset:
        ds = read_files(files)
        ds = self._add_cable_info(ds)
        return ds

    def _add_cable_info(self, ds: xarray.Dataset) -> xarray.Dataset:
        lon, lat = zip(*self.geojson["geometry"]["coordinates"])
        depth = self.geojson["properties"]["depths"]
        n = ds.sizes["x"]
        lat, lon, depth = map(lambda v: numpy.interp(numpy.linspace(0, len(lat), n), numpy.arange(len(lat)), v),
                              [lat, lon, depth])
        ds["lat"] = lat
        ds["lon"] = lon
        ds["depth"] = depth
        return ds
