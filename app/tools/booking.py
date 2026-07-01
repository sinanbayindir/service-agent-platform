import json
from datetime import UTC, date, datetime, time
from pathlib import Path
from uuid import uuid4

from pydantic import BaseModel

from app.tools.availability import AvailabilityRequest, check_availability

BOOKINGS_PATH = Path("data/restaurant/bookings.json")


class BookingRequest(BaseModel):
    customer_name: str
    contact_number: str
    booking_date: date
    booking_time: time
    guests: int


class BookingResult(BaseModel):
    success: bool
    message: str
    booking_id: str | None = None
    table_id: str | None = None


def _load_bookings() -> list[dict]:
    if not BOOKINGS_PATH.exists():
        return []

    return json.loads(BOOKINGS_PATH.read_text(encoding="utf-8"))


def _save_bookings(bookings: list[dict]) -> None:
    BOOKINGS_PATH.parent.mkdir(parents=True, exist_ok=True)
    BOOKINGS_PATH.write_text(
        json.dumps(bookings, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )


def create_booking(request: BookingRequest) -> BookingResult:
    availability = check_availability(
        AvailabilityRequest(
            booking_date=request.booking_date,
            booking_time=request.booking_time,
            guests=request.guests,
        )
    )

    if not availability.available:
        return BookingResult(
            success=False,
            message=availability.reason,
        )

    booking_id = str(uuid4())

    booking = {
        "booking_id": booking_id,
        "customer_name": request.customer_name,
        "contact_number": request.contact_number,
        "booking_date": request.booking_date.isoformat(),
        "booking_time": request.booking_time.strftime("%H:%M"),
        "guests": request.guests,
        "table_id": availability.suggested_table,
        "created_at": datetime.now(UTC).isoformat(),
    }

    bookings = _load_bookings()
    bookings.append(booking)
    _save_bookings(bookings)

    return BookingResult(
        success=True,
        message="Booking created successfully.",
        booking_id=booking_id,
        table_id=availability.suggested_table,
    )
