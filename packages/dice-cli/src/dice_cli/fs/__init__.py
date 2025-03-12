from typing import Any

import typer
from dice_lib import load_config

from ..logger import user_logger

app = typer.Typer(help="DICE filesystem commands")


def _prepare_paths(paths: list[str], config: dict[str, Any]) -> list[str]:
    """
    1. Remove trailing slashes from paths
    2. lookup file system mounts
    3. Replace protocols (e.g. /hdfs/<path> --> hdfs://<path>)
    4. If no protocol is specified, assume local filesystem
    """
    if config:
        pass
    return [path.rstrip("/") for path in paths]


@app.command()
def copy_from_local(
    src: str = typer.Argument(..., help="Source path"),
    dst: str = typer.Argument(..., help="Destination path"),
) -> None:
    """
    Copy a file from local to DICE.

    Parameters
    ----------
    src : str
        Source path.
    dst : str
        Destination path.
    """
    config = load_config()
    src, dst = _prepare_paths([src, dst], config)
    user_logger.info(f"Copying file from local to DICE: {src} -> {dst}")
    user_logger.warning("Not implemented yet")
