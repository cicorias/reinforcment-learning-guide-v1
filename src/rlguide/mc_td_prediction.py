"""Monte Carlo and TD prediction (tabular).

Guide: 01-beginner/04-monte-carlo-td-basics.md,
       03-expert/02-td-lambda-offpolicy-importance-sampling.md

Episode format: a list of (state, reward) pairs where `reward` is R_{t+1},
i.e. the reward received on *leaving* that state.
"""

from __future__ import annotations

from collections import defaultdict
from collections.abc import Hashable, Sequence

import numpy as np

Episode = Sequence[tuple[Hashable, float]]


def returns_backward(episode: Episode, gamma: float = 1.0) -> list[float]:
    """G_t for every t, computed backwards with G_t = R_{t+1} + gamma * G_{t+1}."""
    G, out = 0.0, [0.0] * len(episode)
    for t in reversed(range(len(episode))):
        G = gamma * G + episode[t][1]
        out[t] = G
    return out


def mc_prediction(
    episodes: Sequence[Episode], gamma: float = 1.0, first_visit: bool = True
) -> tuple[dict[Hashable, float], dict[Hashable, list[float]]]:
    """First-visit (default) or every-visit MC. Returns (V, stored returns per state)."""
    stored: dict[Hashable, list[float]] = defaultdict(list)
    for ep in episodes:
        G_all = returns_backward(ep, gamma)
        seen: set[Hashable] = set()
        for t, (s, _) in enumerate(ep):
            if first_visit and s in seen:
                continue
            seen.add(s)
            stored[s].append(G_all[t])
    V = {s: float(np.mean(g)) for s, g in stored.items()}
    return V, dict(stored)


def td0_update(V: dict, s, r: float, s_next, alpha: float, gamma: float, terminal=False):
    """V(s) <- V(s) + alpha [ r + gamma V(s') - V(s) ].  Returns (target, delta)."""
    target = r + (0.0 if terminal else gamma * V[s_next])
    delta = target - V[s]
    V[s] += alpha * delta
    return target, delta


def n_step_return(rewards: Sequence[float], bootstrap: float, gamma: float) -> float:
    """G_{t:t+n} = R_{t+1} + ... + gamma^{n-1} R_{t+n} + gamma^n V(S_{t+n})."""
    n = len(rewards)
    return sum(gamma**k * r for k, r in enumerate(rewards)) + gamma**n * bootstrap


def batch_td0(episodes: Sequence[Episode], gamma=1.0, alpha=0.01, tol=1e-10, max_iter=200_000):
    """Batch TD(0): sweep the fixed dataset until V stops changing (certainty equivalence)."""
    states = {s for ep in episodes for s, _ in ep}
    V = {s: 0.0 for s in states}
    for _ in range(max_iter):
        inc = {s: 0.0 for s in states}
        for ep in episodes:
            for t, (s, r) in enumerate(ep):
                nxt = V[ep[t + 1][0]] if t + 1 < len(ep) else 0.0
                inc[s] += alpha * (r + gamma * nxt - V[s])
        for s in states:
            V[s] += inc[s]
        if max(abs(x) for x in inc.values()) < tol:
            break
    return V


# Sutton & Barto Example 6.4 ("You are the predictor")
EXAMPLE_6_4 = [[("A", 0.0), ("B", 0.0)]] + [[("B", 1.0)]] * 6 + [[("B", 0.0)]]
