from __future__ import annotations

import pathlib

import pytest


@pytest.fixture()
def absolute_path() -> pathlib.Path:
    return pathlib.Path(__file__).resolve().parent


@pytest.fixture()
def config_path(absolute_path: pathlib.Path) -> str:
    return str(absolute_path / "data/config.yaml")
