# Query Decomposition

Split complex [[Query]] $Q$ into multiple sub-queries.

$$Q \rightarrow \{q_1, q_2, ..., q_n\}$$

## Why?

- Simpler queries → easier to match in [[Graph]] $G$
- Each sub-query can be processed independently
- **Can run in parallel** → see [[Parallel Query Optimization]]

## Example

Query: "What is the capital of the country where Einstein was born?"
- $q_1$: "Where was Einstein born?" → Germany
- $q_2$: "What is the capital of Germany?" → Berlin

## In RAG Pipeline

1. [[Query Processor]] splits $Q$
2. [[Retriever]] searches each $q_i$ in [[Graph]] $G$
3. Results aggregated

See also: [[Query Processor]], [[Query Expansion]], [[Parallel Query Optimization]]

#query-processing
