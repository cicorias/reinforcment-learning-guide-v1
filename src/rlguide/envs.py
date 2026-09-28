"""Small tabular MDPs used throughout the guide.

Array conventions (used by every DP / LP routine in this package):
    P : ndarray [A, S, S]   P[a, s, s'] = Pr(s' | s, a)   (rows sum to 1)
    R : ndarray [S, A]      expected immediate reward r(s, a)

Terminal states are modelled as absorbing with zero reward.
Guide: 01-beginner/01-agent-environment-mdps.md
"""

from __future__ import annotations

import numpy as np


def hallway() -> tuple[np.ndarray, np.ndarray, list[str], list[str]]:
    """1-D hallway L-M-R. Actions: 0=left, 1=right.

    Moving into a wall leaves you in place. Reward +1 on *arriving* at R;
    R is terminal (absorbing, reward 0 afterwards).
    """
    S, A = 3, 2
    L, M, Rs = 0, 1, 2
    P = np.zeros((A, S, S))
    R = np.zeros((S, A))
    # left
    P[0, L, L] = 1
    P[0, M, L] = 1
    # right
    P[1, L, M] = 1
    P[1, M, Rs] = 1
    R[M, 1] = 1.0
    # terminal R absorbs under both actions
    P[:, Rs, Rs] = 1
    return P, R, ["L", "M", "R"], ["left", "right"]


def two_state_swap(reward: float = 1.0) -> tuple[np.ndarray, np.ndarray]:
    """Single-action MDP whose two states alternate; reward `reward` each step."""
    P = np.array([[[0.0, 1.0], [1.0, 0.0]]])
    R = np.full((2, 1), reward)
    return P, R


def line_robot() -> tuple[np.ndarray, np.ndarray]:
    """Deterministic robot on positions {0,1,2,3}; actions 0=left, 1=right (clipped).

    No rewards: the structure (finite, Markov, deterministic) is the point.
    """
    S, A = 4, 2
    P = np.zeros((A, S, S))
    for s in range(S):
        P[0, s, max(s - 1, 0)] = 1
        P[1, s, min(s + 1, S - 1)] = 1
    return P, np.zeros((S, A))


def random_mdp(S: int = 6, A: int = 3, seed: int = 0) -> tuple[np.ndarray, np.ndarray]:
    """Random dense MDP for cross-checking VI / PI / LP."""
    rng = np.random.default_rng(seed)
    P = rng.random((A, S, S))
    P /= P.sum(axis=2, keepdims=True)
    R = rng.normal(size=(S, A))
    return P, R


def weather_chain() -> np.ndarray:
    """Markov chain over {sun, rain}; stationary distribution is (2/3, 1/3)."""
    return np.array([[0.8, 0.2], [0.4, 0.6]])


def stationary_distribution(P: np.ndarray) -> np.ndarray:
    """Solve mu = mu P, sum(mu) = 1 for an ergodic chain."""
    n = P.shape[0]
    A = np.vstack([P.T - np.eye(n), np.ones(n)])
    b = np.zeros(n + 1)
    b[-1] = 1.0
    mu, *_ = np.linalg.lstsq(A, b, rcond=None)
    return mu
