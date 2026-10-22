from pathlib import Path
import os


class DirectoryStore:
    def __init__(self, path: str):
        self.path = path
        self.store: dict[str, bytes] = {}
        self.is_existed = self._check_path_existed(path)

    def check_path_existed(self, path: str):
        _path = Path(path)
        return _path.exists()

    def _create_dir(self, path: str):
        _path = Path(path)
        _path.mkdir()

    def _build_chunk_path(self, path: str) -> str:
        return os.path.join(self.path, path)

    def __getitem__(self, key) -> bytes:
        chunk_path = self._build_chunk_path(key)
        if not self.check_path_existed(chunk_path):
            raise KeyError(key)
        with open(chunk_path, mode="rb") as f:
            data = f.read()
        return data

    def __setitem__(self, key: str, value: bytes):
        if not self.is_existed:
            self._create_dir(self.path)
        chunk_path = self._build_chunk_path(key)
        with open(chunk_path, mode="wb") as f:
            f.write(value)
