from datetime import UTC, datetime
from typing import Any
from uuid import uuid4

from pydantic import BaseModel, Field


class Message(BaseModel):
    role: str
    content: str
    created_at: str = Field(default_factory=lambda: datetime.now(UTC).isoformat())


class Session(BaseModel):
    session_id: str = Field(default_factory=lambda: str(uuid4()))
    state: str = "idle"
    slots: dict[str, Any] = Field(default_factory=dict)
    history: list[Message] = Field(default_factory=list)
    created_at: str = Field(default_factory=lambda: datetime.now(UTC).isoformat())
    updated_at: str = Field(default_factory=lambda: datetime.now(UTC).isoformat())

    def add_message(self, role: str, content: str) -> None:
        self.history.append(Message(role=role, content=content))
        self.updated_at = datetime.now(UTC).isoformat()

    def update_slots(self, values: dict[str, Any]) -> None:
        self.slots.update({key: value for key, value in values.items() if value is not None})
        self.updated_at = datetime.now(UTC).isoformat()

    def set_state(self, state: str) -> None:
        self.state = state
        self.updated_at = datetime.now(UTC).isoformat()
