"""
Upload documents from datasets/docs/ to rag_api and save returned file_ids.

Usage:
    python ingest.py [docs_dir]

Output:
    file_ids.json       — {filename: file_id} map
    indexing_throughput.json  — tokens/sec during indexing
"""
import csv
import io
import json
import os
import sys
import time
import uuid
from pathlib import Path

import requests
from dotenv import load_dotenv

from metrics.computational_cost import indexing_throughput

load_dotenv()

RAG_API_URL = os.getenv("RAG_API_URL", "http://localhost:8000")
SUPPORTED = {".pdf", ".docx", ".csv", ".txt"}


def csv_to_text(path: Path) -> bytes:
    """Convert CSV rows to natural language sentences for embedding.

    Handles CSVs with a title row before the actual column header by finding
    the last non-numeric row before the first row that contains numbers.
    """
    with open(path, encoding="utf-8") as f:
        rows = [r for r in csv.reader(f) if any(c.strip() for c in r)]

    if len(rows) < 2:
        return b""

    def has_number(row):
        return any(c.strip().replace(".", "", 1).replace("-", "", 1).isdigit()
                   for c in row if c.strip())

    # Header = last row before the first data row that contains a number
    header_idx = 0
    for i, row in enumerate(rows):
        if has_number(row):
            header_idx = max(0, i - 1)
            break

    header = [c.strip() for c in rows[header_idx]]
    lines = []
    for row in rows[header_idx + 1:]:
        parts = [f"{h}: {v.strip()}" for h, v in zip(header, row)
                 if h and v.strip()]
        if parts:
            lines.append(". ".join(parts).rstrip(".") + ".")

    return "\n".join(lines).encode("utf-8")


def ingest(
    docs_dir: str = "datasets/docs",
    output: str = "file_ids.json",
    cost_output: str = "indexing_throughput.json",
) -> None:
    docs = [p for p in Path(docs_dir).rglob("*") if p.suffix.lower() in SUPPORTED]
    if not docs:
        print(f"No supported documents found in {docs_dir}")
        return

    file_ids = {}
    total_chars = 0
    t0 = time.perf_counter()

    for doc in docs:
        file_id = str(uuid.uuid4())
        print(f"Uploading {doc.name} ...", end=" ", flush=True)

        if doc.suffix.lower() == ".csv":
            file_bytes = csv_to_text(doc)
            upload_name = doc.stem + ".txt"
        else:
            file_bytes = doc.read_bytes()
            upload_name = doc.name

        resp = requests.post(
            f"{RAG_API_URL}/embed",
            files={"file": (upload_name, file_bytes)},
            data={"file_id": file_id},
            timeout=120,
        )
        resp.raise_for_status()
        data = resp.json()
        returned_id = data.get("file_id") or file_id
        chunks_stored = data.get("chunks_stored", 0)
        total_chars += chunks_stored * 1500  # CHUNK_SIZE=1500 chars per chunk
        file_ids[doc.name] = returned_id
        print(f"-> {returned_id} ({chunks_stored} chunks)")

    elapsed = time.perf_counter() - t0

    with open(output, "w") as f:
        json.dump(file_ids, f, indent=2)
    print(f"\nSaved {len(file_ids)} file_id(s) to {output}")

    throughput = indexing_throughput(total_chars, elapsed)
    with open(cost_output, "w") as f:
        json.dump(throughput, f, indent=2)
    print(
        f"Indexing throughput: {throughput['throughput_tokens_per_sec']} tokens/sec "
        f"({throughput['input_tokens_approx']} tokens in {throughput['elapsed_sec']}s) -> {cost_output}"
    )


if __name__ == "__main__":
    ingest(docs_dir=sys.argv[1] if len(sys.argv) > 1 else "datasets/docs")
