# K-means Clustering

## Intuition
Partitions $n$ points into $k$ groups by alternating between assigning each point to its nearest centroid and recomputing those centroids. See [[Broadcast]] for efficient pairwise distance computation.

## Definition
A **$k$-means clustering** of $\{x_i\}_{i=1}^n \subset \mathbb{R}^d$ is a partition $\{C_j\}_{j=1}^k$ solving

$$\min_{\{C_j\}} \sum_{j=1}^k \sum_{x_i \in C_j} \|x_i - \mu_j\|^2, \qquad \mu_j = \frac{1}{|C_j|}\sum_{x_i \in C_j} x_i$$

**Lloyd's algorithm.** Starting from initial centroids $\mu_1^{(0)}, \ldots, \mu_k^{(0)}$, iterate:

$$\text{Assignment:}\quad C_j^{(t)} = \Bigl\{x_i : j = \arg\min_l \|x_i - \mu_l^{(t-1)}\|^2\Bigr\}$$

$$\text{Update:}\quad \mu_j^{(t)} = \frac{1}{|C_j^{(t)}|}\sum_{x_i \in C_j^{(t)}} x_i$$

### Examples

Pairwise distance matrix via broadcasting (see [[Broadcast]]):

$$D_{ij} = \|x_i - \mu_j\|^2, \quad D \in \mathbb{R}^{n \times k}$$

## Properties

### Convergence
**Proof.**
Let $J^{(t)} = \sum_j \sum_{x_i \in C_j^{(t)}} \|x_i - \mu_j^{(t)}\|^2$.

- Assignment step: each $x_i$ moves to the nearest centroid, so $J$ cannot increase.
- Update step: $\mu_j = \arg\min_\mu \sum_{x_i \in C_j} \|x_i - \mu\|^2$ is attained at the mean, so $J$ cannot increase.

Hence $J^{(t)}$ is non-increasing. The number of distinct partitions of $n$ points into $k$ groups is finite, so the sequence of partitions must cycle; combined with strict decrease between distinct partitions, the algorithm terminates. $\square$

### Local minimum
Lloyd's algorithm converges to a local minimum of the objective, not the global one. The result depends on initialisation (e.g. k-means++).

### Complexity
$O(nkd)$ per iteration. Total: $O(nkdT)$ for $T$ iterations.

#clustering #ml
