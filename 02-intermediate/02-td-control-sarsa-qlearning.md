# TD control: SARSA, Q-learning, Expected SARSA, Double Q

> **Tier:** Intermediate · **Prereqs:** `01/04`, `01/05`, `00/05` · **Code:** `rlguide.td_control` · **Notebooks:** `04_cliff_walking`, `07_maximization_bias` · **Demo:** `mise run demo:cliff`

## 1. The three targets

| Algorithm | Target for $Q(S_t, A_t)$ | Policy type |
|---|---|---|
| SARSA | $R_{t+1} + \gamma\,Q(S_{t+1}, A_{t+1})$ | on-policy |
| Q-learning | $R_{t+1} + \gamma\max_a Q(S_{t+1}, a)$ | off-policy |
| Expected SARSA | $R_{t+1} + \gamma\sum_a\pi(a\mid S_{t+1})\,Q(S_{t+1}, a)$ | either |

Update, always: $Q(S_t, A_t) \leftarrow Q(S_t, A_t) + \alpha\big[\text{target} - Q(S_t, A_t)\big]$.

**Worked Q-learning example (quiz).** $Q(s,a) = 0$, $\alpha = 0.5$, $r = 1$, $\max_{a'}Q(s', a') = 0.6$:
$$Q \leftarrow 0 + 0.5\,(1 + 0.6\gamma - 0) = 0.5 + 0.3\gamma \quad(= 0.77 \text{ for } \gamma = 0.9).$$

## 2. On-policy vs off-policy
The **behaviour policy** $b$ generates the data; the **target policy** $\pi$ is the one being evaluated or improved.
- SARSA: $b = \pi$ (ε-greedy).
- Q-learning: target = greedy; behaviour = ε-greedy (anything that keeps exploring).

Off-policy learning enables **experience reuse** (replay buffers, demonstrations).

## 3. Cliff walking (Sutton & Barto Example 6.6)
4×12 grid, start bottom-left, goal bottom-right, bottom row between them is a cliff ($-100$ and reset); every other step $-1$; $\varepsilon = 0.1$.

- **Q-learning** learns the optimal edge path (13 steps) but its ε-greedy behaviour sometimes falls off → worse **online** return.
- **SARSA** learns the longer, safer upper path because its target includes the exploratory actions it will actually take.
- As $\varepsilon \to 0$ both converge to the optimal path.

Output of `mise run demo:cliff` (seed 0, 500 episodes, $\alpha = 0.5$):
```
sarsa           mean return (last 100 eps) =  -26.19   greedy path length =  17
expected_sarsa  mean return (last 100 eps) =  -22.35   greedy path length =  15
qlearning       mean return (last 100 eps) =  -61.81   greedy path length =  13
```

## 4. Maximisation bias and Double Q-learning
Because $\mathbb E[\max_a\hat Q(a)] \ge \max_a\mathbb E[\hat Q(a)]$ (Jensen), maximising over noisy estimates overestimates. Thrun & Schwartz (1993): uniform errors in $[-\epsilon, \epsilon]$ inflate each target by up to $\gamma\epsilon\frac{m-1}{m+1}$ for $m$ actions.

**Double Q-learning** (van Hasselt 2010) keeps $Q^A, Q^B$; on a coin flip update $Q^A$ with
$$R + \gamma\,Q^B\big(S', \arg\max_a Q^A(S', a)\big)$$
(and symmetrically). Selection and evaluation use independent estimates, removing the upward bias (it can slightly *under*estimate).

## 5. Convergence conditions
- **Q-learning (tabular):** converges to $q_*$ w.p. 1 if every $(s,a)$ is updated infinitely often and step sizes satisfy Robbins–Monro per pair, e.g. $\alpha = 1/N(s,a)$ (Watkins & Dayan 1992). Because it is off-policy, its *values* do **not** need GLIE.
- **SARSA(0):** converges to $q_*$ and an optimal policy with lookup tables, Robbins–Monro rates and a **GLIE** policy (Singh et al. 2000), e.g. ε-greedy with $\varepsilon_t(s) = c/n_t(s)$, $0 < c < 1$.
- **Constant α** (0.5, 0.9): with stochastic rewards/transitions estimates keep fluctuating (variance $\propto\alpha$) → no convergence. In a fully deterministic MDP constant α can converge.
- **DP vs samples:** VI converges geometrically (deterministic error bound), PI terminates finitely; sample-based methods converge w.p. 1 only in the limit.

## Pitfalls
- SARSA uses the **actual** next action; Q-learning the **max**. Don't swap them.
- "Q-learning needs GLIE" — only to *act* optimally, not for its values to converge.
- Online return ≠ quality of the learned greedy policy (cliff walking!).

## Practice
<details><summary>Q(s, a) = 2, α = 0.1, r = −1, γ = 1, Q(s′, ·) = (3, 5), next action chosen = 0. SARSA and Q-learning updates?</summary>

SARSA target $-1 + 3 = 2$ → $Q = 2$. Q-learning target $-1 + 5 = 4$ → $Q = 2.2$.
</details>

> **Run it:** `tests/test_worked_examples.py::test_q_learning_quiz_example`; `tests/test_properties.py::test_cliff_walking_sarsa_safer_than_qlearning`, `::test_maximization_bias_double_q_helps`
