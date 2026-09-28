# Linear algebra for policy evaluation

> **Tier:** Foundations · **Used by:** exact policy evaluation, LP · **Code:** `rlguide.mdp_dp.evaluate`

## 1. Matrices as transition operators
A **row-stochastic** matrix has $P_{ss'} \ge 0$ and $\sum_{s'} P_{ss'} = 1$.
$$(Pv)(s) = \sum_{s'} P_{ss'}\,v(s') \quad\text{is the expected next-state value, and}\quad \lVert Pv\rVert_\infty \le \lVert v\rVert_\infty.$$

## 2. Policy evaluation is a linear system
$$v = R_\pi + \gamma P_\pi v \iff (I - \gamma P_\pi)\,v = R_\pi.$$

**Why $(I - \gamma P)$ is invertible.** For $v \ne 0$:
$$\lVert (I - \gamma P)v\rVert_\infty \ge \lVert v\rVert_\infty - \gamma\lVert Pv\rVert_\infty \ge (1-\gamma)\lVert v\rVert_\infty > 0,$$
so the kernel is trivial. Equivalently, the **Neumann series** gives
$$(I - \gamma P)^{-1} = \sum_{k=0}^{\infty}(\gamma P)^k,$$
which literally reads "expected discounted sum over future steps".

## 3. Worked example (quiz): two states, $\gamma = 0.5$
Suppose $\pi$ gives $R_\pi = (1, 1)^\top$ and $P_\pi = \begin{pmatrix}0 & 1\\ 1 & 0\end{pmatrix}$ (states alternate). Then
$$\begin{cases} v_1 - 0.5\,v_2 = 1\\ v_2 - 0.5\,v_1 = 1\end{cases} \Rightarrow v_1 = v_2 = 2.$$
Check: $R/(1-\gamma) = 1/0.5 = 2$. With **any** stochastic $P_\pi$ and constant reward 1, $v = \mathbf 1/(1-\gamma)$.

## 4. Cost
Direct solve: $O(\lvert\mathcal S\rvert^3)$. Iterative evaluation: $O(\lvert\mathcal S\rvert^2)$ per sweep — better for large sparse problems.

## Practice
<details><summary>Solve v = R + γPv with R = (0, 1), P = [[0.5, 0.5], [0, 1]], γ = 0.9.</summary>

$v_2 = 1/(1-0.9) = 10$; $v_1 = 0.9(0.5v_1 + 0.5\cdot 10) \Rightarrow v_1(1 - 0.45) = 4.5 \Rightarrow v_1 \approx 8.18$.
</details>

> **Run it:** `tests/test_worked_examples.py::test_two_state_linear_solve`, `::test_linear_algebra_practice`
