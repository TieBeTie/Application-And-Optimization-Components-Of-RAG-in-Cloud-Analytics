# KGoT — Knowledge Graph of Thoughts

**Paper:** [Knowledge Graph of Thoughts](https://arxiv.org/abs/2504.02670)

## What is it?

LLM structures reasoning into a dynamic KG, enhanced by external tools.

> Not RAG (no pre-built KG). LLM builds KG from scratch per task.

## Architecture

| Component | Role |
|-----------|------|
| LLM Graph Executor | Plan: what info is missing? |
| LLM Tool Executor | Execute: call web/python/APIs |
| KG (Neo4j) | Store: triples accumulate |
| Majority voting | Decide: enhance or solve? |

## Pipeline

$$\text{Task} \xrightarrow{\text{iterate}} KG_{thoughts} \xrightarrow{\text{extract}} \text{Answer}$$

Each iteration: vote → enhance (add triples) or solve (extract answer).

## Key findings

- Python queries > SPARQL (LLMs struggle with SPARQL)
- Smaller models + KGoT ≈ larger models without KGoT
- Dynamic KG > static KG for complex multi-step tasks

## Relation to RAG components

| RAG component | KGoT equivalent |
|---------------|-----------------|
| [[Query Decomposition]] | Enhance path (split into subproblems) |
| [[Query Expansion]] | Tools add knowledge |
| [[Query Structuration]] | [[Structured Reasoning]] |
| [[Retriever]] | Cypher/Python queries to KG |

See also: [[Structured Reasoning]], [[Query Structuration]]

#article #kgot #reasoning
