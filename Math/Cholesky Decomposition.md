# Cholesky Decomposition

## Intuition

Factorize a matrix into "square root" form $A = LL^T$. Cheaper and more stable than LU for symmetric positive definite matrices.

## Definition

A factorization of a symmetric positive definite (SPD) matrix $A \in \mathbb{R}^{n \times n}$ into:

$$A = LL^T$$

where $L$ is lower triangular with positive diagonal entries.

### Example

$$A = \begin{pmatrix} 4 & 2 \\ 2 & 5 \end{pmatrix}$$

$L_{11} = \sqrt{4} = 2, \quad L_{21} = \frac{2}{2} = 1, \quad L_{22} = \sqrt{5 - 1} = 2$

$$L = \begin{pmatrix} 2 & 0 \\ 1 & 2 \end{pmatrix}, \quad LL^T = \begin{pmatrix} 4 & 2 \\ 2 & 5 \end{pmatrix} = A \quad \checkmark$$

## Properties

### Requirements

| Condition | Necessary? |
|-----------|------------|
| Symmetric ($A = A^T$) | Yes |
| Positive definite ($x^T A x > 0\ \forall x \neq 0$) | Yes |

> If $A$ is positive **semi**-definite, decomposition exists but $L$ may have zeros on diagonal (not unique).

### Complexity

$O\!\left(\frac{n^3}{3}\right)$ — half the cost of LU decomposition.

## Theorem: existence and uniqueness

### Intuition

SPD guarantees that every sub-block is also SPD, so the recursive factorization never breaks (no negative square roots).

### Statement

$A$ SPD $\Rightarrow$ $\exists!$ lower triangular $L$ with $L_{jj} > 0$ such that $A = LL^T$.

### Proof

By induction on $n$.

*Base:* $n=1$. $A = (a_{11})$, $a_{11} > 0$. Take $L = (\sqrt{a_{11}})$.

*Step:* Partition $A$ as:

$$A = \begin{pmatrix} a_{11} & v^T \\ v & A' \end{pmatrix}, \quad a_{11} > 0 \text{ (SPD } \Rightarrow \text{ diagonal entries positive)}$$

Ansatz $L = \begin{pmatrix} l_{11} & 0 \\ w & L' \end{pmatrix}$. Then $LL^T = A$ gives:

$$l_{11} = \sqrt{a_{11}}, \quad w = \frac{v}{l_{11}}, \quad L'L'^T = A' - ww^T$$

Need $A' - ww^T$ SPD. For any $x \neq 0$:

$$x^T(A' - ww^T)x = \begin{pmatrix} -w^Tx/l_{11} \\ x \end{pmatrix}^T A \begin{pmatrix} -w^Tx/l_{11} \\ x \end{pmatrix} > 0$$

since $A$ is SPD. By induction, $L'$ exists and is unique. $\blacksquare$

### Algorithm (from the proof)

Entries of $L$ computed column by column:

$$L_{jj} = \sqrt{A_{jj} - \sum_{k=1}^{j-1} L_{jk}^2}$$

$$L_{ij} = \frac{1}{L_{jj}} \left(A_{ij} - \sum_{k=1}^{j-1} L_{ik} L_{jk}\right), \quad i > j$$

The square root is always real ($A_{jj} - \sum L_{jk}^2 > 0$ by SPD of the Schur complement at each step).

## In GPTQ

[[Hessian Matrix]] inverse $H^{-1}$ becomes indefinite after repeated row/column removals via Gaussian elimination $\Rightarrow$ catastrophic quantization errors.

Fix: precompute $\text{Cholesky}(H^{-1})^T$ once, read off rows as needed.

$$H^{-1} \xrightarrow{\text{Cholesky}} L \quad \Rightarrow \quad \text{row } q \text{ of } H^{-1}_{F_q} \text{ read from } L$$

Combined with dampening ($H \leftarrow H + \lambda I$, $\lambda = 0.01 \cdot \text{mean}(\text{diag}(H))$) — robust at billion-parameter scale.

See also: [[Hessian Matrix]], [[GPTQ Algorithm]]

#math #quantization
