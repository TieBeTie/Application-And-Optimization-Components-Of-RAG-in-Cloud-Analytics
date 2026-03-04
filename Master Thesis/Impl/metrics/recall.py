def recall_at_k(chunks: list[str], anchors: list[str], k: int | None = None) -> float | None:
    """
    Anchor coverage@k: fraction of anchor strings found (as substrings, case-insensitive)
    in at least one of the top-k retrieved chunks.

    This is NOT standard IR recall@k (which requires relevance-labelled documents).
    It measures whether the retriever surfaces chunks that contain the key facts.
    Returns None if anchors list is empty.
    """
    if not anchors:
        return None
    search_space = chunks[:k] if k else chunks
    found = sum(
        1 for anchor in anchors
        if any(anchor.lower() in chunk.lower() for chunk in search_space)
    )
    return round(found / len(anchors), 3)
