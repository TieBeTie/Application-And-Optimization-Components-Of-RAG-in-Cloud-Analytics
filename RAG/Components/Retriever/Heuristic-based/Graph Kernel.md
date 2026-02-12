# Graph Kernel

Compare entire graphs by computing similarity between their structures.

> Instead of searching edges/nodes → compare whole graphs.

## Idea

Kernel function $K(G_1, G_2)$ = inner product measuring graph similarity.

$$K(G_1, G_2) = \langle \phi(G_1), \phi(G_2) \rangle$$

Where $\phi$ maps graph to feature vector.

## Methods

### 1. Random Walk Kernel

Count common paths produced by random walks on two graphs.

```
Graph 1: A → B → C
Graph 2: X → Y → Z

Random walk on both → count matching paths
```

### 2. Weisfeiler-Lehman (WL) Kernel

Iteratively relabel nodes based on neighbor labels, then compare.

```
Iteration 0: original labels
Iteration 1: label = hash(original + sorted(neighbor_labels))
Iteration 2: repeat...

Compare: count shared subtree patterns
```

**Complexity:** $O(h \cdot m)$ where $h$ = iterations, $m$ = edges

## When to use

| Use case | Why |
|----------|-----|
| Molecule similarity | Compare chemical structures |
| Document retrieval | Query graph vs document graph |
| Subgraph matching | Find similar substructures |

## Example

```
Query graph: (Einstein) → [won] → (Nobel Prize)
Document graph: (Curie) → [won] → (Nobel Prize)

WL Kernel:
- Both have pattern: (Person) → [won] → (Award)
- Similarity: high
```

## Limitations

- Comparing labels by equality is rigid
- May miss semantic similarities

See also: [[Retriever]], [[Vector Similarity]], [[Graph]]

#retriever #heuristic
