# Probability, expectation and the Markov property

> **Tier:** Foundations · **Used by:** everything · **Notebook:** `01_expectation_and_contraction`

## 1. Random variables
**Intuition.** A random variable (RV) is a number whose value depends on chance — e.g. the next reward.

**Definition.** A discrete RV $X$ takes value $x$ with probability $p(x) \ge 0$, where $\sum_x p(x) = 1$.

## 2. Expectation
$$\mathbb E[X] = \sum_x x\,p(x).$$

**Worked example (quiz).** From state $s$ the next state has values $V(s') \in \{4, 1, 7\}$ with probabilities $\{0.2, 0.5, 0.3\}$:
$$\mathbb E[V(S')] = 0.2\cdot 4 + 0.5 \cdot 1 + 0.3 \cdot 7 = 0.8 + 0.5 + 2.1 = 3.4.$$

**Pitfall.** Expectation weights each outcome by its probability. It is *not* the plain average $(4+1+7)/3 = 4$, and *not* the most likely value (1).

## 3. Linearity of expectation
$$\mathbb E[aX + bY] = a\,\mathbb E[X] + b\,\mathbb E[Y] \quad \text{always — even when } X, Y \text{ are dependent.}$$

*Proof.* $\sum_{x,y}(ax+by)\,p(x,y) = a\sum_x x\sum_y p(x,y) + b\sum_y y\sum_x p(x,y) = a\,\mathbb E[X] + b\,\mathbb E[Y]$. ∎

This one fact powers the MAX-SAT $m/2$ bound, the return decomposition $G_t = R_{t+1} + \gamma G_{t+1}$ inside every Bellman equation, and the policy-evaluation linear system.

## 4. Conditional expectation and the law of total expectation
$$\mathbb E[X \mid Y=y] = \sum_x x\,p(x \mid y), \qquad \mathbb E[X] = \sum_y p(y)\,\mathbb E[X \mid Y=y].$$

- **RL:** $v_\pi(s) = \sum_a \pi(a\mid s)\,q_\pi(s,a)$ is the law of total expectation, conditioning on the action.
- **MAX-SAT:** $\mathbb E[W] = \tfrac12\mathbb E[W\mid x_1{=}T] + \tfrac12\mathbb E[W \mid x_1{=}F]$, so at least one branch is $\ge \mathbb E[W]$ — the heart of derandomisation.

## 5. Variance
$$\operatorname{Var}[X] = \mathbb E\big[(X - \mathbb E X)^2\big] = \mathbb E[X^2] - (\mathbb E X)^2.$$
For $n$ i.i.d. samples, $\operatorname{Var}[\bar X_n] = \sigma^2 / n$. This is why Monte Carlo — which averages long, noisy returns — has high variance and needs many episodes.

## 6. Sample mean and the incremental update
$$\bar X_n = \frac1n\sum_{i=1}^n X_i \quad\Longrightarrow\quad \bar X_n = \bar X_{n-1} + \frac1n\big(X_n - \bar X_{n-1}\big).$$

*Derivation.* $n\bar X_n = (n-1)\bar X_{n-1} + X_n$; divide by $n$ and rearrange.

This is the template **NewEstimate ← OldEstimate + StepSize · (Target − OldEstimate)** shared by every RL update (Sutton & Barto §2.4).

## 7. The Markov property
$$\Pr(S_{t+1}, R_{t+1} \mid S_0, A_0, \dots, S_t, A_t) = \Pr(S_{t+1}, R_{t+1} \mid S_t, A_t).$$
The present state carries all the information about the history that matters for predicting the future.

## 8. `max` vs `argmax`
$\max_a f(a)$ is a **value**; $\arg\max_a f(a)$ is the **set of maximisers** (ties matter).

**Max lemma.** $\lvert \max_a f(a) - \max_a g(a) \rvert \le \max_a \lvert f(a) - g(a)\rvert$.

*Proof.* Let $a^*$ maximise $f$. Then $\max f - \max g \le f(a^*) - g(a^*) \le \max_a\lvert f - g\rvert$; swap $f, g$ for the other direction. ∎

This lemma is the key step in the $T^*$ contraction proof (`03-expert/01`).

## Practice
<details><summary>1. A die pays its face value. Find E[X] and Var[X].</summary>

$\mathbb E[X] = 3.5$; $\mathbb E[X^2] = 91/6$; $\operatorname{Var} = 91/6 - 12.25 = 35/12 \approx 2.92$.
</details>

<details><summary>2. Running mean starts at 0; samples 4, 2, 6 arrive. Give the estimates.</summary>

4, 3, 4.
</details>

<details><summary>3. f = (1, 5, 3), g = (2, 4, 4). Verify the max lemma.</summary>

$\lvert 5 - 4\rvert = 1 \le \max(1, 1, 1) = 1$. ✓
</details>

> **Run it:** `tests/test_worked_examples.py::test_expected_next_state_value`, `::test_incremental_mean_practice`, `::test_die_variance`
