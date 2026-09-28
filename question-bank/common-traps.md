# Common traps

| Trap | Correct idea | Where |
|---|---|---|
| SARSA vs Q-learning target | SARSA uses $Q(S', A')$ with the *actual* next action; Q-learning uses $\max_a Q(S', a)$ | `02/02` |
| First-visit vs every-visit | First-visit: one return per episode per state; every-visit: all occurrences | `01/04` |
| Min vs max ratio | Leaving variable = **minimum** ratio (keeps feasibility); entering = best reduced cost | `02/04` |
| LP inequality direction | Reward-max MDP: **min** Σv, **≥**. Cost-min: **max** Σv, **≤** | `02/05` |
| Fractional LP as incumbent | Never — fractional values are **bounds**; only integral feasible solutions become incumbents | `02/04` |
| ε-soft vs uniform random | ε-soft is a *lower bound* on probabilities; uniform random is one extreme | `02/03` |
| Averaging vs max | Bellman expectation averages over π; optimality maximises; MC averages returns | `01/03` |
| TD vs MC timing | TD updates every step (online); MC waits for episode end | `01/04` |
| Expectation vs most likely value | $\mathbb E[V(S')] = \sum PV$ — not the mode, not the plain average | `00/01` |
| "Every optimum is a vertex" | *Some* optimum is a vertex (when a vertex exists); whole faces can be optimal | `00/04` |
| Constant α converges | Only in deterministic settings; stochastic settings need Robbins–Monro | `00/05` |
| Policy is part of the MDP | The policy is the solution; the MDP is $(S, A, P, R, \gamma, \mu_0)$ | `01/01` |
| VI finite termination | VI converges asymptotically; PI terminates finitely | `02/01` |
| Q-learning needs GLIE | Only to *act* optimally; its values converge under any sufficiently exploratory behaviour | `02/02` |
| Reward index | The reward following $A_t$ is $R_{t+1}$, not $R_t$ | `01/01` |
| Knapsack scaling | Scale **values**, not weights; discard items with $w_i > W$ first | `02/06` |
