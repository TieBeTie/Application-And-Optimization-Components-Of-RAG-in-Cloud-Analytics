# Generator $\Omega^{Generator}$

Generate answer $A$ from processed query $\hat{Q}$ and structured content $S$.

$$A = \Omega^{Generator}(\hat{Q}, S)$$

## Input / Output

- **Input:** $\hat{Q}$ (from [[Query Processor]]), $S$ (from [[Organizer]])
- **Output:** $A$ — final answer to [[Query]] $Q$

## Approaches

| Approach | Description | Papers |
|----------|-------------|--------|
| Direct LLM | Pass $S$ as context to LLM | |
| Map-Reduce | Aggregate community summaries | GraphRAG |
| Iterative | Multi-step generation | |

See also: [[GraphRAG query process]], [[Organizer]], [[Query Processor]]
