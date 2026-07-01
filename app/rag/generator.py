from dotenv import load_dotenv
from openai import OpenAI

from app.rag.search import search_knowledge_base


load_dotenv()
client = OpenAI()


def build_context(search_results: list[dict]) -> str:
    context_parts = []

    for result in search_results:
        context_parts.append(
            f"""
Section: {result["section"]}
Content: {result["content"]}
""".strip()
        )

    return "\n\n".join(context_parts)


def answer_question(question: str) -> str:
    search_results = search_knowledge_base(question)
    context = build_context(search_results)

    prompt = f"""
You are a helpful restaurant reservation assistant.

Answer the QUESTION using only the CONTEXT.
If the answer is not in the CONTEXT, say that you don't know and suggest contacting the restaurant.

QUESTION:
{question}

CONTEXT:
{context}
""".strip()

    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
    )

    return response.choices[0].message.content or ""
