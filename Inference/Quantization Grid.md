# Quantization Grid

## Intuition

The set of allowed values that quantized weights can take. Choice of grid determines the tradeoff between expressiveness and compression.

## Definition

A finite set $\mathcal{Q} = \{q_1, \ldots, q_{2^b}\} \subset \mathbb{R}$ that discretizes the weight space.

$$\text{quant}(w) = argmin_{q \in \mathcal{Q}} |w - q|$$

## Properties

### Uniform vs Non-uniform

| Type | Grid spacing | When to use |
|------|-------------|-------------|
| Uniform | $q_{i+1} - q_i = \text{const}$ | Default, hardware-friendly |
| Non-uniform | Variable spacing | Better for skewed distributions |

### Symmetric vs Asymmetric

| Type | Zero point | Utilization |
|------|-----------|-------------|
| Symmetric | $z = 0$ (grid centered at 0) | Simpler, but wastes 1 bit if weights are biased (e.g. after ReLU) |
| Asymmetric | $z \neq 0$ (grid shifted) | Full range utilized |

**Uniform asymmetric** (used in GPTQ):

$$\hat{w} = \text{round}\left(\frac{w - w_{\min}}{w_{\max} - w_{\min}} \cdot (2^b - 1)\right) \cdot \frac{w_{\max} - w_{\min}}{2^b - 1} + w_{\min}$$

### Granularity

| Granularity | Scale/zero-point shared across |
|-------------|-------------------------------|
| Per-tensor | Entire weight matrix |
| Per-channel (per-row) | One row of $W$ |
| Per-group ($g$) | $g$ consecutive weights |

Finer granularity $\Rightarrow$ better accuracy, more storage for parameters.

### Example

$b = 2$, symmetric: $\mathcal{Q} = \{-3, -1, 1, 3\} \cdot s$ where $s = \frac{w_{\max}}{2^b - 1}$.

$b = 2$, asymmetric: $\mathcal{Q} = \{w_{\min},\ w_{\min} + \Delta,\ w_{\min} + 2\Delta,\ w_{\max}\}$ where $\Delta = \frac{w_{\max} - w_{\min}}{3}$.

See also: [[Quantization]], [[PTQ]], [[GPTQ Algorithm]]

#inference #quantization
