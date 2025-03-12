import typer

from ..logger import user_logger

app = typer.Typer(help="DICE documentation reference")


@app.command()
def software_how_to() -> None:
    user_logger.info(
        "See https://wikis.bris.ac.uk/pages/viewpage.action?title=Software&spaceKey=dic"
    )
