# Role2Vec

Embeddings based on **structural roles**, not proximity (IJCAI 2018).

## Difference from [[Node2Vec]]

| Method | Basis | Similar nodes |
|--------|-------|---------------|
| [[Node2Vec]] | Proximity | Nodes close in graph |
| Role2Vec | Structural role | Nodes with same "position type" |

## Core Idea

Nodes with similar **structural features** → similar embeddings.

Even if nodes are far apart in graph!

## Structural Features

- Degree centrality
- [[Weisfeiler-Lehman]] labeling
- Motif patterns

## How it works

1. Compute structural features for each node
2. **Attributed random walks** (walks carry features)
3. Train embedding model
4. Result: role-based embeddings

## Example

```
Company org chart:

CEO ————— CTO ————— Engineer
 |          |           |
CFO       Manager    Manager
 |          |           |
Analyst   Engineer   Engineer

Role2Vec sees:
- CEO and CTO: similar role (top management)
- All Engineers: similar role (leaf nodes)
- All Managers: similar role (middle layer)

Even though CEO and Engineers are far apart,
Engineers share same structural role.
```

## Use case in GraphRAG

```
Query: "Generate email in formal tone"

Role2Vec retrieves:
- Emails from similar organizational roles
- Formal emails from managers/executives
- Not just emails from nearby people
```

See also: [[Node2Vec]], [[Shallow Embedding]], [[Graph Kernel]]

#retriever #learning #embedding #role
