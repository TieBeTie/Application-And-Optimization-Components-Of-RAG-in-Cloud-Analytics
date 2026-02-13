# Query Structuration

Convert natural language [[Query]] $Q$ into a structured form.

$$Q \xrightarrow{\text{structure}} Q_{struct}$$

## Two approaches

| Approach | Output | When to use |
|----------|--------|-------------|
| [[Structured Query Language]] | SQL, Cypher, SPARQL | Querying databases directly |
| [[Structured Reasoning]] | Graph of Thoughts (KGoT) | Complex multi-step reasoning |

Both structure the query, but differently:
- First structures **format** (into DB language)
- Second structures **reasoning** (into a graph)

See also: [[Query Processor]], [[Query Decomposition]]

#query-processing
