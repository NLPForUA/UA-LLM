from typing import Dict, Union

from data.base_io import BaseIO


class BaseWriter(BaseIO):
    """Writes a CSV file in a streaming fashion."""

    def __init__(self, file_path: str, delimiter: str = ","):
        super().__init__(file_path, delimiter)
        self.output_file = open(self.file_path, "w+")

    def run(self, data: Union[list, Dict[str, list]]):
        raise NotImplementedError

    def stream(self, row: list):
        raise NotImplementedError

    def close(self):
        self.output_file.close()

    def __del__(self):
        self.close()
