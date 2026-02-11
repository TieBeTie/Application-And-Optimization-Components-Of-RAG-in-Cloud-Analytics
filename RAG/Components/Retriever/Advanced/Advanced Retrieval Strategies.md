# Advanced Retrieval Strategies

For complex queries that basic retrievers cannot handle.

## Why needed?

Real-world queries are complex:
- Multi-aspect intentions
- Multi-hop reasoning
- Structure patterns

## Example queries

| Query | Challenge |
|-------|-----------|
| "Fight song of university in Lawrence, Kansas with KC branch?" | Multi-hop reasoning |
| "Main themes in the dataset?" | Community structure + aggregation |
| "Most impactful deep learning scholar?" | Multiple aspects (citations, papers, co-authors) |

## Strategies

| Strategy | What it does | Base methods used |
|----------|--------------|-------------------|
| [[Integrated Retrieval]] | Combine retrievers | Heuristic + Learning |
| [[Iterative Retrieval]] | Multi-step with dependencies | Graph Traversal + GNN |
| [[Adaptive Retrieval]] | Decide when/how much to retrieve | Meta-layer over any |

## Relation to base methods

```
┌─────────────────────────────────────────────┐
│           Advanced Strategies               │
│  ┌───────────┐ ┌──────────┐ ┌──────────┐   │
│  │Integrated │ │Iterative │ │ Adaptive │   │
│  └─────┬─────┘ └────┬─────┘ └────┬─────┘   │
└────────┼────────────┼────────────┼──────────┘
         │            │            │
    ┌────┴────┐  ┌────┴────┐  ┌────┴────┐
    │Heuristic│  │Learning │  │  Any    │
    │+Learning│  │+Traversal│  │Retriever│
    └─────────┘  └─────────┘  └─────────┘
```

See also: [[Retriever]], [[Heuristic-based Retriever]], [[Learning-based Retriever]]

#retriever #advanced
