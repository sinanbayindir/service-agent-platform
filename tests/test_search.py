from app.rag.search import search_knowledge_base


def test_search_finds_vegan_options():
    results = search_knowledge_base("Do you have vegan options?")

    assert len(results) > 0
    assert results[0]["section"] == "Menu Highlights"
    assert "Vegan options are available on request" in results[0]["content"]
