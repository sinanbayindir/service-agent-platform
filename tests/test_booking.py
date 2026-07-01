from datetime import date, time

from app.tools.booking import BookingRequest, create_booking


def test_create_booking_successfully(tmp_path, monkeypatch):
    bookings_path = tmp_path / "bookings.json"

    monkeypatch.setattr("app.tools.booking.BOOKINGS_PATH", bookings_path)

    request = BookingRequest(
        customer_name="Test Guest",
        contact_number="+41000000000",
        booking_date=date(2026, 7, 3),
        booking_time=time(19, 30),
        guests=4,
    )

    result = create_booking(request)

    assert result.success is True
    assert result.booking_id is not None
    assert result.table_id == "T3"
    assert bookings_path.exists()


def test_create_booking_rejects_closed_day(tmp_path, monkeypatch):
    bookings_path = tmp_path / "bookings.json"

    monkeypatch.setattr("app.tools.booking.BOOKINGS_PATH", bookings_path)

    request = BookingRequest(
        customer_name="Test Guest",
        contact_number="+41000000000",
        booking_date=date(2026, 7, 6),
        booking_time=time(19, 30),
        guests=2,
    )

    result = create_booking(request)

    assert result.success is False
    assert "closed" in result.message.lower()
    assert not bookings_path.exists()
