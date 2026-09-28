"""Generate notebooks/*.ipynb from the specs below (stdlib only).

Never hand-edit the .ipynb files — edit NOTEBOOKS here and run
    mise run notebooks:build
CI runs `mise run notebooks:check`, which fails if the committed notebooks are stale.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "notebooks"

SETUP = """\
%matplotlib inline
import numpy as np
import matplotlib.pyplot as plt
from ipywidgets import interact, FloatSlider, IntSlider
np.set_printoptions(precision=4, suppress=True)"""

PREDICT = "> **Predict before you run:** "

NOTEBOOKS: dict[str, list[tuple[str, str]]] = {
    "01_expectation_and_contraction": [
        ("md", "# 01 · Expectation and contraction\nGuide: `00-math-foundations/01` and `/02`."),
        ("code", SETUP),
        ("md", "## Expected next-state value\n$\\mathbb E[V(S')] = \\sum_{s'} P(s'\\mid s)V(s')$"),
        (
            "code",
            "p, V = np.array([0.2, 0.5, 0.3]), np.array([4, 1, 7])\n"
            "print('expectation', p @ V, '| plain average', V.mean(), '| most likely', V[p.argmax()])",
        ),
        (
            "md",
            "## Value iteration error vs the $\\gamma^k$ bound\n"
            + PREDICT
            + "if you double $1-\\gamma$, roughly how many fewer iterations do you need?",
        ),
        (
            "code",
            "from rlguide import envs, mdp_dp\n"
            "P, R = envs.random_mdp(S=10, A=3, seed=0)\n\n"
            "@interact(gamma=FloatSlider(value=0.9, min=0.5, max=0.99, step=0.01))\n"
            "def show(gamma):\n"
            "    v_star, _, _ = mdp_dp.value_iteration(P, R, gamma, theta=1e-12)\n"
            "    V, errs = np.zeros(10), []\n"
            "    for _ in range(200):\n"
            "        V = mdp_dp.bellman_optimality(P, R, V, gamma)\n"
            "        errs.append(mdp_dp.sup_norm(V - v_star))\n"
            "    k = np.arange(1, 201)\n"
            "    plt.semilogy(k, errs, label='||V_k - v*||')\n"
            "    plt.semilogy(k, gamma**k * mdp_dp.sup_norm(v_star), '--', label='gamma^k ||V_0 - v*||')\n"
            "    plt.xlabel('k'); plt.legend(); plt.show()",
        ),
    ],
    "02_gridworld_dp": [
        ("md", "# 02 · Dynamic programming: VI vs PI vs LP\nGuide: `02-intermediate/01`, `/05`."),
        ("code", SETUP),
        (
            "code",
            "from rlguide import envs, mdp_dp, mdp_lp\n"
            "P, R = envs.random_mdp(S=12, A=4, seed=1)\n"
            "v_vi, pi_vi, d_vi = mdp_dp.value_iteration(P, R, 0.9, theta=1e-12)\n"
            "v_pi, pi_pi, iters = mdp_dp.policy_iteration(P, R, 0.9)\n"
            "v_lp = mdp_lp.solve_primal(P, R, 0.9)\n"
            "print('max |VI-PI| =', np.abs(v_vi-v_pi).max(), '  max |LP-PI| =', np.abs(v_lp-v_pi).max())\n"
            "print('PI iterations:', iters, '  VI sweeps:', len(d_vi))",
        ),
        (
            "md",
            "## Jacobi vs Gauss–Seidel evaluation\n"
            + PREDICT
            + "which curve reaches $10^{-8}$ first?",
        ),
        (
            "code",
            "pi = np.full(R.shape, 1 / R.shape[1])\n"
            "_, dj = mdp_dp.iterative_policy_evaluation(P, R, pi, 0.9, theta=1e-8)\n"
            "_, dg = mdp_dp.iterative_policy_evaluation(P, R, pi, 0.9, theta=1e-8, in_place=True)\n"
            "plt.semilogy(dj, label=f'Jacobi ({len(dj)} sweeps)')\n"
            "plt.semilogy(dg, label=f'Gauss-Seidel ({len(dg)} sweeps)')\n"
            "plt.xlabel('sweep'); plt.ylabel('Delta_k'); plt.legend(); plt.show()",
        ),
        ("md", "## The hallway\n$v_*(M)=1$, $v_*(L)=0.9$ with $\\gamma=0.9$."),
        (
            "code",
            "P, R, names, _ = envs.hallway()\n"
            "V, pol, deltas = mdp_dp.value_iteration(P, R, 0.9)\n"
            "print(dict(zip(names, V.round(4))), 'sweeps:', len(deltas))",
        ),
    ],
    "03_mc_vs_td": [
        ("md", "# 03 · Monte Carlo vs TD\nGuide: `01-beginner/04`, `03-expert/02`."),
        ("code", SETUP),
        (
            "code",
            "from rlguide import mc_td_prediction as mt\n"
            "ep = [('A', 0), ('B', 2), ('A', -1), ('C', 3)]\n"
            "print('returns', mt.returns_backward(ep))\n"
            "print('first-visit', mt.mc_prediction([ep])[0])\n"
            "print('every-visit', mt.mc_prediction([ep], first_visit=False)[0])",
        ),
        (
            "md",
            "## Batch TD vs batch MC (Sutton & Barto Example 6.4)\n"
            + PREDICT
            + "what does each method say V(A) is?",
        ),
        (
            "code",
            "data = mt.EXAMPLE_6_4\n"
            "print('batch MC:', mt.mc_prediction(data)[0])\n"
            "print('batch TD:', {k: round(v, 4) for k, v in mt.batch_td0(data).items()})",
        ),
        ("md", "## Random walk: RMS error vs episodes for different α"),
        (
            "code",
            "def random_walk_episode(rng, n=5):\n"
            "    s, ep = n // 2, []\n"
            "    while True:\n"
            "        s2 = s + (1 if rng.random() < 0.5 else -1)\n"
            "        r = 1.0 if s2 == n else 0.0\n"
            "        ep.append((s, r))\n"
            "        if s2 in (-1, n):\n"
            "            return ep\n"
            "        s = s2\n\n"
            "true_v = np.arange(1, 6) / 6\n\n"
            "@interact(alpha=FloatSlider(value=0.1, min=0.01, max=0.5, step=0.01))\n"
            "def compare(alpha):\n"
            "    rng = np.random.default_rng(0)\n"
            "    V_td, V_mc, e_td, e_mc = np.full(5, .5), np.full(5, .5), [], []\n"
            "    for _ in range(100):\n"
            "        ep = random_walk_episode(rng)\n"
            "        for t, (s, r) in enumerate(ep):\n"
            "            nxt = V_td[ep[t + 1][0]] if t + 1 < len(ep) else 0.0\n"
            "            V_td[s] += alpha * (r + nxt - V_td[s])\n"
            "        G = mt.returns_backward(ep)\n"
            "        for (s, _), g in zip(ep, G):\n"
            "            V_mc[s] += alpha * (g - V_mc[s])\n"
            "        e_td.append(np.sqrt(((V_td - true_v)**2).mean()))\n"
            "        e_mc.append(np.sqrt(((V_mc - true_v)**2).mean()))\n"
            "    plt.plot(e_td, label='TD(0)'); plt.plot(e_mc, label='constant-alpha MC')\n"
            "    plt.ylabel('RMS error'); plt.xlabel('episode'); plt.legend(); plt.show()",
        ),
    ],
    "04_cliff_walking": [
        (
            "md",
            "# 04 · Cliff walking: SARSA vs Expected SARSA vs Q-learning\n"
            "Guide: `02-intermediate/02`.\n\n"
            + PREDICT
            + "which algorithm earns the best *online* return, and which has the shortest greedy path?",
        ),
        ("code", SETUP),
        (
            "code",
            "from rlguide import td_control as tc\n\n"
            "@interact(eps=FloatSlider(value=0.1, min=0.0, max=0.3, step=0.02),\n"
            "          alpha=FloatSlider(value=0.5, min=0.05, max=1.0, step=0.05))\n"
            "def compare(eps, alpha):\n"
            "    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 3.5))\n"
            "    for m in ('sarsa', 'expected_sarsa', 'qlearning'):\n"
            "        Q, ret = tc.run(m, episodes=500, alpha=alpha, eps=eps, seed=0)\n"
            "        ax1.plot(np.convolve(ret, np.ones(20) / 20, 'valid'), label=m)\n"
            "        path = tc.greedy_path(Q)\n"
            "        if path:\n"
            "            ys, xs = zip(*path)\n"
            "            ax2.plot(xs, ys, marker='.', label=f'{m} ({len(path)-1} steps)')\n"
            "    ax1.set_ylim(-120, 0); ax1.set_title('online return (20-ep avg)'); ax1.legend()\n"
            "    ax2.fill_between([0.5, 10.5], 2.5, 3.5, color='k', alpha=.3)\n"
            "    ax2.invert_yaxis(); ax2.set_title('greedy paths (black = cliff)'); ax2.legend()\n"
            "    plt.show()",
        ),
    ],
    "05_convergence_stepsizes": [
        (
            "md",
            "# 05 · Step sizes: constant α vs 1/n\nGuide: `00-math-foundations/05`.\n\n"
            + PREDICT
            + "does the constant-α estimate ever stop jittering?",
        ),
        ("code", SETUP),
        (
            "code",
            "from rlguide import stochastic_approx as sa\n\n"
            "@interact(alpha=FloatSlider(value=0.5, min=0.01, max=0.99, step=0.01),\n"
            "          noise=FloatSlider(value=1.0, min=0.0, max=2.0, step=0.1))\n"
            "def show(alpha, noise):\n"
            "    rng = np.random.default_rng(0)\n"
            "    x = 1.0 + noise * rng.normal(size=5000)\n"
            "    plt.plot(sa.estimate_mean(x, alpha), lw=.6, label=f'constant alpha={alpha}')\n"
            "    plt.plot(sa.estimate_mean(x, None), lw=2, label='alpha = 1/n')\n"
            "    plt.axhline(1.0, color='k', ls='--'); plt.legend(); plt.show()\n"
            "    print('theory: stationary variance =', sa.constant_alpha_stationary_variance(alpha, noise**2))",
        ),
    ],
    "06_bandits": [
        ("md", "# 06 · Bandits: ε-greedy vs UCB vs Thompson\nGuide: `01-beginner/05`."),
        ("code", SETUP),
        (
            "code",
            "from rlguide import bandits\n"
            "means = [0.2, 0.5, 1.0, 0.1, 0.8]\n\n"
            "@interact(eps=FloatSlider(value=0.1, min=0.0, max=0.5, step=0.01),\n"
            "          c=FloatSlider(value=2.0, min=0.1, max=4.0, step=0.1))\n"
            "def show(eps, c):\n"
            "    for label, kw in [(f'eps-greedy {eps}', dict(strategy='eps', eps=eps)),\n"
            "                      ('greedy', dict(strategy='greedy')),\n"
            "                      (f'UCB c={c}', dict(strategy='ucb', c=c))]:\n"
            "        reg = np.mean([bandits.run_bandit(means, 3000, seed=s, **kw)['regret']\n"
            "                       for s in range(20)], axis=0)\n"
            "        plt.plot(reg, label=label)\n"
            "    ts = np.mean([bandits.thompson_bernoulli([.2, .5, .7, .1, .6], 3000, seed=s)['regret']\n"
            "                  for s in range(20)], axis=0)\n"
            "    plt.plot(ts, label='Thompson (Bernoulli arms)')\n"
            "    plt.ylabel('cumulative regret'); plt.legend(); plt.show()",
        ),
    ],
    "07_maximization_bias": [
        (
            "md",
            "# 07 · Maximization bias and Double Q-learning\nGuide: `02-intermediate/02` "
            "(Sutton & Barto Example 6.7). Optimal: LEFT 5% of the time (ε/2).",
        ),
        ("code", SETUP),
        (
            "code",
            "from rlguide import td_control as tc\n"
            "q = tc.maximization_bias('q', runs=300, episodes=300)\n"
            "dq = tc.maximization_bias('double', runs=300, episodes=300)\n"
            "plt.plot(q, label='Q-learning'); plt.plot(dq, label='Double Q-learning')\n"
            "plt.axhline(0.05, color='k', ls='--', label='optimal (eps/2)')\n"
            "plt.ylabel('% LEFT from A'); plt.xlabel('episode'); plt.legend(); plt.show()",
        ),
    ],
    "08_simplex_visual": [
        (
            "md",
            "# 08 · Simplex on the quiz LP\n$\\max 3x_1+2x_2$ s.t. $2x_1+x_2\\le4$, "
            "$x_1+2x_2\\le3$. Guide: `02-intermediate/04`.",
        ),
        ("code", SETUP),
        (
            "code",
            "from rlguide import simplex\n"
            "res = simplex.simplex([3, 2], [[2, 1], [1, 2]], [4, 3])\n"
            "for enter, leave, ratios in res.pivots:\n"
            "    print(f'{enter} enters, {leave} leaves (ratios {ratios})')\n"
            "print('x* =', res.x, ' z* =', res.value)",
        ),
        (
            "code",
            "xs = np.linspace(0, 2.5, 200)\n"
            "plt.fill([0, 2, 5/3, 0], [0, 0, 2/3, 1.5], alpha=.3, label='feasible polytope')\n"
            "plt.plot(xs, 4 - 2*xs, label='2x1 + x2 = 4'); plt.plot(xs, (3 - xs)/2, label='x1 + 2x2 = 3')\n"
            "plt.plot([0, 2, 5/3], [0, 0, 2/3], 'ko-', label='pivot path')\n"
            "plt.plot(xs, (19/3 - 3*xs)/2, 'k--', label='z = 19/3')\n"
            "plt.xlim(0, 2.5); plt.ylim(0, 2); plt.legend(); plt.gca().set_aspect('equal'); plt.show()",
        ),
    ],
    "09_branch_and_bound_tree": [
        (
            "md",
            "# 09 · Branch and bound\n$\\max 5x_1+4x_2+3x_3$ s.t. $2x_1+3x_2+x_3\\le4$, "
            "$x\\in\\{0,1\\}^3$. Guide: `02-intermediate/04`.\n\n"
            + PREDICT
            + "which node gets pruned by bound, and why?",
        ),
        ("code", SETUP),
        (
            "code",
            "from rlguide import branch_and_bound as bb\n"
            "res = bb.branch_and_bound([5, 4, 3], [[2, 3, 1]], [4], [(0, 1)] * 3)\n"
            "for i, node in enumerate(res.log):\n"
            "    x = None if node.x is None else np.round(node.x, 3)\n"
            "    print(f'node {i}: bounds={node.bounds}  LP={node.lp_value}  x={x}  -> {node.outcome}')\n"
            "print('optimum', res.value, res.x)",
        ),
    ],
    "10_approx_algorithms": [
        ("md", "# 10 · Approximation algorithms\nGuide: `02-intermediate/06`, `03-expert/05`."),
        ("code", SETUP),
        ("md", "## MAX-SAT: derandomisation trace"),
        (
            "code",
            "from rlguide import maxsat\n"
            "C = maxsat.GUIDE_EXAMPLE\n"
            "print('E[X] =', maxsat.expected_satisfied(C, {}))\n"
            "assign, trace = maxsat.derandomized(C, 3)\n"
            "for v, eT, eF, ch in trace:\n"
            "    print(f'x{v}: E|T={eT:.3f}  E|F={eF:.3f}  -> {ch}')\n"
            "print('satisfied:', maxsat.num_satisfied(C, assign), '/', len(C))",
        ),
        ("md", "## Knapsack FPTAS: ε vs quality and table size"),
        (
            "code",
            "from rlguide import knapsack_fptas as kf\n"
            "rng = np.random.default_rng(0)\n"
            "v = [int(x) for x in rng.integers(1, 1000, 25)]; w = [int(x) for x in rng.integers(1, 100, 25)]\n"
            "W = int(sum(w) * .4); opt = kf.exact(v, w, W)[1]\n"
            "for eps in [0.9, 0.5, 0.25, 0.1, 0.05]:\n"
            "    _, val, info = kf.fptas(v, w, W, eps)\n"
            "    print(f'eps={eps:<5} value/OPT={val/opt:.4f}  (guarantee >= {1-eps:.2f})  DP width={sum(info[\"scaled\"])}')",
        ),
        ("md", "## Vertex cover: LP rounding"),
        (
            "code",
            "from rlguide import vertex_cover as vc\n"
            "for name, n, E in [('path 1-2-3-4', 4, vc.PATH_1234), ('K5', 5, vc.complete_graph(5))]:\n"
            "    C, lp = vc.lp_rounding(n, E)\n"
            "    print(f'{name}: LP*={lp:.2f}  rounded |C|={len(C)}  OPT={vc.brute_force_opt(n, E)}')",
        ),
    ],
    "11_linear_fa_and_deadly_triad": [
        (
            "md",
            "# 11 · Function approximation and the deadly triad\n"
            "Guide: `03-expert/03`. Baird's counterexample: 7 states, linear features, "
            "off-policy semi-gradient TD(0) **diverges**.\n\n"
            + PREDICT
            + "what happens to $\\lVert w\\rVert$ as updates accumulate?",
        ),
        ("code", SETUP),
        (
            "code",
            "# Baird (1995), as in Sutton & Barto Example 11.1 (expected-update version)\n"
            "X = np.zeros((7, 8))\n"
            "for i in range(6):\n"
            "    X[i, i] = 2; X[i, 7] = 1\n"
            "X[6, 6] = 1; X[6, 7] = 2\n"
            "gamma, alpha = 0.99, 0.01\n"
            "w = np.array([1, 1, 1, 1, 1, 1, 10, 1], float)\n"
            "norms = []\n"
            "for _ in range(1000):\n"
            "    # target policy always 'solid' -> state 7; behaviour visits states uniformly\n"
            "    delta = gamma * X[6] @ w - X @ w          # reward is 0 everywhere\n"
            "    w = w + alpha * (X.T @ delta) / 7\n"
            "    norms.append(np.linalg.norm(w))\n"
            "plt.semilogy(norms); plt.xlabel('sweep'); plt.ylabel('||w||'); plt.title('divergence'); plt.show()",
        ),
        (
            "md",
            "Remove any one leg of the triad (tabular features, Monte Carlo targets, or on-policy "
            "state weighting) and the divergence disappears. DQN's replay buffer and target "
            "network are engineering answers to this instability.",
        ),
    ],
}


def cell(kind: str, src: str, nb: str, i: int) -> dict:
    lines = src.splitlines(keepends=True)
    base = {"id": f"{nb[:2]}-{i:02d}", "metadata": {}, "source": lines}
    if kind == "md":
        return {"cell_type": "markdown", **base}
    return {"cell_type": "code", "execution_count": None, "outputs": [], **base}


def render(name: str, cells: list[tuple[str, str]]) -> str:
    nb = {
        "cells": [cell(k, s, name, i) for i, (k, s) in enumerate(cells)],
        "metadata": {
            "kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
            "language_info": {"name": "python"},
        },
        "nbformat": 4,
        "nbformat_minor": 5,
    }
    return json.dumps(nb, indent=1, ensure_ascii=False) + "\n"


def main(check: bool) -> int:
    OUT.mkdir(exist_ok=True)
    stale = []
    for name, cells in NOTEBOOKS.items():
        path = OUT / f"{name}.ipynb"
        text = render(name, cells)
        if check:
            if not path.exists() or path.read_text(encoding="utf-8") != text:
                stale.append(path.name)
        else:
            path.write_text(text, encoding="utf-8")
    if check and stale:
        print("stale notebooks (run `mise run notebooks:build`):", *stale, sep="\n  ")
        return 1
    print(("checked " if check else "wrote ") + f"{len(NOTEBOOKS)} notebooks")
    return 0


if __name__ == "__main__":
    sys.exit(main("--check" in sys.argv))
