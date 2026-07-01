from minsearch import Index


class KeywordIndex:
    def __init__(self, documents: list[dict]) -> None:
        self.index = Index(
            text_fields=["section", "content"],
            keyword_fields=["section"],
        )
        self.index.fit(documents)

    def search(self, query: str, num_results: int = 3) -> list[dict]:
        return self.index.search(query=query, num_results=num_results)
