# Structured Query Language

Convert [[Query]] $Q$ into database query language.

$$Q \xrightarrow{\text{Text-to-SQL}} Q_{db}$$

## Output formats

| Language | Database type |
|----------|---------------|
| SQL, Spark SQL | Relational DB |
| SPARQL | RDF graphs |
| Cypher | Neo4j |
| GraphQL | API |

## When to use?

| Data source | Search method |
|-------------|---------------|
| Vector DB | [[Vector Similarity]] — no structuration needed |
| Relational DB | SQL — **structuration needed** |
| Graph DB (Neo4j) | Cypher — **structuration needed** |

> Not needed when using vector search.

## How it works

Fine-tuned models (Text-to-SQL) generate structured queries from NL.

> LLMs have difficulties formulating effective SPARQL queries (KGoT finding). Python-based queries show better adaptability.

## Example

```
Query: "Who directed Inception?"
→ Cypher: MATCH (m:Movie {title: 'Inception'})-[:DIRECTED_BY]->(d) RETURN d.name
```

See also: [[Query Structuration]], [[Structured Reasoning]]

#query-processing
