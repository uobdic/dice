from typing import Dict, List

import typer
from dice_lib import load_config

from ..logger import user_logger

dice_params = load_config()
app = typer.Typer(help="DICE info commands")


def _print_storage_element_info(
    storage_elemet: str, se_endpoints: Dict[str, str], se_mount_point: str
) -> None:
    user_logger.info(f"Storage element: {storage_elemet}")
    user_logger.info("SE endpoints:")
    for protocol, endpoint in se_endpoints.items():
        user_logger.info(f"  Protocol {protocol}: {endpoint}")
    user_logger.info(f"SE mount point: {dice_params.HDFS_FUSE_MOUNT + se_mount_point}")


def _print_fts_info(fts_servers: List[str]) -> None:
    user_logger.info("FTS servers (for submitting transfers between storage elements):")
    user_logger.info("------------------------------------------------------")
    for server in fts_servers:
        user_logger.info(f"  {server}")
    user_logger.info("------------------------------------------------------")


@app.command()
def grid_storage() -> None:
    """
    Display information about the grid storage
    """
    user_logger.info("=============================")
    user_logger.info("DICE Grid Storage information")
    user_logger.info("=============================")
    user_logger.info("")
    user_logger.info("Storage elements:")
    user_logger.info("-----------------")
    _print_storage_element_info(
        dice_params.STORAGE_ELEMENT,
        dice_params.SE_ENDPOINTS,
        dice_params.SE_MOUNT_POINT,
    )
    user_logger.info("")
    user_logger.warning("[red]To be soon replaced by:[/]")
    user_logger.info("")
    _print_storage_element_info(
        dice_params.STORAGE_ELEMENT_2,
        dice_params.SE_ENDPOINTS_2,
        dice_params.SE_MOUNT_POINT_2,
    )
    user_logger.info("-----------------")
    user_logger.info("for migration scripts please check 'dice migrate grid-storage'")
    user_logger.info("")
    _print_fts_info(dice_params.FTS_SERVERS)
