# Approximation algorithms

> **Tier:** Intermediate · **Prereqs:** `00/01`, `01/06` · **Code:** `rlguide.vertex_cover`, `rlguide.maxsat`, `rlguide.knapsack_fptas` · **Notebook:** `10_approx_algorithms`

## 1. Definitions
- **α-approximation:** a polynomial-time algorithm whose output is within factor α of OPT on every instance (Williamson & Shmoys, Def. 1.1).
- **PTAS:** $(1-\varepsilon)$-approximation (max) in time polynomial in $n$ for each fixed $\varepsilon$ (possibly like $n^{1/\varepsilon}$).
- **FPTAS:** time polynomial in **both** $n$ and $1/\varepsilon$.

## 2. Vertex cover by LP rounding — a 2-approximation
Solve the LP relaxation for $x^*$; output $C = \{v : x^*_v \ge \tfrac12\}$.
- *Feasible:* each edge has $x^*_u + x^*_v \ge 1$, so some endpoint is ≥ ½.
- *Cost:* $\lvert C\rvert \le \sum_v 2x^*_v = 2\,\mathrm{LP}^* \le 2\,\mathrm{OPT}$.

Extreme points of this LP are half-integral, $x_v \in \{0, \tfrac12, 1\}$ (Nemhauser & Trotter 1975).

## 3. Randomised MAX-SAT — a ½-approximation
Set each variable True independently w.p. ½. A clause with $k$ distinct literals is unsatisfied only if all $k$ are false (prob. $2^{-k}$):
$$\Pr[C\text{ satisfied}] = 1 - 2^{-k} \ge \tfrac12.$$
With $X = \sum_C\mathbf 1[C\text{ sat}]$, linearity gives
$$\mathbb E[X] = \sum_C\big(1 - 2^{-k_C}\big) \ge \frac m2 \ge \frac{\mathrm{OPT}}{2}\quad(\text{since }\mathrm{OPT} \le m).$$
Johnson (1974) introduced approximation algorithms with this ½ guarantee (and $1 - 2^{-k}$ when every clause has ≥ $k$ literals).

## 4. Derandomisation by conditional expectations
For $i = 1..n$: compute $\mathbb E[X \mid x_1..x_{i-1}\text{ fixed}, x_i = T]$ and the same with $F$; fix $x_i$ to the larger.

**Why it never decreases:** $\mathbb E[X\mid\text{past}] = \tfrac12\mathbb E[X\mid\text{past}, T] + \tfrac12\mathbb E[X \mid \text{past}, F]$ — an average is at most its larger term. After $n$ steps the "expectation" is the deterministic value of the final assignment, so it is $\ge \mathbb E[X] \ge m/2$.

Each conditional expectation is polynomial: a satisfied clause contributes 1; a clause with $u$ unset literals and none true contributes $1 - 2^{-u}$.

### Worked example
$C_1 = (x_1 \lor x_2)$, $C_2 = (\lnot x_1 \lor x_3)$, $C_3 = (\lnot x_2 \lor \lnot x_3)$, $C_4 = (x_1)$. Start: $\mathbb E = 0.75\cdot 3 + 0.5 = 2.75$.

| step | E \| T | E \| F | choose |
|---|---|---|---|
| $x_1$ | $1 + 0.5 + 0.75 + 1 = 3.25$ | $0.5 + 1 + 0.75 + 0 = 2.25$ | T (avg 2.75 ✓) |
| $x_2$ | $1 + 0.5 + 0.5 + 1 = 3.0$ | $1 + 0.5 + 1 + 1 = 3.5$ | F |
| $x_3$ | 4 | 3 | T |

**All 4 clauses satisfied.**

## 5. Knapsack FPTAS
1. Discard items with $w_i > W$ (they never fit — and keeping them breaks $\mathrm{OPT} \ge v_{\max}$).
2. $K = \varepsilon v_{\max}/n$, $v'_i = \lfloor v_i / K\rfloor$.
3. **Value-indexed DP:** $A[i][p]$ = min weight to reach scaled value exactly $p$ with the first $i$ items,
$$A[i][p] = \min\big(A[i-1][p],\ w_i + A[i-1][p - v'_i]\big).$$
Return the largest $p$ with $A[n][p] \le W$.

**Runtime:** $p \le n\,v'_{\max} \le n^2/\varepsilon$, so $O(n \cdot n^2/\varepsilon) = O(n^3/\varepsilon)$ (Ibarra & Kim 1975; Lawler 1979). Guarantee proof: `03-expert/05`.

### Worked example
Values 60, 100, 120; weights 10, 20, 30; $W = 50$; $\varepsilon = 0.5$.
$K = 0.5\cdot 120/3 = 20$, $v' = (3, 5, 6)$. Best feasible scaled set: items {2, 3} (weight 50, $v' = 11$) → true value **220 = OPT**.

## Pitfalls
- Knapsack FPTAS scales **values**, not weights (weights keep feasibility exact).
- Forgetting to discard too-heavy items breaks the proof.
- The conditional-expectation method gives *one* good assignment; it does not bound every assignment (errata #5).

## Practice
<details><summary>Clause (x₁ ∨ ¬x₂ ∨ x₃) under a uniformly random assignment — probability satisfied?</summary>

$1 - 2^{-3} = 7/8$.
</details>

> **Run it:** `tests/test_worked_examples.py::test_maxsat_derandomization_trace`, `::test_knapsack_fptas_example`, `::test_maxsat_clause_probability`; `tests/test_properties.py::test_vertex_cover_rounding_is_2_approx`, `::test_knapsack_fptas_guarantee`
