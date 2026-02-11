# Iterative Retrieval

Multi-step retrieval where each step depends on previous results.

## Dependencies

| Type | Description |
|------|-------------|
| Causal | Step B needs result of step A |
| Resource | Shared data between steps |
| Temporal | Order matters |

## Key Algorithms

### ToG (Think-on-Graph)

LLM as agent exploring KG interactively.

```
1. Start with query entities
2. Beam search on KG
3. LLM evaluates promising paths
4. Iterate until answer found
```

**Paper:** [Think-on-Graph](https://arxiv.org/abs/2407.10805)

### ToG-2 (Think-on-Graph 2.0)

Hybrid: alternates between graph retrieval and document retrieval.

```
1. Graph retrieval → find entities
2. Context retrieval → get documents
3. Alternate until sufficient info
```

**SOTA on 6/7 knowledge-intensive datasets.**

### KGP (Knowledge Graph Prompting)

For multi-document QA.

```
1. Build KG from passage similarity
2. Select seed nodes (similarity to context)
3. LLM summarizes neighboring nodes
4. Update context, iterate
```

### StructGPT

Pre-defined graph interfaces + LLM invocation.

```
1. Define graph functions (get_neighbors, find_path, etc.)
2. LLM decides which function to call
3. Execute function, get result
4. LLM decides next step or answer
```

## Comparison

| Method | Strategy | LLM role |
|--------|----------|----------|
| ToG | Beam search | Evaluate paths |
| ToG-2 | Hybrid graph+docs | Guide retrieval |
| KGP | Seed expansion | Summarize context |
| StructGPT | Function calling | Invoke interfaces |

## Trade-offs

| ✅ Pros | ❌ Cons |
|---------|---------|
| Higher accuracy | Higher latency |
| Handles multi-hop | More LLM calls |
| Progressive refinement | Complex to implement |

## Example

```
Query: "Fight song of university in Lawrence, KS with KC branch?"

ToG iteration:
1. Find: Lawrence, Kansas → University of Kansas
2. Check: KC branch? → Yes ✓
3. Find: fight song → "I'm a Jayhawk"
4. Answer: "I'm a Jayhawk"
```

See also: [[Graph Traversal]], [[GNN]], [[Advanced Retrieval Strategies]]

#retriever #advanced #iterative
