from fastapi import FastAPI
from pydantic import BaseModel

from app.rag.generator import answer_question


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
    answer = answer_question(request.message)
    return ChatResponse(answer=answer)
