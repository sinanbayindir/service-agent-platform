# Service Agent Platform

A production-minded AI service agent built by applying the concepts learned in LLM Zoomcamp: RAG, hybrid retrieval, tool calling, evaluation, and basic monitoring.

## Capstone MVP

The first vertical is a restaurant reservation assistant.

It can:

- answer restaurant questions from a knowledge base
- retrieve information with hybrid search
- check table availability
- create bookings
- keep session-based conversation history
- log chat interactions
- run a basic evaluation suite

## Architecture

```text
FastAPI
  ↓
Session Engine
  ↓
Agent Loop
  ↓
Tool Registry + Dispatcher
  ↓
Tools
  ├── Restaurant Search
  ├── Availability Check
  └── Booking Creation
  ↓
Business Logic / Knowledge Base
```

## LLM Zoomcamp Concepts Used

| Module | Project Implementation |
|---|---|
| Module 1 — RAG | Restaurant knowledge base and grounded answers |
| Module 2 — Vector Search | Keyword search, vector search, and hybrid retrieval with RRF |
| Module 3 — Orchestration | Custom agent loop with tool calling |
| Module 4 — Evaluation | Basic retrieval and business logic evaluation |
| Module 5 — Monitoring | JSONL chat logs with latency tracking |

## Project Structure

```text
app/
  agent/        Agent loop, tool registry, dispatcher, prompts
  rag/          Loader, embedder, keyword/vector/hybrid search
  session/      Session history, slots, JSON session store
  tools/        Deterministic business logic tools
  monitoring/   Chat interaction logging
  main.py       FastAPI entrypoint

data/
  restaurant/   Restaurant knowledge base

evaluations/    Evaluation test cases and runner
scripts/        Utility scripts
tests/          Automated tests
```

## Setup

```bash
uv sync
```

Create `.env`:

```text
OPENAI_API_KEY=your_api_key_here
```

Download the local ONNX embedding model:

```bash
uv run python scripts/download_embedder.py
```

## Run the API

```bash
uv run uvicorn app.main:app --reload
```

Health check:

```bash
curl http://127.0.0.1:8000/health
```

## Example Usage

Ask a knowledge-base question:

```bash
curl -X POST http://127.0.0.1:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Do you have vegan options?"}'
```

Check availability:

```bash
curl -X POST http://127.0.0.1:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Do you have a table for 4 people on 2026-07-03 at 19:30?"}'
```

Multi-turn booking:

```bash
curl -X POST http://127.0.0.1:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "I want to book a table for 4 people."}'
```

Then continue with the returned `session_id`:

```bash
curl -X POST http://127.0.0.1:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"session_id": "SESSION_ID_HERE", "message": "2026-07-03 at 19:30. My name is Sinan and my phone number is +41000000000."}'
```

## Run Tests

```bash
uv run pytest
```

Current test coverage includes:

- availability logic
- booking creation
- tool dispatcher
- slot extraction
- search
- session persistence

## Run Evaluation

```bash
uv run python -m evaluations.run_evaluation
```

Example result:

```json
{
  "total": 6,
  "passed": 6,
  "accuracy": 1.0,
  "by_type": {
    "knowledge": {
      "total": 3,
      "passed": 3
    },
    "availability": {
      "total": 3,
      "passed": 3
    }
  }
}
```

## Monitoring

The application logs chat interactions to JSONL during runtime.

Each record includes:

- session ID
- user message
- assistant answer
- latency in milliseconds
- timestamp

Runtime logs are ignored by Git.

## Design Principle

LLM thinks. Python executes.

The LLM decides when to use tools and how to communicate with the user. Deterministic business logic such as availability checks, booking creation, session storage, and retrieval is handled by Python.
