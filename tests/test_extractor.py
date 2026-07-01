from app.session.extractor import extract_slots


def test_extracts_booking_slots_from_full_message():
    slots = extract_slots(
        "Book a table for 4 people on 2026-07-03 at 19:30. My name is Sinan and my phone number is +41 00 000 00 00."
    )

    assert slots["guests"] == 4
    assert slots["booking_date"] == "2026-07-03"
    assert slots["booking_time"] == "19:30"
    assert slots["customer_name"] == "Sinan"
    assert slots["contact_number"] == "+41000000000"


def test_extracts_pm_time():
    slots = extract_slots("I need a table for 2 people at 7:30 pm")

    assert slots["guests"] == 2
    assert slots["booking_time"] == "19:30"


def test_returns_empty_slots_when_no_booking_details_found():
    slots = extract_slots("Do you have vegan options?")

    assert slots == {}
