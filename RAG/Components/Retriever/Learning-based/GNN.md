# GNN (Graph Neural Network)

Neural network that learns on graph structure via **message passing**.

## Core Idea

Each node aggregates information from neighbors → learns representation.

## Formulas

### Node-level (Eq 3)

$$x_i^l = \gamma_{\Theta_\gamma} \left( x_i^{l-1} \oplus \sum_{j \in N_i} \phi_{\Theta_\phi}(x_i^{l-1}, x_j^{l-1}, e_{ij}) \right)$$

- $x_i^l$ — node $i$ embedding at layer $l$
- $N_i$ — neighbors of node $i$
- $\phi$ — weighting function (learns important neighbors)
- $\gamma$ — combination function
- $e_{ij}$ — edge features

### Edge-level (Eq 4)

$$e_{ij}^l = \gamma_{\Theta_\gamma} \left( e_{ij}^{l-1} \oplus \sum_{e_{mn} \in N_{ij}^e} \phi_{\Theta_\phi}(e_{ij}^{l-1}, e_{mn}^{l-1}, x_{e_{ij} \cap e_{mn}}) \right)$$

- $N_{ij}^e$ — edges incident to same endpoints

### Graph-level (Eq 5)

$$G^l = \rho_{\Theta_\rho}(\{x_i^l, e_{ij}^l \mid v_i \in V_G, e_{ij} \in E_G\})$$

- $\rho$ — pooling operation over all nodes/edges

## Message Passing

```
Layer 0: Initial features
    ↓
Layer 1: Aggregate 1-hop neighbors
    ↓
Layer 2: Aggregate 2-hop neighbors
    ↓
...
Layer L: L-hop neighborhood encoded
```

## Why it works

| Function | Learns to... |
|----------|--------------|
| $\phi$ (weighting) | Prioritize important neighbors |
| $\gamma$ (combination) | Balance self vs neighborhood |
| $\rho$ (pooling) | Aggregate into graph embedding |

## Example

```
Knowledge Graph query: "Einstein's contributions"

1. GNN encodes all nodes (scientists, works, awards)
2. Query embedding included in message passing
3. Candidate nodes with relevance > threshold
4. Retrieve shortest path to each candidate
5. Context: [Einstein → wrote → Relativity → influenced → Physics]
```

See also: [[Deep Embedding]], [[Learning-based Retriever]], [[Graph]]

#retriever #learning #gnn #deep
