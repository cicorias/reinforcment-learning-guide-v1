"""Vertex cover: ILP, LP relaxation, and the 2-approximation by rounding.

Guide: 01-beginner/06-lp-and-ilp-basics.md, 02-intermediate/06-approximation-algorithms.md
"""

from __future__ import annotations

import itertools

import numpy as np
from scipy.optimize import linprog


def _cover_constraints(n: int, edges):
    A = np.zeros((len(edges), n))
    for k, (u, v) in enumerate(edges):
        A[k, u] = A[k, v] = -1.0  # -(x_u + x_v) <= -1
    return A, -np.ones(len(edges))


def lp_relaxation(n: int, edges) -> tuple[np.ndarray, float]:
    A, b = _cover_constraints(n, edges)
    res = linprog(np.ones(n), A_ub=A, b_ub=b, bounds=[(0, 1)] * n, method="highs")
    return res.x, float(res.fun)


def lp_rounding(n: int, edges) -> tuple[set[int], float]:
    """C = {v : x*_v >= 1/2}. Feasible and |C| <= 2 LP* <= 2 OPT."""
    x, lp = lp_relaxation(n, edges)
    return {v for v in range(n) if x[v] >= 0.5 - 1e-9}, lp


def brute_force_opt(n: int, edges) -> int:
    for k in range(n + 1):
        for C in itertools.combinations(range(n), k):
            S = set(C)
            if all(u in S or v in S for u, v in edges):
                return k
    return n


def is_cover(C: set[int], edges) -> bool:
    return all(u in C or v in C for u, v in edges)


PATH_1234 = [(0, 1), (1, 2), (2, 3)]  # vertices 1..4 stored as 0..3


def complete_graph(n: int):
    return [(i, j) for i in range(n) for j in range(i + 1, n)]
