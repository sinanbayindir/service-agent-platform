from minsearch import Index

from app.rag.loader import load_knowledge_base

def build_index():

    documents = load_knowledge_base()

    index = Index(

        text_fields=["section", "content"],

        keyword_fields=["section"],

    )

    index.fit(documents)

    return index

def search_knowledge_base(query: str, num_results: int = 3) -> list[dict]:

    index = build_index()

    return index.search(

        query=query,

        num_results=num_results,

    )
