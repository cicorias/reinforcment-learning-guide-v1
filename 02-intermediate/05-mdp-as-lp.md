# MDPs as linear programs

> **Tier:** Intermediate · **Prereqs:** `01/03`, `01/06`, `02/01` · **Code:** `rlguide.mdp_lp`

## 1. Reward maximisation
$$\min_v \sum_s v(s) \quad\text{s.t.}\quad v(s) \ge r(s,a) + \gamma\sum_{s'}P(s'\mid s,a)\,v(s') \quad\forall s, a.$$

**Why "min with ≥".** The constraints say $v \ge T^*v$ elementwise (≥ for *every* action ⇔ ≥ the max). $T^*$ is monotone and a contraction, so any such $v$ satisfies $v \ge v_*$. Minimising pushes $v$ down onto the smallest feasible point — $v_*$. Any positive state weights $\mu_0(s)$ give the same minimiser.

**Size:** $\lvert\mathcal S\rvert$ variables, $\lvert\mathcal S\rvert\lvert\mathcal A\rvert$ constraints.

## 2. Cost minimisation (shortest path)
$$\max_v\sum_s v(s)\quad\text{s.t.}\quad v(s) \le c(s,a) + \sum_{s'}P(s'\mid s,a)\,v(s'),\qquad v(\text{goal}) = 0.$$
Now ≤ for every action ⇔ ≤ the min, and maximising pushes $v$ **up** to $v_*$.

## 3. Worked example (quiz)
Edges $s_0 \to s_T$ (cost 5), $s_0 \to s_1$ (cost 2), $s_1 \to s_T$ (cost 1); $v(s_T) = 0$.

- **Correct:** $\max v_0 + v_1$ s.t. $v_0 \le 5$, $v_0 \le 2 + v_1$, $v_1 \le 1$ → $v_1 = 1$, $v_0 = \min(5, 3) = \mathbf 3$ ✓
- **Flawed ("min with ≥"):** $v_0 \ge 5$, $v_0 \ge 2 + v_1$, $v_1 \ge 1$ → $v_0 = \max(5, 3) = \mathbf 5$ — the *longest* path. (`quiz-errata.md` #2)

## Mnemonic
| Goal | LP objective | Constraint | Encodes |
|---|---|---|---|
| maximise reward | **min** Σv | **≥** | $v \ge \max_a(\cdot)$ |
| minimise cost | **max** Σv | **≤** | $v \le \min_a(\cdot)$ |

## Practice
<details><summary>Hallway (γ = 0.9): write the LP constraints at M.</summary>

$v(M) \ge 0 + 0.9\,v(L)$ (left) and $v(M) \ge 1 + 0.9\,v(R)$ (right), with $v(R) = 0$ by the terminal constraints $v(R) \ge 0.9\,v(R)$.
</details>

> **Run it:** `tests/test_worked_examples.py::test_shortest_path_lp_direction`; `tests/test_properties.py::test_vi_pi_lp_agree`
