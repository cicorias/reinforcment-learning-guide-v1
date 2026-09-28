# Roadmap

| Tier | Files | Est. hours | Exit checkpoint |
|---|---|---|---|
| Math foundations | `00-math-foundations/*` | 15–20 | Prove $(I-\gamma P)$ is invertible; prove a contraction has at most one fixed point |
| Beginner | `01-beginner/*` | 25–35 | Hand-compute a return, a TD(0) update, a first-visit MC estimate, one simplex ratio test |
| Intermediate | `02-intermediate/*` | 35–45 | Implement VI / PI / SARSA / Q-learning; solve a 3-variable branch-and-bound; run the knapsack FPTAS by hand |
| Expert | `03-expert/*` | 40–60 | Prove the $T^*$ contraction, policy improvement, the FPTAS bound and the ¾ MAX-SAT bound; explain the deadly triad |

## Suggested order

```
00/01 → 00/02 → 00/03 → 00/04 → 00/05
01/01 → 01/02 → 01/03 → 01/04 → 01/05 → 01/06
02/01 → 02/02 → 02/03 → 02/04 → 02/05 → 02/06
03/01 → 03/02 → 03/03 → 03/04 → 03/05
```

The RL track (`*/01–05` of each tier) and the optimisation track (`01/06`, `02/04–06`, `03/04–05`)
can be studied in parallel; they meet in `02-intermediate/05-mdp-as-lp.md`.

## Self-assessment checkpoints

At the end of each tier, answer that tier's section of
[`question-bank/questions.md`](question-bank/questions.md) **without notes**.

- **≥ 85 %** → move on.
- **< 85 %** → re-read the *Pitfalls* sections for the questions you missed, then check
  [`question-bank/common-traps.md`](question-bank/common-traps.md).

Before each checkpoint, run the matching notebooks and make every **Predict before you run**
prediction in writing first.

## Capstone: "Planner vs. Learner Lab"

Build one gridworld with a cliff, a trap and a movable goal (add it as `src/rlguide/capstone.py`
with tests in `tests/test_capstone.py`):

1. **Plan.** Solve it with value iteration, policy iteration **and** the LP
   (`rlguide.mdp_lp.solve_primal`). Assert all three agree to $10^{-6}$.
2. **Learn.** Train MC control, SARSA, Expected SARSA, Q-learning and Double Q-learning.
   Plot return per episode and $\lVert Q - q_*\rVert_\infty$ (you know $q_*$ from step 1).
   Compare constant $\alpha$ with $\alpha = 1/N(s,a)$.
3. **Move the goal.** Show replanning with the known model is instant, while model-free
   learners must relearn from new experience.
4. **Shape rewards.** Add a step penalty and a trap penalty with slippery moves; show the
   switch to longer, safer paths.
5. **Bonus (optimisation track).** Formulate "place $k$ sensors that cover every cliff-edge
   cell" as a vertex-cover ILP. Solve with `rlguide.branch_and_bound` and compare with
   `rlguide.vertex_cover.lp_rounding`.

**Done when:** `mise run check` passes and the capstone notebook tells the story in plots.
