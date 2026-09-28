# MAX-SAT rounding and the FPTAS proof

> **Tier:** Expert · **Prereqs:** `02/06` · **Code:** `rlguide.maxsat.lp_relaxation`, `best_of_two`, `rlguide.knapsack_fptas` · **Tests:** `test_best_of_two_three_quarters`, `test_knapsack_fptas_guarantee`

## LP randomised rounding for MAX-SAT: $1 - 1/e$
$$\max\sum_C z_C\quad\text{s.t.}\quad \sum_{i\in P_C}y_i + \sum_{i\in N_C}(1 - y_i) \ge z_C,\qquad 0 \le y, z \le 1.$$
Set $x_i = T$ with probability $y_i^*$. For a clause of size $k$ (AM–GM + concavity):
$$\Pr[\text{sat}] \ge \Big(1 - \big(1 - \tfrac1k\big)^k\Big)z_C^* \ge \big(1 - \tfrac1e\big)z_C^*.$$
Hence $\mathbb E \ge (1 - 1/e)\,\mathrm{LP}^* \ge 0.632\,\mathrm{OPT}$.

## Best of two: ¾
- Unbiased coins: size-$k$ clause satisfied w.p. $1 - 2^{-k} \ge (1 - 2^{-k})z_C^*$.
- LP rounding: $\big(1 - (1 - 1/k)^k\big)z_C^*$.

Average of the two guarantees per clause size:

| $k$ | coins | rounding | average |
|---|---|---|---|
| 1 | ½ | 1 | ¾ |
| 2 | ¾ | ¾ | ¾ |
| ≥ 3 | ≥ 0.875 | ≥ 0.632 | > ¾ |

So the better of the two solutions is $\ge \tfrac34\mathrm{OPT}$ (Goemans & Williamson 1994). Yannakakis (1992/1994) gave the first ¾ algorithm via network flow. Williamson & Shmoys Ch. 5 presents the ½ → derandomisation → $1 - 1/e$ → ¾ sequence. `rlguide.maxsat.best_of_two` derandomises both.

## Knapsack FPTAS proof
Let $S$ be the output and $O$ an optimal set. Since $Kv'_i \le v_i < K(v'_i + 1)$, we have $Kv'_i \ge v_i - K$. Then
$$v(S) \ge K\,v'(S) \ge K\,v'(O) \ge v(O) - nK = \mathrm{OPT} - \varepsilon v_{\max} \ge (1 - \varepsilon)\,\mathrm{OPT},$$
using (i) optimality of $S$ for the scaled values and (ii) $\mathrm{OPT} \ge v_{\max}$ — valid **only after discarding items heavier than $W$**. ∎

Knapsack is *weakly* NP-hard, so an FPTAS is possible; **strongly** NP-hard problems have no FPTAS unless P = NP. Faster FPTASs exist (Chan 2018; Jin 2019; a nearly quadratic-time scheme in 2024).

## Practice
<details><summary>Where exactly does the proof use "discard items with w_i > W"?</summary>

In $\mathrm{OPT} \ge v_{\max}$: the single most valuable item must itself be feasible.
</details>
