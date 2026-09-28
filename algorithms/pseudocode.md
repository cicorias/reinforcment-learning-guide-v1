# Pseudocode

Each block names its reference implementation in `src/rlguide/`.

```text
ITERATIVE POLICY EVALUATION (in-place)                 # mdp_dp.iterative_policy_evaluation
  V(s) ← 0 ∀s
  repeat Δ←0
    for s in S: v←V(s); V(s)←Σ_a π(a|s) Σ_{s',r} p(s',r|s,a)[r+γV(s')]; Δ←max(Δ,|v−V(s)|)
  until Δ<θ

POLICY ITERATION                                        # mdp_dp.policy_iteration
  π arbitrary
  loop: V←Evaluate(π); stable←true
        for s: old←π(s); π(s)←argmax_a Σ p(s',r|s,a)[r+γV(s')]; if old≠π(s): stable←false
        if stable: return V,π

VALUE ITERATION                                         # mdp_dp.value_iteration
  repeat Δ←0; for s: v←V(s); V(s)←max_a Σ p[r+γV(s')]; Δ←max(Δ,|v−V(s)|) until Δ<θ
  π(s)←argmax_a Σ p[r+γV(s')]

FIRST-VISIT MC PREDICTION                               # mc_td_prediction.mc_prediction
  for each episode: G←0
    for t=T−1..0: G←γG+R_{t+1}; if S_t ∉ {S_0..S_{t−1}}: append G to Returns(S_t); V(S_t)←mean

TD(0):          V(S)←V(S)+α[R+γV(S')−V(S)]                          # mc_td_prediction.td0_update
SARSA:          A'~ε-greedy(Q,S'); Q(S,A)+=α[R+γQ(S',A')−Q(S,A)]    # td_control.sarsa_update
Q-LEARNING:     Q(S,A)+=α[R+γ max_a Q(S',a)−Q(S,A)]                 # td_control.q_learning_update
EXPECTED SARSA: target R+γ Σ_a π(a|S')Q(S',a)                       # td_control.expected_sarsa_update
DOUBLE Q:       w.p. ½: a*←argmax_a Q1(S',a); Q1(S,A)+=α[R+γQ2(S',a*)−Q1(S,A)]  else symmetric

UCB1: play each arm once; then A_t←argmax_a Q(a)+c√(ln t / N(a))    # bandits.run_bandit

SIMPLEX (max, Ax≤b, b≥0)                                # simplex.simplex
  tableau with slacks; loop: j←most negative objective-row entry; if none: optimal
    i←argmin_{a_ij>0} b_i/a_ij (none → unbounded); pivot(i,j)

BRANCH AND BOUND (max)                                  # branch_and_bound.branch_and_bound
  incumbent←−∞; stack←{root}
  while stack: node←pop; solve LP
    if infeasible or LP≤incumbent: prune
    elif x integral: incumbent←LP value, store x
    else pick fractional x_j=f; push (x_j≤⌊f⌋),(x_j≥⌈f⌉)

VERTEX COVER LP ROUNDING                                # vertex_cover.lp_rounding
  x*←LP relaxation; return {v : x*_v ≥ ½}

DERANDOMIZED MAXSAT                                     # maxsat.derandomized
  for i=1..n: x_i ← argmax_{b∈{T,F}} E[#sat | x_1..x_{i−1}, x_i=b]

KNAPSACK FPTAS                                          # knapsack_fptas.fptas
  drop w_i>W; K←ε v_max/n; v'_i←⌊v_i/K⌋
  A[0]←0, A[p>0]←∞; for each item i: for p from Σv' down to v'_i: A[p]←min(A[p], A[p−v'_i]+w_i)
  return set achieving max{p : A[p]≤W}
```
