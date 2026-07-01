from datetime import date, time
from pydantic import BaseModel


class AvailabilityRequest(BaseModel):
    booking_date: date
    booking_time: time
    guests: int


class AvailabilityResult(BaseModel):
    available: bool
    reason: str
    suggested_table: str | None = None


TABLES = [
    {"table_id": "T1", "capacity": 2},
    {"table_id": "T2", "capacity": 2},
    {"table_id": "T3", "capacity": 4},
    {"table_id": "T4", "capacity": 4},
    {"table_id": "T5", "capacity": 6},
]


OPENING_HOURS = {
    0: None,
    1: ("17:00", "22:00"),
    2: ("17:00", "22:00"),
    3: ("17:00", "22:00"),
    4: ("17:00", "23:00"),
    5: ("12:00", "23:00"),
    6: ("12:00", "21:00"),
}


def check_availability(request: AvailabilityRequest) -> AvailabilityResult:
    opening_hours = OPENING_HOURS.get(request.booking_date.weekday())

    if opening_hours is None:
        return AvailabilityResult(
            available=False,
            reason="The restaurant is closed on this day.",
        )

    opens_at, closes_at = opening_hours
    requested_time = request.booking_time.strftime("%H:%M")

    if requested_time < opens_at or requested_time >= closes_at:
        return AvailabilityResult(
            available=False,
            reason=f"The requested time is outside opening hours ({opens_at}-{closes_at}).",
        )

    if request.guests >= 7:
        return AvailabilityResult(
            available=False,
            reason="Large groups of 7 or more guests require manual confirmation.",
        )

    suitable_tables = [
        table for table in TABLES if table["capacity"] >= request.guests
    ]

    if not suitable_tables:
        return AvailabilityResult(
            available=False,
            reason="No suitable table is available for this party size.",
        )

    table = sorted(suitable_tables, key=lambda item: item["capacity"])[0]

    return AvailabilityResult(
        available=True,
        reason="A suitable table is available.",
        suggested_table=table["table_id"],
    )
