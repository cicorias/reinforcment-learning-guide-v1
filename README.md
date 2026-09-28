# RL · Dynamic Programming · LP/ILP · Approximation Algorithms

A three-tier (**Beginner → Intermediate → Expert**) learning guide with runnable,
tested reference code and interactive notebooks.

> **The one idea:** the optimal value of a sequential decision problem is the
> **fixed point of a Bellman operator**. Dynamic programming computes it exactly;
> Monte Carlo / TD / SARSA / Q-learning estimate it from samples; the MDP linear
> program encodes it as constraints. Approximation algorithms (MAX-SAT, knapsack
> FPTAS) reuse the same toolkit — expectation, relaxation, rounding, DP — to get
> provable guarantees when exact optimisation is intractable.

## Quick start

Everything runs through [mise](https://mise.jdx.dev) (toolchain + tasks) and
[uv](https://docs.astral.sh/uv/) (Python packages). Nothing else is needed.

```bash
# 1. install mise once:  https://mise.jdx.dev/getting-started.html
mise trust            # allow this repo's mise.toml
mise install          # installs Python 3.12 + uv
mise run setup        # uv sync --all-groups  (creates .venv)
mise run test         # 54 tests — every worked example in the guide is asserted
mise run lab          # JupyterLab on the interactive notebooks
```

Run `mise tasks` to see everything. Highlights:

| Task | What it does |
|---|---|
| `mise run test` | full test suite |
| `mise run test:examples` | only the worked-example checks, verbose |
| `mise run demo:examples` | print every headline worked example with its computed value |
| `mise run demo:cliff` | SARSA vs Expected SARSA vs Q-learning on Cliff Walking |
| `mise run lab` | JupyterLab |
| `mise run notebooks:build` | regenerate notebooks from `scripts/build_notebooks.py` |
| `mise run check` | lint + tests + notebook freshness (what CI runs) |

**GitHub Codespaces:** open the repo in a Codespace — `.devcontainer/` installs mise and runs setup for you.

## How to use this guide

1. Start with [`ROADMAP.md`](ROADMAP.md) — tiers, hours, checkpoints, capstone.
2. Read the tier folders in order. Every concept follows the same six steps:
   **Intuition → Definition → Derivation/Proof → Worked example → Pitfalls → Practice** (solutions in collapsible blocks).
3. Each file ends with a **Run it** box pointing to the module, test and notebook for that topic.
4. After each tier, self-test with [`question-bank/questions.md`](question-bank/questions.md).

## Map

| Folder | Contents |
|---|---|
| [`00-math-foundations/`](00-math-foundations) | probability & expectation · series, norms, contractions · linear algebra · convexity & polytopes · stochastic approximation |
| [`01-beginner/`](01-beginner) | agent–environment loop & MDPs · returns & discounting · Bellman equations · MC & TD basics · bandits · LP & ILP basics |
| [`02-intermediate/`](02-intermediate) | dynamic programming · SARSA / Q-learning / Expected SARSA · MC control & convergence · simplex & branch-and-bound · MDP as LP · approximation algorithms |
| [`03-expert/`](03-expert) | contraction proofs & complexity · TD(λ), off-policy, importance sampling · function approximation & deep RL · LP duality & occupancy measures · MAX-SAT rounding & FPTAS proofs |
| [`algorithms/pseudocode.md`](algorithms/pseudocode.md) | pseudocode for every algorithm |
| [`src/rlguide/`](src/rlguide) | NumPy/SciPy reference implementations |
| [`tests/`](tests) | worked-example and theorem/property tests |
| [`notebooks/`](notebooks) | 11 interactive notebooks (generated) |
| [`question-bank/`](question-bank) | 55 quiz-style questions · common traps · quiz errata |
| [`glossary.md`](glossary.md) · [`concept-map.md`](concept-map.md) | vocabulary · Mermaid dependency graph |
| [`CLAUDE.md`](CLAUDE.md) | intent, goals and working rules for AI-assisted editing |

## Notation

Sutton & Barto throughout: $S_t, A_t, R_{t+1}, G_t, v_\pi, q_\pi, v_*, q_*$.
Array code uses `P[a, s, s']` and `R[s, a]` (see `src/rlguide/envs.py`).

## Primary references

- Sutton & Barto, *Reinforcement Learning: An Introduction*, 2nd ed. (MIT Press, 2018) — free online from the authors.
- Puterman, *Markov Decision Processes* (Wiley, 1994); Bertsekas, *Dynamic Programming and Optimal Control*; Bertsekas & Tsitsiklis, *Neuro-Dynamic Programming* (1996).
- Watkins & Dayan, "Q-learning", *Machine Learning* 8 (1992); Singh, Jaakkola, Littman & Szepesvári, "Convergence results for single-step on-policy RL algorithms", *Machine Learning* 38 (2000).
- Mnih et al., "Human-level control through deep RL", *Nature* 518 (2015); van Hasselt, "Double Q-learning", NIPS (2010).
- Bertsimas & Tsitsiklis, *Introduction to Linear Optimization* (1997); CLRS; Kleinberg & Tardos, *Algorithm Design*.
- Vazirani, *Approximation Algorithms* (2001); Williamson & Shmoys, *The Design of Approximation Algorithms* (2011; free electronic edition).
- Courses: David Silver's UCL RL lectures · Stanford CS234 · Berkeley CS285.
