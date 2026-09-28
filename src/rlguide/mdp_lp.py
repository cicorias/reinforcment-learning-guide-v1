"""MDPs and shortest paths as linear programs.

Guide: 02-intermediate/05-mdp-as-lp.md, 03-expert/04-lp-duality-occupancy-measures.md
"""

from __future__ import annotations

import numpy as np
from scipy.optimize import linprog


def solve_primal(P: np.ndarray, R: np.ndarray, gamma: float, weights=None) -> np.ndarray:
    """Reward maximisation:  min sum_s mu(s) v(s)
    s.t. v(s) >= r(s,a) + gamma * sum_s' P(s'|s,a) v(s')   for all (s, a).

    Rewritten for linprog (A_ub x <= b_ub):  gamma*P[a,s,:] - e_s  <=  -r(s,a).
    """
    A, S, _ = P.shape
    mu = np.ones(S) if weights is None else np.asarray(weights, float)
    rows, rhs = [], []
    for s in range(S):
        for a in range(A):
            row = gamma * P[a, s].copy()
            row[s] -= 1.0
            rows.append(row)
            rhs.append(-R[s, a])
    res = linprog(
        mu, A_ub=np.array(rows), b_ub=np.array(rhs), bounds=[(None, None)] * S, method="highs"
    )
    if not res.success:
        raise RuntimeError(res.message)
    return res.x


def solve_dual(P: np.ndarray, R: np.ndarray, gamma: float, mu0=None):
    """Occupancy-measure dual:  max sum_{s,a} d(s,a) r(s,a)
    s.t. sum_a d(s',a) - gamma * sum_{s,a} P(s'|s,a) d(s,a) = mu0(s'),  d >= 0.

    Returns (d [S, A], optimal value, policy pi(a|s) proportional to d).
    """
    A, S, _ = P.shape
    mu0 = np.ones(S) / S if mu0 is None else np.asarray(mu0, float)
    n = S * A  # variable index s*A + a
    A_eq = np.zeros((S, n))
    for sp in range(S):
        for s in range(S):
            for a in range(A):
                A_eq[sp, s * A + a] = (1.0 if s == sp else 0.0) - gamma * P[a, s, sp]
    res = linprog(-R.reshape(-1), A_eq=A_eq, b_eq=mu0, bounds=[(0, None)] * n, method="highs")
    if not res.success:
        raise RuntimeError(res.message)
    d = res.x.reshape(S, A)
    pi = d / np.maximum(d.sum(axis=1, keepdims=True), 1e-300)
    return d, -res.fun, pi


# ---------------------------------------------------------------- shortest path example
# s0 -> sT cost 5 ; s0 -> s1 cost 2 ; s1 -> sT cost 1 ; v(sT) = 0.   Optimal cost: 3.
EDGES = [("s0", "sT", 5.0), ("s0", "s1", 2.0), ("s1", "sT", 1.0)]


def shortest_path_lp(correct: bool = True) -> dict[str, float]:
    """correct=True : max v0+v1  s.t. v(s) <= c + v(s')   (encodes min over actions) -> 3
    correct=False: min v0+v1  s.t. v(s) >= c + v(s')   (the flawed quiz form)       -> 5
    """
    idx = {"s0": 0, "s1": 1}
    rows, rhs = [], []
    for u, w, c in EDGES:
        row = np.zeros(2)
        row[idx[u]] += 1.0
        if w in idx:
            row[idx[w]] -= 1.0
        # correct:  v_u - v_w <= c        flawed:  -(v_u - v_w) <= -c
        rows.append(row if correct else -row)
        rhs.append(c if correct else -c)
    obj = -np.ones(2) if correct else np.ones(2)
    res = linprog(
        obj, A_ub=np.array(rows), b_ub=np.array(rhs), bounds=[(None, None)] * 2, method="highs"
    )
    if not res.success:
        raise RuntimeError(res.message)
    return {"s0": float(res.x[0]), "s1": float(res.x[1])}
