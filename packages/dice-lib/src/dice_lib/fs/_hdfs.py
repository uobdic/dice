from __future__ import annotations

import xml.etree.ElementTree as ET
from collections import defaultdict
from pathlib import Path
from typing import Any

import pyhdfs

from ..logger import log
from ..units import convert_to_largest_unit
from ..user import current_user
from ._base import FileSystem, LsFormat

CONF = "/etc/hadoop/conf/hdfs-site.xml"


def __get_namenodes() -> list[str]:
    """
    Get the list of namenodes from the HDFS configuration file.
    """

    tree = ET.parse(CONF)
    root = tree.getroot()
    namenodes = []

    for prop in root.findall("property"):
        name = prop.find("name")
        if name is None:
            continue
        name_str = str(name.text)

        if name_str.startswith("dfs.namenode.http-address"):
            value = prop.find("value")
            if value is None:
                continue
            namenodes.append(str(value.text))
    return namenodes


def get_hdfs_client(user: str) -> Any:
    """Retrieving the HDFS client to execute operations on HDFS."""
    namenodes = __get_namenodes()
    log.debug("Connecting to HDFS via %s", namenodes)
    return pyhdfs.HdfsClient(namenodes, user_name=user)  # can throw AssertionError


class HDFS(FileSystem):
    """Class for HDFS filesystem."""

    protocol: str = "hdfs://"
    fs: pyhdfs.HdfsClient

    def __init__(
        self,
        user: str | None = None,
    ):
        self.user = current_user() if user is None else user
        self.fs = get_hdfs_client(self.user)

    def size_of_path(self, path: str) -> tuple[str, int, float, str]:
        cs = self.fs.get_content_summary(path)
        total = cs.spaceConsumed
        total_scaled, unit = convert_to_largest_unit(total, "B", scale=1024)
        return str(path), total, total_scaled, unit

    def size_of_paths(self, paths: list[str]) -> list[tuple[str, int, float, str]]:
        return [self.size_of_path(path) for path in paths]

    def get_owner(self, pathstr: str) -> str:
        status: pyhdfs.FileStatus = self.status(pathstr)
        return str(status.owner)

    def ls(self, path: str) -> LsFormat:
        paths = self.fs.listdir(path)
        listing: dict[str, Any] = defaultdict(list)
        for relative_path in paths:
            full_path = str(Path(path) / Path(relative_path))
            status = self.status(full_path)
            listing["permissions"].append(status.permission)
            listing["owner"].append(status.owner)
            listing["group"].append(status.group)
            raw_size = status.length
            listing["size"].append(raw_size)
            tmp_size_scaled, tmp_unit = convert_to_largest_unit(
                raw_size, "B", scale=1024
            )
            listing["size_scaled"].append(tmp_size_scaled)
            listing["size_unit"].append(tmp_unit)
            listing["date"].append(status.modificationTime)
            listing["name"].append(full_path)
        return LsFormat(**listing)

    def status(self, path: str) -> Any:
        """Returns the status of a file or directory."""
        return self.fs.get_file_status(path)

    def mkdir(self, path: str) -> None:
        self.fs.mkdirs(path)

    def rm(self, path: str) -> None:
        log.debug("Removing %s", path)
        self.fs.delete(path)

    def rm_recursive(self, path: str) -> None:
        log.debug("Removing %s", path)
        self.fs.delete(path, recursive=True)

    def copy(self, src: str, dest: str) -> None:
        pass

    def copy_recursive(self, src: str, dest: str) -> None:
        pass

    def move(self, src: str, dest: str) -> None:
        pass
