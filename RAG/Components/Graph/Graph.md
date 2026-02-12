# Graph $G$

Graph-structured data source. Can be Knowledge Graph, Document Graph, or other graph structure.

## Definition

A graph $G = (V, E)$ where:
- $V$ — set of nodes (entities, concepts, chunks)
- $E$ — set of edges (relations between nodes)

## Types

| Type | Nodes | Edges | Example |
|------|-------|-------|---------|
| Knowledge Graph | Entities | Relations | `(Einstein, born_in, Germany)` |
| Document Graph | Text chunks | Semantic similarity | RAG systems |
| Hierarchical Graph | Communities | Containment | GraphRAG |

## Used by

- [[Retriever]] — searches in $G$ to find content $C$
- [[Organizer]] — structures content from $G$

See also: [[GraphRAG query process]]
