# Robust Estimator Selection

## Intuition
The optimal location estimator depends on the contamination level and the shape of the underlying distribution. Efficiency and robustness trade off against each other.

## Decision Table

| Distribution / contamination | Estimator | Reason |
|------------------------------|-----------|--------|
| Symmetric, no outliers, $F \approx \mathcal{N}$ | $\bar X$ | UMVUE under normality |
| Light contamination $\varepsilon \le 0.1$ | $\bar X_{0.1}$ | [[Trimmed_Mean]], small efficiency loss |
| Moderate contamination $\varepsilon \le 0.2$ | $\bar X_{0.2}$ or $W$ | [[Hodges_Lehmann_Estimator]] gives $\varepsilon^* \approx 0.29$ |
| Unknown contamination | $\tilde X$ | [[Breakdown_Point]] $= 0.5$, maximal robustness |
| Heavy-tailed $F$ (e.g. Cauchy) | $\tilde X$ or $W$ | $\mathrm{Var}(\bar X) = \infty$ for Cauchy |

## Symmetry Check

Before applying any location estimator, verify symmetry of $F$. For symmetric $F$:

$$F^{-1}(1/2) - F^{-1}(p) = F^{-1}(1-p) - F^{-1}(1/2) \quad \forall p$$

**Procedure.** Plot empirical quantiles $\hat u_p$ against their mirrors $\hat u_{1/2} - (\hat u_p - \hat u_{1/2})$. Deviations from the diagonal indicate skewness; extreme deviations invalidate symmetry-based theorems.

## Theorem. ARE of Sample Median vs Mean under Normality

### Statement
For $X_i \overset{\text{i.i.d.}}{\sim} \mathcal{N}(\theta, \sigma^2)$:

$$\mathrm{ARE}(\tilde X,\, \bar X) = \frac{2}{\pi} \approx 0.637$$

### Proof
Asymptotic variance of the mean: $\mathrm{AVar}(\bar X) = \sigma^2/n$.

By asymptotic normality of the sample median with $f(\theta) = \phi(0)/\sigma = 1/(\sigma\sqrt{2\pi})$:

$$\mathrm{AVar}(\tilde X) = \frac{1}{4f(\theta)^2 n} = \frac{\pi\sigma^2}{2n}$$

$$\mathrm{ARE}(\tilde X,\, \bar X) = \frac{\sigma^2/n}{\pi\sigma^2/(2n)} = \frac{2}{\pi} \qquad \square$$

### Interpretation
Under normality, the median requires $\pi/2 \approx 1.57\times$ more observations to achieve the same precision as the mean. Under Cauchy, $\mathrm{AVar}(\bar X) = \infty$ while $\mathrm{AVar}(\tilde X) = \pi^2/(4n)$ — the mean is strictly inferior.

## Asymptotic Variance Summary

| Estimator | $\mathrm{AVar}$ under $\mathcal{N}(\theta,\sigma^2)$ | $\varepsilon^*$ |
|-----------|------------------------------------------------------|-----------------|
| $\bar X$ | $\sigma^2/n$ | $0$ |
| $\bar X_\alpha$ | $\sigma_\alpha^2/n$ (see [[Trimmed_Mean]]) | $\alpha$ |
| $W_n$ | $\approx 1.047\,\sigma^2/n$ | $0.293$ |
| $\tilde X$ | $\pi\sigma^2/(2n)$ | $0.5$ |

See [[Breakdown_Point]], [[Trimmed_Mean]], [[Hodges_Lehmann_Estimator]].

#statistics #robust-estimation #estimator-selection
