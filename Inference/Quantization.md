# Quantization

## Intuition

Large models store weights in FP16 (16 bits). Most of these bits are redundant. Quantization compresses weights to fewer bits with minimal accuracy loss.

## Definition

A mapping of full-precision weights to a discrete grid with fewer bits.

$$W \in \mathbb{R} \xrightarrow{\text{quant}} \hat{W} \in \{q_1, q_2, \ldots, q_{2^b}\}$$

where $b$ — target number of bits.

Two types, depending on when quantization is applied:

- **[[PTQ]]** (Post-Training Quantization) — quantization of fixed (already trained) weights.
- **[[QAT]]** (Quantization-Aware Training) — quantization during training, weights continue to update.

### Example

OPT-175B: 175B params $\times$ 16 bits = 326 GB. At $b = 4$: 326 $\times \frac{4}{16}$ $\approx$ 82 GB $\Rightarrow$ fits on a single A100 (80 GB).

## Properties

### PTQ vs QAT

|          | QAT | PTQ |
| -------- | --- | --- |
| Cost ([[FLOPs]])    | Full retraining | Hours, few thousand samples |
| Accuracy ([[Perplexity]]) | Higher | Lower (but improving) |
| Scale    | Limited by training cost | Scales to 175B+ |

> For LLMs, retraining costs $10^5$–$10^6$ GPU-hours $\Rightarrow$ PTQ is the only practical option.

See also: [[PTQ]], [[QAT]], [[Quantization Grid]], [[Layer-wise Quantization]], [[Perplexity]], [[FLOPs]]

#inference #quantization
