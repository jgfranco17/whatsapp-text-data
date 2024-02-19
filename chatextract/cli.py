import click
import logging
from .parser import TextParser


@click.command("parse")
@click.option("--file", "-f", type=str, required=True, help="Path to the input text file.")
@click.option("-v", "--verbose", is_flag=True, help="Enable verbose output.")
@click.option("--export", is_flag=True, help="Export JSON data.")
def parse(file, verbose, export):
    """Run the Whatsapp parser."""
    chat_parser = TextParser(filepath=file, verbose=verbose)
    chat_parser.filter_by_key("haha")
    if export:
        chat_parser.export_json()


@click.group()
@click.pass_context
@click.option(
    "-v",
    "--verbose",
    count=True,
    help="Enable increasingly verbose output logging."
)
@click.version_option()
def cli(context: click.Context, verbose: int) -> None:
    """Whatsapp Parser CLI."""
    logging.getLogger().setLevel(logging.INFO)
    context.ensure_object(dict)


cli.add_command(parse)
