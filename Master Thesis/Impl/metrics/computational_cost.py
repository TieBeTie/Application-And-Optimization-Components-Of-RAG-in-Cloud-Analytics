# Computational cost metric: context tokens sent to the generator per query.
#
# Uses tiktoken (cl100k_base) for accurate counting when available.
# Falls back to chars / 4 heuristic if tiktoken is unavailable or network is blocked.

_enc = None


def _get_enc():
    global _enc
    if _enc is not None:
        return _enc
    try:
        import tiktoken
        _enc = tiktoken.get_encoding("cl100k_base")
    except Exception:
        pass
    return _enc


def _count(text: str) -> int:
    enc = _get_enc()
    if enc is not None:
        return len(enc.encode(text))
    return len(text) // 4


def indexing_throughput(n_chars: int, elapsed_sec: float) -> dict:
    tokens = _count(" " * min(n_chars, 1000)) * (n_chars // 1000 + 1) if n_chars > 0 else 0
    throughput = round(tokens / elapsed_sec, 1) if elapsed_sec > 0 else 0
    return {
        "input_tokens": tokens,
        "elapsed_sec": round(elapsed_sec, 2),
        "throughput_tokens_per_sec": throughput,
    }


def context_tokens(chunks: list[str]) -> int:
    return sum(_count(c) for c in chunks)
