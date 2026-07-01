from app.session.manager import SessionManager
from app.session.store import JsonSessionStore


def test_session_manager_creates_session(tmp_path):
    store = JsonSessionStore(base_dir=tmp_path)
    manager = SessionManager(store=store)

    session = manager.get_or_create()

    assert session.session_id
    assert session.state == "idle"
    assert session.slots == {}


def test_session_manager_persists_session(tmp_path):
    store = JsonSessionStore(base_dir=tmp_path)
    manager = SessionManager(store=store)

    session = manager.get_or_create()
    session.add_message("user", "Book a table for 4.")
    session.update_slots({"guests": 4})
    session.set_state("booking_started")

    manager.save(session)

    loaded_session = manager.get_or_create(session.session_id)

    assert loaded_session.session_id == session.session_id
    assert loaded_session.state == "booking_started"
    assert loaded_session.slots["guests"] == 4
    assert loaded_session.history[0].content == "Book a table for 4."
