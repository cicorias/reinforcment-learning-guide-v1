"""TD control: SARSA, Q-learning, Expected SARSA, Double Q-learning.

Guide: 02-intermediate/02-td-control-sarsa-qlearning.md
Run `mise run demo:cliff` for the Cliff Walking comparison.
"""

from __future__ import annotations

import numpy as np

ACTIONS = [(-1, 0), (0, 1), (1, 0), (0, -1)]  # up, right, down, left


class CliffWalking:
    """Sutton & Barto Example 6.6: 4x12 grid, start bottom-left, goal bottom-right.

    Stepping into the cliff (bottom row, columns 1..10) gives -100 and teleports
    to the start; every other step gives -1.
    """

    H, W = 4, 12
    n_states, n_actions = 48, 4
    START, GOAL = (3, 0), (3, 11)

    def reset(self) -> int:
        self.pos = self.START
        return self._s()

    def _s(self) -> int:
        return self.pos[0] * self.W + self.pos[1]

    def step(self, a: int) -> tuple[int, float, bool]:
        dr, dc = ACTIONS[a]
        r = min(max(self.pos[0] + dr, 0), self.H - 1)
        c = min(max(self.pos[1] + dc, 0), self.W - 1)
        self.pos = (r, c)
        if r == 3 and 1 <= c <= 10:
            self.pos = self.START
            return self._s(), -100.0, False
        return self._s(), -1.0, self.pos == self.GOAL


def eps_greedy(Q: np.ndarray, s: int, eps: float, rng: np.random.Generator) -> int:
    if rng.random() < eps:
        return int(rng.integers(Q.shape[1]))
    q = Q[s]
    return int(rng.choice(np.flatnonzero(q == q.max())))


def eps_greedy_probs(q_row: np.ndarray, eps: float) -> np.ndarray:
    """pi(a|s) for epsilon-greedy: eps/|A| everywhere, + (1-eps) on the greedy action."""
    probs = np.full(q_row.shape[0], eps / q_row.shape[0])
    probs[int(np.argmax(q_row))] += 1.0 - eps
    return probs


# ---------------------------------------------------------------- single updates
def sarsa_update(Q, s, a, r, s2, a2, alpha, gamma, terminal=False):
    target = r + (0.0 if terminal else gamma * Q[s2, a2])
    Q[s, a] += alpha * (target - Q[s, a])
    return target


def q_learning_update(Q, s, a, r, s2, alpha, gamma, terminal=False):
    target = r + (0.0 if terminal else gamma * Q[s2].max())
    Q[s, a] += alpha * (target - Q[s, a])
    return target


def expected_sarsa_update(Q, s, a, r, s2, alpha, gamma, eps, terminal=False):
    target = r + (0.0 if terminal else gamma * eps_greedy_probs(Q[s2], eps) @ Q[s2])
    Q[s, a] += alpha * (target - Q[s, a])
    return target


# ---------------------------------------------------------------- training loop
def run(method: str, episodes=500, alpha=0.5, gamma=1.0, eps=0.1, seed=0):
    """method in {'sarsa', 'qlearning', 'expected_sarsa'}. Returns (Q, returns per episode)."""
    rng = np.random.default_rng(seed)
    env = CliffWalking()
    Q = np.zeros((env.n_states, env.n_actions))
    returns = []
    for _ in range(episodes):
        s = env.reset()
        a = eps_greedy(Q, s, eps, rng)
        G, done = 0.0, False
        while not done:
            s2, r, done = env.step(a)
            G += r
            a2 = eps_greedy(Q, s2, eps, rng)
            if method == "sarsa":
                sarsa_update(Q, s, a, r, s2, a2, alpha, gamma, done)
            elif method == "qlearning":
                q_learning_update(Q, s, a, r, s2, alpha, gamma, done)
            elif method == "expected_sarsa":
                expected_sarsa_update(Q, s, a, r, s2, alpha, gamma, eps, done)
            else:
                raise ValueError(method)
            s, a = s2, a2
        returns.append(G)
    return Q, np.array(returns)


def greedy_path(Q: np.ndarray, max_steps: int = 200) -> list[tuple[int, int]] | None:
    """Follow argmax Q from the start. None if it falls off the cliff or loops."""
    env = CliffWalking()
    env.reset()
    path = [env.pos]
    for _ in range(max_steps):
        _, r, done = env.step(int(np.argmax(Q[env._s()])))
        if r == -100.0:
            return None
        path.append(env.pos)
        if done:
            return path
    return None


# ---------------------------------------------------------------- maximization bias
def maximization_bias(method: str, runs=300, episodes=300, alpha=0.1, eps=0.1, n_b=10, seed=0):
    """Sutton & Barto Example 6.7. Returns fraction of runs choosing LEFT from A per episode.

    A: right -> terminal (0); left -> B (0). B: n_b actions, each -> terminal with
    reward ~ N(-0.1, 1). Optimal: go right (left has expected value -0.1).
    """
    rng = np.random.default_rng(seed)
    left_counts = np.zeros(episodes)
    for _ in range(runs):
        QA1, QB1 = np.zeros(2), np.zeros(n_b)
        QA2, QB2 = np.zeros(2), np.zeros(n_b)
        for ep in range(episodes):
            qa = QA1 + QA2 if method == "double" else QA1
            a = (
                int(rng.integers(2))
                if rng.random() < eps
                else int(rng.choice(np.flatnonzero(qa == qa.max())))
            )
            if a == 1:  # right
                target = 0.0
                if method == "double" and rng.random() < 0.5:
                    QA2[1] += alpha * (target - QA2[1])
                else:
                    QA1[1] += alpha * (target - QA1[1])
                continue
            left_counts[ep] += 1
            # A --left--> B, reward 0: bootstrap from B
            if method == "double":
                if rng.random() < 0.5:
                    QA1[0] += alpha * (QB2[int(np.argmax(QB1))] - QA1[0])
                else:
                    QA2[0] += alpha * (QB1[int(np.argmax(QB2))] - QA2[0])
            else:
                QA1[0] += alpha * (QB1.max() - QA1[0])
            qb = QB1 + QB2 if method == "double" else QB1
            b = (
                int(rng.integers(n_b))
                if rng.random() < eps
                else int(rng.choice(np.flatnonzero(qb == qb.max())))
            )
            r = rng.normal(-0.1, 1.0)
            if method == "double" and rng.random() < 0.5:
                QB2[b] += alpha * (r - QB2[b])
            else:
                QB1[b] += alpha * (r - QB1[b])
    return left_counts / runs


if __name__ == "__main__":
    for m in ("sarsa", "expected_sarsa", "qlearning"):
        Q, ret = run(m, episodes=500, seed=0)
        path = greedy_path(Q)
        rows = sorted({p[0] for p in path}) if path else None
        print(
            f"{m:15s} mean return (last 100 eps) = {ret[-100:].mean():7.2f}   "
            f"greedy path length = {len(path) - 1 if path else 'n/a':>3}   rows used = {rows}"
        )
