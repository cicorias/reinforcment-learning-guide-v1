# The agent–environment loop and MDPs

> **Tier:** Beginner · **Prereqs:** `00/01` · **Code:** `rlguide.envs`, `rlguide.mdp_dp.induced_chain`

## 1. The interaction loop
At time $t$ the agent **observes $S_t$ → chooses $A_t$**; the environment **returns $R_{t+1}$ and $S_{t+1}$**.
The reward carries index $t+1$ because it arrives *with* the next state.

$$S_0, A_0, R_1, S_1, A_1, R_2, S_2, \dots$$

## 2. The model hierarchy (least → most structure)

| Model | Actions? | Dynamics | Rewards? |
|---|---|---|---|
| Markov chain | no | $P(s' \mid s)$ | no |
| Markov reward process | no | $P(s' \mid s)$ | $R(s)$, $\gamma$ |
| Deterministic decision process | yes | $s' = f(s,a)$ | $R(s,a)$ |
| MDP | yes | $P(s' \mid s, a)$ | $R(s,a)$ or $p(s', r \mid s, a)$, $\gamma$ |

**MDP tuple:** $(\mathcal S, \mathcal A, P, R, \gamma, \mu_0)$, with $\mu_0$ the initial-state distribution.
**The policy is *not* part of the MDP** — it is what we solve for (quiz errata #6).

**Markov chain → MDP:** add an action set and let transitions depend on it, $P(s'\mid s) \to P(s' \mid s, a)$; then add rewards.

**Interpreting $P(\cdot \mid s, a)$:** for each fixed $(s, a)$ it is a probability distribution over next states — each row sums to 1.

## 3. A fixed policy induces a Markov chain
$$P_\pi(s' \mid s) = \sum_a \pi(a \mid s)\,P(s' \mid s, a), \qquad R_\pi(s) = \sum_a \pi(a\mid s)\,R(s,a).$$
If $\pi$ is stationary the chain is **time-homogeneous**. That is why policy evaluation is "just" Markov-reward-process evaluation.

## 4. Modelling examples
- **1-D hallway** $\{L, M, R\}$, actions {left, right}; walking into a wall leaves you in place ("boundary stays"); reward $+1$ on *arriving* at $R$, which is terminal. With $\gamma = 0.9$: $v_*(M) = 1$, $v_*(L) = 0.9$.
- **Robot on positions $\{0,1,2,3\}$:** deterministic finite MDP, $f(s, \text{right}) = \min(s+1, 3)$, $f(s, \text{left}) = \max(s-1, 0)$.
- **Gridworld / warehouse robot:** cells = states, moves = actions, optional slip probability, reward $-1$ per step and $+10$ at the goal.
- **Weather chain:** $P = \begin{pmatrix}0.8 & 0.2\\ 0.4 & 0.6\end{pmatrix}$ over {sun, rain}; the stationary distribution solves $\mu = \mu P$: $\mu = (2/3, 1/3)$.
- **Machine chain:** {working, broken} with failure prob. $p$, repair prob. $q$. Adding actions {repair, run} makes it an MDP.

## 5. Reward design and shaping
A step penalty (e.g. $-1$) rewards short paths; a trap penalty (e.g. $-100$) makes risky cells expensive. Together — with stochastic slips — the optimal policy becomes **longer but safer**.

**Potential-based shaping** $F(s, s') = \gamma\Phi(s') - \Phi(s)$ leaves optimal policies unchanged (Ng, Harada & Russell 1999). Other shaping can change what is optimal and invites "reward farming".

## Pitfalls
- Writing $R_t$ for the reward that follows $A_t$ (it is $R_{t+1}$).
- Listing $\pi$ in the MDP tuple.
- Forgetting that a terminal state must be absorbing with zero reward.

## Practice
<details><summary>1. Write P_π for the hallway if π = "right with probability 0.5".</summary>

L→L 0.5, L→M 0.5; M→L 0.5, M→R 0.5; R absorbing.
</details>

<details><summary>2. True/False: "The MDP tuple is (S, A, P, R, γ, π)."</summary>

False — $\pi$ is the decision variable.
</details>

> **Run it:** `tests/test_worked_examples.py::test_hallway_values`, `::test_weather_stationary`; `tests/test_properties.py::test_induced_chain_is_stochastic`
