# Tasks

## 1. Presentation text

Write a coherent, complete, self-contained text for each slide.

Requirements:
- Every term introduced on a slide must be formally defined before or on that slide
- Every formula must be derived or cited
- No synonyms — one term per concept throughout
- No contradictions between slides (e.g. cost definition on slide 3 must match experiment on slide 8)
- Faithfulness and groundedness must be distinguished clearly
- The formal optimisation criterion (quality >= X% of baseline at reduced cost) must appear on slide 3 and be referenced on slide 8

Slides to cover: 1 (title + closed-loop), 2 (motivation), 3 (RAG components + optimisation criterion), 4 (goals), 7 (architecture), 8 (experimental evaluation).

Deliverable: one .md file per slide with speaker notes + formal definitions used.

---

## 2. Validate system results and identify gaps

Current state after first run (naive_rag, 10 queries):

| Metric | Value |
|--------|-------|
| Overall (LLM judge) | 2.9 |
| Faithfulness | 0.5 |
| Groundedness | 0.663 |
| Recall@5 | 0.5 |
| Indexing throughput | 2655 tok/sec |
| Avg latency | 2806 ms |

Known failure: queries 6-10 (CSV financial report) — Recall@5 = 0.0. Cause: text splitter breaks CSV rows, numbers are lost across chunk boundaries.

Gaps to close before defence:

- CSV chunking strategy (parse rows as structured text, not raw split)
- LightRAG baseline (currently stub, needs running instance)
- Embedding dimension experiment (BGE-M3 1024 vs 512)
- Update cost metric (not yet implemented)
- At least 2-3 baselines in aggregate table

---

## 3. Fix CSV retrieval

Reproduce the supervisor's observation: "standard text splitter breaks CSV structure".

Options to test:
- Parse CSV rows into "key: value" sentences before ingestion
- Ingest each row as a separate document with file_id
- Keep raw CSV but reduce CHUNK_SIZE so rows are not split

Deliverable: re-run ingest + eval, Recall@5 on queries 6-10 should increase from 0.0.
