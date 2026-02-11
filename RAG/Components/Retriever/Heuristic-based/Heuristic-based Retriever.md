# Heuristic-based Retriever

Retrieval using predefined rules, algorithms, and domain knowledge.

## Methods

| Method | What it does | Link |
|--------|--------------|------|
| [[Entity Linking]] | Map entities → nodes | NER + mapping |
| [[Relation Matching]] | Map relations → edges | RE + mapping |
| [[Graph Traversal]] | Explore graph (BFS/DFS) | Path finding |
| [[Graph Kernel]] | Compare graph structures | Similarity |
| [[Domain Expertise]] | Domain-specific rules | Expert knowledge |

## Pipeline

```
Query → NER/RE → Entity Linking → Graph Traversal → Results
                 Relation Matching
```

## When to use

- Structured data with clear patterns
- Need for interpretability
- Domain expertise available

## Comparison with Learning-based

| Aspect | Heuristic | Learning |
|--------|-----------|----------|
| Speed | Fast | Slower |
| Flexibility | Rigid | Adaptive |
| Training | None | Required |
| Interpretability | High | Low |

See also: [[Retriever]], [[Named Entity Recognition]], [[Relation Extraction]]

#retriever #heuristic
