from __future__ import annotations

import datetime

DEFAULT_DATE_FORMAT = "%Y-%m-%d"
DEFAULT_TIME_FORMAT = "%H:%M:%S"


def current_formatted_date(date_format: str = DEFAULT_DATE_FORMAT) -> str:
    """Returns big-endian string of the current date"""

    return datetime.datetime.now().strftime(date_format)
