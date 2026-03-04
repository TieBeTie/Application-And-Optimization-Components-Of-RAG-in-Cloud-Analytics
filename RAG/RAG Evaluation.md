# RAG Evaluation

## Intuition
A RAG pipeline has three variable components — Retriever, Generator, Indexer. Each has distinct failure modes. Metrics must cover all failure modes and be component-separable so that degradation can be attributed to a specific component.

See [[Evaluation Metric Selection]] for the general methodology.

## Variable components

| Component | Fixed / Variable |
|---|---|
| Query Processor | fixed |
| Organizer | fixed |
| Retriever | **variable** |
| Generator | **variable** |
| Indexer | **variable** |

Fixed components require no dedicated metrics.

## Failure mode table

| Component | Failure mode | Metric |
|---|---|---|
| Retriever | misses relevant chunks | recall@k |
| Retriever | correct chunk ranked below top-k | recall@k |
| Retriever | query-document distributional mismatch | recall@k (indirectly) |
| Generator | adds facts not in chunks | faithfulness |
| Generator | ignores chunks, answers from parametric memory | groundedness |
| Generator | incomplete answer | Comprehensiveness |
| Generator | not actionable | Empowerment |
| Generator | narrow answer | Diversity |
| Generator | multi-hop inference failure across chunks | Comprehensiveness + faithfulness |
| Generator | cross-document contradiction not flagged | faithfulness (partial) |
| System | lost-in-the-middle: LLM ignores chunks in middle of context | faithfulness |
| System | context window overflow, chunks truncated | faithfulness + recall@k |
| System | stale index, outdated content retrieved | **not detectable** — see note |
| Indexer | indexing too expensive | throughput (tok/s) |
| System | too slow end-to-end | latency |

## Component-separability check

Retriever vs Generator:

| Scenario | recall@k | faithfulness |
|---|---|---|
| Retriever missed chunks | low | high |
| Generator hallucinated | high | low |
| Both failed | low | low |

recall@k isolates Retriever failure; faithfulness isolates Generator failure. The pair is separable.

## Blind spot — temporal staleness

If the index is not updated, retrieved chunks are factually stale. Faithfulness will still be high — the answer is faithful to the stale retrieved context. **No standard metric detects this.**

Workaround: include date-bounded test queries with known expiry dates in the evaluation set.

## Standard framework

**RAGAS** (Es et al., 2023, arXiv:2309.15217) is the standard framework for reference-free RAG evaluation.

Core metrics: Faithfulness, Answer Relevancy, Context Precision, Context Recall.

Notable extended metric: **Noise Sensitivity** — measures degradation when irrelevant documents are added to the context. Directly tests retriever robustness, not covered by the core four.

#rag #evaluation #metrics
