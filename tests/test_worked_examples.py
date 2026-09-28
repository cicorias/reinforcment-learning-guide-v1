"""Every numeric worked example in the guide, asserted.

Rule (see CLAUDE.md): if a number appears in a worked example in the Markdown,
it must be checked here, and the test docstring must name the guide file.
"""

import math

import numpy as np
import pytest

from rlguide import (
    bandits,
    branch_and_bound,
    envs,
    knapsack_fptas,
    maxsat,
    mc_td_prediction,
    mdp_dp,
    mdp_lp,
    simplex,
    td_control,
    vertex_cover,
)


# ---------------------------------------------------------------- 00 math foundations
def test_expected_next_state_value():
    """00-math-foundations/01: E[V(S')] = 0.2*4 + 0.5*1 + 0.3*7 = 3.4"""
    assert np.dot([0.2, 0.5, 0.3], [4, 1, 7]) == pytest.approx(3.4)


def test_incremental_mean_practice():
    """00-math-foundations/01 practice 2: running means 4, 3, 4"""
    q, out = 0.0, []
    for n, x in enumerate([4, 2, 6], start=1):
        q += (x - q) / n
        out.append(q)
    assert out == pytest.approx([4, 3, 4])


def test_die_variance():
    """00-math-foundations/01 practice 1: E=3.5, Var=35/12"""
    x = np.arange(1, 7)
    assert x.mean() == pytest.approx(3.5)
    assert x.var() == pytest.approx(35 / 12)


def test_contraction_example_fixed_point():
    """00-math-foundations/02: T(x)=0.5x+1 -> 1, 1.5, 1.75, 1.875 -> 2"""
    xs, x = [], 0.0
    for _ in range(4):
        x = 0.5 * x + 1
        xs.append(x)
    assert xs == pytest.approx([1, 1.5, 1.75, 1.875])


def test_vi_iterations_needed():
    """00-math-foundations/02 practice 1: 0.9^k * 10 <= 0.01 -> k = 66"""
    k = math.ceil(math.log(0.001) / math.log(0.9))
    assert k == 66 and 0.9**k * 10 <= 0.01 < 0.9 ** (k - 1) * 10


def test_two_state_linear_solve():
    """00-math-foundations/03: alternating states, R=1, gamma=0.5 -> v = (2, 2)"""
    P, R = envs.two_state_swap()
    v = mdp_dp.evaluate(P, R, np.ones((2, 1)), gamma=0.5)
    assert v == pytest.approx([2.0, 2.0])


def test_linear_algebra_practice():
    """00-math-foundations/03 practice: v2 = 10, v1 = 4.5/0.55 ~ 8.18"""
    P = np.array([[[0.5, 0.5], [0.0, 1.0]]])
    R = np.array([[0.0], [1.0]])
    v = mdp_dp.evaluate(P, R, np.ones((2, 1)), gamma=0.9)
    assert v[1] == pytest.approx(10.0)
    assert v[0] == pytest.approx(4.5 / 0.55)


# ---------------------------------------------------------------- 01 beginner
def test_hallway_values():
    """01-beginner/01 and 02-intermediate/01: v*(M) = 1, v*(L) = 0.9 (gamma = 0.9)"""
    P, R, *_ = envs.hallway()
    V, pol, deltas = mdp_dp.value_iteration(P, R, gamma=0.9)
    assert V[:2] == pytest.approx([0.9, 1.0])
    assert list(pol[:2]) == [1, 1]  # always move right


def test_weather_stationary():
    """01-beginner/01: weather chain stationary distribution (2/3, 1/3)"""
    mu = envs.stationary_distribution(envs.weather_chain())
    assert mu == pytest.approx([2 / 3, 1 / 3])


def test_discounted_return_example():
    """01-beginner/02: rewards 1, 0, 2 with gamma 0.5 -> G0 = 1.5"""
    G = mc_td_prediction.returns_backward([("a", 1), ("b", 0), ("c", 2)], gamma=0.5)
    assert G[0] == pytest.approx(1.5)


def test_constant_reward_return():
    """question-bank Q5: reward 1 forever, gamma 0.9 -> 10"""
    assert sum(0.9**k for k in range(5000)) == pytest.approx(10.0)


def test_first_visit_quiz_example():
    """01-beginner/04 ex.1: episode A,B,A,C rewards 0,2,-1,3 -> first-visit V(A)=4.0"""
    ep = [("A", 0), ("B", 2), ("A", -1), ("C", 3)]
    assert mc_td_prediction.returns_backward(ep) == [4, 4, 2, 3]
    V, stored = mc_td_prediction.mc_prediction([ep], first_visit=True)
    assert stored["A"] == [4] and V["A"] == pytest.approx(4.0)
    V_every, _ = mc_td_prediction.mc_prediction([ep], first_visit=False)
    assert V_every["A"] == pytest.approx(3.0)


def test_first_vs_every_visit_three_episodes():
    """01-beginner/04 ex.2: first-visit 3.67, every-visit 3.00"""
    eps = [[("A", 4)], [("A", 2)], [("A", 4), ("A", 1)]]  # returns 4; 2; 5 then 1
    fv, _ = mc_td_prediction.mc_prediction(eps, first_visit=True)
    ev, _ = mc_td_prediction.mc_prediction(eps, first_visit=False)
    assert fv["A"] == pytest.approx(11 / 3)
    assert ev["A"] == pytest.approx(3.0)


def test_mc_practice():
    """01-beginner/04 practice 1: X,Y,X,Z rewards 1,1,1,1 -> first 4, every 3"""
    ep = [("X", 1), ("Y", 1), ("X", 1), ("Z", 1)]
    fv, _ = mc_td_prediction.mc_prediction([ep], first_visit=True)
    ev, _ = mc_td_prediction.mc_prediction([ep], first_visit=False)
    assert (fv["X"], ev["X"]) == (pytest.approx(4), pytest.approx(3))


def test_td0_quiz_example():
    """01-beginner/04: target 9.2, delta 4.2, V(s) 5 -> 7.1"""
    V = {"s": 5.0, "s2": 8.0}
    target, delta = mc_td_prediction.td0_update(V, "s", 2.0, "s2", alpha=0.5, gamma=0.9)
    assert (target, delta, V["s"]) == (pytest.approx(9.2), pytest.approx(4.2), pytest.approx(7.1))


def test_td0_practice():
    """01-beginner/04 practice 2: target 2, delta 2, V(s) = 0.2"""
    V = {"s": 0.0, "s2": 3.0}
    mc_td_prediction.td0_update(V, "s", -1.0, "s2", alpha=0.1, gamma=1.0)
    assert V["s"] == pytest.approx(0.2)


def test_eps_greedy_probabilities():
    """01-beginner/05: k=4, eps=0.2 -> greedy 0.85, others 0.05 (question-bank Q15)"""
    p = bandits.eps_greedy_action_probs(4, 0.2)
    assert p == pytest.approx([0.85, 0.05, 0.05, 0.05])


def test_vertex_cover_path_opt():
    """01-beginner/06: path 1-2-3-4 has minimum vertex cover size 2"""
    assert vertex_cover.brute_force_opt(4, vertex_cover.PATH_1234) == 2


def test_vertex_cover_integrality_gap_complete_graph():
    """01-beginner/06: K_n has LP* = n/2 and OPT = n-1"""
    n = 5
    edges = vertex_cover.complete_graph(n)
    _, lp = vertex_cover.lp_relaxation(n, edges)
    assert lp == pytest.approx(n / 2)
    assert vertex_cover.brute_force_opt(n, edges) == n - 1


# ---------------------------------------------------------------- 02 intermediate
def test_pi_tie_practice():
    """02-intermediate/01 practice: v(1) = 2, v(2) = 4, q(1,a) = q(1,b) = 2 (tie)"""
    # state 0 (=1): a -> stay r=1 ; b -> state 1 r=0.   state 1 (=2): r=2 stay (both actions)
    P = np.zeros((2, 2, 2))
    P[0, 0, 0] = 1
    P[1, 0, 1] = 1
    P[:, 1, 1] = 1
    R = np.array([[1.0, 0.0], [2.0, 2.0]])
    V, pol, _ = mdp_dp.policy_iteration(P, R, gamma=0.5)
    assert V == pytest.approx([2.0, 4.0])
    Q = mdp_dp.q_from_v(P, R, V, 0.5)
    assert Q[0] == pytest.approx([2.0, 2.0])
    assert pol[0] == 0  # tie kept at the current action


def test_q_learning_quiz_example():
    """02-intermediate/02: Q=0, alpha=0.5, r=1, max Q(s')=0.6 -> 0.5 + 0.3*gamma (0.77)"""
    Q = np.zeros((2, 2))
    Q[1] = [0.6, 0.2]
    td_control.q_learning_update(Q, 0, 0, 1.0, 1, alpha=0.5, gamma=0.9)
    assert Q[0, 0] == pytest.approx(0.5 + 0.3 * 0.9) and Q[0, 0] == pytest.approx(0.77)


def test_simplex_quiz_example():
    """02-intermediate/04: first ratios (2, 3) -> s1 leaves; optimum x=(5/3, 2/3), z=19/3"""
    res = simplex.simplex([3, 2], [[2, 1], [1, 2]], [4, 3])
    entering, leaving, ratios = res.pivots[0]
    assert (entering, leaving) == ("x1", "s1") and ratios == pytest.approx([2, 3])
    assert res.x == pytest.approx([5 / 3, 2 / 3])
    assert res.value == pytest.approx(19 / 3)


def test_branch_and_bound_example():
    """02-intermediate/04: root bound 9.33, optimum 8 at (1, 0, 1)"""
    res = branch_and_bound.branch_and_bound([5, 4, 3], [[2, 3, 1]], [4], [(0, 1)] * 3)
    assert res.log[0].lp_value == pytest.approx(28 / 3)
    assert res.value == pytest.approx(8)
    assert list(res.x) == [1, 0, 1]
    outcomes = [node.outcome for node in res.log]
    assert "integral" in outcomes and "pruned-bound" in outcomes


def test_shortest_path_lp_direction():
    """02-intermediate/05 + errata #2: correct LP gives 3; flawed 'min with >=' gives 5"""
    assert mdp_lp.shortest_path_lp(correct=True)["s0"] == pytest.approx(3.0)
    assert mdp_lp.shortest_path_lp(correct=False)["s0"] == pytest.approx(5.0)


def test_maxsat_clause_probability():
    """question-bank Q44: 3-literal clause satisfied w.p. 7/8"""
    assert maxsat.expected_satisfied([[1, 2, 3]], {}) == pytest.approx(7 / 8)


def test_maxsat_derandomization_trace():
    """02-intermediate/06: E=2.75; x1: 3.25 vs 2.25 -> T; x2: 3.0 vs 3.5 -> F; x3: 4 vs 3 -> T"""
    C = maxsat.GUIDE_EXAMPLE
    assert maxsat.expected_satisfied(C, {}) == pytest.approx(2.75)
    assign, trace = maxsat.derandomized(C, 3)
    assert [(round(t, 4), round(f, 4), ch) for _, t, f, ch in trace] == [
        (3.25, 2.25, True),
        (3.0, 3.5, False),
        (4.0, 3.0, True),
    ]
    assert maxsat.num_satisfied(C, assign) == 4


def test_knapsack_fptas_example():
    """02-intermediate/06: K=20, v'=(3,5,6), picks items {2,3} -> 220 = OPT"""
    ex = knapsack_fptas.GUIDE_EXAMPLE
    S, val, info = knapsack_fptas.fptas(ex["values"], ex["weights"], ex["W"], ex["eps"])
    assert info["K"] == pytest.approx(20)
    assert info["scaled"] == [3, 5, 6]
    assert S == {1, 2} and val == 220
    assert knapsack_fptas.exact(ex["values"], ex["weights"], ex["W"])[1] == 220


# ---------------------------------------------------------------- 03 expert
def test_batch_td_vs_batch_mc_example_6_4():
    """03-expert/02: batch MC V(A)=0; batch TD V(A)=0.75; both V(B)=0.75"""
    data = mc_td_prediction.EXAMPLE_6_4
    mc, _ = mc_td_prediction.mc_prediction(data)
    td = mc_td_prediction.batch_td0(data)
    assert mc["A"] == pytest.approx(0.0) and mc["B"] == pytest.approx(0.75)
    assert td["A"] == pytest.approx(0.75, abs=1e-6) and td["B"] == pytest.approx(0.75, abs=1e-6)


def test_best_of_two_three_quarters():
    """03-expert/05: best-of-two >= 3/4 OPT on random 2-SAT-ish instances"""
    rng = np.random.default_rng(1)
    for _ in range(20):
        n, m = 6, 15
        clauses = []
        for _ in range(m):
            k = int(rng.integers(1, 4))
            vs = rng.choice(np.arange(1, n + 1), size=k, replace=False)
            clauses.append([int(v) if rng.random() < 0.5 else -int(v) for v in vs])
        _, got = maxsat.best_of_two(clauses, n)
        assert got >= 0.75 * maxsat.brute_force_opt(clauses, n) - 1e-9
