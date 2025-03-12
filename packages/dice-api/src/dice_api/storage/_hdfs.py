from __future__ import annotations

import json
from dataclasses import dataclass
from functools import cache

from dice_lib.fs import HDFS
from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse, PlainTextResponse
from xrdsum.backends import FILE_SYSTEMS
from xrdsum.checksums import AVAILABLE_CHECKSUM_TYPES, Checksum
from xrdsum.storage_catalog import resolve_file_path


@dataclass
class HDFSSettings:
    storage_catalog: str = (
        "cms|/cvmfs/cms.cern.ch/SITECONF/T2_UK_SGrid_Bristol/PhEDEx/storage.xml"
    )
    checksum_read_size: int = 128 * 1024 * 1024  # MB
    store_checksum: bool = True
    checksum_file_system: str = "HDFS"


router = APIRouter(
    prefix="/storage/hdfs",
    tags=["storage", "hdfs"],
    responses={404: {"description": "Not found"}},
)


@cache
def get_hdfs_client() -> HDFS:
    return HDFS()


@router.get("/")
async def root() -> dict[str, str]:
    return {"message": "You are in the HDFS APIs!"}


@router.get("/list")
async def list(path: str = "/") -> JSONResponse:
    client = get_hdfs_client()
    list_dir = json.loads(client.ls(path).json())
    return JSONResponse(content=list_dir)


@router.get("/checksum/{checksum_type}")
def checksum(path: str, checksum_type: str) -> PlainTextResponse:
    read_size = HDFSSettings.checksum_read_size
    file_path = resolve_file_path(path, storage_catalog=HDFSSettings.storage_catalog)
    file_system = HDFSSettings.checksum_file_system
    try:
        fs_handle = FILE_SYSTEMS[file_system](file_path, read_size)
    except KeyError as e:
        raise HTTPException(
            status_code=404, detail=f"Unknown file system {file_system}"
        ) from e

    try:
        checksum: Checksum = AVAILABLE_CHECKSUM_TYPES[checksum_type]()
    except KeyError as e:
        raise HTTPException(
            status_code=404, detail=f"Unknown checksum type {checksum_type}"
        ) from e
    checksum = fs_handle.get_checksum(checksum)
    if HDFSSettings.store_checksum:
        fs_handle.store_checksum(checksum)

    return PlainTextResponse(checksum.value)
