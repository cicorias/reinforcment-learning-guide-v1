# Convexity, polytopes and vertices

> **Tier:** Foundations · **Used by:** LP geometry, simplex, maximisation bias · **Notebook:** `08_simplex_visual`

- **Convex set:** contains the segment between any two of its points. **Convex combination:** $\sum_i \lambda_i x_i$ with $\lambda_i \ge 0$, $\sum_i\lambda_i = 1$.
- **Polyhedron:** $\{x : Ax \le b\}$ — an intersection of half-spaces, always convex. A **polytope** is a bounded polyhedron.
- **Vertex (extreme point):** a feasible point that is not a convex combination of two *other* feasible points. Algebraically, a **basic feasible solution (BFS)**: $n$ linearly independent constraints are tight.

## Fundamental theorem of LP
If an LP has an optimal solution and its feasible region has at least one vertex, then **some** vertex is optimal.

*Why:* a linear objective evaluated at a convex combination is the same convex combination of objective values, so it cannot beat the best vertex.

> ⚠️ It does **not** say *every* optimal solution is a vertex. $\max x_1 + x_2$ s.t. $x_1 + x_2 \le 1,\ x \ge 0$ is optimal along the whole edge from $(1,0)$ to $(0,1)$. (See `question-bank/quiz-errata.md` #4.)

## Convex functions and Jensen
$f(\lambda x + (1-\lambda)y) \le \lambda f(x) + (1-\lambda)f(y)$.

**Jensen's inequality** for the (convex) max:
$$\mathbb E\big[\max_i X_i\big] \ge \max_i \mathbb E[X_i].$$
This is the root cause of **maximisation bias** in Q-learning (`02-intermediate/02`).

## Practice
<details><summary>Is {x : x₁² + x₂² ≤ 1} a polyhedron?</summary>

Convex, yes; polyhedron, no — it is not a finite intersection of half-spaces (infinitely many extreme points).
</details>
