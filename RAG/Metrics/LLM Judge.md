# LLM Judge

## Intuition
Replaces human annotation with an LLM evaluator scoring answer quality on axes that string-matching metrics cannot capture.

## Definition

Given a query $q$ and answer $a$, the judge scores four criteria on $[1, 10]$:

| Criterion | What it measures |
|-----------|-----------------|
| Comprehensiveness | fraction of question aspects covered |
| Empowerment | answer enables informed decisions |
| Diversity | varied perspectives and angles |
| Overall | combined quality |

$$\text{score}_k = \frac{1}{n}\sum_{i=1}^{n} s_{k,i}, \quad k \in \{\text{Comp, Emp, Div, Overall}\}$$

At `temperature=0` all $n$ runs are identical — $n=1$ suffices.

## Properties

### Component
Generator. Measures output quality independent of retrieval.

### Empowerment — document RAG example
For a financial doc: "revenue 167B RUB, +5% vs Q3" scores high — a reader can act on it. A vague "revenue increased" scores low.

### Limitation — Diversity in document RAG
Diversity was introduced in the GraphRAG paper for knowledge-graph QA, where an answer should synthesize multiple community clusters. For single-document or homogeneous financial reports, low Diversity reflects the nature of the corpus, not retrieval quality. Report Diversity scores with this caveat in the thesis.

### Calibration
An LLM judge is calibrated for a domain iff its scores correlate with human scores on a golden set.

**Protocol.** Collect $\geq 30$ human-annotated $(q, a, s^*)$ triples where $s^* \in [1,10]$ is the human score. Compute Spearman $\rho$ between judge scores and $s^*$. Accept the judge iff $\rho \geq 0.7$.

If $\rho < 0.7$: adjust the judge prompt, switch models, or add domain-specific rubric examples.

Calibration must be re-run if the judge model or prompt changes.

### Relationship to other metrics
LLM Judge captures fluency and reasoning quality; [[Faithfulness]] and [[Groundedness]] capture factual grounding. A high Overall score with low Groundedness indicates a fluent but hallucinated answer.

#rag #metrics #llm-judge
