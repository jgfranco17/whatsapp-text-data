import click
import logging
from .parse import parse
from .search import search


root_logger_verbosity = [
    logging.WARN,
    logging.INFO,
    logging.DEBUG,
]

logger = logging.getLogger(__name__)
logging.Formatter(
    "%(asctime)s %(name)s [%(levelname)8s] %(message)s", 
    datefmt="%Y-%m-%d %H:%M:%S"
)

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
    stf_cli_logger = logging.getLogger(__package__)
    stf_cli_logger.setLevel(logging.DEBUG+verbose)
    context.ensure_object(dict)


cli.add_command(parse)
cli.add_command(search)
