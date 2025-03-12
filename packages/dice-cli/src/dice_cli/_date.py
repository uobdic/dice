import datetime
from enum import Enum
from typing import Dict


class DateFormats(str, Enum):
    ISO8601 = "%Y%m%dT%H%M%S.%fZ"
    ISO8601_WITH_TZ = "%Y%m%dT%H%M%S.%fZ"
    ISO8601_WITH_TZ_NO_MS = "%Y%m%dT%H%M%SZ"
    ISO8601_JUST_Y_M_D = "%Y%m%d"
    ISO8601_JUST_Y_M_D_WITH_DOTS = "%Y.%m.%d"
    STARDATE = "NOT IMPLEMENTED YET"


class DateOptions(str, Enum):
    ISO8601 = "iso8601"
    ISO8601_WITH_TZ = "iso8601_with_tz"
    ISO8601_WITH_TZ_NO_MS = "iso8601_with_tz_no_ms"
    ISO8601_JUST_Y_M_D = "iso8601_just_y_m_d"
    ISO8601_JUST_Y_M_D_WITH_DOTS = "iso8601_just_y_m_d_with_dots"
    STARDATE = "stardate"


OPTION_TO_FORMAT: Dict[DateOptions, DateFormats] = {
    DateOptions.ISO8601: DateFormats.ISO8601,
    DateOptions.ISO8601_WITH_TZ: DateFormats.ISO8601_WITH_TZ,
    DateOptions.ISO8601_WITH_TZ_NO_MS: DateFormats.ISO8601_WITH_TZ_NO_MS,
    DateOptions.ISO8601_JUST_Y_M_D: DateFormats.ISO8601_JUST_Y_M_D,
    DateOptions.ISO8601_JUST_Y_M_D_WITH_DOTS: DateFormats.ISO8601_JUST_Y_M_D_WITH_DOTS,
    DateOptions.STARDATE: DateFormats.STARDATE,
}


def formatted_date(
    date_format_option: DateOptions = DateOptions.ISO8601_JUST_Y_M_D,
) -> str:
    try:
        date_format = OPTION_TO_FORMAT[date_format_option]
    except KeyError:
        msg = f"Invalid date format option {date_format_option!r}"
        msg += f"\nValid options are: {', '.join(OPTION_TO_FORMAT.keys())}"
        raise ValueError(msg) from None
    return datetime.datetime.utcnow().strftime(date_format.value)
