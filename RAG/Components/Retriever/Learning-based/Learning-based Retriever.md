# Learning-based Retriever

Retrieval using ML encoders to embed queries and graph structures into vector space.

## Why needed?

[[Heuristic-based Retriever]] limitations:
- Over-reliance on pre-defined rules
- Cannot handle semantic variations: `doctor` ≠ `physician` (lexically different, same meaning)

Learning-based captures **deeper, abstract relations** without hard-coded rules.

## Core Idea

Compress information into embeddings → similarity search.

$$S^* = \underset{k}{\text{argmax}} \; \phi(q, S)$$

Where:
- $q = F_q(Q) \in \mathbb{R}^d$ — query embedding
- $S = F_s(S) \in \mathbb{R}^{n \times d}$ — source embeddings
- $\phi$ — [[Vector Similarity]] function

## Methods

| Type | Methods | Pros | Cons |
|------|---------|------|------|
| [[Shallow Embedding]] | [[DeepWalk]], [[Node2Vec]], [[Role2Vec]], GraphWave | Fast training | No inductivity, static |
| [[Deep Embedding]] | [[GNN]] | Inductive, uses features | More compute |

## When to use

- Semantic search (meaning > exact match)
- Dynamic graphs (new nodes/edges)
- Multi-modal data (text + structure)

See also: [[Retriever]], [[Heuristic-based Retriever]], [[Vector Similarity]]

#retriever #learning
