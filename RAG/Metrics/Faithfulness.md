# Faithfulness

## Intuition
Checks that every key fact in the answer (anchor) is both stated in the answer AND supported by a retrieved chunk. Detects hallucination from parametric memory.

## Definition
For each anchor $a \in A$, it passes iff:
1. $a$ is present or paraphrased in the answer
2. $a$ is supported by at least one chunk $c \in C_k$

$$\text{Faithfulness} = \frac{|\{a \in A : \text{both conditions hold}\}|}{|A|}$$

## Properties

### Complements
[[Groundedness]] — Faithfulness checks pre-defined anchors. Groundedness audits all claims in the answer, including those not in anchors.

### Component
Both retriever and generator. A failure can mean: retriever did not surface the right chunk, or generator ignored the chunk.

### Correlation with Recall@k
If [[Recall_at_k]] = 0, Faithfulness must also be 0 (anchor cannot be in a chunk that was not retrieved).

#rag #metrics #faithfulness
