from pathlib import Path
from typing import Type

from heimdall.lib.parser.json import JSONParser
from heimdall.lib.parser.parser import Parser
from heimdall.service.json.config import JSONNormalizerConfig
from heimdall.service.json.normalizer import JSONNormalizerService
from heimdall.service.json.schema import GitLeaksSchema


class JSONNormalizerFactory:
    def __init__(self):
        self._parser: Parser | None = None
        self._json_file_path: Path | None = None
        self._output_file_path: Path | None = None
        self._schema: Type[GitLeaksSchema] | None = None

    def with_parser(self, parser: JSONParser):
        self._parser = Parser(parser)
        return self

    def with_json_file_path(self, path: Path):
        self._json_file_path = path
        return self

    def with_output_file_path(self, path: Path):
        self._output_file_path = path
        return self

    def with_schema(self, schema: Type[GitLeaksSchema]):
        self._schema = schema
        return self

    def _validate(self):
        if self._parser is None:
            raise ValueError("Parser is not set.")
        if self._json_file_path is None:
            raise ValueError("JSON file path is not set.")
        if self._output_file_path is None:
            raise ValueError("Output file path is not set.")
        if self._schema is None:
            raise ValueError("Schema is not set.")

    def create(self):
        self._validate()
        assert self._parser is not None
        assert self._json_file_path is not None
        assert self._output_file_path is not None
        assert self._schema is not None

        data = self._parser.parse(self._json_file_path)

        if not isinstance(data, list):
            raise ValueError(
                "Invalid JSON format: expected a list of objects."
            )

        config = JSONNormalizerConfig(
            data=data,
            schema=self._schema,
            output_file_path=self._output_file_path,
        )
        return JSONNormalizerService(config)
