from __future__ import annotations

import importlib.metadata

import dice_api as m


def test_version():
    assert importlib.metadata.version("dice_api") == m.__version__
