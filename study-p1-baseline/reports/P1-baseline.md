# P1 report — Buy & Hold vs DCA vs EMA 12/26

**Date:** 2026-10-31
**Scope:** S0 Buy & Hold, S1 DCA, S2 EMA 12/26 cross; BTC / ETH / XAUT / QQQ, 1D bars, 2026-01-01 → 2026-09-30 (9 months)
**Type:** Exposure experiment, gross. It measures what holding (or switching) each asset did, not a deployable edge.

## Setup

| | Buy & Hold (S0) | DCA (S1) | EMA 12/26 (S2) |
|---|---|---|---|
| Capital | $900 | $900 | $900 |
| Entry | All at the first available open of 2026 | $100 at each month's first open, Jan–Sep (9 buys) | All at the first available open of 2026, regardless of trend |
| Switching | None | None | Sell everything at the next open after EMA 12 crosses below EMA 26; buy back with all cash at the next open after it crosses above. Signals that don't change the position are ignored |
| End | Marked at the 2026-09-30 close | Marked at the 2026-09-30 close | Any open position marked at the 2026-09-30 close |

Zero fees, spread and slippage; uninvested cash earns 0%; QQQ dividends excluded. XAUT uses XAUUSD (see [README](../README.md)). EMAs warm up from 2025 Q4.
S2 here is the EMA cross alone; the study guide's MACD filter is not applied yet.
Notebooks: [buy-hold-1d.ipynb](../buy-hold-1d.ipynb), [dca-1d.ipynb](../dca-1d.ipynb), [ema-signals-1d.ipynb](../ema-signals-1d.ipynb), [ema-trades-1d.ipynb](../ema-trades-1d.ipynb).

## Results

| Asset | Buy & Hold | DCA | EMA 12/26 |
|---|---|---|---|
| BTC | $858.65 (−4.6%), max DD −39.5% | **$1,053.92 (+17.1%)**, −18.7% | $1,007.18 (+11.9%), −18.0% |
| ETH | $813.39 (−9.6%), −53.3% | **$1,140.75 (+26.8%)**, −21.7% | $1,102.20 (+22.5%), −28.2% |
| XAUT | $866.40 (−3.7%), −26.6% | $830.44 (−7.7%), −13.6% | **$981.52 (+9.1%)**, −14.2% |
| QQQ | **$1,077.24 (+19.7%)**, −12.2% | $1,016.64 (+13.0%), −8.4% | $982.30 (+9.1%), −9.6% |

| Asset | EMA trades | Winners | Time in market | DCA avg cost vs first open |
|---|---|---|---|---|
| BTC | 7 | 3 | 52% | 71,404.78 vs 87,643.30 |
| ETH | 4 | 1 | 56% | 2,118.82 vs 2,971.58 |
| XAUT | 2 | 2 | 43% | 4,505.20 vs 4,318.21 |
| QQQ | 4 | 2 | 66% | 657.56 vs 620.57 |

DCA drawdown is measured on total equity (holdings + idle cash), so it is lower partly because less money was exposed.

## Findings

### 1. No method won everywhere; the price path decided

DCA wins exactly when its average cost lands below the first open. BTC and ETH fell after January, so later buys lowered the cost; gold peaked in Feb–Mar and QQQ rose from May, so later buys raised it. EMA beat Buy & Hold on the three assets that ended lower and lost to it on the one that trended up (QQQ). Each choice is a bet on the path, made before the path is known.

### 2. Entry timing dominates the outcome

Buy & Hold return to 2026-09-30, depending only on which day in the window the single buy happened:

| Asset | Worst entry | Best entry | Spread |
|---|---|---|---|
| BTC | −13.8% (01-15) | +42.6% (07-01) | 56 pts |
| ETH | −19.9% (01-15) | +71.3% (06-26) | 91 pts |
| XAUT | −23.3% (01-29) | +4.6% (07-17) | 28 pts |
| QQQ | −0.6% (09-23) | +31.7% (03-31) | 32 pts |

The entry-day spread is larger than the whole gap between any two methods for every asset. DCA does not remove timing risk; it spreads it across nine fixed dates, which is why it can still lose (gold) or lag (QQQ).

### 3. Why EMA changes the result: every exit is a sell-high / buy-back bet

EMA and Buy & Hold enter at the same price and hold the same units while EMA is invested, so their results differ **only during the periods EMA sits in cash**. Each cash period multiplies EMA's result relative to Buy & Hold by exactly *(sell price ÷ buy-back price)*. Multiplying these factors reproduces EMA ÷ Buy & Hold exactly for all four assets.

| Asset | Cash period | Days | Price sell → buy back | Effect vs Buy & Hold |
|---|---|---|---|---|
| BTC | 01-25 → 03-16 | 50 | 89,227.70 → 72,812.40 | **+22.5%** |
| BTC | 03-23 → 03-24 | 1 | 67,862.00 → 70,898.70 | −4.3% |
| BTC | 03-27 → 04-10 | 14 | 68,820.10 → 71,788.90 | −4.1% |
| BTC | 05-23 → 07-16 | 54 | 75,540.30 → 64,756.40 | **+16.7%** |
| BTC | 08-02 → 08-07 | 5 | 62,823.30 → 64,320.40 | −2.3% |
| BTC | 08-13 → 08-20 | 7 | 63,482.90 → 69,338.40 | −8.4% |
| ETH | 01-23 → 03-17 | 53 | 2,952.66 → 2,352.58 | **+25.5%** |
| ETH | 03-28 → 04-08 | 11 | 1,992.70 → 2,240.10 | −11.0% |
| ETH | 05-17 → 07-11 | 55 | 2,180.96 → 1,796.91 | **+21.4%** |
| XAUT | 03-20 → 08-07 | 140 | 4,650.29 → 4,241.17 | **+9.6%** |
| XAUT | 09-16 → 09-30* | 14 | 4,295.03 → 4,156.99 | +3.3% |
| QQQ | 02-06 → 04-13 | 66 | 596.00 → 606.69 | −1.8% |
| QQQ | 07-17 → 08-10 | 24 | 693.48 → 725.99 | −4.5% |
| QQQ | 09-15 → 09-21 | 6 | 706.25 → 726.79 | −2.8% |

\*Still in cash at the end; compared with the 09-30 close.

So yes, timing is the reason, and it can be stated precisely. A cash period helps only if the price at buy-back is below the price at the sell. The cross rule always arrives late at both ends:

- **Late exit:** the sell fill came 2–14% below the highest close of the trade it ended.
- **Late re-entry:** the buy-back came 1–35% above the lowest price while in cash.

A cash period pays only when the fall it sits out is larger than both lags combined. In this window that happened in the long, deep declines (BTC and ETH Jan–Mar and May–Jul, gold Mar–Aug). Every short cash period (≤ 24 days) on BTC, ETH and QQQ lost: the cross fired on a dip, price recovered, and the rule bought back higher. QQQ's long Feb–Apr cash period also lost, because the V-shaped rebound carried price back above the sell before the buy signal came.

That is also why most crypto trades lost yet the total was positive: two large wins from sitting out crashes paid for the whipsaws. EMA's crypto result rests on two or three events in nine months.

### 4. Drawdown has to be managed whatever the method

Even DCA sat underwater on money already invested: −24.2% for BTC and −32.0% for ETH (both on 02-05), −14.8% for gold (06-24), −9.0% for QQQ (03-30). Buy & Hold drawdowns reached −39.5% (BTC) and −53.3% (ETH). EMA was the only method with an exit rule and cut Buy & Hold's drawdown by roughly half on BTC, ETH and gold, but the late exits mean it still absorbed 2–14% of each fall before stepping aside.

### 5. QQQ is the strongest candidate to hold long term

Within the window, QQQ was the only asset positive under all three methods, and switching in and out of it only cost return. The longer history (Buy & Hold, bar open to 2026-09-30 close) supports holding it, with one qualification:

| Asset | Since 2021-07: multiple | CAGR | Max DD | Since 2019: CAGR | Max DD |
|---|---|---|---|---|---|
| BTC | ×2.37 | +17.9% | −76.6% | — | — |
| ETH | ×1.15 | +2.8% | −79.3% | — | — |
| XAUT | ×2.35 | +17.7% | −26.6% | +16.4% | −26.6% |
| QQQ | ×2.09 | +15.1% | −35.6% | **+22.9%** | −35.6% |

- **Against crypto:** QQQ earned a similar return to BTC with less than half the drawdown, and far more than ETH. The crypto returns need tolerating −77% to −79% falls.
- **Against gold:** since 2019 QQQ compounds faster (+22.9% vs +16.4% a year). Since 2021-07 gold slightly out-returned QQQ with a shallower drawdown, so QQQ's edge over gold depends on the start date.
- **Consistency:** QQQ has been positive every calendar year since 2023, including 2026 so far (+20%), while BTC, ETH and gold are all negative in 2026.

## Conclusion

Over these nine months, the method mattered less than the path: when money went in, and whether the asset spent long stretches falling. EMA 12/26 helps exactly when an asset has long, deep declines that outlast its own lag, and costs return in V-shaped recoveries and choppy ranges. As pure exposure, QQQ is the most defensible long-term hold of the four, and trend-switching added nothing there in this window.

## Limitations

- One 9-month window; conclusions about method are path-specific, and EMA's crypto edge rests on two or three events.
- Gross only: no fees, spread, funding or QQQ dividends (dividends would add roughly 0.5–0.6% a year to QQQ). EMA trades most, so costs will hurt it most.
- S2 is the EMA cross without the MACD filter in the study guide.
- Long-history figures are Buy & Hold only and are not a P1 deployment result.
- DCA schedule (monthly, 9 buys) was chosen for this run; the study guide lists the interval as an open decision.

## Next

Add the MACD filter and trading costs to S2, then rerun on the same window and capital to see whether the exit rule still beats the passive baselines net.
