from __future__ import annotations

from abc import ABC, abstractmethod
from datetime import datetime
from typing import Any

import pandas as pd
from pydantic import BaseModel


class LsFormat(BaseModel):
    """A standard format for the output of the list function for different filesystems."""

    permissions: list[str]
    owner: list[str]
    group: list[str]
    size: list[int]
    size_scaled: list[float]
    size_unit: list[str]
    date: list[datetime]
    name: list[str]

    def to_pandas(self) -> pd.DataFrame:
        """Converts the LsFormat to a pandas DataFrame."""
        return pd.DataFrame(
            {
                "permissions": self.permissions,
                "owner": self.owner,
                "group": self.group,
                "size": self.size,
                "size_scaled": self.size_scaled,
                "size_unit": self.size_unit,
                "date": self.date,
                "name": self.name,
            }
        )

    def __repr__(self) -> str:
        return str(self.to_pandas().__repr__())

    def to_list(self) -> Any:
        """Converts the LsFormat to a list."""
        return self.to_pandas().to_numpy().tolist()


class FileSystem(ABC):
    """Abstract class for filesystems."""

    _protocol: str = "file://"

    @abstractmethod
    def __init__(self) -> None:
        ...

    @abstractmethod
    def size_of_path(self, path: str) -> tuple[str, int, float, str]:
        """
        Returns a tuple of (path, size_in_bytes, size_in_largest_unit, largest_unit) for a given path.
        Largest unit is the largest unit where size is smaller than the scale of the next one.
        Scale for sizes is 1024.
        """

    @abstractmethod
    def size_of_paths(self, paths: list[str]) -> list[tuple[str, int, float, str]]:
        """Returns a list of tuples of (path, size_in_bytes, size_in_largest_unit, largest_unit) for a given list of paths."""

    @abstractmethod
    def get_owner(self, pathstr: str) -> str:
        """Returns the owner of a given path."""

    @abstractmethod
    def ls(self, path: str) -> LsFormat:
        """Returns a list of files in the given path."""

    @abstractmethod
    def mkdir(self, path: str) -> None:
        """Creates a directory at the given path."""

    @abstractmethod
    def rm(self, path: str) -> None:
        """Removes the file at the given path."""

    @abstractmethod
    def rm_recursive(self, path: str) -> None:
        """Removes the directory at the given path and all its contents."""

    @abstractmethod
    def copy(self, src: str, dest: str) -> None:
        """Copies the file at the given source path to the given destination path."""

    @abstractmethod
    def copy_recursive(self, src: str, dest: str) -> None:
        """Copies the directory at the given source path to the given destination path recursively."""

    @abstractmethod
    def move(self, src: str, dest: str) -> None:
        """Moves the file at the given source path to the given destination path."""
