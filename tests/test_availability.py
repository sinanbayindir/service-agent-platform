from datetime import date, time

from app.tools.availability import AvailabilityRequest, check_availability


def test_availability_for_valid_booking_request():
    request = AvailabilityRequest(
        booking_date=date(2026, 7, 3),
        booking_time=time(19, 30),
        guests=4,
    )

    result = check_availability(request)

    assert result.available is True
    assert result.suggested_table == "T3"


def test_availability_rejects_closed_day():
    request = AvailabilityRequest(
        booking_date=date(2026, 7, 6),
        booking_time=time(19, 30),
        guests=2,
    )

    result = check_availability(request)

    assert result.available is False
    assert "closed" in result.reason.lower()


def test_availability_rejects_large_groups():
    request = AvailabilityRequest(
        booking_date=date(2026, 7, 3),
        booking_time=time(19, 30),
        guests=7,
    )

    result = check_availability(request)

    assert result.available is False
    assert "manual confirmation" in result.reason.lower()
