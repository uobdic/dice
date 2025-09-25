from __future__ import annotations

from ._config import load_config
from ._version import version as __version__
from .glossary import GLOSSARY

__all__ = (
    "GLOSSARY",
    "__version__",
    "load_config",
)
