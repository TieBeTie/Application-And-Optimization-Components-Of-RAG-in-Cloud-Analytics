# Construction Protocol

## Intuition
The order of steps is not arbitrary — it follows from [[Evaluation Agents]] independence requirements. Anchors must exist before any system runs; the Judge must be calibrated before scores are trusted.

## Definition
A construction protocol for [[Eval Dataset]] is a sequence of steps that guarantees [[Evaluation Agents]] independence and [[Question Taxonomy]] coverage.

## Protocol

**Step 1 — Human golden set**
Annotator reads source documents with no RAG system running. Writes 30–50 queries across all types from [[Question Taxonomy]], following [[Annotator Guide]] for density and anchor extraction rules. Corpus must satisfy [[Corpus Design]] diversity requirements. For each query: pastes verbatim anchor strings from the document.

*Why first:* anchors must predate any Generator run — required by [[Evaluation Agents]] Property 1 and 3.

**Step 2 — Synthetic extension**
A different LLM (not the Generator) produces additional queries for under-represented types. Each generated triple is verified: anchor must exist verbatim in source document.

*Why after Step 1:* synthetic queries fill coverage gaps identified from the golden set distribution.

**Step 3 — Judge calibration**
Run [[LLM Judge]] on golden set queries. Compute Spearman $\rho$ between Judge scores and Annotator scores. Require $\rho \geq 0.7$ before using Judge on full dataset.

*Why after Step 2:* calibration uses the complete golden set; extending it after calibration would require re-running calibration.

**Step 4 — Anti-bias check**
Verify: (1) all anchors were extracted before any system run, (2) synthetic queries were generated from raw document text. If either fails — discard affected triples and return to Step 1.

## Minimum viable dataset for this thesis

| Type | Count | Source |
|------|-------|--------|
| Factoid, single-hop, contract | 5 | human |
| Factoid, single-hop, financial report | 5 | human |
| Multi-hop, cross-document | 5 | human |
| Paraphrase, factoid | 5 | human |
| Synthetic, mixed types | 10–20 | LLM-generated, verified |
| **Total** | **30–40** | |

Current: 10 queries (factoid, single-hop, contract only). See [[Corpus Design]] for what to add.

#rag #evaluation #protocol #dataset
