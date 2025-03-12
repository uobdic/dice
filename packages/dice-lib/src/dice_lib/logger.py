from __future__ import annotations

import logging

from fasthep_logging import get_logger

APP_LOGGER_NAME = "DICE::LIB"

log = get_logger(APP_LOGGER_NAME)
log.debug("Logging initialised")
log.setLevel(logging.INFO)
