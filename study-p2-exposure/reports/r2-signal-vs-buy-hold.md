# FFD + ITR signal vs Jan 1 Buy & Hold, DCA and EMA 12/26 — a simple comparison

**Date:** 2026-11-01
**Scope:** BTC / ETH / XAUT / QQQ, 1D bars, 2026-01-01 → 2026-09-30 (9 months), $900 each
**Type:** One-trade entry-timing comparison, gross. Not a deployable edge.

## Setup

| | Jan 1 Buy & Hold (P1 S0) | DCA (P1 S1) | EMA 12/26 (P1 S2) | Signal Buy & Hold |
|---|---|---|---|---|
| Entry | All $900 at the first open of 2026 | $100 at each month's first open, Jan–Sep (9 buys) | All $900 at the first open of 2026; all out / all back in at the next open after each EMA 12/26 cross (EMAs warm up from 2025 Q4) | All $900 at the open of the bar after the first signal |
| Signal | — | — | EMA 12 crossing EMA 26 | First ITR low (HL or LL) confirmed by the replayer structure engine whose pivot-bar FFD Z (d = 0.25, rolling 445) is ≤ −1 (**BTC ≤ −2**, a hindsight special case) |
| Before entry | — | Unspent tranches in cash at 0% | Cash at 0% while out | Cash at 0% |
| Exit | Marked at the 2026-09-30 close | Marked at the 2026-09-30 close | Open position marked at the 2026-09-30 close | Marked at the 2026-09-30 close |

No fees, spread, funding or dividends. XAUT uses XAUUSD. Notebooks:
[buy-hold-1d.ipynb](../../study-p1-baseline/buy-hold-1d.ipynb),
[dca-1d.ipynb](../../study-p1-baseline/dca-1d.ipynb),
[ema-trades-1d.ipynb](../../study-p1-baseline/ema-trades-1d.ipynb),
[p2-ffd-signal.ipynb](../p2-signal/p2-ffd-signal.ipynb).

## Results

Final value on 2026-09-30 and max drawdown; best final value in bold. DCA's drawdown is on holdings + idle cash, as in P1.

| Asset | Jan 1 Buy & Hold | DCA | EMA 12/26 | Signal Buy & Hold |
|---|---|---|---|---|
| BTC (−2) | $858.65 (−4.6%), −39.5% | $1,053.92 (+17.1%), −18.7% | $1,007.18 (+11.9%), −18.0% | **$1,072.91 (+19.2%)**, −28.7% |
| ETH | $813.39 (−9.6%), −53.3% | $1,140.75 (+26.8%), −21.7% | $1,102.20 (+22.5%), −28.2% | **$1,148.27 (+27.6%)**, −35.2% |
| XAUT | $866.40 (−3.7%), −26.6% | $830.44 (−7.7%), −13.6% | **$981.52 (+9.1%)**, −14.2% | $927.05 (+3.0%), −11.7% |
| QQQ | $1,077.24 (+19.7%), −12.2% | $1,016.64 (+13.0%), −8.4% | $982.30 (+9.1%), −9.6% | **$1,101.03 (+22.3%)**, −10.7% |
| *BTC at the −1 rule* | *$858.65 (−4.6%), −39.5%* | *$1,053.92 (+17.1%), −18.7%* | *$1,007.18 (+11.9%), −18.0%* | *$824.30 (−8.4%), −39.5%* |

| Asset | Signal vs Buy & Hold | Signal vs DCA | Signal vs EMA | Signal entry vs first open | Signal time in market |
|---|---|---|---|---|---|
| BTC (−2) | +$214.26 | +$18.99 | +$65.73 | 70,140.70 (−20.0%), Feb 10 | 85% |
| ETH | +$334.88 | +$7.52 | +$46.07 | 2,104.94 (−29.2%), Feb 10 | 85% |
| XAUT | +$60.65 | +$96.61 | −$54.47 | 4,035.69 (−6.5%), Jul 2 | 34% |
| QQQ | +$23.79 | +$84.39 | +$118.73 | 607.16 (−2.2%), Apr 8 | 65% |
| *BTC at the −1 rule* | *−$34.35* | *−$229.62* | *−$182.88* | *91,295.10 (+4.2%), Jan 13* | *96%* |

## Findings

### 1. The signal only changes the entry price

Both strategies hold the same asset to the same close, so the gap comes entirely from where they bought:
signal value = Buy & Hold value × (first open ÷ signal fill open). Every asset where the signal bought
below the first open of 2026 gained, by exactly that discount. The structure and Z did not time the exit,
add trades or avoid any drawdown after entry.

### 2. With one rule (−1) for all assets, it added gain on 3 of 4 and lost on BTC

ETH, XAUT and QQQ bought below their Jan 1 open and gained $24–$335. BTC at −1 fired on the Jan 8 HL,
bought above the Jan 1 open and lost $34 against Buy & Hold. BTC's +$214 exists only because −2 was chosen
after seeing its Z bottom at −5.5 on Feb 5; it is not evidence for the signal.

### 3. Against DCA it wins clearly only where DCA's average cost rose

On BTC and ETH, DCA also bought into the Feb–Jun lows and ended within $8–$19 of the signal, with
a much smaller drawdown (−19% / −22% vs −29% / −35%) and no signal at all. The signal beat DCA by
$84–$97 on gold and QQQ, where later monthly buys raised DCA's average cost. With the −1 rule, BTC
trails DCA by $230.

### 4. Against EMA 12/26 it wins on 3 of 4, loses on gold

The signal beat EMA by $46–$119 on BTC (−2), ETH and QQQ: one well-priced entry held through the
rallies, where EMA's 4–7 trades sold and bought back at worse prices. Gold is the exception: EMA
(+9.1%) caught gold's rally and decline in two trades, while the signal entered only in July and
made +3.0%. With the −1 rule, BTC trails EMA by $183. EMA's drawdown was lower than the signal's on
BTC (−18.0% vs −28.7%) and ETH (−28.2% vs −35.2%), so the signal's extra gain came with as much or more risk.

### 5. Lower drawdown is mostly less time exposed, not better timing

Max drawdown fell against Buy & Hold on every asset (but stayed above DCA on BTC, ETH and QQQ), and the signal also sat in cash for 15–66% of the window. Gold shows
this most: −11.7% vs −26.6% with only 34% time in market. After entry, crypto still fell hard
(ETH to $670 in late June, about −35%), so a deep-Z ITR low marked a cheaper price, not the bottom.

### 6. Judged on entry price alone, the −1 rule was 2 good, 1 average, 1 bad

Share of all entry days in the window whose open was cheaper than the signal's fill:

| Asset | Cheaper days | Entry quality |
|---|---|---|
| XAUT | 4% | very good |
| QQQ | 18% | good |
| ETH | 49% | average |
| BTC at −1 | 96% | near worst |
| *BTC at −2 (hindsight)* | *45%* | *average* |

The gains over Jan 1 Buy & Hold on BTC and ETH came mostly from 2026's crypto path: prices fell after
January, so almost any later entry beat Jan 1.

## Conclusion

**This is an in-sample, hindsight result, not an edge.** One entry per asset, a rule shaped on the same
window, and a BTC threshold fitted after the fact cannot separate skill from 2026's price path. Under one
fixed rule the entry timing was no better than chance across four assets.

What the window does show is **how the feature behaves**:

1. **Deep Z marks "cheap relative to its 445-day memory", not "the bottom".** ETH entered at Z −3.15 and
   still fell another 35%. Z ranks price; it does not time the end of a decline.
2. **A fixed Z threshold does not transfer across assets.** Crypto lows reached Z −3 to −5.5; gold and QQQ
   rarely went below −1.5. A per-asset threshold, e.g. a low percentile of each asset's own past Z, fits
   the feature better than one number.
3. **Structure confirmation adds 4–8 bars of lag.** Pairing the ITR low with Z selects *which* low to act
   on, but entry always comes after the bounce has started.
4. **In trend regimes Z stays shifted** ([r1](r1-fracdiff-adf-failure.md): gold 2024–25), so a threshold
   can go unreached for a long time.

**Next test, if pursued:** freeze the rule (no BTC override), run it on other windows (e.g. each quarter
or year 2021–2025), and count how often its entry beats a random entry day in the same window.

## Caveats

- One window, one trade per asset: four data points, no statistics.
- The rule (−1 threshold, pivot-bar Z, ITR tier) was shaped while looking at this same window.
- Gold's result covers only one quarter in the market.
- Buy & Hold, DCA and EMA figures are P1's ([P1 report](../../study-p1-baseline/reports/P1-baseline.md)), recomputed and matching.
