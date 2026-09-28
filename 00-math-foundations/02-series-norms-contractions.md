# Geometric series, the sup norm and contraction mappings

> **Tier:** Foundations · **Used by:** discounting, Bellman operators, VI/PI convergence · **Notebook:** `01_expectation_and_contraction`

## 1. Geometric series — why $\gamma < 1$ matters
$$\sum_{k=0}^{\infty}\gamma^k = \frac{1}{1-\gamma} \qquad (0 \le \gamma < 1).$$

*Derivation.* Let $S_N = \sum_{k=0}^N \gamma^k$. Then $S_N - \gamma S_N = 1 - \gamma^{N+1}$, so $S_N = \dfrac{1-\gamma^{N+1}}{1-\gamma} \to \dfrac{1}{1-\gamma}$.

**Consequence.** If $\lvert R\rvert \le R_{\max}$ then
$$\lvert G_t\rvert \le \frac{R_{\max}}{1-\gamma},$$
so returns are finite even for tasks that never end. With $\gamma = 1$ and reward 1 forever, the sum diverges.

## 2. The sup (max) norm
$$\lVert v\rVert_\infty = \max_s \lvert v(s)\rvert \quad\text{— the worst-case error over states.}$$
Stopping rules like $\Delta_k = \max_s \lvert V_{k+1}(s) - V_k(s)\rvert$ are sup-norm distances.

## 3. Contractions and Banach's fixed-point theorem
**Definition.** $T$ is a **$\gamma$-contraction** if $\lVert Tu - Tv\rVert \le \gamma\lVert u - v\rVert$ for some $\gamma < 1$.

**Theorem (Banach).** On a complete metric space — e.g. $\mathbb R^{\lvert\mathcal S\rvert}$ with $\lVert\cdot\rVert_\infty$ — a contraction has **exactly one** fixed point $v^*$, and $v_{k+1} = Tv_k$ converges to it from any start:
$$\lVert v_k - v^*\rVert_\infty \le \gamma^k\,\lVert v_0 - v^*\rVert_\infty.$$

*Proof sketch.*
- *Uniqueness:* if $Tx = x$ and $Ty = y$ then $\lVert x - y\rVert = \lVert Tx - Ty\rVert \le \gamma\lVert x - y\rVert$, forcing $\lVert x - y\rVert = 0$.
- *Existence:* $\lVert v_{k+1} - v_k\rVert \le \gamma^k \lVert v_1 - v_0\rVert$, so the sequence is Cauchy; it converges to some $v^*$, and continuity of $T$ gives $Tv^* = v^*$. ∎

**Stopping-rule bound.** If $\lVert v_{k+1} - v_k\rVert_\infty < \theta$ then
$$\lVert v_{k+1} - v^*\rVert_\infty \le \frac{\gamma\,\theta}{1-\gamma}.$$

**Worked example.** $T(x) = 0.5x + 1$ has fixed point $x^* = 2$. From $x_0 = 0$: $1,\ 1.5,\ 1.75,\ 1.875,\ \dots$ — the error halves each step (contraction factor 0.5).

## Pitfalls
- A small $\Delta_k$ is **not** a small error when $\gamma \approx 1$: the bound multiplies by $\gamma/(1-\gamma)$ (= 99 for $\gamma = 0.99$).
- Contraction is a property of the **operator and the norm** together.

## Practice
<details><summary>1. How many VI iterations guarantee error ≤ 0.01 if γ = 0.9 and the initial error is 10?</summary>

$0.9^k \cdot 10 \le 0.01 \Rightarrow k \ge \ln(0.001)/\ln 0.9 \approx 65.6$, so **66**.
</details>

<details><summary>2. Is T(x) = x² a contraction on [0, 1]?</summary>

No: $\lvert x^2 - y^2\rvert = \lvert x + y\rvert\,\lvert x - y\rvert$ and $x + y$ can approach 2.
</details>

> **Run it:** `tests/test_worked_examples.py::test_contraction_example_fixed_point`, `::test_vi_iterations_needed`; `tests/test_properties.py::test_bellman_operators_are_gamma_contractions`
