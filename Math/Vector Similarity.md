# Vector Similarity

## Intuition

Measure how close two vectors are. Choice of metric depends on whether you care about direction, magnitude, or absolute distance.

## Definition

A function $\text{sim}: \mathbb{R}^n \times \mathbb{R}^n \to \mathbb{R}$ that quantifies closeness of two vectors $A, B$.

### Example

$A = (1, 2, 3),\ B = (2, 4, 6)$. Cosine $= 1$ (same direction), Euclidean $= \sqrt{14} \neq 0$ (different magnitude).

## Properties

| Metric | Formula | Range | Measures |
|--------|---------|-------|----------|
| Cosine | $\frac{A \cdot B}{\|A\| \|B\|}$ | $[-1, 1]$ | Angle only |
| Dot Product | $A \cdot B$ | $(-\infty, +\infty)$ | Angle + magnitude |
| Euclidean | $\|A - B\|$ | $[0, +\infty)$ | Absolute distance |

### Equivalence under normalization

**Claim.** If $\|A\| = \|B\| = 1$, all three metrics are equivalent (monotonic transforms of each other).

**Proof.**

$$\|A - B\|^2 = \|A\|^2 - 2A \cdot B + \|B\|^2 = 2 - 2A \cdot B$$

For normalized vectors: $A \cdot B = \cos\theta = \frac{A \cdot B}{\|A\|\|B\|}$.

So: $\text{Euclidean}^2 = 2(1 - \text{Cosine}) = 2 - 2 \cdot \text{Dot Product}$. $\blacksquare$

### Which to use?

Match the metric used to train your embedding model (e.g., `all-MiniLM-L6-v2` uses cosine).

| Use case | Metric |
|----------|--------|
| Text, semantic search | Cosine |
| Recommendations, magnitude matters | Dot Product |
| Clustering, spatial data | Euclidean |

## In RAG

Used to match:
- Entities → nodes in [[Graph]] $G$ ([[Named Entity Recognition|NER]])
- Relations → edges in [[Graph]] $G$ ([[Relation Extraction]])

See also: [[Named Entity Recognition]], [[Relation Extraction]], [[Retriever]]

#math #embeddings
