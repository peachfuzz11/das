import datetime
import glob
import os
import typing

import xarray

from das.das_file import DASFile


def read_folder(folder_path) -> xarray.Dataset:
    files = glob.glob(os.path.join(folder_path, "*.hdf5"))
    return read_files(files)


def read_files(files: typing.List[str]) -> xarray.Dataset:
    file_list = sorted(files)
    ref_file = DASFile(file_list[0])
    with ref_file as f:
        metadata = f.get_metadata()

    def prepare_file(ds):
        filename = ds.encoding["source"]
        dasfile = DASFile(filename)
        timestamp = dasfile.get_timestamp()

        time_values = [timestamp + datetime.timedelta(seconds=i * metadata["dt"]) for i in
                       range(ds.sizes["phony_dim_0"])]
        ds["time"] = (("phony_dim_0",), time_values)
        ds["distance"] = (("phony_dim_1",), metadata["x"])
        ds = ds.rename({"phony_dim_1": "distance", "phony_dim_0": "time"})
        ds = ds.set_coords(["time", "distance"])
        ds = ds.drop_vars(["fileGenerator", "fileGeneratorSvnRev", "fileVersion", "numberOfAuxData"])
        return ds

    data = xarray.open_mfdataset(
        file_list,
        engine="h5netcdf",
        parallel=True,
        phony_dims="sort",
        preprocess=prepare_file,
        combine="nested",
        concat_dim="time",
    )
    return data
