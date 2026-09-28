# Stochastic approximation: Robbins–Monro

> **Tier:** Foundations · **Used by:** TD, SARSA, Q-learning convergence · **Code:** `rlguide.stochastic_approx` · **Notebook:** `05_convergence_stepsizes`

## The problem
Find the root of $M(\theta) = \mathbb E[H(\theta, \xi)]$ from **noisy samples** (Robbins & Monro, *Ann. Math. Statist.* 22, 1951):
$$\theta_{t+1} = \theta_t - \alpha_t\,H(\theta_t, \xi_t).$$

## The step-size conditions
$$\sum_t \alpha_t = \infty \quad(\text{can travel any distance}), \qquad \sum_t \alpha_t^2 < \infty \quad(\text{noise dies out}).$$

| Schedule | $\sum\alpha_t$ | $\sum\alpha_t^2$ | OK? |
|---|---|---|---|
| $1/t$ | $\infty$ (harmonic) | $\pi^2/6$ | ✅ |
| $1/\sqrt t$ | $\infty$ | $\infty$ | ❌ |
| $1/t^2$ | finite | finite | ❌ (stops too early) |
| constant $\alpha$ | $\infty$ | $\infty$ | ❌ for exact convergence |

## Why constant $\alpha$ never converges under noise
Estimating a mean with noise variance $\sigma^2$, a constant step makes an exponential moving average whose steady-state variance is
$$\operatorname{Var}_\infty = \frac{\alpha\,\sigma^2}{2 - \alpha} \ne 0.$$

*Derivation.* $Q_{n+1} = (1-\alpha)Q_n + \alpha X_n$. In steady state $\operatorname{Var} = (1-\alpha)^2\operatorname{Var} + \alpha^2\sigma^2$, so $\operatorname{Var}\,(2\alpha - \alpha^2) = \alpha^2\sigma^2$. ∎

With $\alpha = 0.5$ the estimate jitters forever with variance $\sigma^2/3$. It *tracks* rather than converges — right for **nonstationary** problems (Sutton & Barto §2.5), wrong for exact convergence.

## The deterministic nuance
If rewards and transitions are deterministic, the noise term is zero: constant $\alpha \in (0, 1]$ converges geometrically. Tabular Q-learning with $\alpha = 1$ in a deterministic MDP performs exact Bellman backups along visited transitions.

## RL connection
Tabular TD(0), SARSA and Q-learning are **asynchronous Robbins–Monro** schemes (Jaakkola, Jordan & Singh 1994; Tsitsiklis 1994). Step sizes are **per state–action pair**, e.g. $\alpha = 1/N(s,a)$.

## Practice
<details><summary>Does α_t = 1/(t log t) (t ≥ 2) satisfy both conditions?</summary>

Yes: $\sum 1/(t\log t)$ diverges (integral test: $\log\log t$), and $\sum 1/(t\log t)^2$ converges.
</details>

> **Run it:** `tests/test_properties.py::test_constant_alpha_does_not_converge_but_one_over_n_does`, `::test_constant_alpha_converges_when_deterministic`
