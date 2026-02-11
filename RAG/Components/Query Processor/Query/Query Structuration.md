# Query Structuration

Convert natural language [[Query]] $Q$ to structured query language.

## Output formats

- SQL, Spark SQL (relational DBs)
- SPARQL (RDF graphs)
- Cypher (Neo4j)
- GraphQL

## When to use?

| Data source | Search method |
|-------------|---------------|
| Vector DB | [[Vector Similarity]] — no structuration needed |
| Relational DB | SQL — **structuration needed** |
| Graph DB (Neo4j) | Cypher — **structuration needed** |

> Used when querying structured databases directly, not vector search.

## How it works

Fine-tuned models (Text-to-SQL) generate structured queries from NL.

## Example

Query: "Who directed Inception?"
→ Cypher: `MATCH (m:Movie {title: 'Inception'})-[:DIRECTED_BY]->(d) RETURN d.name`

See also: [[Query Processor]], [[Query Decomposition]]

#query-processing
