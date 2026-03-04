# Trimmed Mean

## Intuition
Remove the most extreme observations on both tails, then average the rest. Trades some efficiency for robustness to outliers.

## Definition
Given ordered sample $X_{(1)} \le \dots \le X_{(n)}$ and $0 < \alpha < 1/2$, the trimmed mean of order $\alpha$ is called the average of the central $(1-2\alpha)$ fraction:

$$\bar X_\alpha = \frac{1}{n(1-2\alpha)}\sum_{i=\lfloor\alpha n\rfloor+1}^{n-\lfloor\alpha n\rfloor} X_{(i)}$$

### Examples
- $\alpha = 0$: ordinary sample mean $\bar X$.
- $\alpha \to 1/2$: converges to sample median $\tilde X$.

## Properties

### Breakdown Point
$\varepsilon^*(\bar X_\alpha) = \alpha$. See [[Breakdown_Point]].

## Theorem. Asymptotic Normality

### Intuition
Under a symmetric model, $\bar X_\alpha$ is asymptotically normal with a variance that depends on the trimming level and the tails of $F$.

### Statement
Let $X_i \overset{\text{i.i.d.}}{\sim} F_\theta$, $F$ symmetric about $\theta$, density $p$ continuous at $u_\alpha = F^{-1}(\alpha)$. Then

$$\sqrt{n}\,(\bar X_\alpha - \theta) \xrightarrow{d} \mathcal{N}(0,\, \sigma_\alpha^2)$$

where

$$\sigma_\alpha^2 = \frac{1}{(1-2\alpha)^2}\!\left(2\int_0^{u_{1-\alpha}} x^2\,p(x)\,dx\ +\ 2\alpha\,u_{1-\alpha}^2\right)$$

### Proof
Express $\bar X_\alpha$ as a linear combination of order statistics, apply the Bahadur representation $X_{(k)} = F^{-1}(k/n) + O(n^{-1/2}\log n)$ (Bahadur 1966), reduce to a sum of i.i.d. terms, and invoke the CLT. Full argument: Stigler (1973), *JASA*.

### Examples
For $F = \mathcal{N}(0,1)$ and $\alpha = 0.1$: $u_{0.9} \approx 1.28$,
$$\sigma_{0.1}^2 = \frac{1}{0.64}\left(2\int_0^{1.28} x^2\phi(x)\,dx + 2\cdot 0.1\cdot 1.28^2\right) \approx 1.08$$
vs. $\sigma_0^2 = 1$ for the mean — slight efficiency loss in exchange for $\varepsilon^* = 0.1$.

#statistics #robust-estimation
