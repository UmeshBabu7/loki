from heimdall.service.template.config import TemplateGeneratorConfig


class TemplateGeneratorService:
    def __init__(self, config: TemplateGeneratorConfig) -> None:
        self.config = config
        self.env = self.config.environment
        self.template = self.env.get_template(self.config.template_name)
        self.result_file = self.config.output_file

    def render_template(self, context: dict) -> None:
        self.result_file.parent.mkdir(parents=True, exist_ok=True)
        with open(self.result_file, mode="w") as f:
            f.write(self.template.render(context))
        print(f"Template generated: {self.result_file}")
