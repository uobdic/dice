from __future__ import annotations

from datetime import datetime
from pathlib import Path
from typing import Callable

from plumbum import local
from plumbum.commands.base import BoundCommand

from dice_lib.units import convert_to_largest_unit

from ._base import FileSystem, LsFormat


class PosixFileSystem(FileSystem):
    """Class for filesystems that use the POSIX standard."""

    protocol: str = "file://"

    def __init__(self) -> None:
        # command definitions
        self._size_cmd: BoundCommand = local["nice"]["-n19", "du"]["-s"]
        self._copy_cmd: BoundCommand = local["cp"]["-p"]
        self._copy_recursive_cmd: BoundCommand = local["cp"]["-pr"]
        self._move_cmd: BoundCommand = local["mv"]
        self._ls_cmd: BoundCommand = local["ls"]["-la", "--time-style=long-iso"]
        self._mkdir_cmd: BoundCommand = local["mkdir"]["-p"]
        self._rm_cmd: BoundCommand = local["rm"]["-f"]
        self._rm_recursive_cmd: BoundCommand = local["rm"]["-fr"]
        self._dataparser: Callable[[str], datetime] = lambda x: datetime.strptime(
            x, "%Y-%m-%d %H:%M"
        )

    def _remove_protocol(self, path: str) -> str:
        return path.replace(self.protocol, "")

    def get_owner(self, pathstr: str) -> str:
        pathstr = self._remove_protocol(pathstr)
        path = Path(pathstr)
        try:
            owner = path.owner()
        except KeyError:
            owner = "unknown"
        return owner

    def size_of_path(self, path: str) -> tuple[str, int, float, str]:
        path = self._remove_protocol(path)
        total, _ = self._size_cmd(path).split()
        total = int(total)
        total_scaled, unit = convert_to_largest_unit(total, "B", scale=1024)
        return str(path), total, total_scaled, unit

    def size_of_paths(self, paths: list[str]) -> list[tuple[str, int, float, str]]:
        # TODO: should be able to do this in parallel
        return [self.size_of_path(path) for path in paths]

    def copy(self, src: str, dest: str) -> None:
        src, dest = self._remove_protocol(src), self._remove_protocol(dest)
        self._copy_cmd(src, dest)

    def copy_recursive(self, src: str, dest: str) -> None:
        src, dest = self._remove_protocol(src), self._remove_protocol(dest)
        self._copy_recursive_cmd(src, dest)

    def move(self, src: str, dest: str) -> None:
        src, dest = self._remove_protocol(src), self._remove_protocol(dest)
        self._move_cmd(src, dest)

    def ls(self, path: str) -> LsFormat:
        path = self._remove_protocol(path)
        cmd_output = self._ls_cmd(path)
        # skip first 3 lines (total, ., ..) and last line (empty)
        lines = cmd_output.split("\n")[3:-1]
        permissions = []
        owner = []
        group = []
        size = []
        size_scaled = []
        unit = []
        date = []
        name = []
        for new_line in lines:
            line = new_line.split()
            permissions.append(line[0])
            owner.append(line[2])
            group.append(line[3])
            raw_size = int(line[4])
            size.append(raw_size)
            tmp_size_scaled, tmp_unit = convert_to_largest_unit(
                raw_size, "B", scale=1024
            )
            size_scaled.append(tmp_size_scaled)
            unit.append(tmp_unit)
            date.append(self._dataparser(line[5] + " " + line[6]))
            name.append(line[7])
        return LsFormat(
            permissions=permissions,
            owner=owner,
            group=group,
            size=size,
            size_scaled=size_scaled,
            size_unit=unit,
            date=date,
            name=name,
        )

    def mkdir(self, path: str) -> None:
        path = self._remove_protocol(path)
        self._mkdir_cmd(path)

    def rm(self, path: str) -> None:
        path = self._remove_protocol(path)
        self._rm_cmd(path)

    def rm_recursive(self, path: str) -> None:
        path = self._remove_protocol(path)
        self._rm_recursive_cmd(path)
