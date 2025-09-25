from __future__ import annotations

from pathlib import Path
from typing import Any

from dice_lib.host import current_fqdn

from .._io import write_list_data_as_dict_to_csv
from ..logger import admin_logger


def _read_groups() -> list[dict[str, str]]:
    with Path("/etc/group").open() as f:
        group_lines = f.readlines()
    groups = []
    for line in group_lines:
        tokens = line.split(":")
        groups.append({"name": tokens[0], "gid": tokens[2]})
    return groups


def _read_users() -> list[dict[str, str]]:
    with Path("/etc/passwd").open() as f:
        user_lines = f.readlines()
    users = []
    for line in user_lines:
        tokens = line.split(":")
        users.append({"name": tokens[0], "uid": tokens[2], "gid": tokens[3]})
    return users


def _write_users_to_csv(
    users: list[dict[str, Any]],
    output_file: str = "/tmp/users.csv",
) -> None:
    write_list_data_as_dict_to_csv(users, ["name", "uid", "gid"], Path(output_file))


def _write_groups_to_csv(
    groups: list[dict[str, Any]], output_file: str = "/tmp/groups.csv"
) -> None:
    write_list_data_as_dict_to_csv(groups, ["name", "gid"], Path(output_file))


def main() -> None:
    groups = _read_groups()
    users = _read_users()
    hostname = current_fqdn()

    user_output = f"/tmp/00_{hostname}_users.csv"
    group_output = f"/tmp/01_{hostname}_groups.csv"

    _write_users_to_csv(users, user_output)
    _write_groups_to_csv(groups, group_output)

    admin_logger.info(f"Wrote users to {user_output}")
    admin_logger.info(f"Wrote groups to {group_output}")
