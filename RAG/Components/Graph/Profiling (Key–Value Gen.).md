# Profiling (Key–Value Generation)

LLM generates key-value pairs for each entity and relation in [[Graph]] $G$.

$$\{e_j\} \cup \{r_{jk}\} \xrightarrow{\text{LLM}} (K, V)$$

## Structure

| | Key (index) | Value |
|-|-------------|-------|
| **Entity** | Entity name (1 key) | Summary paragraph from data |
| **Relation** | Multiple keys from LLM | Summary paragraph from data |

## Why entities have 1 key?

Entity = concrete thing → name is unique identifier.

```
Entity: "Einstein"
Key: ["Einstein"]
Value: "Albert Einstein, physicist, developed theory of relativity..."
```

## Why relations have multiple keys?

Relation = abstract connection → one word cannot capture all contexts.

LLM generates **global themes** from connected entities.

```
Relation: Einstein → works_at → Princeton

Keys: ["academic employment", "physics research", "Princeton faculty"]
Value: "Einstein worked at Princeton's IAS from 1933..."
```

Multiple keys = more entry points for [[Vector Similarity]] search.

## Persistence / Indexing

After deduplication $K \rightarrow K'$, we store:

| What | Where | Purpose |
|------|-------|---------|
| Keys from $K'$ (as embeddings) | **Vector DB** | Similarity search by query keywords |
| Mapping $K' \rightarrow G$ | **Hash map** (key → node/edge ref) | Jump from matched key to graph element |
| $G = (V, E)$ | **Graph DB** | Structural traversal, neighbors |

```
Stored indices = Vector DB(embeddings of K')
               + HashMap(K' → nodes/edges in G)
               + Graph DB(G)
```

> Vector DB finds relevant keys → HashMap resolves to graph elements → Graph DB provides structure.

## In LightRAG notation

| Symbol | Meaning |
|--------|---------|
| $\varphi(\cdot)$ | Data Indexer — builds $\hat{D}$ from $D$ |
| $\psi(\cdot)$ | Data Retriever — queries indexed data |
| $G(\cdot)$ | Generation module |

$$D \xrightarrow{\varphi} \hat{D} = (G, K')$$

See also: [[LightRAG Init]], [[LightRAG Query]], [[Graph]], [[Vector Similarity]]

#graph #indexing #lightrag
