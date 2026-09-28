# The simplex method and branch and bound

> **Tier:** Intermediate · **Prereqs:** `00/04`, `01/06` · **Code:** `rlguide.simplex`, `rlguide.branch_and_bound` · **Notebooks:** `08_simplex_visual`, `09_branch_and_bound_tree`

## 1. Simplex, step by step
1. Convert to standard form with slacks; the initial BFS is the slacks ($x = 0$).
2. **Entering variable:** a nonbasic variable with positive reduced cost (for max). Dantzig's rule picks the largest — in the tableau row $z - c^\top x$, the most negative entry.
3. **Leaving variable — minimum ratio test:** among rows with a positive pivot-column entry, pick $\min_i b_i/a_{ij}$. **Minimum**, because that constraint becomes tight first; any larger step makes a basic variable negative.
4. Pivot; repeat until no improving direction remains.

### Worked example (quiz)
$$\max 3x_1 + 2x_2 \quad\text{s.t.}\quad 2x_1 + x_2 + s_1 = 4,\quad x_1 + 2x_2 + s_2 = 3.$$
- **Pivot 1.** $x_1$ enters (coefficient 3). Ratios $4/2 = 2$, $3/1 = 3$ → **$s_1$ leaves**.
  Now $x_1 = 2 - \tfrac12x_2 - \tfrac12s_1$, $z = 6 + \tfrac12x_2 - \tfrac32s_1$, $s_2 = 1 - \tfrac32x_2 + \tfrac12s_1$.
- **Pivot 2.** $x_2$ enters (+½). Ratios $2/0.5 = 4$, $1/1.5 = 2/3$ → $s_2$ leaves.
  $x_2 = \tfrac23$, $x_1 = \tfrac53$, $z = \tfrac{19}{3} - \tfrac13s_2 - \tfrac43s_1$.
- All reduced costs ≤ 0 → **optimal**, $z^* = 19/3 \approx 6.33$.

## 2. Degeneracy and Bland's rule
A degenerate BFS has a basic variable at 0; a pivot may leave $z$ unchanged and **cycling** is possible. **Bland's rule** (1977) — always pick the lowest-index eligible entering and leaving variables — guarantees termination (`simplex(..., rule="bland")`).

## 3. Branch and bound (maximisation)
- **Bound:** the node's LP relaxation value upper-bounds every integer solution in its subtree.
- **Prune** when (i) the LP is infeasible, (ii) the LP bound ≤ incumbent, or (iii) the LP solution is integral (update the incumbent if better; stop branching there).
- **Branch** on a fractional $x_j = f$: children $x_j \le \lfloor f\rfloor$ and $x_j \ge \lceil f\rceil$.
- **A fractional LP solution is never an incumbent** — only a bound.

### Worked example
$$\max 5x_1 + 4x_2 + 3x_3 \quad\text{s.t.}\quad 2x_1 + 3x_2 + x_3 \le 4,\quad x \in \{0,1\}^3.$$
- **Root LP** (greedy by value/weight: $x_3$ 3.0, $x_1$ 2.5, $x_2$ 1.33): $x_3 = 1$, $x_1 = 1$, $x_2 = 1/3$ → bound $28/3 \approx 9.33$. Branch on $x_2$.
- **$x_2 = 0$:** LP gives $x_1 = x_3 = 1$, value 8, **integral** → incumbent 8.
- **$x_2 = 1$:** capacity 1 left → $x_3 = 1$, $x_1 = 0$, value 7. $7 \le 8$ → **prune by bound**.
- **Optimum 8** at $(1, 0, 1)$.

> The quiz reported $x_2 = 1.5$ at a node of a 0–1 program — impossible under the relaxation bounds $0 \le x_2 \le 1$. See `question-bank/quiz-errata.md` #3.

## Pitfalls
- Leaving variable uses the **minimum** ratio, over **positive** pivot entries only.
- Never make a fractional point the incumbent.
- For max problems, prune when bound **≤** incumbent (not ≥).

## Practice
<details><summary>max x₁ + x₂ s.t. 2x₁ + 2x₂ ≤ 3, x ∈ {0,1}². What happens in B&B?</summary>

The root LP value is 1.5 with a fractional optimum. Every integer point has $x_1 + x_2 \le 1$ (because $2(x_1+x_2) \le 3$), so the first integral leaf gives incumbent 1 — but plain LP bounds of 1.5 keep other nodes alive. **Trick:** when the objective has integer coefficients, round the bound down: $\lfloor 1.5\rfloor = 1 \le$ incumbent, so everything prunes immediately. Loose bounds are the main cost driver in B&B.
</details>

> **Run it:** `tests/test_worked_examples.py::test_simplex_quiz_example`, `::test_branch_and_bound_example`
