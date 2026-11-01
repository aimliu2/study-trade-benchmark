# P2-f2 — Volatility Representation & Validation Handoff

**Project:** Proj-AlgoTrade  
**Phase:** P2 — Feature Research  
**Feature:** f2 — Current and Forecast Volatility  
**Status:** Validation methodology consolidated  
**Primary timeframe:** 1D  
**Initial universe:** BTCUSDT, ETHUSDT, QQQ

---

## 1. Research Objective

P2-f2 aims to produce interpretable representations of current volatility and next-day close-to-close return uncertainty.

The research question is:

> Does a volatility forecasting model provide credible and useful information beyond simpler historical volatility measurements?

The desired forecast output is:

$$
\boxed{
\hat{\sigma}_{t+1}
=
\sqrt{\widehat{\operatorname{Var}}(r_{t+1}\mid\mathcal F_t)}
}
$$

Where:

- $r_{t+1}$ is the next-day close-to-close log return.
- $\mathcal F_t$ is information available through day $t$.
- $\hat\sigma_{t+1}$ is the predicted next-day return standard deviation.

Volatility is a **P2 feature, not an exposure controller or independent trading signal**.

The research evaluates whether volatility measurements and forecasts are credible enough to retain as candidate features. Their incremental contribution to P2 opportunity estimation is tested separately.

## 2. Candidate Volatility Representations

### Simple historical representations

| Feature | Description |
| --- | --- |
| Normalized ATR | Recent price-range magnitude, including gaps |
| Rolling return SD | Historical close-to-close return dispersion |
| Yang–Zhang volatility | OHLC-based historical volatility estimator |

These provide interpretable current-volatility measurements and simple benchmarks.

ATR measures price ranges rather than close-to-close return variance. Its forecast relevance must therefore be assessed on a compatible target and scale before direct comparison with GARCH.

### Forecast models

| Model | Description |
| --- | --- |
| HAR-YZ | Multi-horizon volatility persistence using Yang–Zhang estimates |
| GARCH(1,1) | Symmetric conditional-variance forecasting |
| EGARCH(1,1) | Asymmetric volatility response using log variance |
| GJR-GARCH(1,1) | Asymmetric response to negative return shocks |

The initial comparison is restricted to these four models.

HAR-YZ must be aligned or calibrated to forecast next-day close-to-close return variance. Forecasting a rolling Yang–Zhang statistic alone does not guarantee this alignment.

No hybrid or ensemble models are required initially.

## 3. Return and Variance Definitions

Use daily percentage log returns:

$$
\boxed{
r_t=100\ln\left(\frac{C_t}{C_{t-1}}\right)
}
$$

The initial conditional mean assumption is:

$$
\boxed{\hat\mu_{t+1}=0}
$$

The return model is:

$$
r_{t+1}=\mu_{t+1}+\sigma_{t+1}Z_{t+1}
$$

Where $Z_{t+1}$ is the standardized innovation.

For a correctly specified conditional mean and variance model:

$$
E[Z_{t+1}\mid\mathcal F_t]=0
$$

$$
\operatorname{Var}(Z_{t+1}\mid\mathcal F_t)=1
$$

These conditions do not require normally distributed innovations.

The forecast conditional variance is:

$$
\boxed{\hat h_{t+1}=\hat\sigma_{t+1}^2}
$$

All models and validation targets must use consistent percentage-return units.

## 4. Existing Validation Target — Retained

The previous implementation used:

$$
RV_{t+1}
=
\left(
100\ln\frac{C_{t+1}}{C_t}
\right)^2
$$

This is **squared daily close-to-close return**, not intraday realized variance.

Rename it:

$$
\boxed{y_{t+1}=r_{t+1}^2}
$$

Under the zero-mean assumption:

$$
E[r_{t+1}^2\mid\mathcal F_t]
=
\operatorname{Var}(r_{t+1}\mid\mathcal F_t)
$$

Therefore, squared daily returns are a valid, although noisy, observable proxy for the conditional variance target.

**Decision:** Retain the existing validation target and methodology. No intraday realized-variance reconstruction is required.

## 5. Consolidated Validation

The validation is reduced to three core components.

### Test 1 — QLIKE

QLIKE remains the primary model-ranking metric.

$$
\boxed{
QLIKE=
\frac1N\sum_{t=1}^{N}
\left(
\ln\hat h_t+\frac{y_t}{\hat h_t}
\right)
}
$$

Where:

$$
y_t=r_t^2
$$

Lower QLIKE indicates better conditional-variance forecasting performance on the evaluated sample.

QLIKE is calculated over chronological out-of-sample observations.

### Test 2 — RMSE

RMSE remains a secondary comparison metric.

$$
\boxed{
RMSE=
\sqrt{
\frac1N\sum_{t=1}^{N}
(\hat h_t-y_t)^2
}
}
$$

It measures squared-return proxy prediction errors.

Because daily squared returns are noisy and large shocks can dominate squared-error losses, RMSE should not independently determine model selection.

### Test 3 — Standardized Innovation Diagnostics

Calculate:

$$
\boxed{
Z_t^{obs}
=
\frac{r_t-\hat\mu_t}{\hat\sigma_t}
}
$$

Under the initial zero-mean assumption:

$$
\boxed{
Z_t^{obs}
=
\frac{r_t}{\sqrt{\hat h_t}}
}
$$

The standardized innovations provide an interpretable diagnostic of forecast calibration.

#### Required checks

**A. Mean and variance**

$$
\bar Z=\frac1N\sum_{t=1}^{N}Z_t^{obs}
$$

$$
\widehat{\operatorname{Var}}(Z)
=
\frac{1}{N-1}
\sum_{t=1}^{N}(Z_t^{obs}-\bar Z)^2
$$

Expected behavior under correct specification:

$$
\bar Z\approx0
$$

$$
\widehat{\operatorname{Var}}(Z)\approx1
$$

These are approximate statistical expectations, not hard acceptance bounds.

A nonzero mean may reflect sampling variation or misspecification of the conditional mean or volatility model.

A variance above one may suggest underestimated volatility; below one may suggest overestimated volatility.

**B. Remaining volatility clustering**

Examine the autocorrelation of squared standardized innovations:

$$
\operatorname{Corr}(Z_t^2,Z_{t-k}^2)
$$

Persistent clustering suggests that the volatility model has not fully captured predictable changes in return variance.

**C. Empirical distribution**

Plot the standardized innovations to inspect:

- Skewness and heavy tails.
- Extreme standardized shocks.
- Differences between instruments.
- Potential model calibration problems.

Normality is not required.

### Relationship to QLIKE

Since:

$$
Z_t^2=\frac{y_t}{\hat h_t}
$$

We can write:

$$
\boxed{
QLIKE=
\frac1N\sum_{t=1}^{N}
\left(
\ln\hat h_t+Z_t^2
\right)
}
$$

Thus, standardized innovations and QLIKE evaluate related aspects of the same forecasts.

The standardized innovation diagnostics provide interpretation; they are not a replacement for QLIKE.

## 6. Optional Empirical Return Intervals

Empirical return intervals are not required for the initial model comparison.

They may be investigated after the basic validation is complete.

Historical standardized innovations can provide empirical quantiles:

$$
q_{0.05}(Z),\qquad q_{0.95}(Z)
$$

For a next-day volatility forecast, a central 90% log-return interval can be constructed as:

$$
\left[
\hat\mu_{t+1}+\hat\sigma_{t+1}q_{0.05},
\;
\hat\mu_{t+1}+\hat\sigma_{t+1}q_{0.95}
\right]
$$

Quantiles must be estimated using historical calibration data and validated on later unseen observations.

This is an optional extension, not a completion requirement.

Monte Carlo simulation is not required.

## 7. Walk-Forward Evaluation

For each instrument and candidate model:

1. Fit or update the model using information available through day $t$.
2. Produce the next-day variance forecast $\hat h_{t+1}$.
3. Observe the actual return $r_{t+1}$ after the next close.
4. Calculate $y_{t+1}=r_{t+1}^2$.
5. Calculate QLIKE, RMSE contributions and standardized innovations.
6. Repeat over the out-of-sample evaluation period.

All models must be evaluated on comparable dates with consistent return definitions and forecast units.

Include simple rolling historical-volatility and/or EWMA forecasts as benchmarks.

Avoid selecting model configurations using the final evaluation sample.

## 8. Instrument Considerations

### BTCUSDT and ETHUSDT

- Use Bybit daily prices.
- Maintain consistent UTC daily boundaries.
- Forecast the next 24-hour close-to-close return uncertainty.

### QQQ

- Use official QQQ ETF daily closing prices.
- Forecast the next trading session's close-to-close return uncertainty.
- Close-to-close returns include the net effects of overnight, weekend and holiday price changes.

Model comparisons should be performed separately for each instrument.

Raw QLIKE and RMSE values should not be treated as directly comparable performance rankings across instruments with different return-variance scales.

## 9. Model Selection and Research Hurdle

The initial decision is based on:

| Criterion | Purpose |
| --- | --- |
| QLIKE | Primary forecast performance ranking |
| RMSE | Secondary variance-error comparison |
| Standardized innovation diagnostics | Forecast calibration and remaining clustering |
| Simple volatility benchmarks | Determine whether model complexity is justified |
| Stability across evaluation periods | Assess robustness |

The preferred model should be interpretable, reasonably calibrated and competitive out of sample.

There is no requirement for a single model to win across all instruments.

If complex volatility models provide little improvement over simple historical measurements, retaining the simpler representation is a legitimate research outcome.

A favorable QLIKE score does not automatically imply a profitable trading signal or useful P2 feature.

## 10. Feature Integration into P2

The candidate feature set may contain two categories.

### Current volatility

Examples:

- Normalized ATR.
- Rolling return standard deviation.
- Historical Yang–Zhang volatility.

### Forecast volatility

Examples:

- Next-day conditional return SD.
- Forecast variance.
- Relative change between current and forecast volatility, where definitions and scales are compatible.

These features describe volatility conditions and expectations.

They do not independently determine whether exposure should increase, decrease or remain unchanged.

The broader P2 model evaluates opportunity, downside risk and uncertainty using volatility alongside other information.

The incremental value of the volatility features must eventually be tested against P2 baselines, including their contribution beyond simpler features.

## 11. Reduced Deliverables

For each instrument and forecast model, produce:

1. **Forecast series:** next-day predicted variance or SD alongside actual daily returns.
2. **Performance table:** out-of-sample QLIKE and RMSE against simple baselines.
3. **Standardized innovation diagnostics:** mean, variance, distribution plot and squared-innovation autocorrelation.
4. **Research conclusion:** preferred volatility representation, or evidence that simpler alternatives are sufficient.

Optional extensions include empirical return intervals, regime-specific calibration, and intraday realized-variance analysis.

## 12. Completion Criteria

P2-f2 validation is complete when:

- The four candidate forecasts are aligned to the same next-day close-to-close variance target.
- Existing squared-return QLIKE and RMSE evaluation is completed.
- Standardized innovation diagnostics are available.
- Results are compared against simple volatility benchmarks.
- The preferred representation, or lack of convincing improvement, is documented.

Downstream P2 feature-value testing remains a separate stage.

---

## Final Research Decision

**Forecast target**

$$
\boxed{
\hat h_{t+1}
=
\widehat{\operatorname{Var}}(r_{t+1}\mid\mathcal F_t)
}
$$

**Observed validation target**

$$
\boxed{
y_{t+1}
=
\left(100\ln\frac{C_{t+1}}{C_t}\right)^2
}
$$

**Additional diagnostic**

$$
\boxed{
Z_{t+1}^{obs}
=
\frac{r_{t+1}}{\sqrt{\hat h_{t+1}}}
}
$$

| Component | Decision |
| --- | --- |
| Forecast models | HAR-YZ, GARCH, EGARCH, GJR-GARCH |
| Primary ranking | QLIKE |
| Secondary ranking | RMSE |
| Calibration diagnostics | Standardized innovations |
| Benchmarks | Rolling SD / EWMA |
| Empirical return intervals | Optional |
| Intraday realized variance | Not required |
| Monte Carlo | Not required |
| Role in P2 | Candidate volatility features, not trade authority |

**Guiding principle**

> Use the simplest credible representation of current and expected volatility. A more complex forecasting model must earn its place through measurable improvements, and even a statistically superior volatility forecast does not automatically justify changing market exposure.