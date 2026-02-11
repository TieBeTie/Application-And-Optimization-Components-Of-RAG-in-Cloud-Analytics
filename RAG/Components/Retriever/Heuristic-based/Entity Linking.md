# Entity Linking

Map entities from [[Query]] $Q$ to nodes in [[Graph]] $G$.

## How it works

1. [[Named Entity Recognition]] extracts entities from $Q$
2. Match entities to nodes via [[Vector Similarity]] or lexical features
3. Return top-k nodes as starting points

## Relation to NER

| Step | Component |
|------|-----------|
| Extract entities | [[Named Entity Recognition]] |
| Map to nodes | Entity Linking |

> Entity Linking = NER + mapping to [[Graph]]

## Challenges

- Semantic vs lexical similarity: `bit` vs `byte`, `president` vs `resident`
- Heuristic methods can distinguish with predefined rules

## Example

```
Query: "Who is the CEO of Apple?"

1. NER: [CEO, Apple]
2. Entity Linking:
   - "Apple" → node:Apple_Inc (similarity: 0.95)
   - "Apple" → node:Apple_fruit (similarity: 0.3)
   - Select: Apple_Inc
```

See also: [[Named Entity Recognition]], [[Relation Matching]], [[Retriever]]

#retriever #heuristic
