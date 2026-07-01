from app.rag.search import search_knowledge_base


def search_restaurant_information(query: str) -> list[dict]:
    return search_knowledge_base(query=query, num_results=3)
