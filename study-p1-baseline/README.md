# P1 baseline study

Working folder for the P1 strategy baseline described in [../docs/study-guide/P1-baseline.md](../docs/study-guide/P1-baseline.md).

## Notebooks

| Notebook | Content |
|---|---|
| `plot-1d-ohlc.ipynb` | Plain 1D candles for BTC, ETH, XAUT, QQQ, 2026 Q1–Q3 |
| `buy-hold-1d.ipynb` | S0 Buy & Hold: $900 bought once at the first available open, held to 2026-09-30 |
| `dca-1d.ipynb` | S1 DCA: $100 at the open of each month's first bar, Jan–Sep (9 buys, $900) |
| `ema-signals-1d.ipynb` | EMA 12/26 cross signals (buy on cross up, sell on cross down), EMAs warmed up from 2025 Q4 |
| `ema-trades-1d.ipynb` | EMA 12/26 all-in / all-out, $900: forced buy at the first open, then every fill at the next bar's open after a signal |

Shared code lives in `helpers/`. Run notebooks with this folder as the working directory.
`python -m helpers.passive_benchmarks` prints the S0 vs S1 summary.

## Assumptions

- Period: 2026 Q1–Q3 (9 months), 1D bars, bar-open timestamps in UTC.
- Capital: $900 per asset.
- Fills at the bar open; zero fees, spread and slippage.
- Uninvested cash earns 0%. QQQ dividends not yet included.

## Known constraints

- **XAUT uses XAUUSD as a substitute.** The replayer has no XAUTUSDT bars yet, so MT5 XAUUSD spot gold stands in. XAUUSD trades on a weekday session (about 193 bars in the period vs 273 for 24/7 crypto), and its price may differ slightly from XAUT on Bybit.
