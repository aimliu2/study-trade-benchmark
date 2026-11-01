# P2-f2 — Volatility Representation & Forecasting
**Research Guideline / Handoff**

**Project:** Proj-AlgoTrade  
**Phase:** P2 — Feature Research  
**Feature:** f2 — Volatility  
**Status:** Research design agreed; implementation and validation pending  
**Primary timeframe:** 1D  
**Initial universe:** BTCUSDT, ETHUSDT, QQQ

---

## 1. Research Objective

P2-f2 aims to identify a practical, reliable volatility representation for the P2 **top/bottom opportunity model**.

The objective is to estimate the scale and evolution of market volatility, providing context for future price excursions and risk.

The feature should help answer:

- How volatile is the market currently?
- How much volatility should we expect over the next trading day?
- Does volatility respond differently to positive and negative return shocks?
- Which representation performs most reliably out of sample?

**P2-f2 is not an exposure controller or a directional trading signal.**

High volatility does not automatically imply a top or bottom. The feature will eventually be evaluated for its incremental usefulness in the broader P2 model.

## 2. Research Scope

The initial study is deliberately limited to four candidate forecasting models.

| Model | Research purpose |
|---|---|
| HAR-YZ | Multi-horizon persistence of Yang–Zhang volatility |
| GARCH(1,1) | Symmetric conditional-volatility forecasting |
| EGARCH(1,1) | Asymmetric volatility response using log variance |
| GJR-GARCH(1,1) | Asymmetric volatility response using a negative-shock indicator |

These four candidates are sufficient for the initial comparison.

**Deferred:** Realized GARCH, HAR-GARCH hybrids, HAR-CJ, neural-network ensembles and more elaborate volatility architectures.

Additional complexity must be justified by measurable out-of-sample improvement.

## 3. Volatility Measurement

### 3.1 Yang–Zhang as the starting representation

Yang–Zhang (YZ) is the original preferred historical volatility estimator.

It uses daily OHLC observations and explicitly accounts for overnight price gaps.

This makes it particularly suitable for QQQ, where the market does not trade continuously.

YZ is a historical estimator, not itself a next-day forecast.

### 3.2 HAR-YZ

Apply a heterogeneous autoregressive structure to the YZ volatility series.

Conceptually:

$$
\hat{\sigma}_{t+1}^{YZ}
=
\beta_0+
\beta_d\sigma_t^{YZ}+
\beta_w\overline{\sigma}_{t,5}^{YZ}+
\beta_m\overline{\sigma}_{t,22}^{YZ}
$$

The daily, weekly and monthly components represent different persistence horizons.

**Implementation caution:** Rolling YZ estimates already aggregate multiple days. Their overlap can make HAR predictors redundant or overly smooth. This must be considered when choosing the YZ estimation window.

HAR-YZ is a custom HAR-style application, not automatically equivalent to the original HAR-RV model.

### 3.3 GARCH family

All three GARCH candidates use daily returns to estimate conditional variance.

**GARCH(1,1)**

$$
h_t=\omega+\alpha\varepsilon_{t-1}^2+\beta h_{t-1}
$$

**EGARCH(1,1)**

$$
\ln h_t=
\omega+\beta\ln h_{t-1}
+\alpha(|z_{t-1}|-E|z|)
+\gamma z_{t-1}
$$

**GJR-GARCH(1,1)**

$$
h_t=
\omega+\alpha\varepsilon_{t-1}^2
+\gamma I_{t-1}\varepsilon_{t-1}^2
+\beta h_{t-1}
$$

Here \(h_t=\sigma_t^2\), \(z_t=\varepsilon_t/\sqrt{h_t}\), and \(I_t=1\) for negative shocks.

The research question for EGARCH and GJR-GARCH is whether modeling return-shock asymmetry improves forecasting over standard GARCH.

No assumption is made that asymmetry must be identical across QQQ, BTC and ETH.

## 4. Market Data and Session Handling

| Instrument | Primary data | Market structure |
|---|---|---|
| BTCUSDT | Bybit OHLCV | Continuous 24/7 |
| ETHUSDT | Bybit OHLCV | Continuous 24/7 |
| QQQ | Official ETF OHLCV via Databento | Regular session plus overnight gaps |

For BTC and ETH, daily bars should use a consistent 24-hour boundary.

For QQQ, daily close-to-close returns include overnight price changes. Yang–Zhang also explicitly incorporates the overnight component.

Intraday realized variance is **not mandatory** for this study.

If realized variance is later introduced as a validation target, QQQ's regular-session variance and overnight variance must be handled consistently. Forward-filled missing minute bars must not be mistaken for newly observed market activity.

## 5. Forecasting Target

**Primary forecast horizon: one completed trading day ahead.**

At the close of day \(t\), estimate volatility for day \(t+1\), using only information available by the forecast timestamp.

All four candidates must produce comparable forecasts in consistent units.

Two representations should be retained:

- Forecast variance: \(\hat h_{t+1}\)
- Forecast volatility: \(\hat\sigma_{t+1}=\sqrt{\hat h_{t+1}}\)

HAR-YZ forecasts must be transformed consistently if the model is fitted to volatility rather than variance.

**Critical validation requirement:** A rolling YZ estimate is not the same target as next-day conditional return variance. Do not compare models against different targets and declare a winner.

The exact common realized-variance proxy must be defined before implementation. Possible choices include squared daily close-to-close returns or a higher-frequency variance proxy with appropriate session handling.

## 6. Out-of-Sample Validation

Use chronological, walk-forward validation.

Random train/test splitting is not appropriate for this time-series study.

### Primary metrics

**RMSE**

$$
RMSE=
\sqrt{\frac1N\sum_{t=1}^{N}
(\hat h_t-RV_t)^2}
$$

Measures variance forecast error, with larger errors receiving greater penalties.

If reporting RMSE in volatility units, apply the square root consistently to both forecasts and observations.

**QLIKE**

$$
QLIKE=
\frac1N\sum_{t=1}^{N}
\left(
\ln\hat h_t+\frac{RV_t}{\hat h_t}
\right)
$$

Measures conditional-variance forecast quality. Lower is better.

Forecast variances must be strictly positive.

### Additional benchmark

Include a naïve persistence forecast, such as carrying forward the latest available volatility estimate.

A sophisticated model should demonstrate improvement over this simple alternative.

### Evaluation requirements

1. Same instrument, evaluation dates and forecast horizon.
2. Same common realized-variance target.
3. No future information in rolling estimators or forecast inputs.
4. Chronological training and testing.
5. Report RMSE and QLIKE separately for BTC, ETH and QQQ.
6. Inspect forecast stability and behavior during volatility shocks.

A single overall ranking across instruments is not required.

## 7. Visualization Deliverables

For each instrument, produce:

- Historical Yang–Zhang volatility plot.
- One-day-ahead forecast series for the four candidates.
- Observed volatility proxy for comparison.
- Forecast-error plots or diagnostics.
- Out-of-sample RMSE and QLIKE comparison table.

Use consistent units, clear forecast timestamps and an explicit distinction between historical estimates and forward forecasts.

The plot should make it possible to inspect volatility clustering, shock responses, persistence and forecast lag.

## 8. Model Selection

Prefer the simplest method that demonstrates reliable out-of-sample performance.

Selection criteria:

- Forecast accuracy.
- QLIKE performance.
- Stability across different market regimes.
- Robustness across evaluation windows.
- Implementation and maintenance complexity.

EGARCH and GJR-GARCH should only be preferred over GARCH if their additional asymmetry mechanism provides useful evidence of improvement.

HAR-YZ should only be preferred if its multi-horizon information adds predictive value.

**There is no requirement that one model must win for all three instruments.**

If the four candidates perform similarly, prefer the simpler or more stable representation.

## 9. Relationship to P2

P2-f2 produces volatility features, not buy/sell instructions.

Potential downstream applications include normalizing future price excursions, describing volatility regimes and improving estimates of future MAE/MFE distributions.

The broader P2 opportunity model will separately determine whether the volatility representation improves top/bottom forecasting.

A strong volatility forecast is not, by itself, proof of a profitable trading edge.

## 10. Future Intraday Extension

Once the daily study is complete, investigate intraday volatility forecasting.

Suggested progression:

1. Intraday realized volatility and HAR-RV.
2. HAR-CJ for continuous versus jump variation.
3. Realized GARCH or hybrid approaches, only if justified.

The intraday extension must account for information availability at each forecast timestamp and QQQ's session structure.

Daily and intraday models may coexist; the decision timeframe does not have to equal the data sampling frequency.

## 11. Research Completion Criteria

P2-f2 is complete when:

- All four models have been implemented consistently.
- The common validation target has been defined.
- Walk-forward out-of-sample RMSE and QLIKE have been calculated.
- Forecasts and observations have been plotted.
- A preferred volatility representation has been selected for each instrument, or the evidence has been judged inconclusive.
- The selected representation is ready to be passed to the broader P2 feature pipeline.

**Research conclusion must be evidence-based.** A more complex model is not automatically a better model.

---

## Final Research Decision

**Current scope**

$$
\boxed{
\text{HAR-YZ,\ GARCH,\ EGARCH,\ GJR-GARCH}
}
$$

**Validation**

$$
\boxed{
\text{Walk-forward OOS RMSE + QLIKE}
}
$$

**Primary timeframe:** 1D

**Initial universe:** BTCUSDT, ETHUSDT, QQQ

**Objective:** Select a useful volatility representation for P2 top/bottom research.

**Out of scope:** Exposure decisions, hedging, execution logic and hybrid volatility architectures.

### Research references

- *Predicting the Volatility of Cryptocurrencies’ Returns Using High-Frequency Data* — supplied research paper, `4-crypto-on-garch-har.pdf`.
- Original volatility research conversation — [GARCH volatility chat](https://app.notion.com/p/85608820937383a9859e8121c2ac4ffd).
- Follow-up research — [HAR-GARCH discussion](https://app.notion.com/p/40808820937380fe95d7f6f9bf6eb8f6).

**Next action:** Define the common realized-variance target and YZ window construction before implementing the four-model comparison.