from dataclasses import dataclass
import numpy as np
from pydantic import BaseModel

from ..store.directory import DirectoryStore


class Compressor(BaseModel):
    blocksize: int
    clevel: int
    cname: str
    id: str


class ZArray(BaseModel):
    chunks: list[int]
    shape: list[int]
    zarr_format: int
    compressor: Compressor
    dtype: str
    fill_value: float | str


class Array:
    def __init__(self, store: DirectoryStore, shape: tuple[int, int], chunks: tuple[int, int]):
        self.store = store
        self._write_zarray(shape=shape, chunks=chunks)
        pass

    def _write_zarray(self, shape: tuple[int, int], chunks: tuple[int, int]):
        zarray = ZArray(
            chunks=chunks,
            shape=shape,
            compressor=Compressor(
                blocksize=0,
                clevel=5,
                cname="lz4",
                id="blosc",
            ),
            dtype=np.float32,
            zarr_format=2,
        )
        self.store[".zarray"] = zarray
        pass
