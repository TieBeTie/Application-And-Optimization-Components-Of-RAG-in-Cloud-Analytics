# Question Taxonomy

## Intuition
RAG evaluation datasets systematically under-represent hard query types — most synthetic generators default to factoid single-hop questions. Explicit taxonomy ensures coverage of failure modes that matter in practice.

## Definition
A question taxonomy for RAG evaluation is a set of dimensions $\mathcal{T} = \{D_1, \ldots, D_k\}$ where each $D_i$ partitions the space of queries into mutually exclusive categories.

The **DataMorgana taxonomy** (Moro et al., 2025) uses four dimensions:

$$\mathcal{T}_{\text{DM}} = \{\text{Factuality},\ \text{Premise},\ \text{Complexity},\ \text{Terminology}\}$$

| Dimension | Values | What it tests |
|-----------|--------|---------------|
| **Factuality** | factoid / open-ended | retriever precision vs answer breadth |
| **Premise** | direct / with-premise | handling of user-supplied context |
| **Complexity** | single-hop / multi-hop | cross-chunk and cross-document reasoning |
| **Terminology** | in-document / paraphrase | lexical vs semantic retrieval |

A balanced dataset samples from all $2^4 = 16$ combinations. In practice, 4–5 combinations cover the critical failure modes.

### Extended dimension — Temporality

RARE (2025) identifies a fifth dimension absent from DataMorgana:

| Value | Meaning | Example |
|-------|---------|---------|
| **static** | Answer does not change over time | "Who signed the contract?" |
| **slow-changing** | Answer changes on a scale of months–years | "What is the current headcount?" |
| **fast-changing** | Answer changes on a scale of days–weeks | "What is the current stock price?" |

For a corpus of internal business documents, most queries are static or slow-changing. Fast-changing queries test whether the system correctly abstains or caveats its answer. GaRAGe (ACL 2025) uses the same three-value split (static / slow-changing / fast-changing) and finds that LLMs systematically fail to deflect on fast-changing questions, hallucinating stale facts instead.

For this thesis: annotate temporality but do not enforce balance — business document queries are predominantly static.

### Examples

| Query | Factuality | Premise | Complexity | Terminology | Temporality |
|-------|-----------|---------|------------|-------------|-------------|
| "What is the total contract value?" | factoid | direct | single-hop | in-document | static |
| "Given that MTS Q4 revenue grew, how does it compare to the contract value?" | factoid | with-premise | multi-hop | in-document | slow-changing |
| "What was the payment schedule for the AI system project?" | factoid | direct | single-hop | paraphrase | static |
| "What are the financial risks across both documents?" | open-ended | direct | multi-hop | paraphrase | slow-changing |

## Properties

### Property 1 — Coverage gap in synthetic generation
LLMs default to factoid + direct + single-hop + in-document when generating test cases without explicit constraints. This combination is the easiest for any retriever — it systematically overestimates system quality.

**Proof by construction.** Given a document chunk $c$, an LLM prompted with "generate a question about this chunk" will produce a question whose answer is contained in $c$. By construction, any retriever that returns $c$ in top-$k$ answers the question — regardless of whether it handles paraphrase or multi-hop queries.

### Property 2 — Failure mode coverage

Each dimension targets a specific failure mode:

| Dimension | Failure mode caught |
|-----------|-------------------|
| Complexity: multi-hop | Retriever returns individual chunks but misses cross-document links |
| Terminology: paraphrase | Lexical retriever (BM25) fails; semantic retriever (BGE-M3) succeeds |
| Factuality: open-ended | Generator gives shallow answer; Comprehensiveness catches it |
| Premise: with-premise | System ignores user context; answer is irrelevant |
| Temporality: fast-changing | System hallucinates stale facts instead of deflecting |

## Relationship to [[Eval Dataset]]
Taxonomy defines the axes; [[Eval Dataset]] defines the construction protocol and minimum sample counts per cell.

#rag #evaluation #dataset #taxonomy
