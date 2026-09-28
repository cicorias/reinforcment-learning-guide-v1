"""Tableau simplex for  max c^T x  s.t.  A x <= b, x >= 0, b >= 0.

Guide: 02-intermediate/04-simplex-and-branch-and-bound.md
Teaching code: dense tableau, Dantzig or Bland entering rule, MINIMUM ratio test.
"""

from __future__ import annotations

from dataclasses import dataclass, field

import numpy as np


@dataclass
class SimplexResult:
    x: np.ndarray
    value: float
    pivots: list[tuple[str, str, list[float]]] = field(default_factory=list)
    """(entering, leaving, ratios) for every pivot — handy for teaching."""


def simplex(c, A, b, rule: str = "dantzig", max_iter: int = 1000) -> SimplexResult:
    A = np.asarray(A, float)
    b = np.asarray(b, float)
    if (b < 0).any():
        raise ValueError("this teaching implementation needs b >= 0 (slack basis feasible)")
    m, n = A.shape
    names = [f"x{j + 1}" for j in range(n)] + [f"s{i + 1}" for i in range(m)]
    T = np.zeros((m + 1, n + m + 1))
    T[:m, :n] = A
    T[:m, n : n + m] = np.eye(m)
    T[:m, -1] = b
    T[-1, :n] = -np.asarray(c, float)  # objective row encodes z - c^T x = 0
    basis = list(range(n, n + m))
    pivots = []
    for _ in range(max_iter):
        obj = T[-1, :-1]
        candidates = np.flatnonzero(obj < -1e-12)
        if candidates.size == 0:
            break  # all reduced costs non-positive -> optimal
        j = int(candidates[0]) if rule == "bland" else int(np.argmin(obj))
        col = T[:m, j]
        ratios = np.full(m, np.inf)
        pos = col > 1e-12
        ratios[pos] = T[:m, -1][pos] / col[pos]
        if not np.isfinite(ratios).any():
            raise ValueError("LP is unbounded")
        best = ratios.min()
        ties = np.flatnonzero(np.isclose(ratios, best))
        i = int(min(ties, key=lambda r: basis[r])) if rule == "bland" else int(ties[0])
        pivots.append((names[j], names[basis[i]], [float(r) for r in ratios]))
        T[i] /= T[i, j]
        for k in range(m + 1):
            if k != i:
                T[k] -= T[k, j] * T[i]
        basis[i] = j
    x = np.zeros(n + m)
    for i, bv in enumerate(basis):
        x[bv] = T[i, -1]
    return SimplexResult(x=x[:n], value=float(T[-1, -1]), pivots=pivots)
