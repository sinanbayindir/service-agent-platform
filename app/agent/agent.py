import json
from typing import Any, cast

from dotenv import load_dotenv
from openai import OpenAI

from app.agent.dispatcher import dispatch_tool
from app.agent.prompts import AGENT_SYSTEM_PROMPT
from app.agent.registry import TOOLS
from app.session.models import Message


load_dotenv()
client = OpenAI()


def _build_messages(history: list[Message]) -> list[dict[str, Any]]:
    messages: list[dict[str, Any]] = [
        {
            "role": "system",
            "content": AGENT_SYSTEM_PROMPT,
        }
    ]

    for message in history:
        if message.role in {"user", "assistant"}:
            messages.append(
                {
                    "role": message.role,
                    "content": message.content,
                }
            )

    return messages


def run_agent(history: list[Message]) -> str:
    messages = _build_messages(history)

    while True:
        response = client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=cast(Any, messages),
            tools=cast(Any, TOOLS),
            tool_choice="auto",
        )

        message = response.choices[0].message
        messages.append(message.model_dump())

        if not message.tool_calls:
            return message.content or ""

        for tool_call in message.tool_calls:
            tool_call_data = cast(Any, tool_call)

            tool_name = tool_call_data.function.name
            arguments = json.loads(tool_call_data.function.arguments)

            tool_result = dispatch_tool(tool_name, arguments)

            messages.append(
                {
                    "role": "tool",
                    "tool_call_id": tool_call_data.id,
                    "content": json.dumps(tool_result, ensure_ascii=False),
                }
            )
