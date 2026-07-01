from datetime import date, time
from typing import Any

from app.tools.availability import AvailabilityRequest, check_availability
from app.tools.booking import BookingRequest, create_booking
from app.tools.search import search_restaurant_information


def _parse_date(value: str) -> date:
    return date.fromisoformat(value)


def _parse_time(value: str) -> time:
    return time.fromisoformat(value)


def _search_restaurant_information(arguments: dict[str, Any]) -> Any:
    return search_restaurant_information(query=arguments["query"])


def _check_availability(arguments: dict[str, Any]) -> Any:
    request = AvailabilityRequest(
        booking_date=_parse_date(arguments["booking_date"]),
        booking_time=_parse_time(arguments["booking_time"]),
        guests=arguments["guests"],
    )

    return check_availability(request)


def _create_booking(arguments: dict[str, Any]) -> Any:
    request = BookingRequest(
        customer_name=arguments["customer_name"],
        contact_number=arguments["contact_number"],
        booking_date=_parse_date(arguments["booking_date"]),
        booking_time=_parse_time(arguments["booking_time"]),
        guests=arguments["guests"],
    )

    return create_booking(request)


TOOL_HANDLERS = {
    "search_restaurant_information": _search_restaurant_information,
    "check_availability": _check_availability,
    "create_booking": _create_booking,
}


def dispatch_tool(tool_name: str, arguments: dict[str, Any]) -> dict[str, Any] | list[dict]:
    if tool_name not in TOOL_HANDLERS:
        raise ValueError(f"Unknown tool: {tool_name}")

    result = TOOL_HANDLERS[tool_name](arguments)

    if hasattr(result, "model_dump"):
        return result.model_dump()

    return result
