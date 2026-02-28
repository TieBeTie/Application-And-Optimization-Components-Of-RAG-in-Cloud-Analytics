# Broadcasting (PyTorch)

## Intuition
Shapes are aligned **from the right**: the rightmost dimension is the "innermost" (e.g. features of a vector), leading dimensions are "outer" (e.g. batch, number of clusters). Missing leading dimensions are treated as 1, so a single vector broadcasts over a batch without copying data.

## Definition
Tensors $A \in \mathbb{R}^{s_1 \times \cdots \times s_m}$ and $B \in \mathbb{R}^{t_1 \times \cdots \times t_n}$ are **broadcastable** under the following rule:

1. Prepend 1s to the shorter shape until both have the same number of dimensions.
2. Dimensions are **compatible** if $s_i = t_i$, or $s_i = 1$, or $t_i = 1$.
3. If all dimensions are compatible, the output shape is $(\max(s_i, t_i))_i$.

### Examples

Pairwise squared distances in [[K-means]], first two lines of the loop:

```python
dist_matrix = torch.sum(
    (points_t[:, None, :] - centroids[None, :, :]) ** 2, dim=2
)
# points_t[:, None, :]   shape: (n, 1, d)
# centroids[None, :, :]  shape: (1, k, d)
# difference             shape: (n, k, d)   ← broadcast
# dist_matrix            shape: (n, k)

assignments = torch.argmin(dist_matrix, dim=1)
# assignments[i] = argmin_j ||x_i - mu_j||^2
```

$\text{diff}[i,j,:] = x_i - \mu_j$ — разность $i$-й точки и $j$-го центроида без явного цикла.

## Properties

### Shape rule
Align from the right. For $(n, 1, d)$ and $(1, k, d)$:

$$(\max(n,1),\ \max(1,k),\ \max(d,d)) = (n,\ k,\ d)$$

### No memory allocation
Expansion is implicit; broadcast does not allocate the full expanded tensor unless forced (e.g. `.expand().clone()`).

### Non-broadcastable example
$(n, d)$ and $(k, d)$ are **not** broadcastable — dimensions $n$ and $k$ are both $\neq 1$ and $\neq$ each other. Fix: insert a new axis with `[:, None, :]` and `[None, :, :]`.

#pytorch #broadcasting #tensors #ml
