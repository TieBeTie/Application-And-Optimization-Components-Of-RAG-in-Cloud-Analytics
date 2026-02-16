# Perplexity

## Intuition

How "surprised" a language model is by a text. Lower = better.

## Definition

Given a sequence $x_1, \ldots, x_N$ and model $p$:

$$\text{PPL} = \exp\left(-\frac{1}{N}\sum_{i=1}^{N} \log p(x_i \mid x_{<i})\right)$$

$\text{PPL} = k$ means the model is on average choosing from $k$ equally likely tokens.

### Example

| PPL | Meaning |
|-----|---------|
| 1 | Perfect prediction |
| 10 | ~10 plausible tokens per position |
| 100 | Very uncertain |

## Properties

### Chain: Entropy → Cross-Entropy → Perplexity

**Shannon entropy** — average information in distribution $p$:

$$H(p) = -\sum_x p(x) \log p(x)$$

**Cross-entropy** — average bits when using model $q$ instead of true $p$:

$$H(p, q) = -\sum_x p(x) \log q(x) \geq H(p)$$

Equality iff $q = p$.

**Perplexity** — exponentiation of cross-entropy:

$$\text{PPL} = b^{H(p,q)}$$

With natural log ($b = e$): $\text{PPL} = e^{H(p,q)}$, which is exactly the formula above applied to the empirical distribution over the text.

### Sensitivity

PPL is sensitive to small weight perturbations — if [[Quantization]] corrupts weights, PPL spikes. More sensitive than downstream task accuracy (e.g. LAMBADA).

### Example (GPTQ)

| Model | FP16 | 4-bit | 3-bit |
|-------|------|-------|-------|
| OPT-175B | 8.34 | 8.37 | 8.68 |

4-bit [[GPTQ Algorithm]] adds only 0.03 PPL — negligible degradation.

See also: [[Quantization]], [[GPTQ Algorithm]], [[FLOPs]]

#inference #metrics
