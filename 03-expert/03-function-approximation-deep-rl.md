# Function approximation and deep RL

> **Tier:** Expert · **Prereqs:** `02/02`, `03/02` · **Notebook:** `11_linear_fa_and_deadly_triad`

## Why tabular fails
A 50×50 gridworld has 2,500 states — fine. Add 10 binary item flags: 2,560,000. Raw 84×84 pixels: astronomically many. A table has **no generalisation**: visiting one state teaches nothing about its neighbours.

## Linear function approximation and semi-gradient TD
$$\hat v(s, w) = w^\top x(s), \qquad w \leftarrow w + \alpha\big[R + \gamma\hat v(S', w) - \hat v(S, w)\big]\,x(S).$$
"Semi" because we do not differentiate through the target. On-policy linear TD converges w.p. 1 to the **TD fixed point**, whose error is bounded relative to the best linear approximation (Tsitsiklis & Van Roy 1997).

## The deadly triad
**Function approximation + bootstrapping + off-policy training** ⇒ possible divergence (Sutton & Barto §11.3). Baird's counterexample (1995) diverges even with *linear* features. Any two of the three are safe. Notebook 11 reproduces the divergence.

## DQN (Mnih et al. 2015)
$$\mathcal L(\theta) = \mathbb E_{(s,a,r,s')\sim\mathcal D}\Big[\big(r + \gamma\max_{a'}Q(s', a'; \theta^-) - Q(s, a; \theta)\big)^2\Big].$$
- **Experience replay** $\mathcal D$: breaks temporal correlations and reuses data (possible because Q-learning is off-policy).
- **Target network** $\theta^-$: copied every $C$ steps; the delayed targets make divergence and oscillation much less likely.
- One architecture and hyperparameter set across 49 Atari games.
- **Double DQN:** target $r + \gamma\,Q\big(s', \arg\max_{a'}Q(s', a'; \theta); \theta^-\big)$.

## Policy gradients and actor–critic (overview)
**Policy gradient theorem** (Sutton, McAllester, Singh & Mansour 2000):
$$\nabla_\theta J = \sum_s d^\pi(s)\sum_a\nabla_\theta\pi(a\mid s)\,q_\pi(s,a)$$
— with no derivative of the state distribution $d^\pi$.

- **REINFORCE:** $\theta \leftarrow \theta + \alpha\,G_t\,\nabla\ln\pi(A_t\mid S_t)$.
- **Baseline:** subtracting $b(s)$ reduces variance without bias.
- **Actor–critic:** a critic learns $\hat v$; the actor uses the TD error $\delta$ as an advantage estimate.

## Pitfalls
- Convergence theorems in `02/*` are **tabular**. With function approximation — especially off-policy — there are generally no guarantees.
- Replay requires an off-policy learner.
