from typing import Dict, Union

from data.writer.base_writer import BaseWriter


class CSVWriter(BaseWriter):
    """Writes a CSV file in a streaming fashion."""

    def run(self, data: Union[list, Dict[str, list]]):
        prep_data = data
        if isinstance(data, dict):
            self.stream(data.keys())
            if isinstance(data[list(data.keys())[0]], dict):
                prep_data = [[x for x in data.values()]]
        for row in prep_data:
            self.stream(row)

    def stream(self, row: list):
        row = [str(x) for x in row]
        self.output_file.write(self.delimiter.join(row) + "\n")
