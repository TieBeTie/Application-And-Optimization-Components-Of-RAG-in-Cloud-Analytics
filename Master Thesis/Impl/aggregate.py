"""
Aggregate results/*.jsonl into a summary table.

Usage:
    python aggregate.py                        # all files in results/
    python aggregate.py results/naive_rag.jsonl results/light_rag.jsonl
"""
import json
import statistics
import sys
from pathlib import Path

JUDGE_KEYS = ("Comprehensiveness", "Empowerment", "Diversity", "Overall")


def load(path: str) -> list[dict]:
    with open(path, encoding="utf-8") as f:
        return [json.loads(line) for line in f if line.strip()]


def aggregate(results: list[dict]) -> dict:
    buckets: dict[str, list[float]] = {
        k: []
        for k in (
            *JUDGE_KEYS,
            "faithfulness",
            "groundedness",
            "recall_at_k",
            "context_tokens_approx",
            "latency_total_ms",
        )
    }

    for r in results:
        for k in JUDGE_KEYS:
            v = r.get("judge", {}).get(k)
            if v is not None:
                buckets[k].append(float(v))

        faith = r.get("faithfulness", {}).get("score")
        if faith is not None:
            buckets["faithfulness"].append(float(faith))

        gnd = r.get("groundedness", {}).get("score")
        if gnd is not None:
            buckets["groundedness"].append(float(gnd))

        rec = r.get("recall_at_k")
        if rec is not None:
            buckets["recall_at_k"].append(float(rec))

        ctx = r.get("context_tokens")
        if ctx is not None:
            buckets["context_tokens_approx"].append(float(ctx))

        buckets["latency_total_ms"].append(float(r.get("latency_total_ms", 0)))

    return {k: round(statistics.mean(v), 3) if v else None for k, v in buckets.items()}


def print_table(rows: list[tuple[str, dict]]) -> None:
    col_w = 22
    keys = list(rows[0][1].keys())
    header = f"{'metric':<{col_w}}" + "".join(f"{name:>{col_w}}" for name, _ in rows)
    print(header)
    print("-" * len(header))
    for key in keys:
        row = f"{key:<{col_w}}" + "".join(
            f"{(str(agg[key]) if agg[key] is not None else '-'):>{col_w}}"
            for _, agg in rows
        )
        print(row)


if __name__ == "__main__":
    paths = [Path(p) for p in sys.argv[1:]] or sorted(Path("results").glob("*.jsonl"))
    if not paths:
        print("No result files found.")
        sys.exit(1)

    rows = [(p.stem, aggregate(load(str(p)))) for p in paths]
    print_table(rows)
