# Notebooks

**Generated files — do not hand-edit.** Edit `scripts/build_notebooks.py`, then run
`mise run notebooks:build`. CI fails if these are stale (`mise run notebooks:check`).

Open with `mise run lab`. Every notebook follows **recap → run → interact (sliders) → "Predict before you run"**.

| Notebook | Guide files | Interactive elements |
|---|---|---|
| `01_expectation_and_contraction` | `00/01`, `00/02` | γ slider; VI error vs $\gamma^k$ bound |
| `02_gridworld_dp` | `02/01`, `02/05` | VI vs PI vs LP; Jacobi vs Gauss–Seidel Δ-curves; hallway |
| `03_mc_vs_td` | `01/04`, `03/02` | first vs every visit; batch TD vs MC (Ex. 6.4); α sweep on random walk |
| `04_cliff_walking` | `02/02` | SARSA / Expected SARSA / Q-learning returns + greedy paths; ε, α sliders |
| `05_convergence_stepsizes` | `00/05` | constant α vs 1/n; noise slider; theory variance |
| `06_bandits` | `01/05` | ε-greedy vs greedy vs UCB vs Thompson regret |
| `07_maximization_bias` | `02/02` | Q vs Double Q on Sutton & Barto Ex. 6.7 |
| `08_simplex_visual` | `02/04` | pivot log; polytope + pivot path |
| `09_branch_and_bound_tree` | `02/04` | node log with prune reasons |
| `10_approx_algorithms` | `02/06`, `03/05` | MAX-SAT derandomisation trace; FPTAS ε vs quality; vertex-cover rounding |
| `11_linear_fa_and_deadly_triad` | `03/03` | Baird's counterexample divergence |

Smoke-test them all: `mise run notebooks:run`.
