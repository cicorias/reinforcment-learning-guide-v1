"""Multi-armed bandits: epsilon-greedy, UCB1, Thompson sampling.

Guide: 01-beginner/05-bandits-exploration.md
"""

from __future__ import annotations

import numpy as np


def run_bandit(true_means, steps=2000, strategy="eps", eps=0.1, c=2.0, q0=0.0, seed=0):
    """Gaussian arms (sd 1). strategy in {'eps', 'ucb', 'greedy'}.

    Returns dict(Q, N, regret) where regret[t] is cumulative (pseudo-)regret.
    """
    rng = np.random.default_rng(seed)
    mu = np.asarray(true_means, float)
    k = len(mu)
    Q = np.full(k, float(q0))
    N = np.zeros(k)
    regret = np.zeros(steps)
    total = 0.0
    for t in range(1, steps + 1):
        if strategy == "ucb":
            if N.min() == 0:
                a = int(np.argmin(N))
            else:
                a = int(np.argmax(Q + c * np.sqrt(np.log(t) / N)))
        elif strategy == "eps" and rng.random() < eps:
            a = int(rng.integers(k))
        else:
            a = int(np.argmax(Q))
        r = rng.normal(mu[a], 1.0)
        N[a] += 1
        Q[a] += (r - Q[a]) / N[a]  # incremental sample mean
        total += mu.max() - mu[a]
        regret[t - 1] = total
    return {"Q": Q, "N": N, "regret": regret}


def thompson_bernoulli(true_p, steps=2000, seed=0):
    """Beta-Bernoulli Thompson sampling. Returns dict(alpha, beta, regret)."""
    rng = np.random.default_rng(seed)
    p = np.asarray(true_p, float)
    a_, b_ = np.ones(len(p)), np.ones(len(p))
    regret = np.zeros(steps)
    total = 0.0
    for t in range(steps):
        arm = int(np.argmax(rng.beta(a_, b_)))
        reward = rng.random() < p[arm]
        a_[arm] += reward
        b_[arm] += 1 - reward
        total += p.max() - p[arm]
        regret[t] = total
    return {"alpha": a_, "beta": b_, "regret": regret}


def eps_greedy_action_probs(k: int, eps: float, greedy_arm: int = 0) -> np.ndarray:
    probs = np.full(k, eps / k)
    probs[greedy_arm] += 1 - eps
    return probs
