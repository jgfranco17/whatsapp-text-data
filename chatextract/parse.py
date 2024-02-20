import click
from .parser import TextParser


@click.command("parse")
@click.option("--file", "-f", type=str, required=True, help="Path to the input text file.")
@click.option("--export", is_flag=True, help="Export JSON data.")
def parse(file, export):
    """Run the Whatsapp parser."""
    chat_parser = TextParser(filepath=file)
    if export:
        chat_parser.export_json()
