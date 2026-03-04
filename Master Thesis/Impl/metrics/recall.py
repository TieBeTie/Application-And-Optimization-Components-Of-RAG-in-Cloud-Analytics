def recall_at_k(chunks: list[str], anchors: list[str], k: int | None = None) -> float | None:
    """
    Proxy recall@k: fraction of anchors found in at least one of the top-k chunks.
    A chunk is relevant if it contains any anchor string (case-insensitive).
    """
    if not anchors:
        return None
    search_space = chunks[:k] if k else chunks
    found = sum(
        1 for anchor in anchors
        if any(anchor.lower() in chunk.lower() for chunk in search_space)
    )
    return round(found / len(anchors), 3)
