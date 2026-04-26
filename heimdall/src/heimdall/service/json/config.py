from dataclasses import dataclass
from pathlib import Path
from typing import Type
from heimdall.service.json.schema import GitLeaksSchema


@dataclass(frozen=True)
class JSONNormalizerConfig:
    data: list
    schema: Type[GitLeaksSchema]
    output_file_path: Path
