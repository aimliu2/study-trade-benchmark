# P1 — Strategy Baseline Study
**Status:** Ready for research  
**Universe:** BTCUSDT, ETHUSDT, XAUTUSDT, QQQ  
**Timeframe:** 1D (daily candles)

## 1. Research objective

Determine whether a simple active Buy/Sell strategy provides meaningful economic value compared with passive Buy & Hold and DCA.

The study should answer:

- Does active trading outperform passive exposure?
- Does it reduce drawdown or improve risk-adjusted performance?
- Does the advantage survive transaction costs, funding, and other deployment expenses?
- Is the strategy practical to deploy with available capital and execution infrastructure?

The objective is **deployable economic value**, not simply predictive accuracy.

## 2. Initial instrument universe

| Asset | Primary deployment | Execution |
|---|---|---|
| BTCUSDT | Bybit | Automated |
| ETHUSDT | Bybit | Automated |
| XAUTUSDT | Bybit, subject to instrument verification | Automated if supported |
| QQQ | InnovestX, actual ETF | Semi-automatic |

All four assets will initially use **1D candles**.

Use the available historical data for each instrument. Compare strategies over identical dates within each asset; cross-asset comparisons should disclose differences in history length.

Keep venue-specific assumptions separate from the underlying strategy logic.

## 3. Strategies to benchmark

| Strategy | Description |
|---|---|
| S0 — Buy & Hold | Purchase at the beginning and hold |
| S1 — DCA | Gradually invest initial capital on a fixed schedule |
| S2 — EMA + MACD | Buy and sell according to technical signals |

### S0 — Buy & Hold

- Invest the allocated capital at the start.
- Hold until the evaluation period ends.
- Include relevant distributions and holding costs.

### S1 — DCA

- Use the same initial capital as S0.
- Divide it into periodic purchases.
- Keep uninvested capital in cash.
- No additional external contributions.

### S2 — EMA + MACD

Initial candidate:

- EMA(12), EMA(26)
- MACD(12, 26, 9)
- Buy when MACD crosses above its signal line and EMA12 > EMA26.
- Sell when MACD crosses below its signal line or EMA12 < EMA26.
- Long or cash only; no leverage or shorting.

Treat these rules as an initial specification, not optimized parameters.

Evaluate signals on completed daily candles and execute no earlier than the next available trading opportunity.

## 4. Economic evaluation

Apply the same initial capital, test period, and accounting conventions within each asset.

**Return**
- Terminal portfolio value
- Net return and CAGR
- Excess return relative to Buy & Hold and DCA

**Risk**
- Maximum drawdown
- Return volatility
- Risk-adjusted performance

**Deployment**
- Transaction fees
- Spread and slippage
- Funding costs where applicable
- Dividends or distributions where applicable
- Turnover and trading frequency
- Idle cash and position-sizing constraints

Report both **gross strategy performance** and **net deployable performance**.

Do not treat a strategy as superior solely because it achieves a higher gross return.

## 5. Instrument-specific constraints

### Crypto — Bybit

- BTCUSDT and ETHUSDT are the established initial Bybit research instruments.
- XAUTUSDT is included in the expanded baseline universe, subject to confirming its available market type and history.
- Distinguish spot and perpetual contracts.
- Apply funding only to instruments and periods where funding actually exists.
- Preserve instrument-specific fees, minimum order quantities and historical data availability.

### QQQ — InnovestX

Verified account capabilities:

- Actual ETF ownership.
- Fractional shares available.
- Minimum order approximately $10 or 0.0001 shares, subject to platform conditions.
- Manual execution is available.
- TradingView connection exists, but automated order routing is unverified.

**Deployment classification: Semi-automatic.**

Use QQQ price data for signal research, and account for dividends when measuring the economic return of actual ETF ownership.

### Thai mutual fund — Alternative only

K-USXNDQ-A(D) remains a possible passive investment alternative, but is not required for the initial baseline.

Its master fund is QQQM, with substantial currency hedging, fund expenses, and daily-NAV execution constraints.

Do not substitute its THB NAV returns directly for QQQ's USD returns.

## 6. Research controls

- No look-ahead bias.
- No execution on an unfinished daily candle.
- No assumed fills at unavailable prices.
- No free dividends, funding income, or frictionless trading.
- Keep missing data and proxy instruments explicitly documented.
- Avoid parameter optimization in the first baseline run.
- Compare strategies under consistent capital assumptions.
- Separate strategy performance from instrument and execution effects.

Where actual execution is unavailable, report a theoretical result separately rather than presenting it as deployable.

## 7. P1 execution sequence

1. **Data readiness:** Verify daily OHLC data, corporate actions where relevant, and instrument-specific costs.
2. **Passive benchmarks:** Run Buy & Hold and DCA.
3. **Active candidate:** Run EMA + MACD without optimization.
4. **Economic accounting:** Add fees, funding, dividends, slippage and cash balances.
5. **Comparison:** Evaluate net return, drawdown, risk-adjusted performance and turnover.
6. **Deployment verdict:** Identify which strategies are economically worthwhile and executable.

## 8. Decisions still open

- DCA purchase interval and deployment horizon.
- Exact treatment of cash interest and dividend reinvestment.
- Spot versus perpetual contract selection for each Bybit instrument.
- QQQ dividend and execution-price data sources.
- Exact execution and cost assumptions.

These decisions should be fixed before running the benchmark, not selected after observing results.

## 9. Completion criterion

P1 is complete when each of the four assets has:

- Buy & Hold results.
- DCA results.
- EMA + MACD results.
- Gross and net economic comparisons.
- Risk and drawdown comparisons.
- A clear deployment feasibility assessment.

**P1 is a baseline, not an optimization exercise.**

The outcome may be that Buy & Hold or DCA is superior. That is a valid research result and becomes the hurdle future strategies must overcome.
