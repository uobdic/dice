from __future__ import annotations

import importlib.metadata

import dice_api as da
import dice_cli as dc
import dice_lib as dl


def test_dice_api_version() -> None:
    assert da.__version__
    assert importlib.metadata.version("dice_api") == da.__version__


def test_dice_cli_version() -> None:
    assert dc.__version__
    assert importlib.metadata.version("dice_cli") == dc.__version__


def test_dice_lib_version() -> None:
    assert dl.__version__
    assert importlib.metadata.version("dice_lib") == dl.__version__
