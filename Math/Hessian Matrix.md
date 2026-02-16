# Hessian Matrix

## Intuition

Gradient tells the direction of steepest ascent. Hessian tells the curvature — how fast the gradient itself changes.

## Definition

A second-order derivative matrix of a scalar function $f \in C^2(\mathbb{R}^n, \mathbb{R})$ (twice continuously differentiable).

$$H_{ij} = \frac{\partial^2 f}{\partial x_i \partial x_j}, \quad i,j = 1,\ldots,n$$

$C^2$ guarantees existence of all second partials.

### Example

$f(x,y) = x^3 + 2xy - y^2$

$$\nabla f = \begin{pmatrix} 3x^2 + 2y \\ 2x - 2y \end{pmatrix}, \quad H = \begin{pmatrix} 6x & 2 \\ 2 & -2 \end{pmatrix}$$

Check: $\nabla f(0,0) = (0, 0)^T$ $\checkmark$ — critical point.

Then: $H(0,0) = \begin{pmatrix} 0 & 2 \\ 2 & -2 \end{pmatrix}$, $\det(H) = 0 \cdot (-2) - 4 = -4 < 0$ $\Rightarrow$ saddle point.

## Properties

### Symmetry (Schwarz's theorem)

**Claim.** $f \in C^2 \Rightarrow H_{ij} = H_{ji}$.

**Proof sketch.** Consider the second-order difference:

$$\Delta = f(a+h, b+k) - f(a+h, b) - f(a, b+k) + f(a, b)$$

Define $\varphi(x) = f(x, b+k) - f(x, b)$. Then $\Delta = \varphi(a+h) - \varphi(a)$.

By MVT: $\Delta = h\,\varphi'(a + \theta_1 h) = h\left[f_x(a+\theta_1 h, b+k) - f_x(a+\theta_1 h, b)\right]$

By MVT again: $\Delta = hk\, f_{xy}(a + \theta_1 h, b + \theta_2 k)$

Symmetrically, define $\psi(y) = f(a+h, y) - f(a, y)$:

$\Delta = hk\, f_{yx}(a + \theta_3 h, b + \theta_4 k)$

As $h,k \to 0$, continuity of second partials gives $f_{xy}(a,b) = f_{yx}(a,b)$. $\blacksquare$

### Definiteness $\Rightarrow$ critical point type (sufficient condition)

For critical point $\nabla f(x_0) = 0$:

| $H(x_0)$ | Type |
|-----------|------|
| Positive definite ($\lambda_i > 0\ \forall i$) | Local minimum |
| Negative definite ($\lambda_i < 0\ \forall i$) | Local maximum |
| Indefinite ($\exists\, \lambda_i > 0, \lambda_j < 0$) | Saddle point |
| Singular ($\exists\, \lambda_i = 0$) | Inconclusive |

**Proof.** Taylor expansion at critical point ($\nabla f(x_0) = 0$):

$$f(x_0 + d) = f(x_0) + \frac{1}{2} d^T H(x_0)\, d + o(\|d\|^2)$$

For small $d$, the $o(\|d\|^2)$ term is negligible, and the sign of $d^T H(x_0)\, d$ determines whether $f$ increases or decreases in every direction. $\blacksquare$

See also: [[Cholesky Decomposition]], [[GPTQ Algorithm]]

#math #quantization
