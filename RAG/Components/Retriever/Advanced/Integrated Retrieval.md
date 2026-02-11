# Integrated Retrieval

Combine multiple retrievers to balance strengths and weaknesses.

## Types

| Type | Combines | Use case |
|------|----------|----------|
| **Neural-symbolic** | Rules + Neural | Knowledge graphs |
| **Multimodal** | Text + Image + Graph | Rich data sources |

## Neural-symbolic Retrieval

Interleaves:
- **Symbolic** (rule-based) — [[Heuristic-based Retriever]]
- **Neural** (embedding-based) — [[Learning-based Retriever]]

## Approaches

### 1. Symbolic → Neural

First expand with rules, then neural matching.

```
Query → Expand neighbors (symbolic) → Path retrieval (neural)
```

**Papers:** Luo et al., Wen et al.

### 2. Neural → Symbolic

First find seeds with GNN, then extract paths.

```
Query → GNN retrieves seeds (neural) → Shortest paths (symbolic)
```

**Papers:** Mavromatis & Karypis

### 3. Symbolic + Neural attention

Fetch k-hop neighborhood (symbolic), then attention for relevance (neural).

```
Query → k-hop subgraph (symbolic) → Attention scoring (neural)
```

**Papers:** Tian et al., Yasunaga et al., Wang et al.

## Example

```
Query: "Medications that interact with aspirin for heart patients"

1. Symbolic: Expand "aspirin" node → drug interactions
2. Neural: Score relevance to "heart patients" with attention
3. Result: Filtered list of relevant interactions
```

## Trade-offs

| ✅ Pros | ❌ Cons |
|---------|---------|
| Best of both worlds | More complex pipeline |
| Handles semantic + structural | Harder to debug |

See also: [[Heuristic-based Retriever]], [[Learning-based Retriever]], [[GNN]]

#retriever #advanced #neural-symbolic
