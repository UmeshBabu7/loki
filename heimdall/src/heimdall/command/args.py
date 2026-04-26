from dataclasses import dataclass
from heimdall.enums import ArgsEnum


@dataclass(frozen=True)
class TemplateArgs:
    class Meta:
        _type = ArgsEnum.TEMPLATE

    json_file_path: str
    template_file_name: str
    output_file_path: str


@dataclass(frozen=True)
class JSONArgs:
    class Meta:
        _type = ArgsEnum.JSON

    json_file_path: str
    output_file_path: str


@dataclass(frozen=True)
class CliArgs:
    args: TemplateArgs | JSONArgs
