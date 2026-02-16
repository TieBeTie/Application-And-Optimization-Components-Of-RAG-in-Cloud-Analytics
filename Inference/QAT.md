# QAT — Quantization-Aware Training

## Intuition

Instead of quantizing after training, simulate quantization during training so the model learns to work with low-precision weights.

## Definition

[[Quantization]] during training. Fake quantization nodes (QDQ) are inserted into the forward pass:

$$\tilde{w} = \text{dequant}(\text{quant}(w))$$

Weights stay in FP16/FP32 but pass through quant $\to$ dequant, introducing quantization noise $\varepsilon = \tilde{w} - w$. The model adapts its weights to minimize loss under this noise.

### Example

$$w \xrightarrow{\text{quant}} \hat{w} \in \mathcal{Q} \xrightarrow{\text{dequant}} \tilde{w} = w + \varepsilon$$

The model trains on $\tilde{w}$, so at deployment the real quantization $w \to \hat{w}$ causes minimal accuracy loss.

## Properties

### Straight-Through Estimator (STE)

**Problem.** $\text{quant}(w) = \text{round}(w)$ is piecewise constant $\Rightarrow$ $\frac{\partial\, \text{quant}}{\partial w} = 0$ a.e. $\Rightarrow$ backpropagation breaks.

**Solution.** Replace the zero derivative with a surrogate in the backward pass:

$$\frac{\partial \tilde{w}}{\partial w} := 1 \quad \text{(treat quant as identity during backprop)}$$

Then the gradient flows through:

$$\frac{\partial \mathcal{L}}{\partial w} := \frac{\partial \mathcal{L}}{\partial \tilde{w}}$$

> STE is a heuristic, not an exact gradient. But it can be shown that the resulting coarse gradient is a descent direction for the population loss.

### Cost

Requires full training/fine-tuning $\Rightarrow$ impractical for LLMs ($10^5$–$10^6$ GPU-hours).

Higher accuracy than [[PTQ]], but does not scale beyond $\sim 1$B parameters.

See also: [[Quantization]], [[PTQ]]

#inference #quantization
