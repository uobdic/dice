from itertools import groupby
from pathlib import Path
from typing import List

from .._io import read_ints_from_csv
from ..logger import admin_logger


def _read_userids(filename: str) -> List[int]:
    return read_ints_from_csv(Path(filename), "uid")


def _read_groupids(filename: str) -> List[int]:
    return read_ints_from_csv(Path(filename), "gid")


def main(users_file: str, group_file: str) -> None:
    """
    Prints the unused ID ranges for all groups and users.
    """
    from dice_lib.ranges import as_range, groupby_inverse_range

    userids = _read_userids(users_file)
    groupids = _read_groupids(group_file)

    unused_uids = sorted({i for i in range(max(userids))} - set(userids))
    unused_uids_ranges = ",".join(
        as_range(g) for _, g in groupby(unused_uids, key=groupby_inverse_range)
    )

    unused_gids = sorted({i for i in range(max(groupids))} - set(groupids))
    unused_gids_ranges = ",".join(
        as_range(g) for _, g in groupby(unused_gids, key=groupby_inverse_range)
    )

    admin_logger.debug(f"Used UIDs: {userids}")
    admin_logger.info(f"Unused UID ranges: {unused_uids_ranges}")

    admin_logger.debug(f"Used GIDs: {groupids}")
    admin_logger.info(f"Unused GID ranges: {unused_gids_ranges}")
