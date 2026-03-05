"""
Aggregate results/*.jsonl into a summary table.

Usage:
    python aggregate.py                        # all files in results/
    python aggregate.py results/naive_rag.jsonl results/light_rag.jsonl

Statistics per metric type:
    Quality scores (C, E, D, Overall, faithfulness, groundedness, recall@k):
        mean — standard in RAGAS / LeanRAG / GraphRAG literature.
    Latency:
        mean, p50, p95 — mean is sensitive to outliers; p95 captures tail behaviour
        and is required for any SLA claim (e.g. "latency ≤ 5 s").
    Context tokens:
        mean — average resource consumption per query.
"""
import json
import math
import statistics
import sys
from pathlib import Path

JUDGE_KEYS = ("Comprehensiveness", "Empowerment", "Diversity", "Overall")


def percentile(data: list[float], p: float) -> float:
    """
    Nearest-rank percentile. p in [0, 100].
    With small n (e.g. n=10) results are approximate.
    """
    if not data:
        return 0.0
    sorted_data = sorted(data)
    idx = min(len(sorted_data) - 1, max(0, math.ceil(len(sorted_data) * p / 100) - 1))
    return sorted_data[idx]


def load(path: str) -> list[dict]:
    with open(path, encoding="utf-8") as f:
        return [json.loads(line) for line in f if line.strip()]


def aggregate(results: list[dict]) -> dict:
    buckets: dict[str, list[float]] = {
        k: [] for k in (*JUDGE_KEYS, "faithfulness", "groundedness",
                        "recall_at_k", "context_tokens_approx", "latency_ms")
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

        lat = r.get("latency_total_ms")
        if lat is not None:
            buckets["latency_ms"].append(float(lat))

    out: dict[str, float | None] = {}

    # Quality metrics: mean ± std (standard in RAGAS / LeanRAG literature)
    for k in (*JUDGE_KEYS, "faithfulness", "groundedness", "recall_at_k", "context_tokens_approx"):
        v = buckets[k]
        if v:
            out[k] = round(statistics.mean(v), 3)
            out[f"{k}_std"] = round(statistics.stdev(v), 3) if len(v) > 1 else 0.0
        else:
            out[k] = None
            out[f"{k}_std"] = None

    # Latency: mean + p50 + p95 (skewed distribution, SLA claim)
    lat_vals = buckets["latency_ms"]
    out["latency_mean_ms"] = round(statistics.mean(lat_vals), 1) if lat_vals else None
    out["latency_p50_ms"]  = round(percentile(lat_vals, 50), 1) if lat_vals else None
    out["latency_p95_ms"]  = round(percentile(lat_vals, 95), 1) if lat_vals else None

    return out


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
