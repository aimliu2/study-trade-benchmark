The HAR (Heterogeneous Autoregressive) model, introduced by Fulvio Corsi in 2009, is a highly popular econometric model used to forecast financial market volatility.
While estimators like the Yang-Zhang formula calculate historical volatility from past price data (such as OHLC prices), the HAR framework takes those calculated measurements (usually Realized Volatility) and forecasts where volatility is heading next.

1. The Core Philosophy: The Heterogeneous Market Hypothesis

Traditional models like ARMA or GARCH assume all market participants are identical. The HAR model recognizes that the market is made of different types of traders with different time horizons:
• Short-term traders: Day traders, market makers, and high-frequency algorithms (Daily horizon).
• Medium-term traders: Portfolio managers and swing traders who rebalance weekly (Weekly horizon).
• Long-term traders: Institutional investors, pension funds, and buy-and-hold investors (Monthly horizon).
Each group creates a distinct layer of volatility that feeds into the next. Long-term sentiment affects short-term trading, and intense short-term volatility can alter long-term trends.

2. The HAR Model Formula

The HAR model predicts tomorrow's volatility by taking a simple linear combination of yesterday's volatility, the average volatility over the past week, and the average volatility over the past month.
The mathematical formulation for predicting tomorrow's volatility ($RV_{t+1}$) is:
$$RV_{t+1}=\beta _{0}+\beta _{d}RV_{t}+\beta _{w}RV_{t,w}+\beta _{m}RV_{t,m}+\epsilon _{t+1}$$

Component Breakdowns:

• $RV_{t+1}$: Tomorrow's **actual** realized volatility (the regression target). (Corrected 2026-11-01:) it is not the forecast; the forecast is the fitted part without the error, $\hat{RV}_{t+1}=\beta_0+\beta_d RV_t+\beta_w RV_{t,w}+\beta_m RV_{t,m}$.
• $RV_{t}$: The Daily component: the realized volatility of day t, the latest completed day when the forecast is made ("yesterday" relative to the day being forecast).
• $RV_{t,w}$: The Weekly component. The average realized volatility of the last 5 trading days:
$RV_{t,w}=\frac{1}{5}\sum _{i=0}^{4}RV_{t-i}$
• $RV_{t,m}$: The Monthly component. The average realized volatility of the last 22 trading days:
$RV_{t,m}=\frac{1}{22}\sum _{i=0}^{21}RV_{t-i}$
• $\beta_0, \beta_d, \beta_w, \beta_m$: Coefficients estimated using standard Ordinary Least Squares (OLS) regression.
• $\epsilon _{t+1}$: The error term (residual noise).

3. Why It Is Widely Used

Despite its mathematical simplicity (it's just a multiple linear regression), the HAR model often outperforms complex GARCH variations, especially when fed intraday realized volatility (corrected 2026-11-01: "often", not always; in this study's daily-data results it does not win on every asset). It naturally replicates two critical features of financial data:
1. Long Memory: Financial volatility has a "long memory," meaning a shock today can continue influencing market volatility weeks or months into the future. By nesting 1-day, 5-day, and 22-day lags, HAR approximates this persistence (it is not a true long-memory model; the three horizons mimic slow decay up to about a month).
2. Volatility Clustering: Volatility tends to bunch up—high volatility days follow high volatility days. The multi-component lookback window naturally mirrors this structure.

4. Connecting Yang-Zhang and HAR

In practice, these tools are often paired together in quantitative finance workflows:
```
[ OHLC Market Data ] 
       │
       ▼
[ Yang-Zhang Estimator ]  ──► Calculates a range-based daily variance estimate (stands in for RV_t; true RV uses intraday returns)
       │
       ▼
[ HAR Forecast Model ]   ──► Uses rolling averages (Daily, Weekly, Monthly) to forecast tomorrow's market volatility (RV_t+1)

```

---

## Remark: what "refit" means in P2-f2 (2026-11-01)

A refit re-estimates **only the four coefficients β₀, β_d, β_w, β_m** (OLS).

| Part of the formula | What it is | Changes when |
|---|---|---|
| RV_t, RV_t,w, RV_t,m | Inputs: `yz_var_daily` and its 5- and 22-day averages | Every day, computed from data |
| 1 / 5 / 22 | Horizons (model design) | Never (fixed) |
| **β₀, β_d, β_w, β_m** | **Coefficients** | **At each refit** |

- The inputs update daily whether or not the model is refit. Each day's forecast
  = latest β × that day's inputs. A refit only changes how much weight each
  horizon gets.
- HAR itself doesn't require a refit schedule; how often is our choice. Refitting is one
  OLS fit, so daily costs nothing; monthly or annual are also valid.
- Scheme: expanding window from 2019. The forecast for t+1 uses β fitted on data up to t only.
  Compare refit frequencies on train (2021–23), fix one, then score test (2024+)
  once. With an expanding window, β should move slowly after a few years, so
  frequency likely matters little (unverified).
- **Open (decide together with the target):** what goes on the left side, RV_{t+1}. This file
  uses next-day YZ. The guide scores every model against one common target
  (provisionally next-day squared return). Recommended: fit HAR directly to that
  target, so it matches how it's scored and matches GARCH (fitted to returns).
- Also to test on train: fit in variance levels (can give negative forecasts,
  which QLIKE can't score) vs log variance (always positive; needs a correction
  when converting back to variance).
