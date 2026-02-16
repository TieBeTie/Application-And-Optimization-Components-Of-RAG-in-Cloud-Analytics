# PTQ — Post-Training Quantization

## Intuition

Model is already trained. We compress it without retraining — only a few hundred calibration samples needed.

## Definition

[[Quantization]] of fixed (already trained) weights. The training process is not involved.

$$W_{\text{trained}} \xrightarrow{\text{quant}} \hat{W}$$

### Example

GPTQ quantizes OPT-175B in 4.2h on a single A100, using 128 random 2048-token segments from C4 as calibration data.

## Methods

| Method | Approach | Scale |
|--------|----------|-------|
| RTN | Round to nearest | Any (but poor at $\leq$ 4-bit) |
| AdaRound | Data-dependent rounding | $\leq 100$M |
| BRECQ | Block reconstruction + Fisher info | $\leq 100$M |
| [[OBQ]] | Second-order, greedy per-weight | $\leq 100$M |
| [[GPTQ Algorithm]] | Second-order, column-wise | 175B+ |

### RTN (Round-To-Nearest)

Simplest: $\hat{w} = \text{round}(w)$ to nearest grid point. No error compensation.

Works at 8-bit. Collapses at $\leq$ 3-bit on large models.

### Second-order methods

Use [[Hessian Matrix]] to compensate: when quantizing $w_q$, adjust remaining weights to minimize output error. See [[OBQ]], [[GPTQ Algorithm]].

See also: [[Quantization]], [[QAT]], [[Layer-wise Quantization]]

#inference #quantization
