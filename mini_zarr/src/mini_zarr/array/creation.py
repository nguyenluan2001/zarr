from ..store.directory import DirectoryStore
from .array import Array, ZArray
from .models import OpenArrayMode
import numpy as np


def init_array_metadata(
    shape: tuple[int, ...],
    chunks: tuple[int, ...],
    dtype: str,
    fill_value: int = 0,
):
    return ZArray(
        chunks=chunks,
        compressor={"blocksize": 0, "clevel": 5, "cname": "lz4", "id": "blosc", "shuffle": 1},
        dtype=dtype,
        fill_value=fill_value,
        filters=None,
        order="C",
        shape=shape,
        zarr_format=2,
    )


def init_array(
    store: DirectoryStore,
    shape: tuple[int, ...],
    chunks: tuple[int, ...],
    dtype: str,
    fill_value: int = 0,
    mode: OpenArrayMode = "r",
):

    is_existed = store.check_path_existed(store.path)
    if not is_existed:
        zarray = init_array_metadata(shape=shape, chunks=chunks, dtype=dtype, fill_value=fill_value)
        store[".zarray"] = bytes(zarray.model_dump_json())
    # array = Array(store)


def open_array(
    store: DirectoryStore,
    shape: tuple[int, ...],
    chunks: tuple[int, ...],
    dtype: str = np.float32.dtype,
    fill_value: int = 0,
    mode: OpenArrayMode = "r",
) -> Array:
    init_array(store, shape=shape, chunks=chunks, dtype=dtype, fill_value=fill_value)
