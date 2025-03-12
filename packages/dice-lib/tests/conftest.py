from __future__ import annotations

import pytest


@pytest.fixture()
def config_path() -> str:
    return "tests/data/config.yaml"
