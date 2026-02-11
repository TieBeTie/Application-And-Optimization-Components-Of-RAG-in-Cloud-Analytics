# Node2Vec

Improvement over [[DeepWalk]] with **biased random walks** (2016, Stanford).

## Core Idea

Control walk strategy with parameters **p** and **q**.

## Parameters

| Parameter | High value | Low value |
|-----------|------------|-----------|
| **p** (return) | Less likely to return to previous node | More backtracking |
| **q** (in-out) | Stay local (≈ BFS) | Go far (≈ DFS) |

```
      p controls: ← return
      q controls: → explore outward

Previous — Current — Next
              ↓
           Neighbor
```

## Trade-off: BFS vs DFS

| Strategy | What captures | Use case |
|----------|---------------|----------|
| BFS-like (high q) | Local neighborhood | Community detection |
| DFS-like (low q) | Global structure | Role similarity |

## How it works

1. Generate **biased** random walks (using p, q)
2. Train Word2Vec on walks
3. Result: flexible node embeddings

## Example

```
Citation network:

BFS-like (q=2): papers in same research area
DFS-like (q=0.5): papers with similar citation patterns

Query: "Find papers similar to Paper A"
→ Node2Vec embedding
→ Top-k by cosine similarity
```

See also: [[DeepWalk]], [[Role2Vec]], [[Shallow Embedding]]

#retriever #learning #embedding #proximity
