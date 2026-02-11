# Domain Expertise

Design retriever using domain-specific knowledge and rules.

## When needed

| Domain | Graph type | Expertise required |
|--------|------------|-------------------|
| Chemistry | Molecular graphs | Chemical bonds, reactions |
| Biology | DNA/protein graphs | Genomic patterns |
| Medicine | Medical KG | Disease-symptom relations |
| Legal | Case law graphs | Legal precedents |

## Approach

1. Domain experts define retrieval rules
2. Combine heuristic + learning-based methods
3. Use domain-specific templates

See also: [[Template-based Optimization]]

## Example: Molecular Search

```
Query: "Find molecules similar to aspirin"

Domain rules:
1. Match functional groups (-COOH, -OH)
2. Compare ring structures
3. Check molecular weight range

Result: Molecules with similar chemical properties
```

## Example: Medical RAG

```
Query: "Symptoms of diabetes"

Domain rules:
1. Start from disease node
2. Traverse "has_symptom" edges only
3. Filter by symptom severity

Result: [high blood sugar, fatigue, frequent urination]
```

## Trade-off

| ✅ Pros | ❌ Cons |
|---------|---------|
| High accuracy for domain | Not transferable |
| Interpretable rules | Requires experts |
| Fast (predefined logic) | Maintenance cost |

See also: [[Retriever]], [[Template-based Optimization]], [[Graph]]

#retriever #heuristic #domain
