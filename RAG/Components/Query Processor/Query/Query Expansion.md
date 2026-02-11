# Query Expansion

Expand [[Query]] $Q$ by adding context.

$$Q \rightarrow Q + \text{context} = \hat{Q}$$

## Problems it solves

- Queries are **ambiguous** (multiple topics)
- Queries are **too brief** (don't capture intent)
- Users are **uncertain** what they're seeking

## Approaches

| Approach | How |
|----------|-----|
| **LLM expansion** | LLM adds missing context |
| **Graph neighbors** | Add info from neighbor nodes in [[Graph]] $G$ |
| **Predefined templates** | Use templates to structure query → see [[Template-based Optimization]] |

## Example

Query: "Einstein's discoveries"
Expansion: + "physicist" + "relativity" + "Nobel Prize" (from neighbors in $G$)

## In RAG Pipeline

1. [[Query Processor]] receives $Q$
2. Find initial matches in [[Graph]] $G$
3. Retrieve neighboring nodes/edges
4. Add to query: $\hat{Q} = Q + \text{neighbors}$
5. Pass to [[Retriever]]

See also: [[Query Processor]], [[Query Decomposition]], [[Template-based Optimization]]

#query-processing
