from __future__ import annotations

from ._base import FileSystem


class S3FileSystem(FileSystem):
    """Class for S3 filesystems."""

    _protocol: str = "s3://"
