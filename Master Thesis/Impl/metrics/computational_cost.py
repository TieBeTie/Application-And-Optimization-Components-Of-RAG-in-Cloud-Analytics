# Computational cost metric: embedding throughput in tokens/sec.
#
# Throughput = (input tokens) / (indexing time in seconds).
# Input tokens are approximated as n_chars / 4 (standard heuristic).
#
# Higher throughput means lower computational cost of indexing.
# Used to compare RAG configurations on the same hardware.


def indexing_throughput(n_chars: int, elapsed_sec: float) -> dict:
    tokens_approx = n_chars // 4
    throughput = round(tokens_approx / elapsed_sec, 1) if elapsed_sec > 0 else 0
    return {
        "input_tokens_approx": tokens_approx,
        "elapsed_sec": round(elapsed_sec, 2),
        "throughput_tokens_per_sec": throughput,
    }


def context_tokens(chunks: list[str]) -> int:
    # Approximate token count of retrieved context passed to the generator.
    return sum(len(c) for c in chunks) // 4
