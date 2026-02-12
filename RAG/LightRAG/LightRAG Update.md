# LightRAG Incremental Update

Fast adaptation to evolving knowledge base **without full reprocessing**.

## Problem

New document $D'$ arrives → do we rebuild entire graph?

❌ Full reprocessing = expensive
✅ Incremental update = fast

## How it works

1. Process new document with same indexing function $\varphi$:

$$\hat{D}' = \varphi(D') = (\hat{V}', \hat{E}')$$

2. Union with existing graph:

$$V_{new} = \hat{V} \cup \hat{V}'$$
$$E_{new} = \hat{E} \cup \hat{E}'$$

3. Done. No reprocessing of old data.

## Why it works

Same $\varphi$ (NER, RE, [[Profiling (Key–Value Gen.)|Profiling]], dedup) ensures compatible format.

```
Existing graph:  G = (V, E)
New document:    D' → φ → (V', E')
Updated graph:   G' = (V ∪ V', E ∪ E')
```

## Comparison

| Approach | Cost | When |
|----------|------|------|
| Full rebuild | $O(n)$ all docs | Schema change |
| Incremental (LightRAG) | $O(m)$ new doc only | New data arrives |

## Complexity

$O(m)$ where $m$ = new document size. No overhead on existing data.

See also: [[LightRAG Init]], [[Graph]], [[Profiling (Key–Value Gen.)]]

#lightrag #optimization #indexing
