from app.agent.dispatcher import dispatch_tool


def test_dispatcher_searches_restaurant_information():
    result = dispatch_tool(
        "search_restaurant_information",
        {"query": "Do you have vegan options?"},
    )

    assert isinstance(result, list)
    assert len(result) > 0
    assert result[0]["section"] == "Menu Highlights"


def test_dispatcher_checks_availability():
    result = dispatch_tool(
        "check_availability",
        {
            "booking_date": "2026-07-03",
            "booking_time": "19:30",
            "guests": 4,
        },
    )

    assert isinstance(result, dict)
    assert result["available"] is True
    assert result["suggested_table"] == "T3"


def test_dispatcher_rejects_unknown_tool():
    try:
        dispatch_tool("unknown_tool", {})
    except ValueError as exc:
        assert "Unknown tool" in str(exc)
    else:
        raise AssertionError("Expected ValueError")
