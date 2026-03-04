# Benchmark MVP — Analysis & Thoughts

## Component Status

| Component | Status | File |
|-----------|--------|------|
| NaiveRAG retriever (ROGP baseline) | ready | retrievers/naive_rag.py |
| LightRAG retriever | stub — needs server | retrievers/light_rag.py |
| LLM judge (Comp/Emp/Div/Overall) | ready | metrics/llm_judge.py |
| Faithfulness (anchor validation) | ready | metrics/faithfulness.py |
| Groundedness (claim extraction) | ready | metrics/groundedness.py |
| Recall@k (anchor string match) | ready | metrics/recall.py |
| Indexing cost (throughput tokens/sec) | ready | metrics/cost.py + ingest.py |
| Query cost (context tokens) | ready | metrics/cost.py + run_eval.py |
| Update cost | not yet | planned |

---

## Committee Requirements Coverage

| Requirement (Замечания комиссии) | How addressed |
|----------------------------------|--------------|
| Real metrics, not just plans | run_eval.py produces results/*.jsonl with numbers |
| Formal cost definition | indexing_cost.json (throughput) + context_tokens_approx per query |
| Faithfulness | faithfulness.py: anchor presence in answer AND in retrieved chunks |
| Groundedness | groundedness.py: LLM extracts claims from answer, checks each vs chunks |
| Robustness of judge | llm_judge.py: temperature=0.0, n_runs=5, averaged |
| Judge calibration | queries.jsonl anchors field — fill manually for 30-50 questions |
| 2-3 baselines | naive_rag (running), light_rag (stub), lean_rag (planned) |
| Synthetic Q&A bias | queries.jsonl: anchors empty — must be filled with real ground-truth |
| CSV in dataset | ingest.py: SUPPORTED includes .csv |

---

## Cost Model

Three cost types requested by Дмитрий:

**1. Indexing cost** (ingest.py → indexing_cost.json)
- Proxy: file bytes / 4 / elapsed_sec = approx tokens/sec throughput
- Limitation: measures file upload + server embedding time together, not embedding alone
- Real measurement: instrument rag_api to report embedding time separately

**2. Query cost** (run_eval.py → query_cost field per result)
- context_tokens_approx = sum(len(chunk) for chunk in chunks) / 4
- Directly correlated with generator inference cost
- BGE-M3 dimension experiment: reduce 1024 → 512, compare context quality vs cost

**3. Update cost** (not yet implemented)
- Proxy: run ingest.py on a single new file, measure elapsed_sec
- For NaiveRAG: O(1 file) — just embed the new file
- For LeanRAG: O(file + affected clusters) — rebuild GMM hierarchy

---

## Metric Semantics

**Faithfulness vs Groundedness** — they are not the same:
- Faithfulness answers: "are the pre-defined anchor facts present and supported?"
  Works only when anchors are filled in queries.jsonl. Useful for regression testing.
- Groundedness answers: "does the model hallucinate anything in this answer?"
  Works for any answer, no manual anchors needed. More expensive (LLM call per query).

**Recall@k:**
- Proxy only: checks if anchor strings appear in retrieved chunks by substring match
- If anchors are empty → returns None
- Real recall would require embedding-level relevance judgments

**LLM judge reliability:**
- 5 runs at temperature=0 → variance should be low (judge is deterministic at temp=0)
- Calibration on 30-50 manually labeled Q&A pairs is the next step
- DeepSeek-V3 is acceptable per supervisor confirmation

---

## Known Limitations

1. Anchors in queries.jsonl are empty → faithfulness returns score=None for all 5 queries
2. LightRAG retriever does not return source chunks → recall, faithfulness, groundedness all return None for LightRAG
3. Indexing throughput is a file-size proxy, not actual embedding model throughput
4. Context token count uses chars/4 heuristic (no tiktoken dependency)
5. No documents in datasets/docs/ yet — ingest.py has nothing to upload

---

## How to Run

```
# 1. Start services
docker compose up -d

# 2. Add documents
mkdir -p datasets/docs
# copy PDF / DOCX / CSV files into datasets/docs/

# 3. Index documents
python ingest.py
# → file_ids.json, indexing_cost.json

# 4. Run evaluation
python run_eval.py --retriever naive_rag
# → results/naive_rag.jsonl

# 5. Compare (once LightRAG is set up)
python run_eval.py --retriever light_rag
# → results/light_rag.jsonl

# 6. Summary table
python aggregate.py
```

---

## Next Steps (priority order)

1. Add real documents to datasets/docs/ and fill in anchors in queries.jsonl
2. Run ingest.py + run_eval.py for naive_rag — get first real numbers
3. Set up LightRAG server (add to docker-compose.yml), connect LightRAGRetriever
4. Add lean_rag retriever (calls LeanRAG REST API after building graph)
5. Embedding dimension experiment: test context quality at dim=512 vs dim=1024
6. Implement update cost measurement: time ingest of single new file per retriever
