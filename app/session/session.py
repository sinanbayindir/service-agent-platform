import json
from pathlib import Path

from app.session.models import Session


SESSIONS_DIR = Path("data/sessions")


class JsonSessionStore:
    def __init__(self, base_dir: Path = SESSIONS_DIR) -> None:
        self.base_dir = base_dir
        self.base_dir.mkdir(parents=True, exist_ok=True)

    def _path(self, session_id: str) -> Path:
        return self.base_dir / f"{session_id}.json"

    def get(self, session_id: str) -> Session | None:
        path = self._path(session_id)

        if not path.exists():
            return None

        data = json.loads(path.read_text(encoding="utf-8"))
        return Session.model_validate(data)

    def save(self, session: Session) -> None:
        path = self._path(session.session_id)
        path.write_text(
            json.dumps(session.model_dump(), indent=2, ensure_ascii=False),
            encoding="utf-8",
        )
