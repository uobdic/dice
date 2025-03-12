from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from typing import Any

from omegaconf import OmegaConf

DEFAULT_DICE_CONFIG_PATH = "/etc/dice/config.yaml"


class ServerStatus(Enum):
    """DICE server status enum"""

    ONLINE = "online"
    OFFLINE = "offline"
    ACTIVE = "active"
    RETIRED = "retired"
    COMMISSIONING = "commissioning"
    DECOMMISSIONING = "decommissioning"


@dataclass
class ComputingElement:
    """DICE computing element config structure"""

    name: str
    status: str
    type: str


@dataclass
class StorageElement:
    """DICE storage element config structure"""

    name: str
    status: str
    type: str
    endpoints: dict[str, str]
    root_dir: str


@dataclass
class ComputingGrid:
    """DICE WLCG config structure"""

    site_name: str
    cms_site_name: str
    computing_elements: list[ComputingElement]
    storage_elements: list[StorageElement]
    fts_servers: list[str]


@dataclass
class Storage:
    """DICE storage config structure. Refers to a storage type, e.g. HDFS, NFS, etc."""

    mounts: list[str]
    binaries: dict[str, str] | None
    env: dict[str, str] | None
    extras: dict[str, Any] | None
    protocol: str | None = "file://"
    remove_mount_for_native_access: bool | None = False


@dataclass
class LoginNode:
    """DICE login node config structure"""

    name: str
    status: ServerStatus
    group: str


@dataclass
class DiceConfig:
    """DICE config file structure"""

    cluster_name: str
    documentation: str
    login_nodes: list[LoginNode]
    computing_grid: ComputingGrid
    storage: dict[str, Storage]
    glossary: dict[str, str]
    site_info: dict[str, Any]
    node_info: dict[str, Any]


def load_config(config_file: str = DEFAULT_DICE_CONFIG_PATH) -> Any:
    """Loads the DICE config file and returns a structured OmegaConf object"""
    path = Path(config_file)
    if not path.exists():
        msg = f"DICE config, {config_file}, does not exist. Please contact dice-admin"
        raise FileNotFoundError(msg)
    schema = OmegaConf.structured(DiceConfig)
    conf = OmegaConf.load(path)
    return OmegaConf.merge(schema, conf)
