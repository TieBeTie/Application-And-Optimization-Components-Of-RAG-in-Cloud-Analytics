# Deep Embedding Methods

Address limitations of [[Shallow Embedding]] using neural networks.

## Why needed?

[[Shallow Embedding]] limitations:
- ❌ No semantic features (only structure)
- ❌ No inductivity (retrain for new nodes)
- ❌ Static (cannot adapt to dynamic graphs)

## Solution: GNN

[[GNN]] (Graph Neural Networks):
- ✅ Fuse features + structure
- ✅ Inductive (works on new nodes)
- ✅ Message-passing for structural signals

## Key Property: Inductivity

```
Training: Graph with nodes [A, B, C, D]
Testing:  New node E added

Shallow: Must retrain from scratch
Deep:    E shares feature space → works immediately
```

## Embedding Levels

| Level | What embeddings | Formula |
|-------|-----------------|---------|
| Node | Each node $v_i$ | Eq (3) |
| Edge | Each edge $e_{ij}$ | Eq (4) |
| Graph | Entire (sub)graph $G$ | Eq (5) |

## Combining embeddings

Path embedding = aggregate(node embeddings + edge embeddings along path)

```
Path: A → r1 → B → r2 → C

Path embedding = f(emb(A), emb(r1), emb(B), emb(r2), emb(C))
```

## Use in GraphRAG

| Method | How it uses GNN |
|--------|-----------------|
| GNN-RAG | Message passing per query, threshold candidates |
| Liu et al. | Conditional GNN, backtrack paths |
| REANO | Query-conditioned edge attention, top-k triples |

See also: [[GNN]], [[Shallow Embedding]], [[Learning-based Retriever]]

#retriever #learning #embedding #deep
