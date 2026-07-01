import numpy as np
from minsearch import VectorSearch

from app.rag.embedder import Embedder


class VectorIndex:
    def __init__(self, documents: list[dict]) -> None:
        self.documents = documents
        self.embedder = Embedder()

        vectors = self.embedder.encode_batch(
            [document["content"] for document in documents]
        )

        self.index = VectorSearch(keyword_fields=["section"])
        self.index.fit(np.array(vectors), documents)

    def search(self, query: str, num_results: int = 3) -> list[dict]:
        query_vector = self.embedder.encode(query)
        return self.index.search(query_vector, num_results=num_results)
