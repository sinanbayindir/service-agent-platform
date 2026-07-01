from app.rag.hybrid import reciprocal_rank_fusion
from app.rag.keyword_index import KeywordIndex
from app.rag.loader import load_knowledge_base
from app.rag.vector_index import VectorIndex


class HybridSearchEngine:
    def __init__(self) -> None:
        self.documents = load_knowledge_base()
        self.keyword_index = KeywordIndex(self.documents)
        self.vector_index = VectorIndex(self.documents)

    def keyword_search(self, query: str, num_results: int = 5) -> list[dict]:
        return self.keyword_index.search(query=query, num_results=num_results)

    def vector_search(self, query: str, num_results: int = 5) -> list[dict]:
        return self.vector_index.search(query=query, num_results=num_results)

    def search(self, query: str, num_results: int = 3) -> list[dict]:
        keyword_results = self.keyword_search(query=query)
        vector_results = self.vector_search(query=query)

        return reciprocal_rank_fusion(
            [keyword_results, vector_results],
            k=60,
            num_results=num_results,
        )


_search_engine: HybridSearchEngine | None = None


def get_search_engine() -> HybridSearchEngine:
    global _search_engine

    if _search_engine is None:
        _search_engine = HybridSearchEngine()

    return _search_engine


def search_knowledge_base(query: str, num_results: int = 3) -> list[dict]:
    return get_search_engine().search(query=query, num_results=num_results)
