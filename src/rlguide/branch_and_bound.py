"""LP-based branch and bound for (mixed) integer maximisation.

Guide: 02-intermediate/04-simplex-and-branch-and-bound.md
"""

from __future__ import annotations

import math
from dataclasses import dataclass, field

import numpy as np
from scipy.optimize import linprog


@dataclass
class BBNode:
    bounds: list[tuple[float, float]]
    lp_value: float | None
    x: list[float] | None
    outcome: str  # 'infeasible' | 'pruned-bound' | 'integral' | 'branched'


@dataclass
class BBResult:
    value: float
    x: np.ndarray | None
    log: list[BBNode] = field(default_factory=list)


def branch_and_bound(c, A_ub, b_ub, bounds, tol: float = 1e-6) -> BBResult:
    """max c^T x  s.t. A_ub x <= b_ub, bounds, x integer.  Depth-first search.

    Prune rules: (i) LP infeasible, (ii) LP bound <= incumbent, (iii) LP integral.
    A fractional LP solution is ONLY a bound — never an incumbent.
    """
    c = np.asarray(c, float)
    best_val, best_x = -math.inf, None
    log: list[BBNode] = []
    stack = [list(bounds)]
    while stack:
        bnds = stack.pop()
        res = linprog(-c, A_ub=A_ub, b_ub=b_ub, bounds=bnds, method="highs")
        if not res.success:
            log.append(BBNode(bnds, None, None, "infeasible"))
            continue
        val = float(-res.fun)
        x = res.x
        if val <= best_val + tol:
            log.append(BBNode(bnds, val, x.tolist(), "pruned-bound"))
            continue
        frac = [i for i, xi in enumerate(x) if abs(xi - round(xi)) > tol]
        if not frac:
            best_val, best_x = val, np.round(x)
            log.append(BBNode(bnds, val, x.tolist(), "integral"))
            continue
        log.append(BBNode(bnds, val, x.tolist(), "branched"))
        i = frac[0]
        lo, hi = bnds[i]
        down = list(bnds)
        down[i] = (lo, math.floor(x[i]))
        up = list(bnds)
        up[i] = (math.ceil(x[i]), hi)
        stack += [up, down]  # explore the "down" child first
    return BBResult(best_val, best_x, log)
