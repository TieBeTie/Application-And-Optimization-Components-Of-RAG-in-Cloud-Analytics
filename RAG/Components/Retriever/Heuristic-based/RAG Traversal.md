
Explore [[Graph]] $G$ using traversal algorithms starting from nodes found by [[Entity Linking]].

## Algorithms

| Algorithm | Strategy | Use case |
|-----------|----------|----------|
| BFS | Level by level | Find shortest paths |
| DFS | Deep first | Explore specific branch |
| A* | Heuristic-guided | Optimal path search |
| MCTS | Monte Carlo Tree Search | Complex decisions |

## Problem: Exponential Explosion

Graph can have exponential number of edges → information overload.

## Solutions

### 1. L-hop Limit

Restrict traversal to $L$ hops from starting nodes.

```
Start nodes: [A, B] (from Entity Linking)
L = 2

A → neighbors(A) → neighbors(neighbors(A))  ← STOP
B → neighbors(B) → neighbors(neighbors(B))  ← STOP
```

### 2. L-hop Subgraph

Extract subgraph within $L$ hops around initial entities.

### 3. LLM Pruning

Use LLM to prune irrelevant paths during traversal.

> Optimization: LLM decides which branches to explore.

### 4. Predefined Templates

Use templates/rules for traversal patterns.

See also: [[Template-based Optimization]]

## Example

```
Query: "How is Einstein related to Nobel Prize?"

1. Entity Linking: [Einstein, Nobel_Prize]
2. BFS from both nodes, L=3
3. Find connecting path:
   Einstein → won → Nobel_Prize_Physics → is_a → Nobel_Prize
```

See also: [[Entity Linking]], [[Retriever]], [[Graph]]

#retriever #heuristic #traversal
