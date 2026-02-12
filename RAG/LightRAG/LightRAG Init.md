## Given

- [[Raw Documents]] $D$ — corpus used to construct the [[Graph]]
- Data Indexer $\varphi(\cdot)$ — transforms $D$ into structured graph data

---
## RAG — Graph Initialization ($\varphi$)

### Objective

$$D \xrightarrow{\varphi} \hat{D} = (G, K')$$

Construct:
- $G = (V, E)$ — knowledge graph (entities + relations)
- $K'$ — deduplicated keys (words/phrases linked to nodes and edges)

---

## Pipeline

| Step | Component | Input → Output |
|------|-----------|----------------|
| 1 | Chunking | $D \rightarrow \{c_i\}$ |
| 2 | [[Named Entity Recognition]] & [[Relation Extraction]] | $\{c_i\} \rightarrow \{(e_j, r_{jk})\}$ |
| 3 | [[Profiling (Key–Value Gen.)]] | $\{e_j\} \cup \{r_{jk}\} \rightarrow K$ |
| 4 | Deduplication | $K \rightarrow K'$ |
| 5 | Graph Construction | $\{(e_j, r_{jk})\} \rightarrow G$ |
| 6 | Persistence / Indexing | see below |

## Persistence / Indexing

From $G$ and $K'$ we build:

| What we store | How | Purpose |
|---------------|-----|---------|
| Embeddings of keys from $K'$ | **Vector DB** | [[Vector Similarity]] search at query time |
| Mapping $K' \rightarrow G$ | **HashMap** (key → node/edge ref) | Resolve matched key to graph element |
| Graph $G = (V, E)$ | **Graph DB** | Structural traversal, 1-hop neighbors |

```
              K'
              ↓
    ┌─── Vector DB ───┐
    │  embed(key₁)    │ ──→ HashMap ──→ node/edge in G
    │  embed(key₂)    │ ──→ HashMap ──→ node/edge in G
    │  ...            │
    └─────────────────┘
                               ↓
                          Graph DB (G)
                        for neighbors, paths
```

> At query time: [[LightRAG Query]] uses Vector DB to find keys → HashMap to jump into G → Graph DB for expansion.

## Complexity

LLM called $\frac{\text{total tokens}}{\text{chunk size}}$ times. No additional overhead.

![[Pasted image 20260211232442.png]]
