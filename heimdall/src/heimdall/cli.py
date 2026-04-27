from pathlib import Path

from heimdall.command import CliArgs, arg_parser
from heimdall.enums import ArgsEnum
from heimdall.lib import (
    ArgsFactory,
    JSONNormalizerFactory,
    JSONParser,
    Parser,
    TemplateFactory,
)
from heimdall.service.json import GitLeaksSchema, JSONNormalizerService
from heimdall.service.template import TemplateGeneratorService

base_dir = Path(__file__).parent


class Cli:
    def __init__(
        self,
        cli_args: CliArgs,
        parser: JSONParser,
        template: TemplateGeneratorService | None,
        json_normalizer: JSONNormalizerService | None,
        json_file_path: Path,
    ):
        self.cli_args = cli_args
        self.parser = Parser(parser)
        self.template = template
        self.json_normalizer = json_normalizer
        self.context = {}
        self.json_file_path = json_file_path

    def start(self):
        self._run()

    def _run(self):
        match self.cli_args.args.Meta._type:
            case ArgsEnum.TEMPLATE:
                if self.template is None:
                    raise ValueError("Template not found.")
                parsed_results = self.parser.parse(self.json_file_path)
                self.context = {"results": parsed_results}

                self.template.render_template(self.context)

            case ArgsEnum.JSON:
                if self.json_normalizer is None:
                    raise ValueError(
                        "JSONNormalizerService is not initilized."
                    )
                self.json_normalizer.normalize_json()

            case _:
                raise Exception("Failed to run the cli service")


def app():
    args = arg_parser.parse_args()

    if args.command is None:
        arg_parser.print_help()
        return

    _args = ArgsFactory(args).with_subcommand(args.command).create()
    cli_args = CliArgs(_args)

    parser = JSONParser()
    template = None
    json_normalizer = None

    json_file_path = (base_dir / args.json_file_path).resolve()
    output_file_path = (base_dir / args.output_file_path).resolve()

    match ArgsEnum(args.command):
        case ArgsEnum.TEMPLATE:
            template = (
                TemplateFactory()
                .with_base_dir(base_dir)
                .with_template_filename(args.template_file_name)
                .with_output_filepath(args.output_file_path)
                .create()
            )

        case ArgsEnum.JSON:
            json_normalizer = (
                JSONNormalizerFactory()
                .with_parser(JSONParser())
                .with_json_file_path(json_file_path)
                .with_output_file_path(output_file_path)
                .with_schema(GitLeaksSchema)
                .create()
            )

    Cli(
        cli_args,
        parser,
        template,
        json_normalizer,
        json_file_path,
    ).start()


if __name__ == "__main__":
    app()
