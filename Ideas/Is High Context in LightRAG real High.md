# Is High Context in LightRAG real High?

#idea #question #optimization

## Problem

LightRAG defines high-level context as 1-hop neighbors:

$$H = \{v_i \mid v_i \in V \land (v_i \in N_v \lor v_i \in N_e)\}$$

**No formal proof** that $N_v \cup N_e$ = semantic context. It's a heuristic.

Evaluation in paper: LLM-based comparison (GPT-4o-mini ranks outputs). Not a metric of context quality itself.

## Why it's questionable

- Not all neighbors are semantically relevant
- 1-hop = structural proximity ≠ semantic proximity
- Same criticism applies to GraphRAG's Leiden — ignores node/edge semantics

## Better alternatives exist

| Paper | Approach | Improvement |
|-------|----------|-------------|
| SemToG | Semantic community detection | +2-5% accuracy, relation-query similarity |
| ArchRAG | Attributed communities | Structure + semantic themes together |

> Attributed communities: nodes must be **densely connected AND semantically similar**.

## Research directions

- Can we prune $H$ using LLM or similarity threshold?
- Attributed communities instead of 1-hop?
- Weighted neighbors (closer semantically → higher weight)?

See also: [[LightRAG Query]], [[Graph Traversal]], [[Adaptive Retrieval]]
