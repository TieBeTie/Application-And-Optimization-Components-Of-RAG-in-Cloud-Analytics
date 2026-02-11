# Shallow Embedding Methods

Learn node/edge/graph embeddings that retain structural information.

## Categories

| Type | Methods | What preserves |
|------|---------|----------------|
| **Proximity-based** | [[DeepWalk]], [[Node2Vec]] | Nodes close in graph → close in embedding |
| **Role-based** | [[Role2Vec]], GraphWave | Structural roles (not proximity) |

## How it works

1. Initialize each node with random embedding vector
2. Unsupervised training on graph structure
3. Squeeze structural signals into embeddings

## Use cases in GraphRAG

| Method | Use case |
|--------|----------|
| Proximity-based | Academic papers with similar topics |
| Proximity-based | Products co-purchased |
| Role-based | Emails with similar tone/role |
| Role-based | Entities with similar structural position |

## Limitations ⚠️

| Problem | Why it matters |
|---------|----------------|
| **No inductivity** | New nodes → re-initialize + retrain |
| **Static** | Cannot adapt to dynamic graphs |
| **No semantic features** | Only structure, no text/attributes |

> Real-world knowledge evolves dynamically → shallow embeddings struggle.

## Example

```
Academic citation network:

Paper A cites [B, C, D]
Paper E cites [B, C, F]

Proximity embedding:
- A and E are close (share citations B, C)
- Use to retrieve: "papers similar to A"
```

See also: [[Deep Embedding]], [[Learning-based Retriever]], [[Vector Similarity]]

#retriever #learning #embedding
