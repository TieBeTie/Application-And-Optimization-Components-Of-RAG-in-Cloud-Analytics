# Evaluation Metric Selection

## Intuition
Metrics chosen by intuition may miss entire failure modes or overlap unnecessarily. A systematic method guarantees that every way a system can fail is detectable and attributable to a specific component.

## Definition

A **system** $S = (C_1, \ldots, C_n)$ is a composition of components, each mapping inputs to outputs.

A **failure mode** of component $C_i$ is a distinguishable way $C_i$ produces incorrect output. Let $F_i$ be the set of failure modes of $C_i$ and $F = \bigcup_i F_i$ the full failure space.

A **metric** $m$ **detects** failure mode $f$ if:
$$\mathbb{E}[m \mid f \text{ active}] \neq \mathbb{E}[m \mid f \text{ absent}]$$

A metric set $M$ achieves **coverage** if:
$$\forall f \in F,\quad \exists\, m \in M : m \text{ detects } f$$

A metric set $M$ is **component-separable** *(coined term)* if for each pair of variable components $i \neq j$, at least one metric detects $F_i$ but not $F_j$. Required for root cause analysis.

## Method

- List components that **vary** across experiments. Fixed components require no coverage.
- For each variable component, enumerate failure modes $F_i$.
- Assign at least one metric to each $f \in F$.
- Verify component-separability across all pairs of variable components.
- Fix $M$ **before** running experiments. Post-hoc metric selection inflates apparent performance (multiple comparisons).

## Properties

### Redundancy is acceptable, gaps are not
Overlapping metrics are wasteful but harmless. An uncovered failure mode invalidates conclusions over the domain where that mode can occur.

### Component-separability enables root cause analysis
Without it, metric degradation cannot be attributed to a specific component — two different component failures produce the same signal.

## Pitfalls

| Pitfall | Description |
|---|---|
| Goodhart's Law | A metric that becomes an optimisation target ceases to measure the underlying capability. Never optimise directly on evaluation metrics. |
| Metric confounding | One metric captures multiple phenomena — improvement cannot be attributed to a specific factor. Design metrics as narrow as possible. |
| Distribution shift | Test-set metrics do not guarantee deployment performance under covariate shift. Report distribution assumptions alongside results. |
| Aggregation masking | Averaging across subgroups hides disparate performance (Simpson's paradox). Report per-subgroup results for heterogeneous data. |
| Construct invalidity | A metric may not measure the intended construct. Validate on a calibration set with known ground truth. |

## Origin

Adapted from **FMEA** (Failure Mode and Effects Analysis), formalised in MIL-STD-1629A (1980) and the AIAG-VDA automotive standard. FMEA uses a 1–10 detection score per control; the statistical framing $(\mathbb{E}[m|f] \neq \mathbb{E}[m|\neg f])$ is an adaptation for ML evaluation design.

See also: [[RAG Evaluation]] for a RAG-specific instantiation.

#evaluation #metrics #ml
