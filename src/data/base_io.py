import os

from hydra.utils import get_original_cwd


class BaseIO:
    def __init__(self, file_path: str, delimiter: str = ","):
        self.file_path = os.path.join(get_original_cwd(), file_path)
        self.delimiter = delimiter

    def run():
        pass
