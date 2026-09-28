# Dynamic programming: evaluation, improvement, PI and VI

> **Tier:** Intermediate · **Prereqs:** `00/02`, `00/03`, `01/03` · **Code:** `rlguide.mdp_dp` · **Notebook:** `02_gridworld_dp`

## 1. Iterative policy evaluation
$V_{k+1} = T^\pi V_k$.

- **Synchronous (Jacobi):** compute all of $V_{k+1}$ from the old array $V_k$ (two arrays).
- **In-place (Gauss–Seidel):** overwrite $V(s)$ immediately so later states in the same sweep use fresh values — usually faster; the result depends on sweep order.

**Keep $\pi$ fixed during evaluation.** Changing it mid-evaluation turns the procedure into something else (VI or GPI).

**Stopping rule:** $\Delta_k = \max_s\lvert V_{k+1}(s) - V_k(s)\rvert < \theta$.

**Reading convergence plots:** on a log scale $\Delta_k$ falls roughly linearly with slope $\log\gamma$ (geometric decay). A plateau or increase signals a bug — e.g. $\pi$ changing, or $\gamma \ge 1$ with no terminal state.

## 2. Policy improvement theorem
If $q_\pi(s, \pi'(s)) \ge v_\pi(s)$ for all $s$, then $v_{\pi'}(s) \ge v_\pi(s)$ for all $s$.

*Proof.*
$$\begin{aligned}
v_\pi(s) &\le q_\pi(s, \pi'(s)) = \mathbb E\big[R_{t+1} + \gamma v_\pi(S_{t+1}) \mid S_t = s, A_t = \pi'(s)\big]\\
&\le \mathbb E_{\pi'}\big[R_{t+1} + \gamma\,q_\pi(S_{t+1}, \pi'(S_{t+1})) \mid S_t = s\big]\\
&\le \dots \le \mathbb E_{\pi'}[G_t \mid S_t = s] = v_{\pi'}(s). \quad\blacksquare
\end{aligned}$$

The **greedy** policy $\pi'(s) = \arg\max_a q_\pi(s,a)$ satisfies the premise. If $\pi'$ is no better than $\pi$, then $v_\pi$ satisfies the Bellman *optimality* equation — so $\pi$ is optimal.

## 3. Policy iteration (PI)
Evaluate → improve greedily → repeat until the policy is stable.

**Terminates finitely:** at most $\lvert\mathcal A\rvert^{\lvert\mathcal S\rvert}$ deterministic policies, and each iteration strictly improves unless already optimal, so no policy repeats.

## 4. Value iteration (VI)
$V_{k+1} = T^* V_k$ — one sweep of truncated evaluation fused with improvement. Converges **asymptotically** (geometrically, rate $\gamma$), not finitely in general; the greedy policy is often optimal long before $V$ converges.

**$\pi_{VI}$ vs $\pi_{PI}$:** both are greedy w.r.t. (essentially) the same $v_*$, so they agree on values; they may differ only where actions tie.

## 5. Generalised policy iteration (GPI)
Any interleaving of evaluation and improvement, at any granularity, converges to $(v_*, \pi_*)$. VI, PI, MC control and SARSA are all instances.

## 6. Planning vs learning
With a known model you **plan** (DP). If the goal moves you change $R$ and re-solve — no new experience needed. Model-free learners must collect new experience.

## Worked VI example (hallway, $\gamma = 0.9$, $V_0 = 0$)
- Sweep 1: $V(M) = 1$ (move right onto R), $V(L) = 0$.
- Sweep 2: $V(L) = 0.9$.
- Sweep 3: nothing changes, $\Delta = 0$ → stop.

## Pitfalls
- Updating the policy *during* evaluation.
- Expecting VI to hit $v_*$ exactly in finitely many sweeps.
- Assuming $\pi_{VI} = \pi_{PI}$ action-for-action (ties!).

## Practice
<details><summary>Two states, γ = 0.5. State 1: action a gives r = 1 and stays; action b gives r = 0 and moves to 2. State 2: r = 2, stay. Run PI from π(1) = a.</summary>

$v_\pi(1) = 1/(1-0.5) = 2$, $v(2) = 2/(1 - 0.5) = 4$. $q(1, b) = 0 + 0.5\cdot4 = 2$ ties with $q(1, a) = 2$. Keeping the tie at $a$, the policy is stable — both actions are optimal.
</details>

> **Run it:** `tests/test_worked_examples.py::test_hallway_values`, `::test_pi_tie_practice`; `tests/test_properties.py::test_vi_pi_lp_agree`, `::test_value_iteration_geometric_rate`, `::test_in_place_evaluation_converges_to_same_values`
