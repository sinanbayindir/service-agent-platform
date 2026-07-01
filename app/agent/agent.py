import json
from typing import Any, cast

from dotenv import load_dotenv
from openai import OpenAI

from app.agent.dispatcher import dispatch_tool
from app.agent.prompts import AGENT_SYSTEM_PROMPT
from app.agent.registry import TOOLS


load_dotenv()
client = OpenAI()


def run_agent(user_message: str) -> str:
    messages: list[dict[str, Any]] = [
        {
            "role": "system",
            "content": AGENT_SYSTEM_PROMPT,
        },
        {
            "role": "user",
            "content": user_message,
        },
    ]

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
