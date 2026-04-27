from dataclasses import dataclass
from pathlib import Path
from jinja2 import Environment


@dataclass(frozen=True)
class TemplateGeneratorConfig:
    environment: Environment
    output_file: Path
    template_name: str
