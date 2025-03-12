from __future__ import annotations

from ._base import FileSystem


class GridFTPFileSystem(FileSystem):
    """Class for GridFTP filesystems."""

    _protocol: str = "gsiftp://"
