# Breakdown Point

## Intuition
Measures the maximum fraction of contaminated observations an estimator can tolerate before its output becomes unbounded.

## Definition
The breakdown point of an estimator $\hat\theta_n$ is called the largest contamination fraction under which $\hat\theta_n$ remains bounded:

$$\varepsilon^*(\hat\theta_n) = \max\left\{\frac{k}{n} : \sup_{\text{any } k\text{ replacements}} \bigl|\hat\theta_n(X)\bigr| < \infty\right\}$$

### Examples

| Estimator | $\varepsilon^*$ |
|-----------|-----------------|
| Sample mean $\bar X$ | $0$ |
| Trimmed mean $\bar X_\alpha$ | $\alpha$ |
| Hodges–Lehmann $W$ | $1 - 1/\sqrt{2} \approx 0.29$ |
| Sample median $\tilde X$ | $0.5$ |

The mean has breakdown point $0$: a single outlier sent to $\pm\infty$ destroys the estimate.

#statistics #robust-estimation
