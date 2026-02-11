# Vector Similarity

Measure how similar two vectors are. Used in [[Named Entity Recognition|NER]], [[Relation Extraction]], [[Retriever]].

## Metrics

| Metric | Formula | Range | Best for |
|--------|---------|-------|----------|
| **Cosine** | $\frac{A \cdot B}{\|A\| \|B\|}$ | $[-1, 1]$ | Text, semantic search |
| **Dot Product** | $A \cdot B$ | $(-\infty, +\infty)$ | Recommendations, when magnitude matters |
| **Euclidean** | $\|A - B\|$ | $[0, +\infty)$ | Clustering, spatial data |

## Key insight

> If vectors are **normalized**, all three metrics are equivalent.

Cosine = angle only
Dot Product = angle + magnitude
Euclidean = absolute distance

## In RAG

Used to match:
- Entities → nodes in [[Graph]] $G$ ([[Named Entity Recognition|NER]])
- Relations → edges in [[Graph]] $G$ ([[Relation Extraction]])

## Which to use?

Match the metric used to train your embedding model (e.g., `all-MiniLM-L6-v2` uses cosine).

#math #embeddings
