# Organizer $\Omega^{Organizer}$

Arrange and refine retrieved content $C$ into structured content $S$.

$$S = \Omega^{Organizer}(C)$$

## Input / Output

- **Input:** $C$ — retrieved content (from [[Retriever]])
- **Output:** $S$ — structured/organized content for [[Generator]]

## Structures

| Structure | Description | Papers |
|-----------|-------------|--------|
| Flat KG | Simple [[Graph]] | LightRAG |
| Community hierarchy | Leiden/Louvain clustering | GraphRAG |
| Temporal KG | Time-aware | T-GRAG |

## Functions

- Deduplication
- Ranking
- Summarization

See also: [[Formal Task]], [[Retriever]], [[Generator]], [[Graph]]
