# Contraction proofs and complexity

> **Tier:** Expert · **Prereqs:** `00/01` (max lemma), `00/02`, `01/03` · **Tests:** `tests/test_properties.py::test_bellman_operators_are_gamma_contractions`

## Theorem: $T^\pi$ and $T^*$ are $\gamma$-contractions in $\lVert\cdot\rVert_\infty$

**$T^\pi$.**
$$(T^\pi u - T^\pi v)(s) = \gamma\sum_a\pi(a\mid s)\sum_{s'}P(s'\mid s,a)\,(u - v)(s').$$
**The rewards cancel** — they don't depend on $u$ or $v$. The right side is $\gamma$ times a convex combination of entries of $u - v$, bounded by $\lVert u - v\rVert_\infty$. Hence $\lVert T^\pi u - T^\pi v\rVert_\infty \le \gamma\lVert u - v\rVert_\infty$.

**$T^*$.** By the max lemma (`00/01` §8),
$$\big\lvert(T^*u)(s) - (T^*v)(s)\big\rvert \le \max_a\,\gamma\,\Big\lvert\sum_{s'}P(s'\mid s,a)(u-v)(s')\Big\rvert \le \gamma\lVert u - v\rVert_\infty. \quad\blacksquare$$

## Consequences
1. Unique $v_\pi$ and $v_*$ (Banach).
2. VI error: $\lVert V_k - v_*\rVert_\infty \le \gamma^k\lVert V_0 - v_*\rVert_\infty$.
3. **Greedy-policy loss:** if $\lVert V - v_*\rVert_\infty \le \epsilon$ then the greedy policy $\pi_V$ satisfies
$$\lVert v_{\pi_V} - v_*\rVert_\infty \le \frac{2\gamma\epsilon}{1-\gamma}.$$
4. **Monotonicity:** $u \le v \Rightarrow T^*u \le T^*v$ — used in the LP argument (`02/05`).

## Complexity landmarks
- Simplex with Dantzig's rule can take exponentially many pivots (Klee & Minty 1972). Ellipsoid (Khachiyan 1979) and interior-point methods (Karmarkar 1984) are polynomial.
- **For MDPs:** Ye (2011, *Math. Oper. Res.* 36(4)) proved simplex with Dantzig's rule and Howard's PI are **strongly polynomial** for fixed $\gamma$, with $O\big(\frac{mn}{1-\gamma}\log\frac{n}{1-\gamma}\big)$ iterations ($n$ states, $m$ total actions). Hansen, Miltersen & Zwick (*J. ACM* 60(1), 2013) improved PI to $O\big(\frac{m}{1-\gamma}\log\frac{n}{1-\gamma}\big)$.

## Practice
<details><summary>Prove T* is monotone.</summary>

If $u \le v$ then for every $a$: $R(s,a) + \gamma\sum_{s'}P\,u \le R(s,a) + \gamma\sum_{s'}P\,v$ (non-negative weights). Taking max over $a$ preserves ≤.
</details>

<details><summary>Show v ≥ T*v implies v ≥ v*.</summary>

By monotonicity $v \ge T^*v \ge (T^*)^2v \ge \dots \to v_*$.
</details>
