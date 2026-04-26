from abc import ABC, abstractmethod
from pathlib import Path


class AbstractParser(ABC):
    @abstractmethod
    def parse(self, json_file_path: Path):
        pass


class Parser:
    def __init__(self, parser: AbstractParser) -> None:
        self.parser = parser

    def parse(self, json_file_path: Path):
        return self.parser.parse(json_file_path)
