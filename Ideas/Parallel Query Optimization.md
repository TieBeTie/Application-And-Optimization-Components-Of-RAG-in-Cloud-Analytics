# Parallel Query Optimization

#idea #question 

## Hypothesis

Instead of 1 large query → **N small parallel sub-queries**.

$$Q \xrightarrow{\text{decompose}} \{q_1, q_2, ..., q_n\} \xrightarrow{\text{parallel}} \text{Results}$$

## Why it might work

1. [[Query Decomposition]] splits $Q$ into sub-queries
2. Each $q_i$ runs **in parallel** through [[Retriever]]
3. Results combined

## Connection to Attention

- Each query $q_i$ = vector in attention matrix
- More sub-queries = more vectors from same user
- Matrix multiplication in attention can process batch

```
User Query → [q₁, q₂, q₃, ..., qₙ] → Attention Matrix
                                      ↓
                               Parallel processing
```

## Trade-offs to investigate

| More decomposition | Effect |
|--------------------|--------|
| ✅ Higher accuracy? | Each sub-query more focused |
| ✅ Parallelization | GPU batch processing |
| ❓ Overhead | Decomposition + aggregation cost |
| ❓ Context loss | Sub-queries may lose global context |

## Questions

- Does more decomposition = more accuracy?
- Optimal number of sub-queries?
- How to aggregate results from parallel queries?
- Impact on summarization in [[Generator]]?

See also: [[Query Decomposition]], [[Retriever]], [[Generator]]

