"""Print every headline worked example from the guide with its computed value."""

import numpy as np

from rlguide import (
    branch_and_bound,
    envs,
    knapsack_fptas,
    maxsat,
    mc_td_prediction,
    mdp_dp,
    mdp_lp,
    simplex,
)


def main() -> None:
    rows = []
    rows.append(("E[V(S')] (math/01)", np.dot([0.2, 0.5, 0.3], [4, 1, 7])))
    P, R = envs.two_state_swap()
    rows.append(("two-state v, gamma=0.5 (math/03)", mdp_dp.evaluate(P, R, np.ones((2, 1)), 0.5)))
    P, R, *_ = envs.hallway()
    rows.append(("hallway v*(L), v*(M) (beginner/01)", mdp_dp.value_iteration(P, R, 0.9)[0][:2]))
    ep = [("A", 0), ("B", 2), ("A", -1), ("C", 3)]
    rows.append(("first-visit V(A) (beginner/04)", mc_td_prediction.mc_prediction([ep])[0]["A"]))
    V = {"s": 5.0, "s2": 8.0}
    rows.append(
        (
            "TD(0) target, new V(s) (beginner/04)",
            (mc_td_prediction.td0_update(V, "s", 2, "s2", 0.5, 0.9)[0], V["s"]),
        )
    )
    res = simplex.simplex([3, 2], [[2, 1], [1, 2]], [4, 3])
    rows.append(("simplex x*, z* (intermediate/04)", (res.x, res.value)))
    bb = branch_and_bound.branch_and_bound([5, 4, 3], [[2, 3, 1]], [4], [(0, 1)] * 3)
    rows.append(("branch & bound optimum (intermediate/04)", (bb.value, bb.x)))
    rows.append(
        (
            "shortest path LP correct vs flawed (intermediate/05)",
            (mdp_lp.shortest_path_lp(True)["s0"], mdp_lp.shortest_path_lp(False)["s0"]),
        )
    )
    a, _ = maxsat.derandomized(maxsat.GUIDE_EXAMPLE, 3)
    rows.append(
        (
            "derandomized MAXSAT satisfied (intermediate/06)",
            maxsat.num_satisfied(maxsat.GUIDE_EXAMPLE, a),
        )
    )
    ex = knapsack_fptas.GUIDE_EXAMPLE
    rows.append(
        (
            "knapsack FPTAS value (intermediate/06)",
            knapsack_fptas.fptas(ex["values"], ex["weights"], ex["W"], ex["eps"])[1],
        )
    )
    width = max(len(k) for k, _ in rows)
    for k, v in rows:
        print(f"{k:<{width}}  {v}")


if __name__ == "__main__":
    main()
