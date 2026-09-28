"""Property / behaviour tests: the theorems behind the worked examples."""

import numpy as np
import pytest

from rlguide import (
    bandits,
    envs,
    knapsack_fptas,
    mdp_dp,
    mdp_lp,
    stochastic_approx,
    td_control,
    vertex_cover,
)


@pytest.mark.parametrize("seed", range(5))
def test_bellman_operators_are_gamma_contractions(seed):
    """03-expert/01: ||T u - T v||_inf <= gamma ||u - v||_inf for T^pi and T^*."""
    P, R = envs.random_mdp(seed=seed)
    rng = np.random.default_rng(seed)
    gamma = 0.9
    pi = rng.random(R.shape)
    pi /= pi.sum(axis=1, keepdims=True)
    for _ in range(20):
        u, v = rng.normal(size=R.shape[0]) * 10, rng.normal(size=R.shape[0]) * 10
        d = mdp_dp.sup_norm(u - v)
        assert (
            mdp_dp.sup_norm(
                mdp_dp.bellman_optimality(P, R, u, gamma)
                - mdp_dp.bellman_optimality(P, R, v, gamma)
            )
            <= gamma * d + 1e-12
        )
        assert (
            mdp_dp.sup_norm(
                mdp_dp.bellman_expectation(P, R, pi, u, gamma)
                - mdp_dp.bellman_expectation(P, R, pi, v, gamma)
            )
            <= gamma * d + 1e-12
        )


@pytest.mark.parametrize("seed", range(5))
def test_vi_pi_lp_agree(seed):
    """Capstone check: value iteration, policy iteration and the LP give the same v*."""
    P, R = envs.random_mdp(S=8, A=3, seed=seed)
    gamma = 0.9
    v_vi, _, _ = mdp_dp.value_iteration(P, R, gamma, theta=1e-12)
    v_pi, _, _ = mdp_dp.policy_iteration(P, R, gamma)
    v_lp = mdp_lp.solve_primal(P, R, gamma)
    assert v_vi == pytest.approx(v_pi, abs=1e-6)
    assert v_lp == pytest.approx(v_pi, abs=1e-6)


def test_dual_lp_matches_primal_and_is_deterministic():
    """03-expert/04: strong duality; optimal basic dual gives a deterministic policy."""
    P, R = envs.random_mdp(S=5, A=3, seed=3)
    gamma = 0.9
    mu0 = np.ones(5) / 5
    v = mdp_lp.solve_primal(P, R, gamma, weights=mu0)
    d, val, pi = mdp_lp.solve_dual(P, R, gamma, mu0)
    assert val == pytest.approx(mu0 @ v, abs=1e-6)
    assert np.allclose(pi.max(axis=1), 1.0, atol=1e-6)
    assert d.sum() == pytest.approx(1 / (1 - gamma))  # total discounted occupancy


def test_value_iteration_geometric_rate():
    """02-intermediate/01: Delta_k shrinks by at most a factor gamma per sweep."""
    P, R = envs.random_mdp(seed=7)
    _, _, deltas = mdp_dp.value_iteration(P, R, gamma=0.8, theta=1e-10)
    d = np.array(deltas[1:-1])
    assert np.all(d[1:] <= 0.8 * d[:-1] + 1e-12)


def test_in_place_evaluation_converges_to_same_values():
    """02-intermediate/01: Jacobi and Gauss-Seidel reach the same v_pi."""
    P, R = envs.random_mdp(S=10, A=2, seed=2)
    pi = np.full(R.shape, 0.5)
    exact = mdp_dp.evaluate(P, R, pi, 0.9)
    v_j, d_j = mdp_dp.iterative_policy_evaluation(P, R, pi, 0.9, in_place=False)
    v_gs, d_gs = mdp_dp.iterative_policy_evaluation(P, R, pi, 0.9, in_place=True)
    assert v_j == pytest.approx(exact, abs=1e-8)
    assert v_gs == pytest.approx(exact, abs=1e-8)
    assert len(d_gs) <= len(d_j)


def test_policy_iteration_terminates_quickly():
    P, R = envs.random_mdp(S=20, A=4, seed=11)
    _, _, iters = mdp_dp.policy_iteration(P, R, 0.95)
    assert iters < 4**20  # trivially finite; in practice a handful
    assert iters <= 20


def test_backward_induction_nonstationary():
    """01-beginner/02: finite horizon on the hallway; with 1 step left, L cannot reach R."""
    P, R, *_ = envs.hallway()
    V, pol = mdp_dp.backward_induction(P, R, horizon=3)
    assert V[2, 0] == 0.0  # at L with one step to go: no reward reachable
    assert V[1, 0] == 1.0  # at L with two steps to go: reach R
    assert V[0, 1] == 1.0


def test_cliff_walking_sarsa_safer_than_qlearning():
    """02-intermediate/02: Q-learning learns the 13-step edge path; SARSA the safer path,
    and SARSA earns more *online* return while exploring with eps = 0.1."""
    Q_q, ret_q = td_control.run("qlearning", episodes=500, seed=0)
    Q_s, ret_s = td_control.run("sarsa", episodes=500, seed=0)
    path_q, path_s = td_control.greedy_path(Q_q), td_control.greedy_path(Q_s)
    assert path_q is not None and len(path_q) - 1 == 13
    assert path_s is not None and len(path_s) - 1 > 13
    assert ret_s[-100:].mean() > ret_q[-100:].mean()


def test_maximization_bias_double_q_helps():
    """02-intermediate/02: Q-learning chooses LEFT far more often early on than Double Q."""
    q = td_control.maximization_bias("q", runs=200, episodes=100, seed=0)
    dq = td_control.maximization_bias("double", runs=200, episodes=100, seed=0)
    assert q[:30].mean() > dq[:30].mean() + 0.1


def test_constant_alpha_does_not_converge_but_one_over_n_does():
    """00-math-foundations/05: stationary variance alpha*sigma^2/(2-alpha)."""
    rng = np.random.default_rng(0)
    x = rng.normal(1.0, 1.0, size=200_000)
    est_const = stochastic_approx.estimate_mean(x, alpha=0.5)
    est_rm = stochastic_approx.estimate_mean(x, alpha=None)
    tail = est_const[1000:]
    assert tail.var() == pytest.approx(
        stochastic_approx.constant_alpha_stationary_variance(0.5, 1.0), rel=0.05
    )
    assert abs(est_rm[-1] - 1.0) < 0.01


def test_constant_alpha_converges_when_deterministic():
    """00-math-foundations/05 deterministic nuance."""
    est = stochastic_approx.estimate_mean(np.full(200, 3.0), alpha=0.5)
    assert est[-1] == pytest.approx(3.0)


def test_ucb_beats_pure_greedy_regret():
    """01-beginner/05: exploration matters; pure greedy can lock onto a bad arm."""
    means = [0.2, 0.5, 1.0, 0.1, 0.8]
    greedy = np.mean(
        [bandits.run_bandit(means, 3000, "greedy", seed=s)["regret"][-1] for s in range(10)]
    )
    ucb = np.mean([bandits.run_bandit(means, 3000, "ucb", seed=s)["regret"][-1] for s in range(10)])
    assert ucb < greedy


def test_vertex_cover_rounding_is_2_approx():
    """02-intermediate/06: LP rounding cover is feasible and <= 2 * LP*."""
    rng = np.random.default_rng(0)
    for _ in range(20):
        n = 7
        edges = [(i, j) for i in range(n) for j in range(i + 1, n) if rng.random() < 0.4]
        if not edges:
            continue
        C, lp = vertex_cover.lp_rounding(n, edges)
        assert vertex_cover.is_cover(C, edges)
        assert len(C) <= 2 * lp + 1e-9
        assert len(C) <= 2 * vertex_cover.brute_force_opt(n, edges)


@pytest.mark.parametrize("eps", [0.5, 0.25, 0.1])
def test_knapsack_fptas_guarantee(eps):
    """03-expert/05: value >= (1 - eps) OPT on random instances."""
    rng = np.random.default_rng(42)
    for _ in range(25):
        n = 8
        v = [int(x) for x in rng.integers(1, 200, n)]
        w = [int(x) for x in rng.integers(1, 50, n)]
        W = int(sum(w) * 0.4)
        _, got, _ = knapsack_fptas.fptas(v, w, W, eps)
        _, opt = knapsack_fptas.exact(v, w, W)
        assert got >= (1 - eps) * opt - 1e-9


def test_induced_chain_is_stochastic():
    """01-beginner/01: a fixed policy induces a Markov chain (rows sum to 1)."""
    P, R = envs.random_mdp(seed=5)
    pi = np.full(R.shape, 1 / R.shape[1])
    P_pi, _ = mdp_dp.induced_chain(P, R, pi)
    assert P_pi.sum(axis=1) == pytest.approx(np.ones(P_pi.shape[0]))
