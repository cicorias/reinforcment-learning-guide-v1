"""MAX-SAT: random assignment, derandomisation, LP rounding, best-of-two.

Guide: 02-intermediate/06-approximation-algorithms.md,
       03-expert/05-maxsat-rounding-and-fptas-proofs.md

Clause encoding: list of non-zero ints; +k means x_k, -k means NOT x_k (DIMACS style).
"""

from __future__ import annotations

import numpy as np
from scipy.optimize import linprog

Clause = list[int]


def num_satisfied(clauses: list[Clause], assign: dict[int, bool]) -> int:
    return sum(any(assign[abs(lit)] == (lit > 0) for lit in C) for C in clauses)


def expected_satisfied(clauses: list[Clause], assign: dict[int, bool], p=None) -> float:
    """E[#satisfied | fixed variables in `assign`], unfixed x_i True w.p. p[i] (default 1/2)."""
    total = 0.0
    for C in clauses:
        prob_unsat = 1.0
        for lit in C:
            v = abs(lit)
            if v in assign:
                if assign[v] == (lit > 0):
                    prob_unsat = 0.0
                    break
                # fixed literal is false: contributes factor 1
            else:
                pv = 0.5 if p is None else p[v]
                prob_unsat *= (1 - pv) if lit > 0 else pv
        total += 1.0 - prob_unsat
    return total


def derandomized(clauses: list[Clause], n: int, p=None):
    """Method of conditional expectations. Returns (assignment, trace).

    trace[i] = (var, E[.|x=T], E[.|x=F], choice). The conditional expectation never
    decreases, so the final count >= E[X] (>= m/2 for p = 1/2).
    """
    assign: dict[int, bool] = {}
    trace = []
    for v in range(1, n + 1):
        assign[v] = True
        eT = expected_satisfied(clauses, assign, p)
        assign[v] = False
        eF = expected_satisfied(clauses, assign, p)
        assign[v] = eT >= eF
        trace.append((v, eT, eF, assign[v]))
    return assign, trace


def lp_relaxation(clauses: list[Clause], n: int):
    """max sum z_C  s.t.  sum_{i in P_C} y_i + sum_{i in N_C} (1 - y_i) >= z_C,  0<=y,z<=1.

    Returns (y [1..n] as dict, LP value).
    """
    m = len(clauses)
    # variables: y_1..y_n, z_1..z_m
    c = np.concatenate([np.zeros(n), -np.ones(m)])
    A, b = [], []
    for j, C in enumerate(clauses):
        row = np.zeros(n + m)
        negs = 0
        for lit in C:
            if lit > 0:
                row[lit - 1] -= 1.0
            else:
                row[-lit - 1] += 1.0
                negs += 1
        row[n + j] = 1.0
        A.append(row)
        b.append(float(negs))  # z_C - sum_P y + sum_N y <= |N_C|
    res = linprog(c, A_ub=np.array(A), b_ub=np.array(b), bounds=[(0, 1)] * (n + m), method="highs")
    y = {i + 1: float(res.x[i]) for i in range(n)}
    return y, float(-res.fun)


def best_of_two(clauses: list[Clause], n: int):
    """Derandomised Johnson (p=1/2) vs derandomised LP rounding; keep the better (>= 3/4 OPT)."""
    a1, _ = derandomized(clauses, n)
    y, _ = lp_relaxation(clauses, n)
    a2, _ = derandomized(clauses, n, p=y)
    s1, s2 = num_satisfied(clauses, a1), num_satisfied(clauses, a2)
    return (a1, s1) if s1 >= s2 else (a2, s2)


def brute_force_opt(clauses: list[Clause], n: int) -> int:
    best = 0
    for mask in range(1 << n):
        assign = {v: bool(mask >> (v - 1) & 1) for v in range(1, n + 1)}
        best = max(best, num_satisfied(clauses, assign))
    return best


GUIDE_EXAMPLE: list[Clause] = [[1, 2], [-1, 3], [-2, -3], [1]]
