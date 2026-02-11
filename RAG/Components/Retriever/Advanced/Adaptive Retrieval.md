# Adaptive Retrieval

Decide **when** and **how much** external knowledge to retrieve.

## Problem

Retrieved knowledge can be:
- ✅ Helpful — adds missing info
- ❌ Redundant — LLM already knows
- ❌ Conflicting — contradicts internal knowledge

## Solution: Knowledge Checking

Assess if retrieval is needed before doing it.

```
Query → Check internal knowledge → Sufficient?
                                      ↓
                               Yes: Answer directly
                               No:  Retrieve → Answer
```

## Adaptive Depth in GraphRAG

| Problem | Solution |
|---------|----------|
| Too few hops | Miss critical relations |
| Too many hops | Introduce noise |

**Approach:** Train model to predict required hops for query.

```
Query → Predict hops (1? 2? 3?) → Retrieve with L=predicted
```

**Papers:** Guo et al., Wu et al.

## Types of Adaptation

| What adapts | How |
|-------------|-----|
| Retrieval trigger | Check if LLM knows answer |
| Retrieval depth | Predict required hops |
| Retrieval amount | Predict k for top-k |

## Open Problem ⚠️

> Resolving knowledge conflicts in GraphRAG — no existing works yet.

When retrieved knowledge contradicts LLM's internal knowledge:
- Which to trust?
- How to reconcile?

**Future work direction.**

## Example

```
Query 1: "What is 2+2?"
→ LLM knows → No retrieval needed

Query 2: "Latest stock price of Apple?"
→ LLM doesn't know (dynamic) → Retrieve

Query 3: "Einstein's birthplace?"
→ LLM might know → Check confidence
→ Low confidence → Retrieve to verify
```

## Trade-offs

| ✅ Pros | ❌ Cons |
|---------|---------|
| Reduces unnecessary retrieval | Extra inference step |
| Avoids conflicts | Hard to calibrate |
| More efficient | May skip needed retrieval |

See also: [[Advanced Retrieval Strategies]], [[Graph Traversal]]

#retriever #advanced #adaptive
