# P2 exposure studies

## Warm-up period (shared across features)

| Item | Setting |
|---|---|
| Data start | 2019-01 for every asset (crypto: Binance spot before 2022-01-01, Bybit after; QQQ/XAUUSD: 2019-01-02) |
| Warm-up | **2019-01 → 2020-12** |
| Train | 2021-01-01 → 2023-12-31 |
| Test | 2024-01-01 onward |
| Bars in warm-up | ~731 crypto (24/7), ~505 QQQ, ~517 XAUUSD |

What warm-up means depends on the feature. Check each new feature against it:

| Feature | What it needs before the first valid value | Fits in 2019–20? |
|---|---|---|
| f1 FFD (d = 0.25, τ = 1e-4) | 444 bars of history to fill the 445-bar window | Yes. First value 2020-03-20 (crypto), 2020-10-06 (QQQ) |
| f2 YZ + HAR (22-day average) | ~44 bars | Yes. First value Feb–Mar 2019 |
| f2 GARCH / EGARCH / GJR | No window. The starting variance has to wear off: ~200–250 bars at persistence ≈ 0.98 | Yes |

### f1 vs f2: how the warm-up is used

- **f1 (FFD):** warm-up only fills the window. FFD values in 2020 exist but are
  not used for d-selection.
- **f2 (volatility):** features exist almost from the start of 2019, so
  2019–2020 is **fitting data, not filler**. Start the expanding walk-forward fit
  there. That keeps the March 2020 crash in the sample, which the EGARCH/GJR
  asymmetry fits need. The binding constraint is the size of the fitting sample
  (GARCH MLE needs several hundred bars, the asymmetry term γ more), not the
  warm-up.

### f2 notes to keep (2026-11-01)

- **HAR-YZ overlap:** HAR on a rolling 22-day YZ gives daily/weekly predictor
  correlation 0.98–0.99 (2021–23), so HAR has almost nothing to separate. Using a
  per-day YZ variance averaged over 1 / 5 / 22 days drops it to 0.63–0.70.
  Recommended construction.
- **Target still open:** next-day squared close-to-close return (works with daily
  bars for all assets; recommended primary) vs intraday realized variance (5m
  crypto, 1m QQQ available; needs QQQ overnight handling; robustness check later).
- `arch` package is not installed yet (needed for GARCH family).
