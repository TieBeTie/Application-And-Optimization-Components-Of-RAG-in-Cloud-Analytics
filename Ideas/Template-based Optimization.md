# Template-based Optimization

**Status:** Idea 💡

## Hypothesis

Use **predefined templates** in each RAG component for domain-specific tasks.

> If not building general AGI, but specific GraphRAG — templates are valid optimization.

## Where templates can be used

| Component               | Template usage              |
| ----------------------- | --------------------------- |
| [[Query Processor]]     | Query structure templates   |
| [[Query Expansion]]     | Context expansion patterns  |
| [[Query Decomposition]] | Sub-query splitting rules   |
| [[Retriever]]           | Search patterns for domain  |
| [[Organizer]]           | Result formatting templates |
| [[Generator]]           | Answer generation prompts   |

## Example

Domain: Medical RAG

```
Query Template: "What are symptoms of {disease}?"
Expansion Template: + "treatment" + "causes" + "risk factors"
Answer Template: "Symptoms include: ... Treatment: ..."
```

## Trade-offs

| ✅ Pros | ❌ Cons |
|---------|---------|
| Higher accuracy for domain | Not general purpose |
| Faster (no LLM reasoning) | Maintenance of templates |
| Predictable output | Rigid, less flexible |

## Questions

- How to design templates for specific domain?
- Can templates be learned/generated automatically?
- Hybrid: templates + LLM fallback?

See also: [[Query Expansion]], [[Query Processor]], [[Generator]]

#idea #optimization #templates #question 