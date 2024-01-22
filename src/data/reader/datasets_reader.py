import csv
import os

from hydra.utils import get_original_cwd

from data.reader.base_reader import BaseReader


class DatasetsReader(BaseReader):
    """Reads a local or remote datasets file in a streaming fashion."""

    def run(self):
        with open(os.path.join(get_original_cwd(), self.file_path), "r") as f:
            reader = csv.reader(f, delimiter=self.delimiter)
            headers = next(reader, None)
            for row in reader:
                yield dict(zip(headers, row))
