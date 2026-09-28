# LP duality and occupancy measures

> **Tier:** Expert · **Prereqs:** `02/05` · **Code:** `rlguide.mdp_lp.solve_dual` · **Test:** `tests/test_properties.py::test_dual_lp_matches_primal_and_is_deterministic`

**Primal** (reward maximisation):
$$\min_v \sum_s\mu_0(s)\,v(s)\quad\text{s.t.}\quad v(s) \ge r(s,a) + \gamma\sum_{s'}P(s'\mid s,a)\,v(s')\quad\forall s, a.$$

**Dual:**
$$\max_{d \ge 0}\sum_{s,a}d(s,a)\,r(s,a)\quad\text{s.t.}\quad \sum_a d(s', a) = \mu_0(s') + \gamma\sum_{s,a}P(s'\mid s,a)\,d(s,a)\quad\forall s'.$$

$d(s,a)$ is the **discounted state–action occupancy measure**
$$d_\pi(s,a) = \mathbb E\Big[\sum_t\gamma^t\,\mathbf 1\{S_t = s, A_t = a\}\Big],$$
and the constraint is **flow conservation**. Summing it over $s'$ gives $\sum_{s,a}d(s,a) = 1/(1-\gamma)$ when $\mu_0$ sums to 1.

## Facts
- An optimal **basic** dual solution corresponds to a **deterministic** optimal policy, $\pi(a\mid s) \propto d^*(s,a)$ (Puterman 1994 §6.9).
- **Weak duality:** primal value ≥ dual value. **Strong duality:** equal at the optimum.
- **Complementary slackness:** $d^*(s,a) > 0 \Rightarrow$ that primal constraint is tight, i.e. $a$ is greedy w.r.t. $v_*$.
- **Constrained MDPs** add linear constraints on $d$ (e.g. expected cost budgets); optimal policies may then need randomisation (Altman 1999).

## Practice
<details><summary>Why is the total occupancy 1/(1−γ)?</summary>

Each time step contributes $\gamma^t$ total mass across all $(s,a)$; $\sum_t\gamma^t = 1/(1-\gamma)$.
</details>
