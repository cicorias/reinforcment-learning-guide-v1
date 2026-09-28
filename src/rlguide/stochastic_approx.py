"""Robbins-Monro step sizes vs constant alpha.

Guide: 00-math-foundations/05-stochastic-approximation.md
"""

from __future__ import annotations

import numpy as np


def estimate_mean(samples: np.ndarray, alpha: float | None = None) -> np.ndarray:
    """Q_{n+1} = Q_n + a_n (X_n - Q_n); a_n = 1/n if alpha is None else constant."""
    q, out = 0.0, np.empty(len(samples))
    for n, x in enumerate(samples, start=1):
        a = 1.0 / n if alpha is None else alpha
        q += a * (x - q)
        out[n - 1] = q
    return out


def constant_alpha_stationary_variance(alpha: float, sigma2: float) -> float:
    """Var of the exponential moving average in steady state: alpha*sigma^2/(2-alpha)."""
    return alpha * sigma2 / (2.0 - alpha)


def robbins_monro_ok(alpha_fn, n_terms: int = 10**6) -> tuple[float, float]:
    """Partial sums (sum a_t, sum a_t^2) — a quick numerical feel for the two conditions."""
    t = np.arange(1, n_terms + 1, dtype=float)
    a = alpha_fn(t)
    return float(a.sum()), float((a**2).sum())
