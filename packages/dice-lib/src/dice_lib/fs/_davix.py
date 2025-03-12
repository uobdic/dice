from __future__ import annotations

from ._base import FileSystem


class DavixFileSystem(FileSystem):
    """Class for Davix filesystems."""

    _protocol: str = "davs://"
