# DeepWalk

First algorithm to apply Word2Vec to graphs (2014, Stony Brook University).

## Core Idea

Graph → Random Walks → Word2Vec → Embeddings

## How it works

1. Generate **random walks** starting from each node
2. Walk = sequence of nodes (like a sentence)
3. Train **Word2Vec** (Skip-gram) on walks
4. Result: node embeddings

```
Graph:     A — B — C — D
           |       |
           E — — — F

Random walk from A: [A, B, C, F, E, A, B, ...]
Random walk from C: [C, D, B, A, E, ...]

→ Word2Vec training
→ Node embeddings
```

## Key insight

> Nodes appearing in same random walks → close embeddings

## Limitations

- **Uniform** random walks (no control over exploration)
- [[Node2Vec]] improves with biased walks

## Example

```
Social network: find users similar to User A

1. Random walks from all users
2. Train DeepWalk
3. Embedding(A) close to Embedding(B) if they share neighbors
4. Retrieve: top-k users by cosine similarity
```

See also: [[Node2Vec]], [[Shallow Embedding]], [[Vector Similarity]]

#retriever #learning #embedding #proximity
