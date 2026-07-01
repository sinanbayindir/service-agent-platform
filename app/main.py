from fastapi import FastAPI
from pydantic import BaseModel

from app.agent.agent import run_agent
from app.session.extractor import extract_slots
from app.session.manager import SessionManager


app = FastAPI(
    title="Service Agent Platform",
    version="0.1.0",
)

session_manager = SessionManager()


class ChatRequest(BaseModel):
    message: str
    session_id: str | None = None


class ChatResponse(BaseModel):
    answer: str
    session_id: str


@app.get("/health")
def health_check() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest) -> ChatResponse:
    session = session_manager.get_or_create(request.session_id)

    session.add_message("user", request.message)
    session.update_slots(extract_slots(request.message))

    answer = run_agent(session.history)

    session.add_message("assistant", answer)
    session_manager.save(session)

    return ChatResponse(
        answer=answer,
        session_id=session.session_id,
    )
