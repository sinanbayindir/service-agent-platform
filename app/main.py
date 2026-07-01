from fastapi import FastAPI
from pydantic import BaseModel

from app.agent.agent import run_agent


app = FastAPI(
    title="Service Agent Platform",
    version="0.1.0",
)


class ChatRequest(BaseModel):
    message: str


class ChatResponse(BaseModel):
    answer: str


@app.get("/health")
def health_check() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest) -> ChatResponse:
    answer = run_agent(request.message)
    return ChatResponse(answer=answer)
