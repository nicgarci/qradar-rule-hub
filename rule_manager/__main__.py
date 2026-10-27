import logging
import pathlib
import click

from rule_manager.rules import Rules

LOGGER = logging.getLogger()

ROOT_DIR = pathlib.Path(__file__).parent.parent
RULES_DIR = ROOT_DIR / "rules"

BANNER = """
██████╗ ██╗   ██╗██╗     ███████╗    ███╗   ███╗ █████╗ ███╗   ██╗ █████╗  ██████╗ ███████╗██████╗ 
██╔══██╗██║   ██║██║     ██╔════╝    ████╗ ████║██╔══██╗████╗  ██║██╔══██╗██╔════╝ ██╔════╝██╔══██╗
██████╔╝██║   ██║██║     █████╗      ██╔████╔██║███████║██╔██╗ ██║███████║██║  ███╗█████╗  ██████╔╝
██╔══██╗██║   ██║██║     ██╔══╝      ██║╚██╔╝██║██╔══██║██║╚██╗██║██╔══██║██║   ██║██╔══╝  ██╔══██╗
██║  ██║╚██████╔╝███████╗███████╗    ██║ ╚═╝ ██║██║  ██║██║ ╚████║██║  ██║╚██████╔╝███████╗██║  ██║
╚═╝  ╚═╝ ╚═════╝ ╚══════╝╚══════╝    ╚═╝     ╚═╝╚═╝  ╚═╝╚═╝  ╚═══╝╚═╝  ╚═╝ ╚═════╝ ╚══════╝╚═╝  ╚═╝
"""

class RuleOperations:

    @classmethod
    def dump(cls, csv_file_path: pathlib.Path):
        extracted_rules = Rules.parse_rules(csv_file_path=csv_file_path)
        if not extracted_rules.rules:
            return
        for local_rule_file in list(RULES_DIR.glob("*.json")):
            local_rule_file.unlink()
        extracted_rules.dump_rules()

@click.group()
def cli():
    """Rule Manager."""

@click.command(
    "dump",
    short_help="""Dump rules from CSV report to local files."""
)

@click.argument(
    "csv_file_path",
    required=True,
    type=click.Path(
        exists=True, file_okay=True, dir_okay=True, path_type=pathlib.Path
    ),
    help="File path for the CSV to dump.",
)

def dump_rules(csv_file_path: pathlib.Path):
    """Dump rules from CSV report to local files."""
    LOGGER.info(
        "Attempting to dump and update all rules from CSV report to local files."
    )
    RuleOperations.dump(csv_file_path=csv_file_path)

if __name__ == "__main__":
    RULES_DIR.mkdir(exist_ok=True)
    print(BANNER)
    cli.add_command(dump_rules)
    cli()