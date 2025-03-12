from __future__ import annotations

from ._config import load_config
from ._version import version as __version__
from .glossary import GLOSSARY

__all__ = (
    "__version__",
    "GLOSSARY",
    "load_config",
)
