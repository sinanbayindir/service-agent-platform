import numpy as np
from minsearch import Index, VectorSearch

from app.rag.embedder import Embedder
from app.rag.loader import load_knowledge_base


def build_keyword_index(documents: list[dict]) -> Index:
    index = Index(
        text_fields=["section", "content"],
        keyword_fields=["section"],
    )
    index.fit(documents)
    return index


def build_vector_index(documents: list[dict], vectors: np.ndarray) -> VectorSearch:
    index = VectorSearch(keyword_fields=["section"])
    index.fit(vectors, documents)
    return index


def rrf(result_lists: list[list[dict]], k: int = 60, num_results: int = 3) -> list[dict]:
    scores = {}
    docs = {}

    for results in result_lists:
        for rank, doc in enumerate(results):
            key = doc["section"]
            scores[key] = scores.get(key, 0) + 1 / (k + rank)
            docs[key] = doc

    ranked_keys = sorted(scores.keys(), key=lambda key: scores[key], reverse=True)
    return [docs[key] for key in ranked_keys[:num_results]]


class HybridSearchEngine:
    def __init__(self) -> None:
        self.documents = load_knowledge_base()
        self.embedder = Embedder()

        self.keyword_index = build_keyword_index(self.documents)

        vectors = self.embedder.encode_batch(
            [document["content"] for document in self.documents]
        )
        self.vectors = np.array(vectors)

        self.vector_index = build_vector_index(self.documents, self.vectors)

    def keyword_search(self, query: str, num_results: int = 3) -> list[dict]:
        return self.keyword_index.search(query=query, num_results=num_results)

    def vector_search(self, query: str, num_results: int = 3) -> list[dict]:
        query_vector = self.embedder.encode(query)
        return self.vector_index.search(query_vector, num_results=num_results)

    def hybrid_search(self, query: str, num_results: int = 3) -> list[dict]:
        keyword_results = self.keyword_search(query, num_results=5)
        vector_results = self.vector_search(query, num_results=5)

        return rrf(
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
    search_engine = get_search_engine()
    return search_engine.hybrid_search(query=query, num_results=num_results)
