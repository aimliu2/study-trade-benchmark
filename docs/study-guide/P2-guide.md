# Proj-AlgoTrade — P2 Objective Guide

**Date:** 2026-10-31
**Status:** Objective and conceptual signal defined; methodology not selected
**Phase:** P2 — Opportunity Inference & Dynamic Long Exposure

---

## 1. Ultimate objective

Develop a repeatable process for improving **net compounded wealth under acceptable risk**, using information available at each decision point.

P2 focuses on estimating opportunities and adjusting long exposure. It does not attempt to eliminate all uncertainty or guarantee profitable trades.

## 2. P1 findings

P1 compared Buy & Hold, monthly DCA, and EMA(12/26) long/cash switching across BTC, ETH, XAUT, and QQQ.

It demonstrated that exposure timing can materially change historical outcomes, but did not establish a sustainable timing advantage.

**P2 should aim to improve upon P1 through economically useful inference, rather than relying solely on historical indicator crossovers.**

P1 strategies remain the principal benchmarks.

## 3. P2 objective

> Determine the appropriate long exposure, from 0% to 100% of available portfolio capital, by estimating whether current market conditions justify increasing, maintaining, or reducing exposure relative to cash.

The system should continuously address three decisions:

- **Increase:** Is additional long exposure economically justified?
- **Maintain:** Is the current exposure still appropriate?
- **Reduce:** Is returning some or all capital to cash preferable?

Regular buying and selling are permitted. No fixed holding period or automatic liquidation deadline is assumed.

## 4. Conceptual opportunity signal

P2 requires a signal describing the **forward-looking attractiveness of holding an asset**, rather than simply measuring how far its price has already risen or fallen.

The signal should account for:

1. **Expected reward:** Potential future return from holding the asset.
2. **Downside risk:** Potential unfavorable outcomes.
3. **Uncertainty:** Confidence and limitations of the inference.
4. **Cash alternative:** Whether taking market exposure offers sufficient compensation relative to remaining uninvested.

An illustrative formulation is:

$$
S_t =
\mathbb{E}[R_{t,H}\mid I_t]
-
\lambda\,\operatorname{Risk}(R_{t,H}\mid I_t)
$$

Where:

- $S_t$: Estimated opportunity attractiveness.
- $I_t$: Information observable at decision time.
- $R_{t,H}$: Future return over horizon \(H\).
- $\lambda$: Risk-aversion parameter.

This is a conceptual expression, **not the selected model, loss function, or final trading signal**.

The forecast horizon, risk measure, probability estimation, and signal construction remain research choices.

The expected return should eventually be evaluated relative to the cash alternative, and the exposure decision must account for transaction costs.

### Signal interpretation

- **Increasing attractiveness:** Consider turning long exposure up.
- **Stable attractiveness:** Maintaining exposure may be appropriate.
- **Decreasing attractiveness:** Consider turning exposure down.

The signal does not directly dictate position size. A separate decision policy translates inference into exposure while accounting for capital, costs, risk limits, and the existing position.

## 5. Capital constraints

Initial research capital: approximately **$5,000 USD**.

The initial framework is spot-compatible, long-only, and unleveraged.

$$
0 \leq w_t \leq 1
$$

Where $w_t$ represents the fraction of current portfolio equity allocated to the asset.

- 0%: Fully in cash.
- 50%: Half invested, half in cash.
- 100%: Fully invested.

At 100%, further purchases require new capital or borrowing and are therefore outside the initial framework.

Cash is a valid allocation and the simplest means of reducing directional exposure.

## 6. Minimum and maximum capabilities of P2

### Minimum capability — Useful opportunity discrimination

At minimum, the signal should demonstrate that it can distinguish relatively favorable from unfavorable conditions for long exposure better than an appropriate uninformed baseline.

Its information should produce economically meaningful exposure decisions after realistic transaction costs.

A signal that cannot improve decisions relative to simple alternatives has not established sufficient value for deployment.

### Maximum standalone capability — Adaptive long exposure

Within its defined scope, P2 may:

- Identify favorable opportunities to accumulate exposure.
- Reduce exposure ahead of some unfavorable market periods.
- Maintain exposure through sustained favorable conditions.
- Adapt position sizing as expected reward and risk change.
- Improve net compounded performance or the return–risk trade-off compared with P1.

However, P2 cannot:

- Reliably identify every exact market bottom or top.
- Guarantee positive returns.
- Prevent every drawdown.
- Profit directly from falling prices while fully in cash.
- Exceed 100% long exposure without leverage.
- Eliminate prediction error, market uncertainty, or unexpected events.

These limitations are inherent to the initial long/cash framework.

## 7. Relationship to hedging

P2's signal is not expected to predict every market movement correctly.

Its first defense against unfavorable outcomes is appropriate exposure sizing, including reducing exposure to cash.

**Hedging is a separate risk-management layer**, potentially introduced in later research.

Hedging may offset specific residual risks that cannot be adequately managed through exposure reduction alone, but introduces costs, complexity, and additional exposures.

Hedging does not manufacture alpha or guarantee protection against all prediction errors.

P2's standalone performance should be evaluated before attributing benefits to a hedging overlay.

## 8. Forecasting and labeling remain undecided

The earlier triple-barrier approach was designed around predetermined trade outcomes.

P2 instead investigates recurring capital-allocation decisions, which may not require fixed TP, SL, or timeout rules.

Candidate prediction targets include:

- Conditional future return distributions.
- Expected upside and downside.
- Favorable and adverse price excursions.
- Turning-point probabilities.
- Barrier-hit probabilities.
- Expected value of holding versus waiting or selling.

The previous 1–3-day horizon is not automatically retained. A seven-day horizon is only a possible experiment.

GRU, LSTM, CNN, stochastic models, statistical approaches, and other methods remain available.

**The objective and signal requirements must be established before selecting a method.**

## 9. Performance expectations and validation

**P2 is expected to demonstrate incremental economic value beyond P1.**

Benchmarks include:

- Buy & Hold.
- DCA.
- EMA(12/26).
- Cash.
- Constant fractional exposure.
- Appropriate risk-matched alternatives.

Evaluate:

- Net compounded growth.
- Maximum drawdown and downside risk.
- Sharpe/Sortino and other risk-adjusted measures.
- Transaction costs and turnover.
- Capital efficiency.
- Performance across assets and market regimes.
- Out-of-sample robustness.

### Research success

P2 succeeds when its inference-driven exposure decisions demonstrate a credible, repeatable economic improvement over appropriate simple benchmarks, after costs and with comparable risk.

Outperforming P1 on a single historical period is insufficient.

A lower-risk strategy may have lower absolute returns while still providing valuable risk-adjusted improvement. Such results must be distinguished from genuine benchmark-relative alpha.

### Research failure

If P2 cannot demonstrate incremental value, its added complexity is not justified.

The appropriate response is to revise or reject the hypothesis, rather than automatically increase model complexity.

## 10. Research boundaries

**Defined:**

- Objective: Net compounded wealth under acceptable risk.
- Signal concept: Forward-looking opportunity attractiveness.
- Decision: Increase, maintain, or reduce long exposure.
- Capital range: 0–100%.
- P1: Benchmark and minimum economic hurdle.
- Hedging: Separate future layer.

**Undecided:**

- Forecast target.
- Forecast horizon.
- Signal estimation method.
- Features and data sources.
- Decision frequency.
- Signal-to-exposure mapping.
- Risk constraints and rebalancing thresholds.
- Statistical and economic acceptance criteria.

## 11. Next research question

> What should P2 estimate about future market outcomes so that its signal can justify increasing, maintaining, or reducing exposure more effectively than the P1 baselines?

Only then should the research choose the labeling method, forecast architecture, and decision policy.

---

**Guiding principle**

P2 should estimate opportunities as accurately as practical, recognize its uncertainty, and convert useful information into better capital-exposure decisions.

Its standalone value must be demonstrated before introducing hedging, leverage, or complex derivative structures.

**Inference → Exposure decision → Net economic validation → Additional risk management when justified.**
