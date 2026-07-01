def reciprocal_rank_fusion(
    result_lists: list[list[dict]],
    k: int = 60,
    num_results: int = 3,
) -> list[dict]:
    scores: dict[str, float] = {}
    docs: dict[str, dict] = {}

    for results in result_lists:
        for rank, doc in enumerate(results):
            key = doc["section"]
            scores[key] = scores.get(key, 0.0) + 1 / (k + rank)
            docs[key] = doc

    ranked_keys = sorted(
        scores.keys(),
        key=lambda key: scores[key],
        reverse=True,
    )

    return [docs[key] for key in ranked_keys[:num_results]]
