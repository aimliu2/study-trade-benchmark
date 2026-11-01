The GARCH(1,1) model (Generalized Autoregressive Conditional Heteroskedasticity) is the gold standard in quantitative finance for modeling and forecasting asset volatility. Unlike a standard rolling standard deviation, GARCH accounts for volatility clustering—the real-world phenomenon where large market shocks are followed by more large shocks, and quiet periods follow quiet periods. [ref1](https://riskhub.org/blogs/garch-11-model-explained), [ref2](https://mcpanalytics.ai/articles/garch-practical-guide-for-data-driven-decisions), [ref3](https://math.berkeley.edu/~btw/thesis4.pdf)

## 1. The GARCH(1,1) Formula Explained

To calculate volatility with GARCH, we break the process into two stages: the asset return equation and the variance equation. [ref1](https://mingze-gao.com/posts/garch-estimation/)

### Step A: Calculate the Shocks (Innovations)

**First**, we look at the daily return $r_{t}$ and subtract its mean μ (often assumed to be 0 or a small constant) to find the daily market "shock" $\epsilon _{t}$:

$$\epsilon _{t}=r_{t}-\mu $$

### Step B: The Variance Equation

The actual GARCH(1,1) formula forecasts tomorrow's variance $\sigma _{t}^{2}$ using three specific ingredients: 

$$\sigma _{t}^{2}=\omega +\alpha \epsilon _{t-1}^{2}+\beta \sigma _{t-1}^{2}$$

|Component| Component Name	|What it Means Economically|
|--|--|--|
|$\sigma _{t}^{2}$|	Conditional Variance|	The variance forecast for today, given everything we know up to yesterday.|
|ω|	Baseline Intercept	|A tiny constant anchor that keeps variance from dropping to zero.|
|$\alpha \epsilon_{t-1}^2$|	The ARCH Term (Shock)|	Represents the reaction to recent news. It looks at yesterday's squared return anomaly to see how hard the market was hit.|
|$\beta \sigma_{t-1}^2$|	The GARCH Term (Persistence)|	Represents volatility memory. It looks at yesterday's variance forecast, ensuring shocks decay slowly rather than vanishing overnight.|


The "(1,1)" Lags:

- The first 1 means it looks back at one day of market shock $\epsilon _{t-1}^{2}$
- The second 1 means it looks back at one day of its own variance forecast $\sigma _{t-1}^{2}$

Rules for Stability:

For the model to make mathematical sense, ω > 0 and α, β ≥ 0 (non-negative; zero is allowed). Crucially, α + β < 1, and then variance reverts to the long-run level ω / (1 − α − β); a shock's half-life is ln 0.5 / ln(α + β) days. (Corrected 2026-11-01:) if α + β = 1 (IGARCH), shocks never decay and no long-run variance exists; if α + β > 1, variance explodes. "Compound forever" applies only to the > 1 case. [ref1](https://mcpanalytics.ai/articles/garch-practical-guide-for-data-driven-decisions), [ref2](https://www.quantt.co.uk/resources/garch-model-explained), [ref3](https://medium.com/@polanitzer/building-a-garch-1-1-model-in-python-step-by-step-f8503e868efa), [ref4](https://www.youtube.com/watch?v=88oOzPFVWTU&t=324)

## 2. How to Fit GARCH(1,1) on OHLC Data

GARCH is designed for stationary return series, meaning you cannot feed it raw Open, High, Low, or Close stock prices directly. You must first convert your Close prices into Log Returns. [ref1](https://riskhub.org/blogs/garch-11-model-explained)
The most robust way to fit GARCH(1,1) is using Python's specialized arch library. [ref1](https://mcpanalytics.ai/articles/garch-practical-guide-for-data-driven-decisions), [ref2](https://mingze-gao.com/posts/garch-estimation/)



## 3. How to Interpret the Output Summary

When you run print(res.summary()), focus your attention on the Constant Mean and Volatility Parameter tables: [ref1](https://mcpanalytics.ai/articles/garch-practical-guide-for-data-driven-decisions)
• mu: The baseline mean asset return (μ). [ref1](https://www.youtube.com/watch?v=88oOzPFVWTU&t=324), [ref2](https://riskhub.org/blogs/garch-11-model-explained)
• omega: The variance intercept (ω). [ref1](https://mcpanalytics.ai/articles/garch-practical-guide-for-data-driven-decisions)
• alpha[1]: Look for values typically between 0.05 and 0.15. A higher alpha means volatility reacts sharply to sudden market spikes. [ref1](https://www.youtube.com/watch?v=7PEaWHIGTFs), [ref2](https://mcpanalytics.ai/articles/garch-practical-guide-for-data-driven-decisions)
• beta[1]: Look for values typically between 0.80 and 0.90. A high beta means volatility has a strong "memory" and will take a long time to cool down after a crash. [ref1](https://www.youtube.com/watch?v=oDXw0r0Oqmk&t=133), [ref2](https://www.youtube.com/watch?v=7PEaWHIGTFs), [ref3](https://mcpanalytics.ai/articles/garch-practical-guide-for-data-driven-decisions)
• alpha[1] + beta[1]: Calculate this value. If it is close to 0.99, your asset exhibits strong volatility persistence—meaning high-volatility environments will hang around for weeks. [ref1](https://mcpanalytics.ai/articles/garch-practical-guide-for-data-driven-decisions), [ref2](https://www.youtube.com/watch?v=88oOzPFVWTU&t=324)

---

# Maximum Likelihood Estimation (MLE)

Because the GARCH formula depends on its own past forecasts, there is no simple algebraic equation (like ordinary linear regression) that can instantly give you the answers. Instead, it must be solved numerically through a computer algorithm.
Here is exactly how the MLE method works behind the scenes to find the perfect parameters for your data:

## 1. The Core Idea: "Probability Reversed"

In everyday statistics, you take known parameters (like a coin having a 50% chance of heads) and guess the data outcome.
MLE does the exact opposite: It takes your actual historical OHLC returns as fixed facts, and asks: "If these returns actually happened, what specific values of $\omega $, $\alpha $, and $\beta $ would make this history the most likely scenario possible?"

## 2. Step-by-Step Optimization Process

To find the solution, the optimization engine (which runs automatically under the hood when you type model.fit()) goes through an iterative loop:
1. **The Initial Guess: The computer picks a reasonable starting guess for the parameters (e.g., $\omega=0.01, \alpha=0.1, \beta=0.8$)**.
2. Rolling the Variance Forward: Using those guess parameters and your actual historical returns, the computer loops through your entire dataset day-by-day to calculate the daily variance ($\sigma _{t}^{2}$) for every single day in your history.
3. Calculating the Likelihood Score: For each day, it looks at how far the actual return missed the predicted variance. Assuming a normal distribution, it calculates the mathematical probability (the "likelihood") of that daily error occurring. It sums up these scores across your entire history into a metric called the Log-Likelihood.
4. Tweaking and Repeating: The algorithm looks at the total score. It tweaks the values of $\omega $, $\alpha $, and $\beta $ slightly, runs through the history again, and checks if the new score is higher.
5. Convergence: It repeats this loop hundreds of times until the parameters reach a "peak" where the score cannot get any higher. This peak represents the Maximum Likelihood Estimate.

## 3. What if it fails to solve?

When your Maximum Likelihood Estimation (MLE) diverges or fails to converge, it means the mathematical solver got lost trying to find a stable peak for your parameters. Adding "more coverage" (meaning a larger dataset) can sometimes help, but if the underlying data has massive spikes or structural shifts, more data can actually compound the problem.
To get the model to converge safely, you can fix the issue using four distinct levers: scaling, fat-tailed distributions, bounding parameters, or adding constraints.

### 3.1 Scale Your Data (The Quickest Fix)

The number one reason MLE diverges in GARCH is numerical scale. If your raw percentage returns look like 0.02 (for 2%), squaring that value yields 0.0004. The solver struggles to optimize an ω value that needs to be 0.000001.
The Fix: Multiply your returns by 100 so they are on a whole percentage scale (e.g., 2.0 instead of 0.02). The arch library handles these magnitudes much better.

```python
# Do this before fitting
df['Return'] = 100 * np.log(df['Close'] / df['Close'].shift(1))
```

### 3.2. Switch to a Student's t-Distribution (Handling Shocks)

By default, GARCH assumes asset returns are normally distributed. However, real-world financial data has "fat tails" (extreme crashes and spikes). When a massive 10% drop occurs, a normal distribution treats it as extremely unlikely, so that day adds a very large negative term to the log-likelihood. (Corrected 2026-11-01: it is a finite penalty, not negative infinity, but a few such days can dominate the fit and destabilize the optimizer.) Note: for forecasting *variance*, normal MLE stays consistent even when returns are fat-tailed (quasi-MLE), so t is a fix for fitting trouble, not a requirement.
The Fix: Change the distribution to 't' (Student's t-distribution). This tells the solver to expect extreme outliers, preventing it from panicking and diverging.

```python
# Change dist='normal' to dist='t'
model = arch_model(df['Return'], p=1, q=1, vol='Garch', dist='t')
res = model.fit(disp='off')
```

### 3.3. Adjust the Optimization Bounds & Algorithms

If the solver is bouncing around wildly, you can switch the backend mathematical algorithm or give it better starting parameters so it doesn't wander off into unstable territory.
~~The Fix: Use the update_freq or change the method parameter within .fit(). The default algorithm is SLSQP, but L-BFGS-B is often more robust against divergence.~~

(Corrected 2026-11-01:) In `arch` (checked on 8.0.0), `.fit()` has **no `method` argument**: it always uses SLSQP, so `model.fit(method='L-BFGS-B')` raises a TypeError. `update_freq` only controls how often progress is printed. The levers that exist are starting values, optimizer options and the tolerance:

```python
# Give better starting values (omega, alpha, beta for GARCH(1,1)) and/or more iterations
res = model.fit(disp='off', starting_values=np.array([0.05, 0.10, 0.85]), options={'maxiter': 1000})
```

Restarting from several starting values and checking that they reach the same log-likelihood is also a good test that the optimizer found the true peak.

### 3.4. When does adding "More Data" actually help?

Adding more data (broader coverage) helps only if your current dataset is too short.
• If you have fewer than 500 rows, the solver doesn't have enough history to map out a clear baseline variance, so estimates become imprecise (persistence especially) and the fit can fail. Expanding to 1,000+ rows gives it structural stability.
• The Caveat: If you add too much historical data (e.g., 20 years of data), you run into structural breaks (e.g., the 2008 crash vs. the 2020 crash). The asset's baseline volatility changed fundamentally over those decades, and one single ω, α, β combo cannot fit both regimes. (Corrected 2026-11-01: the MLE usually still converges, but to a compromise. A typical symptom is persistence α + β pushed towards 1.)

### Summary Troubleshooting Checklist


|If your code throws a warning...|	Try this step first:	|Why it works:|
|--|--|--|
|ConditionNumberWarning or flat lines|	Multiply returns by 100.|	Fixes internal rounding errors.|
|Non-positive definite or NaN values|	Switch to dist='t'.	|Allows the model to accept extreme crashes.|
|Failed to converge	|Try other `starting_values` or raise `options={'maxiter': ...}` (`arch` has no `method` switch; corrected 2026-11-01).|	Starts the solver nearer the peak / gives it more steps.|
|Data size is < 300 daily bars|	Expand data to at least 500-1000 rows.|	Gives the MLE a clear statistical baseline.|



