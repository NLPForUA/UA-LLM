from typing import Dict

from data.base_io import BaseIO


class BaseReader(BaseIO):
    """Reads a file in a streaming fashion."""

    def run(self, apply_fn: Dict[str, callable] = {}) -> dict:
        raise NotImplementedError

    def stream(self) -> dict:
        raise NotImplementedError
