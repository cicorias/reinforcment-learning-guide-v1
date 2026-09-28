# Linear and integer programming basics

> **Tier:** Beginner · **Prereqs:** `00/04` · **Code:** `rlguide.vertex_cover`

## 1. Standard forms
- **Canonical:** $\max c^\top x$ s.t. $Ax \le b$, $x \ge 0$.
- **Standard (equality):** add slacks $s \ge 0$ so that $Ax + s = b$.

## 2. Geometry
The feasible region is a convex polyhedron; the objective's level sets are parallel hyperplanes; the optimum (if one exists) is attained at a vertex — a basic feasible solution (see `00/04`).

## 3. Integer programming
Adding $x \in \mathbb Z^n$ (or $\{0,1\}^n$) makes the problem NP-hard in general.

**Vertex cover on the path 1–2–3–4** (edges 12, 23, 34):
$$\min\ x_1 + x_2 + x_3 + x_4 \quad\text{s.t.}\quad x_1 + x_2 \ge 1,\ \ x_2 + x_3 \ge 1,\ \ x_3 + x_4 \ge 1,\ \ x_i \in \{0,1\}.$$
Optimum **2** — e.g. $\{2,3\}$, $\{1,3\}$ or $\{2,4\}$.

**Contrast — independent set:** $\max\sum_i x_i$ s.t. $x_i + x_j \le 1$ per edge. Both the constraint direction **and** the objective flip. On this path the maximum independent set also has size 2 ($\{1,3\}$, $\{1,4\}$, $\{2,4\}$).

## 4. LP relaxation and the integrality gap
Replace $x \in \{0,1\}$ by $0 \le x \le 1$. For minimisation, $\mathrm{LP}^* \le \mathrm{OPT}$ (more feasible points).

**Integrality gap** $= \sup_I \mathrm{OPT}(I)/\mathrm{LP}^*(I)$. For vertex cover it is $2 - 2/n$, attained on $K_n$: the LP puts ½ on every vertex ($\mathrm{LP}^* = n/2$) while $\mathrm{OPT} = n - 1$. The path is bipartite, so its LP is integral.

## Pitfalls
- Vertex cover: **min** with **≥**. Independent set: **max** with **≤**.
- An LP relaxation value is a **bound**, not a feasible integer answer.

## Practice
<details><summary>Write the vertex-cover ILP for the triangle 1–2–3 and give OPT and LP*.</summary>

$\min x_1 + x_2 + x_3$ s.t. $x_1 + x_2 \ge 1$, $x_2 + x_3 \ge 1$, $x_1 + x_3 \ge 1$. OPT = 2; LP* = 1.5 (all ½).
</details>

> **Run it:** `tests/test_worked_examples.py::test_vertex_cover_path_opt`, `::test_vertex_cover_integrality_gap_complete_graph`
