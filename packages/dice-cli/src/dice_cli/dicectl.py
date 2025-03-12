import logging
from typing import Any

import rich
import typer

from . import __version__, _date, admin
from .logger import admin_logger, console_handler


def admin_callback(
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Verbose output"),
    debug: bool = typer.Option(False, "--debug", "-d", help="Debug output"),
) -> Any:
    # verbose is debug
    verbose = debug or verbose
    debug = verbose

    if debug:
        admin_logger.setLevel(logging.DEBUG)
        # workaround for rich
        console_handler.setLevel(logging.DEBUG)


app = admin.app
app.callback = admin_callback


@app.command()
def version() -> None:
    """
    Show version
    """
    rich.print(f"[blue]DICE CLI Version[/]: [magenta]{__version__}[/]")


@app.command()
def date(
    date_format: _date.DateOptions = typer.Option(
        _date.DateOptions.ISO8601_JUST_Y_M_D,
        "--format",
        "-f",
        help="Format to print",
        case_sensitive=False,
    )
) -> None:
    """
    Print the current date in ISO8601 format
    """
    rich.print(_date.formatted_date(date_format))


def main() -> Any:
    return app()
