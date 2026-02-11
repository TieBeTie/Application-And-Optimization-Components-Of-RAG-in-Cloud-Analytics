# Relation Matching

Map relations from [[Query]] $Q$ to edges in [[Graph]] $G$.

## How it works

1. [[Relation Extraction]] extracts relations from $Q$
2. Match relations to edges via [[Vector Similarity]]
3. Return top-k edges

## Relation to Relation Extraction

| Step | Component |
|------|-----------|
| Extract relations | [[Relation Extraction]] |
| Map to edges | Relation Matching |

> Similar to [[Entity Linking]], but for edges instead of nodes.

## Example

```
Query: "What is the capital of France?"

1. Relation Extraction: (?, capital_of, France)
2. Relation Matching:
   - Find edges with label "capital_of"
   - Filter by target node "France"
   - Result: (Paris, capital_of, France)
```

## Challenges

Same as [[Entity Linking]]:
- Semantic/lexical ambiguity
- Predefined rules help distinguish similar relations

See also: [[Relation Extraction]], [[Entity Linking]], [[Retriever]]

#retriever #heuristic
