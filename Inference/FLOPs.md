# FLOPs

## Intuition

Count of arithmetic operations — hardware-independent measure of how expensive an algorithm is.

## Definition

The total number of floating-point operations ($+, -, \times, /$) required to execute a computation.

$$\text{FLOPs} = \text{total count of float operations}$$

### Example

Matrix multiply $A \in \mathbb{R}^{m \times n}$, $B \in \mathbb{R}^{n \times k}$:

$$\text{FLOPs}(AB) = 2mnk$$

($n$ multiplications + $n$ additions per output element, $mk$ elements).

## Properties

### FLOPs vs FLOPS

| Term | Meaning | Measures |
|------|---------|----------|
| FLOPs | Floating-point operations (count) | Algorithm cost |
| FLOPS | FLOPs per second | Hardware speed |

### MACs

One MAC (Multiply-Accumulate) = one $\times$ and one $+$:

$$\text{FLOPs} = 2 \times \text{MACs}$$

### GPU-hours

Wall-clock cost $\approx$ FLOPs / FLOPS. Hardware-dependent.

| Operation | GPU-hours (A100) |
|-----------|------------------|
| [[GPTQ Algorithm]] on OPT-175B | 4.2h |
| Training OPT-175B | $\sim 10^5$ |

> GPU-hours are not rigorous (depend on hardware, implementation, memory bandwidth). FLOPs are hardware-independent but don't capture memory bottlenecks.

See also: [[Quantization]], [[Perplexity]]

#inference #metrics
