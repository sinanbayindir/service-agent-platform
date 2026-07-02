import json
from datetime import UTC, datetime
from pathlib import Path
from typing import Any


LOGS_PATH = Path("data/logs/chat_logs.jsonl")


def log_chat_interaction(
    *,
    session_id: str,
    user_message: str,
    assistant_answer: str,
    latency_ms: float,
) -> None:
    LOGS_PATH.parent.mkdir(parents=True, exist_ok=True)

    record: dict[str, Any] = {
        "session_id": session_id,
        "user_message": user_message,
        "assistant_answer": assistant_answer,
        "latency_ms": latency_ms,
        "created_at": datetime.now(UTC).isoformat(),
    }

    with LOGS_PATH.open("a", encoding="utf-8") as file:
        file.write(json.dumps(record, ensure_ascii=False) + "\n")
