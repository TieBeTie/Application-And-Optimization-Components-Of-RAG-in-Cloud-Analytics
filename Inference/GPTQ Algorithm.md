# GPTQ Algorithm

## Intuition

[[OBQ]] is accurate but cubic — too slow for LLMs. GPTQ makes three observations that give $\sim 10^3\times$ speedup without losing accuracy.

## Definition

An optimization of [[OBQ]] for large-scale [[Layer-wise Quantization]].

$$O(d_{row} \cdot d_{col}^3) \xrightarrow{\text{GPTQ}} O(\max\{d_{row} \cdot d_{col}^2,\ d_{col}^3\})$$

## Theorem 1: arbitrary order

### Intuition

Greedy order (pick easiest weight first) barely helps on large layers. Fixed column order lets all rows share the same $H^{-1}$.

### Statement and proof

Quantize all rows in the **same column order** instead of greedy per-row.

OBQ: each row picks its own greedy order $\Rightarrow$ $d_{row}$ independent $H^{-1}$ update sequences, each of length $d_{col}$.

$$T_{\text{OBQ}} = d_{row} \cdot \underbrace{d_{col} \cdot O(d_{col}^2)}_{\text{Eq. 3 per row}} = O(d_{row} \cdot d_{col}^3)$$

GPTQ: all rows share the same column order. $H^{-1}_F$ depends only on $X_F$ (not on weights) $\Rightarrow$ one update sequence for all rows:

$$T_{\text{GPTQ}} = \underbrace{d_{col} \cdot O(d_{col}^2)}_{H^{-1} \text{ updates}} + \underbrace{d_{row} \cdot d_{col} \cdot O(d_{col})}_{\delta_F \text{ per row per col}} = O(\max\{d_{col}^3,\, d_{row} \cdot d_{col}^2\})$$

Speedup: $\times \min\{d_{row}, d_{col}\}$. $\blacksquare$

## Theorem 2: lazy batch updates

### Intuition

Rounding decision for column $j$ depends only on updates to column $j$ itself. Updates to later columns can be deferred and applied in one batch.

### Statement and proof

Process $B = 128$ columns at a time. Let $Q = \{i, \ldots, i+B-1\}$ be the block indices. Apply [[OBQ]] update for each $q \in Q$ sequentially inside the block, then combine all deferred updates:

$$\boxed{\delta_F = -(w_Q - \text{quant}(w_Q))\,([H^{-1}_F]_{QQ})^{-1}\,(H^{-1}_F)_{:,Q}}$$

**Proof.** Single-weight update: $\delta_F^{(q)} = -\frac{w_q - \text{quant}(w_q)}{[H^{-1}_F]_{qq}} (H^{-1}_F)_{:,q}$.

Stacking all $q \in Q$ and accounting for sequential dependencies within the block, the accumulated error vector $(w_Q - \text{quant}(w_Q))$ propagates through the $B \times B$ submatrix $[H^{-1}_F]_{QQ}$. Inverting this submatrix replaces the sequential single-weight divisions. $\blacksquare$

Global update of $W$ and $H^{-1}$ only after each block $\Rightarrow$ same FLOPs, but memory-bound $\to$ compute-bound.

## Property 3: Cholesky reformulation

Precompute all needed rows of $H^{-1}$ via [[Cholesky Decomposition]] instead of iterative Gaussian elimination.

$$H^{-1} \xrightarrow{\text{Cholesky}} L, \quad \text{read row } q \text{ from } L$$

Combined with dampening: $H \leftarrow H + \lambda I$, $\lambda = 0.01 \cdot \overline{\text{diag}(H)}$.

## Algorithm

```
Input: W, H⁻¹ = (2XX^T + λI)⁻¹, block size B
L ← Cholesky(H⁻¹)^T

for i = 0, B, 2B, ... do
    for j = i, ..., i+B-1 do
        Q[:,j] ← quant(W[:,j])
        E[:,j-i] ← (W[:,j] - Q[:,j]) / [H⁻¹]_jj
        W[:,j:(i+B)] -= E[:,j-i] · H⁻¹[j, j:(i+B)]
    end
    W[:,(i+B):] -= E · H⁻¹[i:(i+B), (i+B):]
end
```

### Example (results)

| Model | Time | Bits | [[Perplexity]] (Wiki2) | vs FP16 |
|-------|------|------|-------------|---------|
| OPT-175B | 4.2h | 4 | 8.37 | +0.03 |
| OPT-175B | 4.2h | 3 | 8.68 | +0.34 |
| BLOOM-176B | 3.8h | 4 | 8.21 | +0.10 |
| BLOOM-176B | 3.8h | 3 | 8.64 | +0.53 |

Speedup at inference: $3.25\times$ (A100), $4.5\times$ (A6000).

OPT-175B at 3-bit fits in a single A100 (63 GB).

See also: [[OBQ]], [[Quantization]], [[Hessian Matrix]], [[Cholesky Decomposition]]

#inference #quantization
