# Returns and discounting

> **Tier:** Beginner · **Prereqs:** `00/02` · **Code:** `rlguide.mc_td_prediction.returns_backward`, `rlguide.mdp_dp.backward_induction`

## 1. The return
$$G_t = R_{t+1} + \gamma R_{t+2} + \gamma^2 R_{t+3} + \dots = \sum_{k\ge 0}\gamma^k R_{t+k+1}.$$

**Recursive form** — the seed of every Bellman equation:
$$G_t = R_{t+1} + \gamma\,G_{t+1}.$$

## 2. Three equivalent readings of $\gamma$
1. **Time preference:** a reward now is worth more than the same reward later.
2. **Survival probability:** each step the process ends with probability $1-\gamma$; then $\mathbb E[\text{undiscounted sum until termination}] = \mathbb E\big[\sum_k\gamma^k R_{t+k+1}\big]$.
3. **Mathematical device:** keeps infinite sums finite, $\lvert G\rvert \le R_{\max}/(1-\gamma)$, and makes the Bellman operators contractions.

## 3. Episodic vs continuing
- **Episodic:** ends in a terminal state ($G = 0$ afterwards); $\gamma = 1$ is allowed.
- **Continuing:** never ends; needs $\gamma < 1$ (or the average-reward formulation).

## 4. Finite horizon and backward induction
With horizon $H$: set $V_H \equiv 0$ and for $t = H-1, \dots, 0$
$$V_t(s) = \max_a\Big[R(s,a) + \sum_{s'}P(s'\mid s,a)\,V_{t+1}(s')\Big].$$
The optimal policy is generally **non-stationary** (depends on $t$). This is "sequential decision-making as optimisation over time" (Bellman 1957).

## 5. Worked example
Rewards $1, 0, 2$ then termination, $\gamma = 0.5$:
$$G_0 = 1 + 0.5\cdot 0 + 0.25 \cdot 2 = 1.5.$$
Computed backwards: $G_2 = 2$, $G_1 = 0 + 0.5\cdot 2 = 1$, $G_0 = 1 + 0.5 \cdot 1 = 1.5$.

## Pitfalls
- Discounting starts at the **next** reward: $R_{t+1}$ gets weight $\gamma^0$.
- $\gamma$ is **not** a learning rate (that's $\alpha$).

## Practice
<details><summary>γ = 0.9, reward 1 forever. What is G?</summary>

$1/(1-0.9) = 10$.
</details>

<details><summary>Hallway with horizon 3: what is V at L with one step to go?</summary>

0 — one step can only reach M, which pays nothing.
</details>

> **Run it:** `tests/test_worked_examples.py::test_discounted_return_example`, `::test_constant_reward_return`; `tests/test_properties.py::test_backward_induction_nonstationary`
