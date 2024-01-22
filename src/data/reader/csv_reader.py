import csv
from typing import Dict, List, Union

from data.reader.base_reader import BaseReader


class CSVReader(BaseReader):
    """Reads a CSV file in a streaming fashion."""

    def run(
        self, apply_fn: Dict[str, callable] = {}
    ) -> Union[Dict[str, list], List[dict]]:
        data = {}
        headers = None
        with open(self.file_path, "r", encoding="utf-8") as f:
            reader = csv.reader(f, delimiter=self.delimiter)
            if headers is None:
                headers = next(reader, None)
                data = {h: [] for h in headers}
            for row in reader:
                for h, v in zip(headers, row):
                    if h in apply_fn:
                        v = apply_fn[h](v)
                    data[h].append(v)
        return data

    def stream(self, apply_fn: Dict[str, callable] = {}):
        with open(self.file_path, "r", encoding="utf-8") as f:
            reader = csv.reader(f, delimiter=self.delimiter)
            headers = next(reader, None)
            for row in reader:
                yield dict(zip(headers, row))
