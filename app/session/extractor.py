import re
from datetime import date, timedelta
from typing import Any


GUESTS_PATTERN = re.compile(
    r"\b(?:for\s+)?(\d{1,2})\s+(?:people|persons|guests|pax)\b",
    re.IGNORECASE,
)
PHONE_PATTERN = re.compile(r"(\+?\d[\d\s]{6,}\d)")
DATE_PATTERN = re.compile(r"\b(\d{4}-\d{2}-\d{2})\b")
NAME_PATTERN = re.compile(
    r"\bmy name is\s+([a-zA-Z]+(?:\s+[a-zA-Z]+)?)(?=\.|,| and\b|$)",
    re.IGNORECASE,

)


def _normalize_phone(value: str) -> str:
    return value.replace(" ", "")


def _extract_date(message: str) -> str | None:
    date_match = DATE_PATTERN.search(message)

    if date_match:
        return date_match.group(1)

    lowered = message.lower()
    today = date.today()

    if "today" in lowered:
        return today.isoformat()

    if "tomorrow" in lowered:
        return (today + timedelta(days=1)).isoformat()

    return None


def _extract_time(message: str) -> str | None:
    lowered = message.lower()

    candidates = re.finditer(
        r"\bat\s+(\d{1,2})(?::(\d{2}))?\s*(am|pm)?\b"
        r"|\b(\d{1,2}):(\d{2})\b"
        r"|\b(\d{1,2})\s*(am|pm)\b",
        lowered,
        re.IGNORECASE,
    )

    for match in candidates:
        if match.group(1):
            hour = int(match.group(1))
            minute = int(match.group(2) or "00")
            meridiem = match.group(3)
        elif match.group(4):
            hour = int(match.group(4))
            minute = int(match.group(5))
            meridiem = None
        else:
            hour = int(match.group(6))
            minute = 0
            meridiem = match.group(7)

        if hour > 23 or minute > 59:
            continue

        if meridiem:
            if meridiem.lower() == "pm" and hour != 12:
                hour += 12
            elif meridiem.lower() == "am" and hour == 12:
                hour = 0

        return f"{hour:02d}:{minute:02d}"

    return None


def extract_slots(message: str) -> dict[str, Any]:
    slots: dict[str, Any] = {}

    guests_match = GUESTS_PATTERN.search(message)
    if guests_match:
        slots["guests"] = int(guests_match.group(1))

    phone_match = PHONE_PATTERN.search(message)
    if phone_match:
        slots["contact_number"] = _normalize_phone(phone_match.group(1))

    name_match = NAME_PATTERN.search(message)
    if name_match:
        slots["customer_name"] = name_match.group(1).strip()

    extracted_date = _extract_date(message)
    if extracted_date:
        slots["booking_date"] = extracted_date

    extracted_time = _extract_time(message)
    if extracted_time:
        slots["booking_time"] = extracted_time

    return slots
