# Question bank

Format: **question** → answer. *Why.* Tags: **[B]** beginner · **[I]** intermediate · **[E]** expert.
Cover the answers and work each one before looking. Numeric answers are asserted in `tests/`.

## Beginner
1. [B] Ordering in the RL loop? → Observe $S_t$ → choose $A_t$ → receive $R_{t+1}, S_{t+1}$. *The reward is indexed with the next state.*
2. [B] Which is NOT in the MDP tuple: S, A, P, R, γ, π? → **π**. *The policy is the solution, not the problem.*
3. [B] A Markov chain differs from an MDP by lacking? → Actions (and rewards).
4. [B] $P(s'\mid s) = (0.2, 0.5, 0.3)$, $V = (4, 1, 7)$. $\mathbb E[V(S')]$? → **3.4**.
5. [B] $\gamma = 0.9$, reward 1 forever. $G$? → **10** $= 1/(1-0.9)$.
6. [B] Which is NOT an interpretation of γ: time preference, survival probability, learning rate, finiteness device? → **Learning rate** (that is α).
7. [B] A fixed π in an MDP induces? → A time-homogeneous Markov chain, $P_\pi(s'\mid s) = \sum_a\pi(a\mid s)P(s'\mid s,a)$.
8. [B] Hallway L–M–R, +1 on arriving at R, γ = 0.9. $v_*(L)$? → **0.9**.
9. [B] Step penalty −1 and trap −100 with slippery moves typically produce? → Longer, safer paths.
10. [B] First-visit MC: episode A,B,A,C, rewards 0,2,−1,3, γ = 1. V(A)? → **4.0** (returns list [4]). *If 4.0 isn't offered, the question is flawed; 3.0 is every-visit.*
11. [B] Returns for A: 4, 2, (5 then 1 in the same episode). First-visit vs every-visit? → **3.67 vs 3.00**.
12. [B] TD target with r = 2, γ = 0.9, V(s′) = 8? → **9.2**. Update from 5 with α = 0.5? → **7.1**.
13. [B] TD differs from MC because it? → Bootstraps and updates online before the episode ends.
14. [B] Lower variance, MC or TD(0)? → TD(0). *(MC is unbiased; TD is biased.)*
15. [B] ε-greedy, ε = 0.2, k = 4: probability of the greedy arm? → **0.85**.
16. [B] Incremental mean formula? → $Q_{n+1} = Q_n + \frac1n(R_n - Q_n)$.

## Intermediate
17. [I] Bellman expectation vs optimality — which averages over actions? → Expectation (weights π); optimality maximises.
18. [I] $(I - \gamma P_\pi)v = R_\pi$, $P_\pi$ swaps 2 states, R = (1, 1), γ = 0.5? → $v = (2, 2)$.
19. [I] During iterative policy evaluation, the policy should be? → **Held fixed.**
20. [I] Jacobi vs Gauss–Seidel? → Two arrays vs in-place; in-place usually converges faster.
21. [I] Stopping criterion $\Delta_k$? → $\max_s\lvert V_{k+1}(s) - V_k(s)\rvert < \theta$.
22. [I] Does PI terminate in finitely many iterations? → **Yes** (finite policy set, strict improvement).
23. [I] Does VI reach $v_*$ exactly in finite steps in general? → **No** — asymptotically (geometrically).
24. [I] $\pi_{VI}$ vs $\pi_{PI}$ after convergence? → Same $v_*$; actions may differ only at ties.
25. [I] Goal moves; dynamics known. Best approach? → Replan with DP (model-based); no new samples needed.
26. [I] SARSA target? → $R + \gamma Q(S', A')$. Q-learning target? → $R + \gamma\max_a Q(S', a)$.
27. [I] Expected SARSA target? → $R + \gamma\sum_a\pi(a\mid S')Q(S', a)$.
28. [I] Q = 0, α = 0.5, r = 1, max Q(s′) = 0.6. New Q? → **0.5 + 0.3γ**.
29. [I] Cliff walking: which learns the safer path? → **SARSA**. Which falls more during training? → **Q-learning**.
30. [I] Why is Q-learning off-policy? → Its target evaluates the greedy policy regardless of behaviour.
31. [I] Q-learning convergence requires? → All (s,a) visited infinitely often + Robbins–Monro α per (s,a) + tabular representation.
32. [I] Why does constant α = 0.9 fail to converge in a stochastic MDP? → $\sum\alpha^2 = \infty$; noise never averages out (variance $\alpha\sigma^2/(2-\alpha)$).
33. [I] Could constant α converge in a deterministic MDP? → **Yes** — no sampling noise.
34. [I] GLIE means? → Infinite exploration of all pairs + greedy in the limit (e.g. ε = 1/k).
35. [I] ε-soft vs uniform random? → ε-soft only requires $\pi(a\mid s) \ge \varepsilon/\lvert A\rvert$; uniform random is one special case; ε-greedy is the usual one.
36. [I] Simplex leaving variable: max or min ratio? → **Minimum** ratio. *Quiz example: ratios 2 and 3 → s₁ leaves.*
37. [I] Simplex optimum for max 3x₁+2x₂, 2x₁+x₂≤4, x₁+2x₂≤3? → $x = (5/3, 2/3)$, $z = 19/3$.
38. [I] Vertex cover ILP on path 1–2–3–4? → min Σx s.t. $x_1+x_2 \ge 1$, $x_2+x_3 \ge 1$, $x_3+x_4 \ge 1$, x binary. OPT = 2.
39. [I] Independent set constraint direction? → $x_i + x_j \le 1$, maximise.
40. [I] B&B: node LP is fractional with value 9.33 > incumbent. Action? → **Branch** (never make it the incumbent).
41. [I] B&B prune rules? → Infeasible; bound ≤ incumbent; integral (update incumbent if better).
42. [I] MDP LP for reward maximisation? → **min** Σv s.t. **≥** constraints.
43. [I] Shortest path via LP (costs)? → **max** Σv s.t. **≤** constraints. Example optimum 3, not 5.
44. [I] Random assignment: probability a 3-literal clause is satisfied? → **7/8**.
45. [I] Why is $\mathbb E[X] \ge \mathrm{OPT}/2$ for random MAX-SAT? → Each clause ≥ ½, linearity ⇒ ≥ m/2, and m ≥ OPT.
46. [I] Knapsack FPTAS scale factor and runtime? → $K = \varepsilon v_{\max}/n$; $O(n^3/\varepsilon)$.

## Expert
47. [E] Why do rewards cancel in the contraction proof? → They don't depend on v; only $\gamma P(u - v)$ remains.
48. [E] Deadly triad? → Function approximation + bootstrapping + off-policy ⇒ possible divergence.
49. [E] Two DQN stabilisers? → Experience replay, target network.
50. [E] Double Q-learning fixes? → Maximisation (overestimation) bias, by decoupling selection from evaluation.
51. [E] Batch TD vs batch MC on Example 6.4: V(A)? → TD 0.75 (certainty equivalence); MC 0.
52. [E] LP randomised-rounding MAX-SAT ratio? → $1 - 1/e \approx 0.632$. Best-of-two? → ¾.
53. [E] Dual MDP LP variables? → Discounted occupancy measures $d(s,a)$.
54. [E] PTAS vs FPTAS? → Polynomial in $n$ for fixed ε vs polynomial in $n$ and $1/\varepsilon$.
55. [E] Is simplex polynomial? → Not in the worst case (Klee–Minty); strongly polynomial on fixed-γ MDPs (Ye 2011). Ellipsoid and interior-point methods are polynomial.
