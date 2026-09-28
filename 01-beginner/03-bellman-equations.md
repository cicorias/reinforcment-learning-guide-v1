# Bellman equations

> **Tier:** Beginner · **Prereqs:** `00/01`, `01/02` · **Code:** `rlguide.mdp_dp.bellman_expectation`, `bellman_optimality`

## 1. Value functions
$$v_\pi(s) = \mathbb E_\pi[G_t \mid S_t = s], \qquad q_\pi(s,a) = \mathbb E_\pi[G_t \mid S_t = s, A_t = a].$$

## 2. Bellman expectation equations
Start from $G_t = R_{t+1} + \gamma G_{t+1}$, take conditional expectations, and use the law of total expectation plus the Markov property:
$$v_\pi(s) = \sum_a \pi(a\mid s)\sum_{s', r}p(s', r \mid s, a)\,\big[r + \gamma\,v_\pi(s')\big],$$
$$q_\pi(s,a) = \sum_{s', r}p(s', r\mid s,a)\Big[r + \gamma\sum_{a'}\pi(a'\mid s')\,q_\pi(s', a')\Big].$$

**Deterministic form** (policy $\pi(s)$, transition $T(s,a)$):
$$V^\pi(s) = R\big(s, \pi(s)\big) + \gamma\,V^\pi\big(T(s, \pi(s))\big).$$

## 3. Bellman optimality equations
$$v_*(s) = \max_a \sum_{s',r}p(s',r\mid s,a)\big[r + \gamma\,v_*(s')\big],$$
$$q_*(s,a) = \sum_{s',r}p(s',r\mid s,a)\Big[r + \gamma\max_{a'}q_*(s',a')\Big].$$
Any policy greedy with respect to $q_*$ is optimal: $\pi_*(s) \in \arg\max_a q_*(s,a)$.

**Principle of optimality (Bellman).** Whatever the first state and decision, the remaining decisions of an optimal policy form an optimal policy from the resulting state.

## 4. Fixed-point view
$$(T^\pi v)(s) = \sum_a \pi(a\mid s)\Big[R(s,a) + \gamma\sum_{s'}P(s'\mid s,a)\,v(s')\Big],$$
$$(T^* v)(s) = \max_a\Big[R(s,a) + \gamma\sum_{s'}P(s'\mid s,a)\,v(s')\Big].$$
Then $v_\pi = T^\pi v_\pi$ and $v_* = T^* v_*$. Both operators are $\gamma$-contractions (proof in `03-expert/01`).

## Pitfalls
- The **expectation** equation *averages* over actions using $\pi$; the **optimality** equation *maximises*. Mixing them up is a classic quiz trap.
- $q_*$ uses $\max_{a'}$ *inside* the expectation over $s'$.

## Practice
<details><summary>Hallway, γ = 0.9: write the optimality equation at L and solve.</summary>

$v_*(L) = \max\{0 + 0.9\,v_*(L),\ 0 + 0.9\,v_*(M)\}$ with $v_*(M) = \max\{0.9\,v_*(L),\ 1\} = 1$, so $v_*(L) = 0.9$.
</details>
