# Proj-AlgoTrade — P2-M1 Research Handoff

**Date:** 2026-10-31  
**Phase:** P2 — Opportunity Inference & Dynamic Long Exposure  
**Milestone:** M1 — Market Memory & Feature Research  
**Status:** Research hypothesis defined; methodology and empirical validation pending

---

## 1. Parent objective — P2

Develop a repeatable process for improving **net compounded wealth under acceptable risk** through information-driven long exposure allocation.

P2 adjusts exposure between 0% and 100% of available portfolio capital.

The system must eventually determine whether to:

- Increase exposure.
- Maintain existing exposure.
- Reduce exposure toward cash.

The opportunity signal should consider expected reward, downside risk, uncertainty, and the cash alternative.

**P1 remains the economic benchmark**, including Buy & Hold, DCA, EMA(12/26), cash, and appropriate risk-matched alternatives.

P2 must ultimately demonstrate credible incremental economic value after costs. Predictive improvement alone is insufficient for deployment.

Hedging, leverage, and derivative overlays remain outside the initial P2 scope.

## 2. M1 research philosophy

### Market efficiency assumption

For globally traded assets such as BTC, ETH, gold, and QQQ, the working assumption is that market prices already incorporate substantial publicly available information.

Different assets have different fundamental return drivers:

- QQQ represents ownership in cash-flow-generating businesses.
- Gold and BTC do not generate intrinsic cash flows.
- USD-denominated prices also respond to monetary conditions, supply, demand, and changes in the value of the dollar.

However, **independent fundamental valuation is outside the initial research scope**.

M1 instead investigates information contained in observable market history and price behavior.

Market efficiency is a working assumption, not a claim that historical prices must contain exploitable predictive signals.

### From absolute valuation to relative valuation

Rather than attempting to determine an asset's intrinsic fair value or identify exact tops and bottoms, investigate:

> Is the asset currently relatively cheap or expensive compared with its own historical market memory?

This is a statistical description, not a claim of fundamental mispricing.

Relative cheapness does not necessarily imply an attractive buying opportunity. An asset can remain relatively cheap while continuing to decline.

Likewise, relative expensiveness does not necessarily imply that a decline is imminent.

## 3. M1 feature hypothesis — H1

**H1: Fractional-memory relative valuation**

> A stationary, fractionally differentiated price series, standardized against a historical reference, contains incremental information about future market outcomes that conventional price and momentum features may not capture.

The proposed feature uses fractional differentiation (`fracdiff`) to retain potentially useful historical dependence while reducing nonstationarity.

It is intended to represent relative historical price location or displacement, rather than provide an independent trading signal.

**Critical boundary: Fracdiff is one candidate feature, not the authority controlling portfolio exposure.**

## 4. Proposed feature construction

### Step 1 — Price transformation

Begin with a candidate price representation, such as log price:

\[
X_t=\log(P_t)
\]

The exact input representation remains subject to testing.

### Step 2 — Fractional differentiation

Apply:

\[
Y_t=(1-B)^dX_t
\]

Where:

- \(B\): Backshift operator.
- \(d\): Fractional differencing order.
- \(Y_t\): Fractionally differentiated series.

The intended objective is to select a differencing order that sufficiently reduces nonstationarity while preserving useful historical memory.

The choice of \(d\), weight truncation, and memory length remains open.

The earlier reference to `T=4,5` has not been formally resolved as a specific parameter definition.

### Step 3 — Stationarity validation

Evaluate whether the transformed series is sufficiently stationary for the proposed historical-reference interpretation.

Potential diagnostics include ADF, KPSS, and examination of distribution stability.

Passing a stationarity test does not prove that the original asset price is mean-reverting.

Stationarity must not be interpreted as evidence of a guaranteed price recovery.

### Step 4 — Historical Z-score

Standardize the fractionally differentiated series against a historical reference beginning at a selected anchor year.

\[
Z_t^{FD}=
\frac{Y_t-\mu_{\mathrm{ref},t}}
{\sigma_{\mathrm{ref},t}}
\]

A causal reference should use information available before the decision point.

Two reference methods remain available:

- Fixed calibration reference.
- Expanding historical reference from a selected anchor year.

The anchor year, reference method, and minimum calibration history have not been selected.

### Step 5 — Descriptive interpretation

| Feature state | Working interpretation |
|---|---|
| \(Z_t^{FD}<0\) | Relatively cheap against historical memory |
| \(Z_t^{FD}\approx0\) | Near historical reference |
| \(Z_t^{FD}>0\) | Relatively expensive against historical memory |

These are descriptive labels only.

They do not establish intrinsic undervaluation, overvaluation, or future expected returns.

## 5. Important observed limitation

During conceptual exploration, the user observed that the fracdiff Z-score could remain around −1 for an extended period while the underlying price continued declining.

This illustrates an important limitation:

**A stationary transformed series does not imply that the original price will return to its previous level.**

A persistently negative Z-score may simply describe continuing market weakness.

Even a recovery in the transformed Z-score does not necessarily require the underlying price to appreciate.

Therefore, the following interpretation is explicitly rejected:

\[
Z_t^{FD}<0
\;\not\Rightarrow\;
\text{Buy}
\]

Similarly:

\[
Z_t^{FD}>0
\;\not\Rightarrow\;
\text{Sell}
\]

The feature may describe market conditions without providing actionable predictive information.

Its economic relevance must be tested.

## 6. Relationship to RSI and other features

RSI measures recent relative upward and downward price movements.

Fracdiff Z-score attempts to describe price displacement relative to a longer historical-memory reference.

They may capture different aspects of market behavior.

However, a more sophisticated transformation does not automatically produce a more informative feature.

**The objective is not to prove that fracdiff is universally superior to RSI.**

Instead, test whether fracdiff contributes incremental information beyond conventional features.

Possible comparisons include:

- Ordinary returns.
- Momentum.
- RSI.
- Moving-average deviation.
- Volatility.
- Fractionally differentiated price representations.

These are candidates, not a finalized feature set.

## 7. Proposed validation framework

### Stage A — Validate the representation

Construct and examine the feature before introducing complex predictive models.

Investigate:

1. Fractional differencing order and stationarity.
2. Historical memory retention.
3. Sensitivity to weight truncation.
4. Anchor-year and normalization choices.
5. Stability across different market regimes.
6. Behavior during sustained appreciation, declines, and sideways periods.
7. Causal calculation without future-data leakage.

Plot the original price, fractionally differentiated series, and Z-score to examine their relationships.

#### Practical check — Does \(d\) hold over time?

A \(d\) that passes ADF on the full sample may not hold in every sub-period. Full-sample tests average across regimes.

Run ADF and track the FFD mean and standard deviation on a **rolling one-year window**, using the same ADF settings. Then diagnose which component failed:

| Observation in a period | Meaning | Response |
|---|---|---|
| FFD itself fails ADF (trends, does not revert) | \(d\) too low for this regime; too much memory retained | Raise \(d\), re-selected walk-forward on past data only |
| FFD passes ADF but its level or spread shifts (e.g. Z stuck near −1) | Feature is stationary but its center moved; Z reference is stale | Change the Z reference: new anchor, expanding or rolling window |

Notes:

- The anchor belongs only to the Z-score. FFD has no anchor; each value uses only its own fixed lag window.
- Changing \(d\) changes the feature's scale and meaning; Z-scores before and after a change are not comparable. Re-select on a fixed schedule, not in reaction to charts.
- One-year windows (~200–250 daily bars) give ADF low power; a failure on a short window may reflect limited data rather than a unit root.

### Stage B — Evaluate predictive information

Investigate whether the feature contains useful information about subsequent market outcomes.

An initial comparison can use identical forecasting methods:

\[
\begin{aligned}
M_0 &: \text{Baseline features}\\
M_1 &: \text{Baseline features}+Z_t^{FD}
\end{aligned}
\]

Compare out-of-sample performance to isolate the incremental contribution of fracdiff.

Potential targets include:

- Conditional future returns.
- Future return distributions.
- Downside risk.
- Favorable and adverse price excursions.
- Other opportunity-relevant outcomes.

The forecast target and horizon have not yet been selected.

A simple exploratory test may group observations by Z-score and compare subsequent return distributions.

However, any observed relationship must be validated out of sample and assessed for regime dependence, statistical uncertainty, and overlapping observations.

### Stage C — Economic relevance

If the feature improves inference, investigate whether that improvement produces better exposure decisions.

This stage belongs to the broader P2 decision-policy and economic-validation process.

A feature is not economically validated merely because it passes a stationarity test or improves an isolated forecasting metric.

Its contribution must eventually survive realistic costs, turnover, risk constraints, and comparison against P1.

## 8. Research safeguards

- No future information may enter feature construction, normalization, parameter selection, or model training.
- Fractional differencing and stationarity settings must be selected using training data only.
- Distinguish statistical stationarity from economic mean reversion.
- Distinguish descriptive market states from predictive opportunity.
- Account for temporal dependence and overlapping forecast horizons during validation.
- Do not assume negative Z implies positive future returns.
- Do not assume positive Z implies negative future returns.
- Avoid selecting features solely because they look convincing on historical charts.
- Reject or revise H1 if it fails to demonstrate incremental information.

## 9. Scope and unresolved decisions

**Established:**

- M1 investigates market-memory representations.
- Fracdiff Z-score is the first explicit feature hypothesis.
- Relative valuation means statistical comparison against historical memory.
- Fundamental fair-value estimation is excluded from initial M1 research.
- Fracdiff is not an independent trading rule.
- Predictive usefulness and economic usefulness require separate validation.
- The ultimate P2 objective and P1 benchmarks remain unchanged.

**Undecided:**

- Input price representation.
- Fractional differencing order \(d\).
- Exact meaning and setting of `T=4,5`.
- Memory length and weight truncation.
- Stationarity acceptance criteria.
- Anchor year.
- Fixed versus expanding Z-score reference.
- Feature sampling timeframe.
- Forecast target and horizon.
- Baseline feature set.
- Statistical acceptance thresholds.
- Model architecture.
- Exposure decision policy.

No GRU, LSTM, CNN, or other forecasting architecture has been selected.

## 10. Immediate next research task

**Construct and inspect the fractional-memory feature before attempting to use it for prediction.**

The initial research sequence is:

1. Define the input series and fractional differencing configuration.
2. Construct the fracdiff series.
3. Test stationarity and inspect memory retention, including the rolling one-year check of whether \(d\) holds over time (Stage A).
4. Construct the historical Z-score.
5. Plot price, fracdiff, and Z-score together.
6. Investigate the empirical relationship between Z-score states and subsequent returns.
7. Determine whether the feature deserves further predictive testing.

The research should not assume success before examining the evidence.

---

## Guiding principle

**Market memory is information, not an instruction.**

A low relative price does not necessarily imply an opportunity, and a high relative price does not necessarily imply danger.

M1 investigates whether fractional-memory representations help characterize future market outcomes more effectively than conventional features.

Only demonstrated predictive information should advance toward P2's opportunity signal and eventual exposure decision policy.

**Market history → Feature representation → Empirical validation → Opportunity inference → Exposure decision → Economic validation.**