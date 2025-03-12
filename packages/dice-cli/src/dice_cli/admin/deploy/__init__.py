import typer

from dice_cli.logger import admin_logger

from ._hdfs_mount import get_setup_commands

app = typer.Typer(help="Commands for deployments")


@app.command()
def hdfs_mount(
    host: str = typer.Option(..., "--host", "-h", help="Destination hostname"),
    noop: bool = typer.Option(False, "--noop", "-n", help="Do not execute commands"),
) -> None:
    """
    Mount the HDFS
    """
    commands = get_setup_commands()
    if noop:
        admin_logger.info(">> Would execute:")
        for command in commands:
            admin_logger.info(f"{command}")
        return

    # create download destination
    # download tar
    # extract tar
    # copy config
    # create symlinks
    # create mount point
    # add mount instructions to /etc/fstab
    # mount
