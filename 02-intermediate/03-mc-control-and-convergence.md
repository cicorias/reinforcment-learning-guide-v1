# Monte Carlo control and convergence

> **Tier:** Intermediate · **Prereqs:** `01/04`, `02/01` · **Code:** `rlguide.mc_td_prediction`

- **MC control (GPI):** evaluate $Q$ from returns, then act greedily or ε-greedily.
- **Exploring starts (ES):** every $(s, a)$ has nonzero probability of starting an episode — coverage without ε.
- **ε-soft policies:** $\pi(a\mid s) \ge \varepsilon/\lvert\mathcal A\rvert$ for all $a$. The ε-greedy policy w.r.t. $q_\pi$ is at least as good as any ε-soft $\pi$, so the policy improvement theorem holds **within the ε-soft class**. The result is the best ε-soft policy — not $\pi_*$.
- **GLIE:** all pairs visited infinitely often **and** the policy becomes greedy in the limit (e.g. $\varepsilon_k = 1/k$). GLIE MC control converges to $q_*$.
- **MC properties:** unbiased returns, high variance, must wait for episode end, episodic only, no bootstrapping (robust to non-Markov features).

## Why ε-greedy improvement works within the ε-soft class
Let $\pi$ be ε-soft and $\pi'$ ε-greedy w.r.t. $q_\pi$. Then
$$\sum_a\pi'(a\mid s)\,q_\pi(s,a) = \frac{\varepsilon}{\lvert\mathcal A\rvert}\sum_a q_\pi(s,a) + (1-\varepsilon)\max_a q_\pi(s,a) \ge v_\pi(s),$$
because the max is at least the weighted average $\sum_a\frac{\pi(a\mid s) - \varepsilon/\lvert\mathcal A\rvert}{1-\varepsilon}\,q_\pi(s,a)$ (weights non-negative, summing to 1). Apply the policy improvement theorem.

## Pitfalls
- ε-soft ≠ uniform random: ε-soft is a *lower bound* on probabilities.
- Fixed ε MC control converges to the best ε-soft policy, not the optimal one.

## Practice
<details><summary>Why does MC control without exploring starts or ε-soft policies fail?</summary>

A deterministic greedy policy never tries some actions, so their $Q$ values are never updated and a better action can stay hidden forever.
</details>
