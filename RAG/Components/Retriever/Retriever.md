# Retriever $\Omega^{Retriever}$

Retrieve content $C$ from [[Graph]] $G$ based on processed query $\hat{Q}$.

$$C = \Omega^{Retriever}(\hat{Q}, G)$$

## Input / Output

- **Input:** $\hat{Q}$ (from [[Query Processor]]), [[Graph]] $G$
- **Output:** $C$ — retrieved content (subgraph, nodes, chunks)

## Classification

| Type | Methods | When to use |
|------|---------|-------------|
| [[Heuristic-based Retriever]] | Rules, traversal, kernels | Structured data, clear patterns |
| [[Learning-based Retriever]] | Embeddings, GNN | Semantic search, dynamic graphs |
| [[Advanced Retrieval Strategies]] | Integrated, Iterative, Adaptive | Complex multi-hop queries |

## Advanced Methods

- [[Integrated Retrieval]] — Heuristic + Learning (neural-symbolic)
- [[Iterative Retrieval]] — ToG, KGP, StructGPT
- [[Adaptive Retrieval]] — decide when/how much to retrieve

## Learning-based Methods

- [[Shallow Embedding]] — [[DeepWalk]], [[Node2Vec]], [[Role2Vec]]
- [[Deep Embedding]] — [[GNN]] (inductive, uses features)

## Heuristic-based Methods

- [[Entity Linking]] — map entities to nodes
- [[Relation Matching]] — map relations to edges
- [[RAG Traversal]] — BFS, DFS, L-hop
- [[Graph Kernel]] — compare graph structures
- [[Domain Expertise]] — domain-specific rules

## Trade-offs

| Method | ✅ Pros | ❌ Cons |
|--------|---------|---------|
| Heuristic | Fast, interpretable | Rigid, needs expertise |
| Learning | Flexible, semantic | Slow, needs training |

See also: [[GraphRAG query process]], [[Query Processor]], [[Organizer]], [[Graph]]

#retriever
