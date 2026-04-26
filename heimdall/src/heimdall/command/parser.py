import argparse

arg_parser = argparse.ArgumentParser()

subparsers = arg_parser.add_subparsers(dest="command")

template_parser = subparsers.add_parser(
    "template",
    help="Generate HTML report from json",
)
template_parser.add_argument(
    "--json-file-path",
    required=True,
    help="Path to the json file",
)
template_parser.add_argument(
    "--template-file-name",
    required=True,
    help="Template file name",
)
template_parser.add_argument(
    "--output-file-path", required=True, help="Output html file path"
)
json_parser = subparsers.add_parser(
    "json",
    help="Filter JSON and write to output file",
)
json_parser.add_argument(
    "--json-file-path",
    required=True,
    help="Path to the input json file",
)
json_parser.add_argument(
    "--output-file-path",
    required=True,
    help="Output json file path",
)
