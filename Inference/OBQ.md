# OBQ — Optimal Brain Quantization

## Intuition

When you quantize one weight, the error can be compensated by adjusting the remaining weights. OBQ finds the optimal adjustment using second-order information.

Generalizes Optimal Brain Surgeon (OBS, pruning) to quantization.

## Definition

A greedy weight-by-weight [[Quantization]] method that solves the [[Layer-wise Quantization]] problem using the inverse [[Hessian Matrix]].

For each row $w$ independently:
- Pick weight $w_q$ with least quantization error (greedy)
- Quantize $w_q$, update all remaining weights $F$ to compensate

## Theorem: optimal update

### Intuition

Constrained optimization — minimize total error subject to "weight $q$ is quantized."

### Statement and proof

The objective per row $w$ is quadratic: $\mathcal{L} = \frac{1}{2}\delta_w^T H \,\delta_w$ (Taylor expansion at trained weights, gradient $\approx 0$).

**Constraint:** quantize weight $q$ to grid value, i.e. $e_q^T \delta_w + (w_q - \text{quant}(w_q)) = 0$.

**Lagrangian:**

$$\mathcal{L}_q = \frac{1}{2}\delta_w^T H\, \delta_w + \lambda\left(e_q^T \delta_w + w_q - \text{quant}(w_q)\right)$$

**Solve.** $\nabla_{\delta_w} \mathcal{L}_q = 0$:

$$H\,\delta_w + \lambda e_q = 0 \quad \Rightarrow \quad \delta_w = -\lambda H^{-1} e_q$$

Substitute into constraint:

$$-\lambda [H^{-1}]_{qq} + (w_q - \text{quant}(w_q)) = 0 \quad \Rightarrow \quad \lambda = \frac{w_q - \text{quant}(w_q)}{[H^{-1}]_{qq}}$$

**Optimal update:**

$$\boxed{\delta_F = -\frac{w_q - \text{quant}(w_q)}{[H^{-1}_F]_{qq}} \cdot (H^{-1}_F)_{:,q}}$$

**Saliency** (error from quantizing $w_q$):

$$\mathcal{L}_q = \frac{1}{2}\frac{(w_q - \text{quant}(w_q))^2}{[H^{-1}_F]_{qq}}$$

**Greedy selection** — pick $w_q$ with minimal saliency:

$$\boxed{w_q = argmin_{w_q} \frac{(\text{quant}(w_q) - w_q)^2}{[H^{-1}_F]_{qq}}} \quad \blacksquare$$

## Theorem: Hessian inverse update

### Intuition

After quantizing $w_q$, we need $H^{-1}$ without row/column $q$. Schur complement gives this in $O(d_{col}^2)$ instead of recomputing $H^{-1}$ from scratch.

### Statement and proof

**Claim.** $H^{-1}_{-q} = \left(H^{-1} - \frac{1}{[H^{-1}]_{qq}} H^{-1}_{:,q} H^{-1}_{q,:}\right)_{-p}$

**Proof.** Partition $H^{-1}$ around index $q$:

$$H^{-1} = \begin{pmatrix} [H^{-1}]_{qq} & H^{-1}_{q,F} \\ H^{-1}_{F,q} & H^{-1}_{FF} \end{pmatrix}$$

The Schur complement of $[H^{-1}]_{qq}$ in $H^{-1}$ gives:

$$H^{-1}_{-q} = H^{-1}_{FF} - \frac{1}{[H^{-1}]_{qq}} H^{-1}_{F,q}\, H^{-1}_{q,F}$$

which is exactly the formula above restricted to indices $F$. $\blacksquare$

## Properties

### Complexity

$$O(d_{row} \cdot d_{col}^3)$$

Cubic in columns $\Rightarrow$ feasible for $\leq 100$M parameters ($\approx 1$h for ResNet-50).

Infeasible for LLMs ($d_{col} \sim 10^4$, billions of parameters).

### Bottlenecks

| Problem | Why |
|---------|-----|
| Greedy order | Each row picks different order $\Rightarrow$ $d_{row} \times d_{col}$ Hessian updates |
| Sequential updates | Low compute-to-memory ratio, GPU underutilized |
| Numerical instability | Repeated Gaussian elimination $\Rightarrow$ $H^{-1}$ becomes indefinite |

All three solved by [[GPTQ Algorithm]].

See also: [[Layer-wise Quantization]], [[Hessian Matrix]], [[GPTQ Algorithm]]

#inference #quantization
