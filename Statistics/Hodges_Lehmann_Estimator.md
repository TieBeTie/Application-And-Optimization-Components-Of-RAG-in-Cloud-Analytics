# Hodges–Lehmann Estimator

## Intuition
Take the median of all pairwise averages. Achieves a better breakdown point than the trimmed mean and near-optimal efficiency under normality.

## Definition
The Hodges–Lehmann estimator is called the median of all pairwise averages:

$$W_n = \mathrm{med}\!\left\{\frac{X_i + X_j}{2} : 1 \le i \le j \le n\right\}$$

The $n(n+1)/2$ pairwise averages $Y_{ij} = (X_i + X_j)/2$ are called Walsh averages.

### Examples
For $n = 3$, $X = (1, 3, 7)$: Walsh averages are $1, 2, 4, 3, 5, 7$; $W_3 = \mathrm{med} = 3.5$.

## Properties

### Breakdown Point
$\varepsilon^*(W_n) = 1 - 1/\sqrt{2} \approx 0.293$. See [[Breakdown_Point]].

**Proof.**
Let $k = \lfloor\varepsilon n\rfloor$ outliers be present. Total Walsh averages: $N = n(n+1)/2$. A Walsh average $Y_{ij}$ is uncontaminated iff both $X_i$ and $X_j$ are clean:

$$N_\text{clean} \approx \frac{[(1-\varepsilon)n]^2}{2}$$

$W_n$ fails when contaminated averages form the majority, i.e. $N_\text{clean} < N/2$:

$$(1-\varepsilon)^2 < \frac{1}{2} \implies \varepsilon > 1 - \frac{1}{\sqrt{2}}$$

Hence $\varepsilon^* = 1 - 1/\sqrt{2}$. $\square$

### Asymptotic Relative Efficiency

For $X_i \sim \mathcal{N}(\theta, \sigma^2)$:

$$\mathrm{ARE}(W_n,\, \bar X) = \frac{3}{\pi} \approx 0.955$$

$$\mathrm{ARE}(W_n,\, \tilde X) = \frac{3}{\pi} \cdot \frac{\pi}{2} = \frac{3}{2} \approx 1.5$$

$W_n$ is 50% more efficient than the median under normality, while maintaining $\varepsilon^* \approx 0.29$.

#statistics #robust-estimation #hodges-lehmann
