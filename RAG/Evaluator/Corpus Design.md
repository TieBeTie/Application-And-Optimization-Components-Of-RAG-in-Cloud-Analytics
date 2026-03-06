# Corpus Design

## Intuition
A corpus of two identical-type documents evaluates only one failure mode. Diversity forces the system to handle different lexical registers, structures, and reasoning demands.

## Definition

A corpus $\mathcal{C} = \{d_1, \ldots, d_m\}$ is **evaluation-valid** iff it satisfies three conditions simultaneously: type diversity, size diversity, and format diversity.

## Minimum viable corpus for a thesis

| Property | Minimum | Recommended |
|----------|---------|-------------|
| Documents | 3 | 5–7 |
| Total tokens | 5 000 | 15 000–30 000 |
| Distinct document types | 2 | 3–4 |
| Multi-page documents | 1 | 2+ |
| Documents requiring cross-doc reasoning | 1 pair | 2 pairs |

## Properties

### Property 1 — Type diversity

Each document type activates a different failure mode:

| Document type | Failure mode exposed | Example |
|---------------|---------------------|---------|
| Legal contract | Entity extraction (parties, dates, clauses) | Contract № 2024-МТС-00147 |
| Financial report | Tabular reasoning, numerical comparison | МТС Q4 2023 |
| Procedural / SLA | Multi-step reasoning, condition chains | Maintenance agreement |
| FAQ / knowledge base | Paraphrase tolerance | Internal IT wiki |
| Analytical report | Open-ended synthesis across sections | Strategy document |

At least one document pair must share an entity (e.g. same company) to enable cross-document multi-hop queries.

### Property 2 — Size diversity

Documents of homogeneous length systematically miss chunking artefacts. A short document (< 500 tokens) fits in a single chunk; a long document (> 5 000 tokens) tests whether the retriever surfaces the right chunk among many.

| Size class | Token range | Role in evaluation |
|------------|-------------|-------------------|
| Short | 300–800 | Tests precision: single relevant chunk among few |
| Medium | 1 000–3 000 | Baseline; most business documents |
| Long | 5 000+ | Tests recall: answer may be in any of many chunks |

The corpus must contain at least one short and one medium document.

### Property 3 — Format diversity

Different file formats exercise different parsing paths:

| Format | Parsing risk | Present in current corpus |
|--------|-------------|--------------------------|
| `.txt` | None | Yes (contract) |
| `.csv` | Column alignment, header loss | Yes (financial report) |
| `.pdf` | OCR artefacts, table extraction | Recommended |
| `.docx` | Style stripping, footnotes | Recommended |

## Note on real vs synthetic documents

Synthetic documents (LLM-generated) introduce the same annotation bias described in [[Eval Dataset]]: the Generator has seen similar text during pretraining, inflating all metrics. **Use real or lightly anonymised documents wherever possible.**

For a thesis on cloud analytics, appropriate real documents include: SLA agreements, financial disclosures, technical specifications, internal reports.

## References
- [GaRAGe (ACL 2025)](https://arxiv.org/abs/2506.07671): 4,752 passages from private knowledge bases + 30,599 from the Web; mixed Enron emails, Arxiv abstracts, AWS DevOps guides, SEC filings
- [RARE (2025)](https://www.cs.cmu.edu/~sherryw/assets/pubs/2025-rare.pdf): 527 expert-level documents; emphasis on time-sensitive and domain-specific content

#rag #evaluation #corpus #dataset
