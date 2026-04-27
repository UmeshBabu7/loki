from pathlib import Path

from jinja2 import Environment, FileSystemLoader

from heimdall.service.template import (
    TemplateGeneratorConfig,
    TemplateGeneratorService,
)


class TemplateFactory:
    def with_base_dir(self, base_dir: Path):
        self.base_dir = base_dir
        return self

    def with_template_filename(self, template_filename: str):
        self.template_filename = template_filename
        return self

    def with_output_filepath(self, output_filepath: str):
        self.output_path = output_filepath
        return self

    def _validate(self):
        if not self.template_filename:
            raise FileNotFoundError("Template filename cannot be empty.")

        template_dir = self.base_dir / "templates"

        if not (template_dir / self.template_filename).exists():
            raise FileNotFoundError(
                f"Template not found: {template_dir / self.template_filename}"
            )

        if not self.output_path:
            raise FileNotFoundError("Output path cannot be empty.")

    def create(self) -> TemplateGeneratorService:
        self._validate()

        template_dir = self.base_dir / "templates"

        env = Environment(loader=FileSystemLoader(str(template_dir)))
        config = TemplateGeneratorConfig(
            environment=env,
            output_file=self.base_dir / self.output_path,
            template_name=self.template_filename,
        )
        return TemplateGeneratorService(config)
