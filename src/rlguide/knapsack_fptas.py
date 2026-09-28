"""0-1 knapsack: exact value-indexed DP and the (1 - eps) FPTAS.

Guide: 02-intermediate/06-approximation-algorithms.md,
       03-expert/05-maxsat-rounding-and-fptas-proofs.md
"""

from __future__ import annotations

import math


def _min_weight_dp(vals: list[int], weights, W):
    """A[p] = min weight achieving value exactly p. Returns best set (indices into vals)."""
    P = sum(vals)
    INF = math.inf
    A = [0.0] + [INF] * P
    choice: list[frozenset[int] | None] = [frozenset()] + [None] * P
    for i, (v, w) in enumerate(zip(vals, weights, strict=True)):
        for p in range(P, v - 1, -1):
            if A[p - v] + w < A[p]:
                A[p] = A[p - v] + w
                choice[p] = choice[p - v] | {i}
    best = max(p for p in range(P + 1) if A[p] <= W)
    return set(choice[best] or ())


def exact(values: list[int], weights, W) -> tuple[set[int], int]:
    """Exact pseudo-polynomial DP over integer values."""
    S = _min_weight_dp(list(values), weights, W)
    return S, sum(values[i] for i in S)


def fptas(values, weights, W, eps: float) -> tuple[set[int], float, dict]:
    """Returns (item set, true value, info). Guarantees value >= (1 - eps) OPT.

    1. drop items with w_i > W   (needed for OPT >= v_max)
    2. K = eps * v_max / n,  v'_i = floor(v_i / K)
    3. exact DP on v'   -> O(n^3 / eps)
    """
    items = [i for i in range(len(values)) if weights[i] <= W]
    if not items:
        return set(), 0.0, {"K": None, "scaled": []}
    n = len(items)
    vmax = max(values[i] for i in items)
    K = eps * vmax / n
    scaled = [math.floor(values[i] / K) for i in items]
    local = _min_weight_dp(scaled, [weights[i] for i in items], W)
    S = {items[j] for j in local}
    return S, float(sum(values[i] for i in S)), {"K": K, "scaled": scaled}


GUIDE_EXAMPLE = {"values": [60, 100, 120], "weights": [10, 20, 30], "W": 50, "eps": 0.5}
