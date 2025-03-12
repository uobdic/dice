from __future__ import annotations

from pathlib import Path

from omegaconf import OmegaConf

import dice_lib._config as config

FOUND_CFG = Path(config.DEFAULT_DICE_CONFIG_PATH).exists()


def test_server_status() -> None:
    assert config.ServerStatus.ACTIVE.value == "active"
    assert config.ServerStatus.RETIRED.value == "retired"
    assert config.ServerStatus.COMMISSIONING.value == "commissioning"
    assert config.ServerStatus.DECOMMISSIONING.value == "decommissioning"
    assert config.ServerStatus.OFFLINE.value == "offline"
    assert config.ServerStatus.ONLINE.value == "online"


def test_computing_element() -> None:
    cfg = OmegaConf.create(
        {
            "status": "active",
            "type": "ce",
        }
    )
    schema = OmegaConf.structured(config.ComputingElement)
    merged_cfg = OmegaConf.merge(schema, cfg)

    assert merged_cfg.status == "active"
    assert merged_cfg.type == "ce"


def test_storage_element() -> None:
    cfg = OmegaConf.create(
        {
            "status": "active",
            "type": "se",
            "endpoints": {
                "gsiftp": "gsiftp://lcgse01.phy.bris.ac.uk:2811",
                "xrootd": "root://lcgse01.phy.bris.ac.uk/",
            },
            "root_dir": "/dpm/phy.bris.ac.uk/home",
        }
    )
    schema = OmegaConf.structured(config.StorageElement)
    merged_cfg = OmegaConf.merge(schema, cfg)

    assert merged_cfg.status == "active"
    assert merged_cfg.type == "se"
    assert merged_cfg.endpoints == {
        "gsiftp": "gsiftp://lcgse01.phy.bris.ac.uk:2811",
        "xrootd": "root://lcgse01.phy.bris.ac.uk/",
    }
    assert merged_cfg.root_dir == "/dpm/phy.bris.ac.uk/home"


def test_computing_grid() -> None:
    cfg = OmegaConf.create(
        {
            "site_name": "TEST",
            "cms_site_name": "TEST",
            "computing_elements": [
                {
                    "name": "ce001",
                    "status": "active",
                    "type": "ce",
                },
                {
                    "name": "ce002",
                    "status": "retired",
                    "type": "ce",
                },
            ],
            "storage_elements": [
                {
                    "name": "se001",
                    "status": "active",
                    "type": "se",
                    "endpoints": {
                        "gsiftp": "gsiftp://lcgse01.phy.bris.ac.uk:2811",
                        "xrootd": "root://lcgse01.phy.bris.ac.uk/",
                    },
                    "root_dir": "/dpm/phy.bris.ac.uk/home",
                },
                {
                    "name": "se002",
                    "status": "retired",
                    "type": "se",
                    "endpoints": {
                        "gsiftp": "gsiftp://lcgse01.phy.bris.ac.uk:2811",
                        "xrootd": "root://lcgse01.phy.bris.ac.uk/",
                    },
                    "root_dir": "/dpm/phy.bris.ac.uk/home",
                },
            ],
            "fts_servers": [
                "fts1.lcg.cscs.ch",
                "fts2.lcg.cscs.ch",
            ],
        }
    )
    schema = OmegaConf.structured(config.ComputingGrid)
    merged_cfg = OmegaConf.merge(schema, cfg)

    assert merged_cfg.site_name == "TEST"
    assert merged_cfg.cms_site_name == "TEST"
    assert merged_cfg.computing_elements[0].status == "active"
    assert merged_cfg.computing_elements[0].type == "ce"
    assert merged_cfg.computing_elements[1].status == "retired"
    assert len(merged_cfg.fts_servers) == 2


def test_storage() -> None:
    cfg = OmegaConf.create(
        {
            "mounts": ["/start/path", "/end/path"],
            "binaries": {"bash": "/bin/bash"},
            "env": {"X509_USER_PROXY": "/tmp/x509_proxy"},
        }
    )
    schema = OmegaConf.structured(config.Storage)
    merged_cfg = OmegaConf.merge(schema, cfg)
    assert merged_cfg.mounts == ["/start/path", "/end/path"]
    assert merged_cfg.binaries == {"bash": "/bin/bash"}
    assert merged_cfg.env == {"X509_USER_PROXY": "/tmp/x509_proxy"}


def test_storage_from_config(config_path: str) -> None:
    cfg = OmegaConf.load(config_path)
    schema = OmegaConf.structured(config.Storage)
    for _, data in cfg.storage.items():
        merged_cfg = OmegaConf.merge(schema, data)
        assert len(merged_cfg.mounts) >= 1


def test_computing_grid_from_config(config_path: str) -> None:
    cfg = OmegaConf.load(config_path)
    schema = OmegaConf.structured(config.ComputingGrid)
    merged_cfg = OmegaConf.merge(schema, cfg.computing_grid)
    assert len(merged_cfg.computing_elements) == 2
    assert len(merged_cfg.storage_elements) == 2
    assert merged_cfg.site_name == "UKI-SOUTHGRID-BRIS-HEP"
    assert merged_cfg.cms_site_name == "T2_UK_SGrid_Bristol"


def test_login_nodes_from_config(config_path: str) -> None:
    cfg = OmegaConf.load(config_path)
    schema = OmegaConf.structured(config.LoginNode)
    assert len(cfg.login_nodes) == 4
    for data in cfg.login_nodes:
        merged_cfg = OmegaConf.merge(schema, data)
        assert merged_cfg.status in [
            config.ServerStatus.ONLINE,
            config.ServerStatus.OFFLINE,
        ]


def test_full_config(config_path: str) -> None:
    cfg = OmegaConf.load(config_path)
    schema = OmegaConf.structured(config.DiceConfig)
    merged_cfg = OmegaConf.merge(schema, cfg)
    assert merged_cfg.computing_grid.site_name == "UKI-SOUTHGRID-BRIS-HEP"
    assert len(merged_cfg.computing_grid.computing_elements) == 2
    assert len(merged_cfg.site_info.supported_vos) == 13
    assert merged_cfg.node_info.owner == "ME"
