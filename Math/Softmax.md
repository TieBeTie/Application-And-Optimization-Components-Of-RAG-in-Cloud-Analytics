# Softmax

## Intuition

Turns a vector of raw scores (logits) into a probability distribution. Larger values get exponentially more weight.

## Definition

A function $\sigma: \mathbb{R}^n \to (0,1)^n$ defined as:

$$\sigma(z)_i = \frac{e^{z_i}}{\sum_{j=1}^{n} e^{z_j}}, \quad i = 1, \ldots, n$$

### Example

$z = (2, 1, 0)$:

$$\sigma(z) = \frac{1}{e^2 + e^1 + e^0}(e^2, e^1, e^0) \approx (0.67, 0.24, 0.09)$$

Largest logit $z_1 = 2$ gets most probability mass.

## Properties

### Output is a valid probability distribution

**Claim.** $\sigma(z)_i > 0\ \forall i$ and $\sum_i \sigma(z)_i = 1$.

**Proof.** $e^{z_i} > 0\ \forall z_i \in \mathbb{R}$, so each $\sigma(z)_i > 0$. Sum:

$$\sum_{i=1}^n \sigma(z)_i = \sum_{i=1}^n \frac{e^{z_i}}{\sum_j e^{z_j}} = \frac{\sum_i e^{z_i}}{\sum_j e^{z_j}} = 1 \quad \blacksquare$$

### Translation invariance

**Claim.** $\sigma(z + c\mathbf{1}) = \sigma(z)$ for any $c \in \mathbb{R}$.

**Proof.**

$$\sigma(z + c)_i = \frac{e^{z_i + c}}{\sum_j e^{z_j + c}} = \frac{e^c \cdot e^{z_i}}{e^c \cdot \sum_j e^{z_j}} = \frac{e^{z_i}}{\sum_j e^{z_j}} = \sigma(z)_i \quad \blacksquare$$

Used in practice: subtract $\max(z)$ before computing to avoid overflow.

### Jacobian

**Claim.** The Jacobian $\frac{\partial \sigma_i}{\partial z_j} = \sigma_i(\delta_{ij} - \sigma_j)$.

**Proof.** Let $p_i = \sigma(z)_i$.

*Case $i = j$:* By quotient rule:

$$\frac{\partial p_i}{\partial z_i} = \frac{e^{z_i} \sum_j e^{z_j} - e^{z_i} \cdot e^{z_i}}{(\sum_j e^{z_j})^2} = p_i - p_i^2 = p_i(1 - p_i)$$

*Case $i \neq j$:*

$$\frac{\partial p_i}{\partial z_j} = \frac{0 - e^{z_i} \cdot e^{z_j}}{(\sum_k e^{z_k})^2} = -p_i \cdot p_j$$

Combined: $\frac{\partial p_i}{\partial z_j} = p_i(\delta_{ij} - p_j)$. $\blacksquare$

### Softmax is not injective

$\sigma$ is surjective onto the open simplex but not injective: $\sigma(z) = \sigma(z + c\mathbf{1})$ (follows from translation invariance).

See also: [[Perplexity]]

#math #activation
