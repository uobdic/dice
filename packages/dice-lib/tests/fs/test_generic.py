from __future__ import annotations

from typing import Any

import pytest

from dice_lib import load_config
from dice_lib.fs import FSClient, get_mount_settings_from_config, prepare_paths


@pytest.mark.parametrize(
    ("mount", "mount_settings"),
    [
        ("/hdfs", {"protocol": "hdfs://", "remove_mount_for_native_access": True}),
        ("/software", {"protocol": "nfs://", "remove_mount_for_native_access": False}),
        ("/storage", {"protocol": "file://", "remove_mount_for_native_access": False}),
    ],
)
def test_get_mount_settings_from_config(
    config_path: str, mount: str, mount_settings: dict[str, Any]
) -> None:
    config = load_config(config_path)
    m_settings = get_mount_settings_from_config(config)
    assert mount in m_settings
    settings = m_settings[mount]
    assert settings["protocol"] == mount_settings["protocol"]
    assert (
        settings["remove_mount_for_native_access"]
        == mount_settings["remove_mount_for_native_access"]
    )


@pytest.mark.parametrize(
    ("path", "expected"),
    [
        ("/hdfs/user/username", "hdfs:///user/username"),
        ("/storage/user/username", "file:///storage/user/username"),
        ("/software/user/username", "nfs:///software/user/username"),
        ("nfs:///software/user/username", "nfs:///software/user/username"),
    ],
)
def test_prepare_paths(config_path: str, path: str, expected: str) -> None:
    config = load_config(config_path)
    mount_settings = get_mount_settings_from_config(config)
    prepared_paths = prepare_paths([path], mount_settings)
    assert prepared_paths[0] == expected


@pytest.mark.parametrize(
    ("path", "expected"),
    [
        ("/tmp", "root"),
    ],
)
def test_get_owner(config_path: str, path: str, expected: str) -> None:
    fs = FSClient(config_path)
    owner = fs.get_owner(path)
    assert owner == expected
