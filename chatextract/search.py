"""New CLI Group."""
import click
from chatextract.parser import TextParser


@click.group("search")
def search() -> None:
    """Search a word."""
    pass


@click.command("word")
@click.option("--file", "-f", type=str, required=True, help="Path to the input text file.")
@click.option("--keyword", "-k", type=str, required=True, help="Keyword to search.")
def search_by_keyword(file, keyword: str):
    """Search by keyword."""
    chat_parser = TextParser(filepath=file)
    chat_parser.filter_by_key(keyword)


search.add_command(search_by_keyword)