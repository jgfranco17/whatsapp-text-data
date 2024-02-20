"""New CLI Group."""
import click

from chatextract.parser import TextParser


@click.group("search")
def search() -> None:
    """Search a word."""
    pass


@click.command("word")
@click.argument("keyword", type=str)
@click.option(
    "file", "-f", type=str, required=True, help="Path to the input text file."
)
def search_by_keyword(file, keyword: str):
    """Search by keyword."""
    chat_parser = TextParser(filepath=file)
    chat_parser.filter_by_key(keyword)


@click.command("user")
@click.argument("sender", type=str)
@click.option(
    "file", "-f", type=str, required=True, help="Path to the input text file."
)
def search_by_user(file, sender: str):
    """Search by user."""
    chat_parser = TextParser(filepath=file)
    chat_parser.filter_by_person(sender)


search.add_command(search_by_keyword)
search.add_command(search_by_user)
