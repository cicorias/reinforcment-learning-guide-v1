# Bandits and exploration

> **Tier:** Beginner · **Prereqs:** `00/01` · **Code:** `rlguide.bandits` · **Notebook:** `06_bandits`

## 1. The problem
$k$ actions, no states; each reward $R \sim$ an unknown distribution with mean $q_*(a)$. The estimate $Q_t(a)$ is the incremental sample mean.

**Exploration vs exploitation:** exploit $\arg\max_a Q_t(a)$; explore other arms to improve estimates.

## 2. ε-greedy
With probability $\varepsilon$ choose uniformly at random, otherwise greedily:
$$\pi(a) = \begin{cases} 1 - \varepsilon + \varepsilon/k & a = \text{greedy}\\ \varepsilon / k & \text{otherwise.}\end{cases}$$

**Worked example.** $k = 4$, $\varepsilon = 0.2$: greedy arm $0.8 + 0.05 = 0.85$; each other arm $0.05$.

**ε-greedy is not uniform random.** Fixed $\varepsilon$ explores forever (linear regret); decaying $\varepsilon_t$ (e.g. $c/t$) can reach logarithmic regret if tuned.

## 3. Regret
$$L_T = \sum_{t=1}^T\big(q_*(a^*) - q_*(A_t)\big) \quad\text{(in expectation).}$$

## 4. Better exploration
- **Optimistic initialisation:** start $Q_1(a)$ high (e.g. +5) so every arm is tried early.
- **UCB1:**
$$A_t = \arg\max_a\Big[Q_t(a) + c\sqrt{\frac{\ln t}{N_t(a)}}\Big].$$
Auer, Cesa-Bianchi & Fischer (2002) proved logarithmic regret uniformly over time for bounded rewards; Lai & Robbins (1985) showed logarithmic growth is also a lower bound.
- **Thompson sampling:** keep a posterior (e.g. Beta$(\alpha_a, \beta_a)$ for Bernoulli arms), sample $\tilde\theta_a$, play $\arg\max_a\tilde\theta_a$.

## Pitfalls
- Pure greedy can lock onto a bad arm forever after one unlucky sample.
- A larger $\varepsilon$ is not "better" late in training — it keeps paying for exploration.

## Practice
<details><summary>k = 10, ε = 0.1: probability of picking the greedy arm?</summary>

$0.9 + 0.01 = 0.91$.
</details>

> **Run it:** `tests/test_worked_examples.py::test_eps_greedy_probabilities`; `tests/test_properties.py::test_ucb_beats_pure_greedy_regret`
