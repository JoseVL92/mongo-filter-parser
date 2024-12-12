import json
import re
from datetime import datetime
from typing import Any, Dict, Pattern, Union

from .exceptions import ValueParsingError


def _date_parse(date: str) -> Union[datetime, str]:
    try:
        return datetime.fromisoformat(date)
    except (ValueError, TypeError):
        return date


REGEX_PARSER: Dict[Union[str, Pattern[str]], Any] = {
        # Match floats even with scientific notation. Eg: 12.34, -12.34, .34, 12e4, -12.34E5, 0.12
        re.compile(r"^[-+]?(?=.*\.\d|\d[eE])\d*\.?\d+([eE][-+]?\d+)?$"): float,

        # Match ints. Eg: 8, -8
        re.compile(r"^[-+]?\d+$"): int,

        # Match string dates formatted as ISO 8601 convention. Eg:
        # 2023-01-15 14:30:00.123456+02:00
        # 2023-01-15T14:30:00Z
        # 2023-01-15
        re.compile(
            r"^([12]\d{3})-(0[1-9]|1[0-2])-(0[1-9]|[12]\d|3[01])"  # Date: YYYY-MM-DD
            r"([T ]"  # Separator: T or space (optional for datetime)
            r"([01]\d|2[0-3]):([0-5]\d):([0-5]\d(\.\d{1,6})?)"  # Time: HH:MM:SS(.microseconds)
            r"(Z|[+-][01]\d:[0-5]\d)?)?$"  # Timezone: Z or ±hh:mm (optional for datetime)
        ): _date_parse,

        # Match JSON-compliant list-formatted strings. Eg: ["hola", "mundo", 4]
        re.compile(r"^\[.*\]$"): lambda list_value: json.loads(list_value),

        # Match boolean and nulls values
        "true": lambda boolean: True,
        "false": lambda boolean: False,
        "null": lambda null: None,
        "none": lambda none: None,
}


def parse_value(value: str) -> Any:
    try:
        for regex, cast in REGEX_PARSER.items():
            if isinstance(regex, Pattern):
                if regex.match(value):
                    return cast(value)
            else:
                if regex == value.lower():
                    return cast(value)
        return value
    except (ValueError, json.JSONDecodeError) as e:
        raise ValueParsingError(f"Failed to parse value '{value}': {str(e)}")
