from argparse import Namespace

from heimdall.command.args import JSONArgs, TemplateArgs
from heimdall.enums import ArgsEnum


class ArgsFactory:
    def __init__(self, args: Namespace):
        self.args = vars(args).items()
        self.args_dict = {k: v for k, v in self.args if k != "command"}
        self.subcmd = None

    def with_subcommand(self, subcommand: str):
        if subcommand is None:
            raise ValueError(
                "A subcommand is required. Choose from: template, json"
            )
        self.subcmd = ArgsEnum(subcommand)
        return self

    def create(self) -> TemplateArgs | JSONArgs:
        if self.subcmd is None:
            raise ValueError("Set the value of subcommand")

        match self.subcmd:
            case ArgsEnum.TEMPLATE:
                return TemplateArgs(**self.args_dict)
            case ArgsEnum.JSON:
                return JSONArgs(**self.args_dict)
            case _:
                raise ValueError(f"Invalid subcommand: {self.subcmd}.")
