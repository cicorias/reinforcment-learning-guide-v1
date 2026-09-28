"""Dynamic programming for finite MDPs.

Guide: 02-intermediate/01-dynamic-programming.md,
       03-expert/01-contraction-proofs-and-complexity.md
"""

from __future__ import annotations

import numpy as np


def induced_chain(P: np.ndarray, R: np.ndarray, pi: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    """P_pi(s'|s) = sum_a pi(a|s) P(s'|s,a);  R_pi(s) = sum_a pi(a|s) r(s,a)."""
    P_pi = np.einsum("sa,ast->st", pi, P)
    R_pi = (pi * R).sum(axis=1)
    return P_pi, R_pi


def evaluate(P: np.ndarray, R: np.ndarray, pi: np.ndarray, gamma: float) -> np.ndarray:
    """Exact policy evaluation: solve (I - gamma P_pi) v = R_pi."""
    P_pi, R_pi = induced_chain(P, R, pi)
    S = R.shape[0]
    return np.linalg.solve(np.eye(S) - gamma * P_pi, R_pi)


def q_from_v(P: np.ndarray, R: np.ndarray, V: np.ndarray, gamma: float) -> np.ndarray:
    """One-step lookahead: Q[s, a] = r(s,a) + gamma * sum_s' P(s'|s,a) V(s')."""
    return R + gamma * np.einsum("ast,t->sa", P, V)


def bellman_expectation(P, R, pi, V, gamma):
    """(T^pi V)(s)."""
    return (pi * q_from_v(P, R, V, gamma)).sum(axis=1)


def bellman_optimality(P, R, V, gamma):
    """(T^* V)(s)."""
    return q_from_v(P, R, V, gamma).max(axis=1)


def iterative_policy_evaluation(
    P, R, pi, gamma, theta=1e-10, in_place=False, max_sweeps=100_000
) -> tuple[np.ndarray, list[float]]:
    """Iterative evaluation of a FIXED policy.

    in_place=False : synchronous / Jacobi (two arrays)
    in_place=True  : Gauss-Seidel (overwrite V(s) immediately)
    Returns (V, deltas) where deltas[k] = max_s |V_{k+1}(s) - V_k(s)|.
    """
    S = R.shape[0]
    V = np.zeros(S)
    deltas: list[float] = []
    for _ in range(max_sweeps):
        if in_place:
            delta = 0.0
            for s in range(S):
                old = V[s]
                V[s] = sum(pi[s, a] * (R[s, a] + gamma * P[a, s] @ V) for a in range(R.shape[1]))
                delta = max(delta, abs(old - V[s]))
        else:
            V_new = bellman_expectation(P, R, pi, V, gamma)
            delta = float(np.abs(V_new - V).max())
            V = V_new
        deltas.append(delta)
        if delta < theta:
            break
    return V, deltas


def value_iteration(P, R, gamma=0.9, theta=1e-10, max_iter=100_000):
    """Value iteration. Returns (V, greedy_policy, deltas)."""
    V = np.zeros(R.shape[0])
    deltas: list[float] = []
    for _ in range(max_iter):
        V_new = bellman_optimality(P, R, V, gamma)
        deltas.append(float(np.abs(V_new - V).max()))
        V = V_new
        if deltas[-1] < theta:
            break
    return V, q_from_v(P, R, V, gamma).argmax(axis=1), deltas


def greedy(P, R, V, gamma) -> np.ndarray:
    """Deterministic greedy policy as a one-hot [S, A] matrix (ties -> lowest index)."""
    Q = q_from_v(P, R, V, gamma)
    return np.eye(R.shape[1])[Q.argmax(axis=1)]


def policy_iteration(P, R, gamma=0.9, max_iter=10_000):
    """Howard's policy iteration. Returns (V, policy_indices, n_iterations).

    Terminates finitely: finitely many deterministic policies, strict improvement.
    Ties are broken toward the *current* action to avoid flip-flopping.
    """
    S, A = R.shape
    pi = np.eye(A)[np.zeros(S, dtype=int)]
    for it in range(1, max_iter + 1):
        V = evaluate(P, R, pi, gamma)
        Q = q_from_v(P, R, V, gamma)
        current = pi.argmax(axis=1)
        best = Q.argmax(axis=1)
        keep = np.isclose(Q[np.arange(S), current], Q[np.arange(S), best])
        new_actions = np.where(keep, current, best)
        if np.array_equal(new_actions, current):
            return V, current, it
        pi = np.eye(A)[new_actions]
    raise RuntimeError("policy iteration did not terminate")


def backward_induction(P, R, horizon: int):
    """Finite-horizon DP (gamma = 1). Returns V[t, s] and non-stationary policy[t, s]."""
    S, A = R.shape
    V = np.zeros((horizon + 1, S))
    pol = np.zeros((horizon, S), dtype=int)
    for t in range(horizon - 1, -1, -1):
        Q = R + np.einsum("ast,t->sa", P, V[t + 1])
        V[t] = Q.max(axis=1)
        pol[t] = Q.argmax(axis=1)
    return V, pol


def sup_norm(x: np.ndarray) -> float:
    return float(np.abs(x).max())
