import json
from pathlib import Path
from heimdall.lib.parser.parser import AbstractParser


class JSONParser(AbstractParser):
    def _load_json(self, json_file_path: Path):
        if not json_file_path.exists():
            raise FileNotFoundError(f"File does not exists: {json_file_path}")

        try:
            with open(json_file_path, "r") as f:
                data = json.load(f)
            return data
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid json format in {json_file_path}: {e}")

    def parse(self, json_file_path: Path):
        return self._load_json(json_file_path)
