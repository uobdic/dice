from __future__ import annotations

from ._base import FileSystem


class XrootDFileSystem(FileSystem):
    """Class for XRootD filesystems."""

    _protocol: str = "root://"
