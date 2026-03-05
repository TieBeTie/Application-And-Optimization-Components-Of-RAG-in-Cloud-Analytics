# Recall@k (Anchor Coverage)

## Intuition
Measures whether the retriever surfaced chunks that physically contain the key facts. If recall=0, the generator could not have answered correctly regardless of quality.

## Definition
A fraction of anchor strings found as case-insensitive substrings in at least one of the top-k retrieved chunks:

$$\text{Recall@k} = \frac{|\{a \in A : \exists c \in C_k,\; a \subseteq c\}|}{|A|}$$

where $A$ is the anchor set, $C_k$ is the top-k chunks.

## Properties

### Component
Retriever — not the generator. A failure here means the retriever did not surface the right chunks.

### Relationship to other metrics
If Recall@k = 0 and Faithfulness > 0, the generator is hallucinating from parametric memory — the answer is not grounded in retrieved context.

#rag #metrics #retrieval
