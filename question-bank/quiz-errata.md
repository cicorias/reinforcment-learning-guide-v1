# Quiz errata

Six items from the original quiz were wrong or ambiguous. The guide and tests use the corrected versions.

1. **First-visit MC (A, B, A, C; rewards 0, 2, −1, 3; γ = 1).** Correct answer **4.0** (returns list [4]) — not among the options. The likely distractor 3.0 is the *every-visit* answer. → `tests/test_worked_examples.py::test_first_visit_quiz_example`
2. **Shortest-path LP direction.** "Minimise Σv s.t. $v(s) \ge c + v(s')$" yields **5** (the longest path). The correct cost formulation is **maximise with ≤**, giving **3**. → `::test_shortest_path_lp_direction`
3. **Branch-and-bound data.** A node LP reported $x_2 = 1.5$ in a 0–1 program. The relaxation bounds $0 \le x_2 \le 1$ make that impossible, so the node's bound and branching are unreliable. Use the self-consistent example in `02-intermediate/04`. → `::test_branch_and_bound_example`
4. **"Every optimal solution lies at a vertex."** Overstatement. The theorem guarantees *at least one* optimal vertex (when vertices exist); when the objective is parallel to a face, infinitely many non-vertex points are optimal.
5. **Method of conditional expectations as a "lower bound".** Precisely: the conditional expectation never decreases as variables are fixed, so the final assignment's value is ≥ the initial expectation ≥ m/2. The expectation is not a lower bound on *every* assignment — it guarantees that *some* (the constructed) assignment achieves it. (Historically, Johnson's 1974 algorithm was a deterministic greedy procedure; "random assignment + derandomise" is the modern textbook presentation of the same ½ guarantee.)
6. **Policy in the MDP tuple.** Listing π as part of the MDP is incorrect. π is chosen/optimised; the MDP is $(\mathcal S, \mathcal A, P, R, \gamma, \mu_0)$.

**Policy:** when a quiz answer contradicts a derivation in this guide, trust the derivation and its test — then add an entry here.
