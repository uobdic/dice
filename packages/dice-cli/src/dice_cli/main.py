import logging
import os
from typing import Any, Optional

import rich
import typer

from . import __version__, _date, benchmark, check, docs, info, job
from .logger import console_handler, user_logger


def user_callback(
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Verbose output"),
    debug: bool = typer.Option(False, "--debug", "-d", help="Debug output"),
) -> Any:
    # verbose is debug
    verbose = debug or verbose
    debug = verbose

    if debug:
        user_logger.setLevel(logging.DEBUG)
        # workaround for rich
        console_handler.setLevel(logging.DEBUG)


app = typer.Typer()
app.add_typer(benchmark.app, name="benchmark", callback=user_callback)
app.add_typer(check.app, name="check", callback=user_callback)
app.add_typer(docs.app, name="docs", callback=user_callback)
app.add_typer(info.app, name="info", callback=user_callback)
app.add_typer(job.app, name="job", callback=user_callback)


@app.command()
def version() -> None:
    """
    Show version
    """
    rich.print(f"[blue]DICE CLI Version[/]: [magenta]{__version__}[/]")


@app.command()
def glossary(
    word: Optional[str] = typer.Argument(None, help="Word to search for"),
    print_all: bool = typer.Option(
        False, "--all", "-a", help="Print all glossary entries"
    ),
) -> None:
    """
    Show the meaning of a given word (in DICE context)
    """
    from dice_lib import GLOSSARY

    if print_all:
        from prettytable import PrettyTable

        x = PrettyTable()
        x.field_names = ["Word", "Meaning"]
        for word, meaning in GLOSSARY.items():
            x.add_row([word, meaning])
        x.align = "l"
        rich.print(x)
        return

    if word not in GLOSSARY:
        rich.print(f"[red]Word {word!r} not found[/]")
        typer.echo("To list all glossary items use 'dice glossary -a'")
        return

    rich.print(f"[blue]{word}[/]: [magenta]{GLOSSARY[word]}[/]")


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


@app.command()
def contribute() -> None:
    """
    Contribute to DICE
    """
    rich.print("[blue]Contribute[/]:")
    rich.print("[blue]  DICE CLI[/]: [red]https://github.com/uobdic/dice-cli[/]")
    rich.print("[blue]  DICE LIB[/]: [red]https://github.com/uobdic/dice-lib[/]")
    rich.print("[blue]  DICE WIKI[/]: [red]https://wikis.bris.ac.uk/display/dic[/]")


def __create_dir(path: str) -> None:
    """Create a directory if it does not exist"""
    if os.path.exists(path):
        user_logger.warning(f"Directory {path!r} already exists - skipping")
        return
    user_logger.info(f"Creating directory {path!r}")
    try:
        os.makedirs(path)
    except Exception as e:
        user_logger.error(f"Unable to create directory {path!r}: {e}")
        raise typer.Exit(1) from e


@app.command()
def setmeup() -> None:
    """
    Command to set you up across all DICE systems
    """
    from dice_lib.user import current_user

    # create /storage/<username> directory
    # create /scratch/<username> directory
    # create /shared/<username> directory
    # create /software/<username> directory
    # check if hdfs://<username> exists --> if not, print instructions to create it
    username = current_user()
    local_paths = ["/storage", "/scratch", "/shared", "/software"]
    dirs_to_create = [
        os.path.join(path, username) for path in local_paths if os.path.exists(path)
    ]
    user_logger.info("Will create the following directories:")
    for path in dirs_to_create:
        user_logger.info(f"  {path}")
    user_logger.info(
        "For more information on the paths, please check the wiki for the current node you are on."
    )

    typer.confirm("Do you want to continue?", abort=True)

    for path in local_paths:
        if os.path.exists(path):
            __create_dir(f"{path}/{username}")


def main() -> Any:
    return app()
