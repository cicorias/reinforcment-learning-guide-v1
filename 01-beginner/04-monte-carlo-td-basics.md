# Monte Carlo and TD(0) prediction

> **Tier:** Beginner · **Prereqs:** `00/01`, `01/02` · **Code:** `rlguide.mc_td_prediction` · **Notebook:** `03_mc_vs_td`

## 1. Monte Carlo (MC) prediction
**Idea.** $v_\pi(s)$ is an expectation, so average observed returns. You must wait for the episode to end.

- **First-visit MC:** average $G_t$ only from the *first* time $s$ appears in each episode.
- **Every-visit MC:** average $G_t$ from *every* occurrence.

Both converge to $v_\pi(s)$. First-visit averages i.i.d. unbiased samples; every-visit is biased for finite samples but consistent (Sutton & Barto §5.1).

**Incremental form:** $V(s) \leftarrow V(s) + \frac{1}{N(s)}\big[G - V(s)\big]$.

### Worked example 1 (quiz)
Episode $A, B, A, C$ with rewards (after each step) $0, 2, -1, 3$, $\gamma = 1$. Returns, computed backwards:

| $t$ | state | $R_{t+1}$ | $G_t$ |
|---|---|---|---|
| 3 | C | 3 | 3 |
| 2 | A | −1 | 2 |
| 1 | B | 2 | 4 |
| 0 | A | 0 | 4 |

**First-visit** for A uses only $t=0$: stored $[4]$, so $V(A) = 4.0$. **Every-visit** stores $[4, 2]$, giving $3.0$.

### Worked example 2 (quiz)
Three episodes; A's first-visit returns are 4, 2, 5, and episode 3 also visits A a second time with return 1.
- First-visit: $(4 + 2 + 5)/3 = 3.67$
- Every-visit: $(4 + 2 + 5 + 1)/4 = 3.00$

## 2. TD(0) prediction
$$V(S_t) \leftarrow V(S_t) + \alpha\big[\underbrace{R_{t+1} + \gamma V(S_{t+1})}_{\text{TD target}} - V(S_t)\big], \qquad \delta_t = R_{t+1} + \gamma V(S_{t+1}) - V(S_t).$$

**Worked example (quiz).** $r = 2$, $\gamma = 0.9$, $V(s') = 8$: target $= 2 + 7.2 = 9.2$. With $V(s) = 5$, $\alpha = 0.5$: $\delta = 4.2$, and $V(s) \leftarrow 5 + 0.5 \cdot 4.2 = 7.1$.

**TD = MC + DP.** Like MC it **samples** (no model); like DP it **bootstraps** (uses the current estimate $V(S_{t+1})$). It updates online after every step and works for continuing tasks.

## 3. Bias–variance

| | MC | TD(0) |
|---|---|---|
| Target | $G_t$ (unbiased) | $R_{t+1} + \gamma V(S_{t+1})$ (biased while $V \ne v_\pi$) |
| Variance | high (many random rewards) | low (one reward, one transition) |
| Updates | end of episode | every step |
| Needs Markov property? | no | exploits it |

## Pitfalls
- Every-visit ≠ first-visit: count occurrences carefully.
- TD's target is *not* unbiased until $V$ is correct.
- The first-visit question in the quiz had no correct option — see `question-bank/quiz-errata.md` #1.

## Practice
<details><summary>1. Episode X, Y, X, Z with rewards 1, 1, 1, 1, γ = 1. First- and every-visit estimates for X?</summary>

Returns from X: $t=0$ → 4, $t=2$ → 2. First-visit **4**, every-visit **3**.
</details>

<details><summary>2. TD(0): V(s) = 0, r = −1, γ = 1, V(s') = 3, α = 0.1.</summary>

Target 2, $\delta = 2$, $V(s) = 0.2$.
</details>

> **Run it:** `tests/test_worked_examples.py::test_first_visit_quiz_example`, `::test_first_vs_every_visit_three_episodes`, `::test_td0_quiz_example`, `::test_mc_practice`, `::test_td0_practice`
