from pathlib import Path
import sys

sys.path.append(str(Path(__file__).resolve().parents[1]))

from app.rag.search import search_knowledge_base


if __name__ == "__main__":
    query = "Do you have vegan options?"
    results = search_knowledge_base(query)

    for idx, result in enumerate(results, start=1):
        print(f"\nResult {idx}")
        print("-" * 40)
        print(f"Section: {result['section']}")
        print(result["content"])
