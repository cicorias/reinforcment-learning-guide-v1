# CLAUDE.md

Guidance for Claude (and any AI assistant) working in this repository.

## Intent

This repo is a **self-checking learning workspace** for one person moving from beginner to
expert in four connected areas:

1. Markov decision processes and dynamic programming
2. Model-free RL (Monte Carlo, TD, SARSA, Q-learning, bandits, deep RL)
3. Linear and integer programming (LP geometry, simplex, branch and bound, the MDP LP)
4. Approximation algorithms (vertex-cover rounding, MAX-SAT, knapsack FPTAS)

It grew out of a 75-question quiz. The organising idea, which every piece of content should
reinforce, is:

> **The optimal value of a sequential decision problem is the fixed point of a Bellman operator.**
> DP computes it; sampling methods estimate it; the LP encodes it; approximation algorithms reuse
> the same tools (expectation, relaxation, rounding, DP) when exact optimisation is intractable.

## Goals (in priority order)

1. **Correctness.** Every number, formula and claim is right. Every numeric worked example is
   asserted by a test. When a source (including the original quiz) is wrong, say so and record it.
2. **Root understanding.** Math is built from first principles. Nothing is used before it is defined;
   prerequisites are linked. Prefer a short proof to an appeal to authority.
3. **Progression.** Beginner → Intermediate → Expert, with explicit prerequisites and checkpoints.
4. **Interactivity.** Theory → runnable code → notebook with sliders → "predict before you run".
5. **Low friction.** One toolchain (mise + uv), one command per action, green CI.

Non-goals: production-grade RL libraries, GPU deep learning, covering topics that never
connect back to the core idea.

## Toolchain rules — mise and uv only

- **mise** owns the toolchain (Python, uv) and all tasks. **uv** owns Python packages and the venv.
- Never use `pip`, `pip install`, `python -m venv`, `conda`, `poetry` or a bare `python`/`pytest`.
  Run Python through `uv run …` or, better, a `mise run <task>`.
- Add dependencies with `uv add <pkg>` (runtime) or `uv add --group <dev|notebooks> <pkg>`.
  Commit both `pyproject.toml` and `uv.lock`. Never edit `uv.lock` by hand.
- `mise.toml` sets `UV_PYTHON_DOWNLOADS=never`: uv must use mise's Python. Change the Python
  version only in `mise.toml` (`[tools] python`), and keep `requires-python` in `pyproject.toml` consistent.
- New recurring commands become **mise tasks** in `mise.toml` with a `description`. Don't add
  Makefiles, shell scripts or npm scripts for the same purpose.

### Commands

| Need | Command |
|---|---|
| first-time setup | `mise trust && mise install && mise run setup` |
| all tests | `mise run test` |
| worked-example tests only | `mise run test:examples` |
| lint / format | `mise run lint` / `mise run fmt` |
| everything CI runs | `mise run check` then `mise run notebooks:run` |
| regenerate notebooks | `mise run notebooks:build` |
| JupyterLab | `mise run lab` |
| list tasks | `mise tasks` |

**Before you report any change as done, run `mise run check`** (and `mise run notebooks:run`
if you touched notebooks or code they import). Report the actual result.

## Repository map

```
00-math-foundations/  01-beginner/  02-intermediate/  03-expert/   ← the guide (Markdown)
algorithms/pseudocode.md                                           ← pseudocode for every algorithm
src/rlguide/                                                       ← reference implementations
tests/test_worked_examples.py                                      ← every numeric example in the guide
tests/test_properties.py                                           ← theorems as tests (contraction, VI=PI=LP, …)
scripts/build_notebooks.py                                         ← SINGLE SOURCE for notebooks/*.ipynb
notebooks/                                                         ← generated; never hand-edit .ipynb
question-bank/{questions,common-traps,quiz-errata}.md
glossary.md  concept-map.md  ROADMAP.md  README.md
```

Module ↔ guide mapping lives in each module's docstring (`Guide: …`). Keep it accurate.

## Content conventions (Markdown)

- **Six-step template** for every concept:
  Intuition → Formal definition → Derivation/proof → Worked numeric example → Pitfalls → Practice.
- Practice solutions go in `<details><summary>…</summary> … </details>` blocks.
- Every guide file starts with a header line:
  `> **Tier:** … · **Prereqs:** … · **Code:** … · **Notebook:** …`
  and ends with a `> **Run it:**` line naming the exact tests / notebook.
- **Notation:** Sutton & Barto — $S_t, A_t, R_{t+1}, G_t, v_\pi, q_\pi, v_*, q_*$, $\gamma$ discount,
  $\alpha$ step size, $\varepsilon$ exploration. The reward following $A_t$ is $R_{t+1}$.
- **Math:** GitHub-flavoured LaTeX. Inline `$…$`; display `$$…$$` on their own lines.
  Use `\lvert x\rvert` / `\lVert x\rVert` instead of bare `|` inside tables. Don't use macros
  GitHub can't render (`\newcommand`, `\begin{align}` — use `\begin{aligned}` inside `$$`).
- Diagrams: Mermaid code blocks (they render on GitHub).
- File references use tier/number shorthand in prose (e.g. `02/05`) and full paths in links.
- Keep tone direct and warm; no filler. A beginner should never meet an undefined symbol.

## Code conventions (`src/rlguide/`)

- Python ≥ 3.12, NumPy + SciPy only at runtime. Teaching clarity beats performance.
- MDP arrays: `P[a, s, s']`, `R[s, a]`, stochastic policies `pi[s, a]` (rows sum to 1).
  Terminal states are absorbing with zero reward.
- Functions are pure where possible, take an explicit `seed` for anything random, and use
  `np.random.default_rng(seed)`. No global RNG state.
- Each module docstring names its guide file(s). Public functions get a one-line docstring
  containing the key formula.
- Ruff config in `pyproject.toml` is the style authority (`mise run fmt`).

## The testing contract (most important rule)

1. **Every numeric worked example in the Markdown has a test** in `tests/test_worked_examples.py`
   whose docstring names the guide file, e.g. `"""02-intermediate/04: ... z = 19/3"""`.
2. **Theorems get property tests** in `tests/test_properties.py` (contraction, VI = PI = LP,
   FPTAS ≥ (1−ε)OPT, rounding ≤ 2·LP, …).
3. If you change a number in the guide, change the test in the same commit — and vice versa.
4. Stochastic tests use fixed seeds and assert robust inequalities, not fragile exact values.
5. A number that cannot be tested (e.g. a historical runtime bound) must carry a citation.

## Notebooks

- `scripts/build_notebooks.py` is the only source. Edit the `NOTEBOOKS` dict, then
  `mise run notebooks:build`. `notebooks:check` (in CI) fails on drift.
- Notebooks import from `rlguide`; don't duplicate algorithm code inside them.
- Every notebook: recap → run → an `ipywidgets` slider where it teaches something →
  at least one "**Predict before you run:**" prompt. It must execute headless (`mise run notebooks:run`).
- Update `notebooks/README.md` when adding one.

## Correctness and errata policy

- The original quiz had six flawed items, documented in `question-bank/quiz-errata.md`.
  **Never "fix" the guide to match a flawed quiz answer.** Trust the derivation + test.
- When you find a new error (in a source, the quiz, or this repo): fix it, add/adjust a test,
  and add an errata entry if it concerns external material.
- Be precise about scope: convergence theorems here are **tabular, finite MDPs** unless stated.
  Distinguish "converges w.p. 1 in the limit" (sampling) from geometric/finite (DP).
- Watch these recurring traps (see `question-bank/common-traps.md`): SARSA vs Q-learning target,
  first- vs every-visit, **minimum** ratio test, LP direction (reward-max = min with ≥;
  cost-min = max with ≤), fractional LP ≠ incumbent, ε-soft ≠ uniform random,
  "*some* optimum is a vertex", constant α converges only without noise.

## Citations

Prefer primary sources and standard texts: Sutton & Barto (2nd ed.), Puterman, Bertsekas,
Bertsimas & Tsitsiklis, CLRS, Kleinberg & Tardos, Vazirani, Williamson & Shmoys, and original
papers (Watkins & Dayan 1992; Singh et al. 2000; Mnih et al. 2015; van Hasselt 2010; Ye 2011;
Goemans & Williamson 1994). Cite chapter/section only when you've verified it; otherwise cite
the work. Don't invent page or theorem numbers.

## Adding a new topic — checklist

1. Decide the tier and prerequisites; add a node + edges in `concept-map.md`.
2. Write the Markdown with the six-step template, header line and `Run it` line.
3. Implement in `src/rlguide/<module>.py` (docstring names the guide file).
4. Add worked-example tests and, if there's a theorem, a property test.
5. Add pseudocode to `algorithms/pseudocode.md`.
6. Add a notebook spec in `scripts/build_notebooks.py` if interaction helps; rebuild.
7. Add 2–3 questions to `question-bank/questions.md`, traps to `common-traps.md`, terms to `glossary.md`.
8. Update the README map / ROADMAP if structure changed.
9. `mise run check` and `mise run notebooks:run` — both green.

## When the learner asks for help (tutoring mode)

- Find where the topic lives in the guide and teach at the learner's current tier; link the file.
- Lead with intuition, then the formula, then a tiny numeric example — and offer the matching
  test or notebook so they can poke at it.
- For quiz-style questions, explain why each wrong option is wrong; check `quiz-errata.md` first.
- If the question reveals a gap in the guide, propose adding it using the checklist above.
- Never just hand over practice solutions that are hidden in `<details>` blocks unless asked.

## Definition of done

- Guide text, code, tests, notebooks and question bank are consistent with each other.
- `mise run check` passes; notebooks execute.
- No new tool outside mise/uv; `uv.lock` updated if dependencies changed.
- Errata updated if an external source was found to be wrong.
