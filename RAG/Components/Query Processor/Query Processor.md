# Query Processor $\Omega^{Processor}$

Preprocess [[Query]] $Q$ into processed query $\hat{Q}$.

$$\hat{Q} = \Omega^{Processor}(Q)$$

## Input / Output

- **Input:** $Q$ — user query
- **Output:** $\hat{Q}$ — processed query for [[Retriever]]

## Approaches

| Approach | Description | Location |
|----------|-------------|----------|
| [[Named Entity Recognition]] | Extract entities from $Q$ | [[NLP]] |
| Relation Extraction | Identify relationships in $Q$ | |
| [[Query Structuration]] | Convert $Q$ to structured form | [[Query]] |
| [[Query Decomposition]] | Split $Q$ into sub-queries | [[Query]] |
| [[Query Expansion]] | Add context from [[Graph]] $G$ | [[Query]] |

See also: [[Formal Task]], [[Retriever]], [[Graph]]
