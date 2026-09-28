# n-step TD, TD(λ), batch methods and importance sampling

> **Tier:** Expert · **Prereqs:** `01/04`, `02/02` · **Code:** `rlguide.mc_td_prediction.n_step_return`, `batch_td0` · **Notebook:** `03_mc_vs_td`

## n-step returns
$$G_{t:t+n} = R_{t+1} + \gamma R_{t+2} + \dots + \gamma^{n-1}R_{t+n} + \gamma^n V(S_{t+n}).$$
$n = 1$ is TD(0); $n = \infty$ (or reaching the terminal) is MC. Larger $n$: less bias, more variance.

## λ-returns and TD(λ)
$$G_t^\lambda = (1-\lambda)\sum_{n\ge1}\lambda^{n-1}G_{t:t+n}.$$
**Backward view** with eligibility traces:
$$z_t = \gamma\lambda z_{t-1} + \nabla\hat v(S_t), \qquad w \leftarrow w + \alpha\,\delta_t\,z_t.$$
$\lambda = 0$ is TD(0); $\lambda = 1$ approximates MC.

## Batch TD vs batch MC (Sutton & Barto Example 6.4)
Data: one episode $A, 0, B, 0$; six episodes $B, 1$; one episode $B, 0$.
- Both give $V(B) = 6/8 = 0.75$.
- **Batch MC:** $V(A) = 0$ — minimises squared error on the observed returns.
- **Batch TD:** $V(A) = 0.75$ — the **certainty-equivalence** estimate for the maximum-likelihood Markov model (A always goes to B).

TD is often better on future data because it exploits the Markov structure.

## Convergence of tabular TD(0)
Converges to $v_\pi$ w.p. 1 under Robbins–Monro steps (Dayan 1992; Jaakkola et al. 1994), and in the mean for small constant $\alpha$.

## Importance sampling
$$\rho_{t:T-1} = \prod_{k=t}^{T-1}\frac{\pi(A_k\mid S_k)}{b(A_k \mid S_k)}.$$
- **Ordinary IS:** unbiased, possibly unbounded variance.
- **Weighted IS:** biased (consistent), much lower variance.
- **Coverage:** $\pi(a\mid s) > 0 \Rightarrow b(a\mid s) > 0$.

Q-learning and Expected SARSA need **no** IS for one-step targets: the next action is evaluated in expectation under $\pi$ (or by the max), not sampled from $b$.

## Practice
<details><summary>Rewards 1, 1, 1 then terminal, γ = 1, V ≡ 0. Give G_{0:1}, G_{0:2}, G_{0:3}.</summary>

1, 2, 3.
</details>

> **Run it:** `tests/test_worked_examples.py::test_batch_td_vs_batch_mc_example_6_4`
