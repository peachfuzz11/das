import abc
import json
import os


class Cable(abc.ABC):
    CABLE_RESOURCE = None

    def __init__(self):
        json_path = os.path.join(os.path.dirname(__file__), "resources", self.CABLE_RESOURCE)
        with open(json_path, "r", encoding="utf-8") as f:
            self._geojson = json.load(f)

    @property
    def geojson(self):
        return self._geojson
