from app.session.models import Session
from app.session.store import JsonSessionStore


class SessionManager:
    def __init__(self, store: JsonSessionStore | None = None) -> None:
        self.store = store or JsonSessionStore()

    def get_or_create(self, session_id: str | None = None) -> Session:
        if session_id:
            existing_session = self.store.get(session_id)

            if existing_session:
                return existing_session

        session = Session()
        self.store.save(session)

        return session

    def save(self, session: Session) -> None:
        self.store.save(session)
