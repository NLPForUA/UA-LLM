from data.reader.base_reader import BaseReader
from data.writer.base_writer import BaseWriter


class BaseTask:
    def __init__(self, model, reader: BaseReader, writer: BaseWriter):
        self.model = model
        self.reader = reader
        self.writer = writer

    def run(self):
        raise NotImplementedError
