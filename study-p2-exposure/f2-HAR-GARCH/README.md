# P2-f2 — Volatility (HAR-YZ, GARCH family)

Guide: [P2-f2 guide](../../docs/study-guide/P2-f2-guide.md) · YZ formula: [yang-zhang.md](yang-zhang.md) · Shared warm-up: [../README.md](../README.md)

## YZ window: n = 22 bars, same for all four assets (decided 2026-11-01)

Applies to the **standalone YZ** (the formula in `yang-zhang.md`, used for the
historical YZ plot). HAR-YZ does not use n: it averages a per-day YZ variance
over 1 / 5 / 22 days, and those horizons take the place of n.

**Evidence:** train 2021–2023. QLIKE of YZ_n used as a forecast of next-day
squared close-to-close return. The table shows the gap to the best n for each
asset (0 = best, lower is better):

| n | BTC | ETH | QQQ | XAUUSD |
|---:|---:|---:|---:|---:|
| 5 | 0.163 | 0.086 | 0.026 | 0.000 |
| 10 | 0.041 | 0.013 | 0.000 | 0.004 |
| 15 | 0.026 | 0.000 | 0.001 | 0.016 |
| 22 | 0.051 | 0.027 | 0.006 | 0.018 |
| 44 | 0.009 | 0.019 | 0.027 | 0.009 |
| 63 | 0.000 | 0.041 | 0.029 | 0.023 |

**Why 22:**

- **No n wins.** Each asset has a different best n, and the gaps between
  n = 10 and 63 are small. Significance not tested. The one clear result:
  n = 5 is too noisy for crypto.
- **Matches HAR's monthly horizon**, so the YZ plot and HAR's monthly input
  describe the same thing.
- **Standard one-month convention.**
- **Choosing the best n for each asset would mean fitting to noise.** The
  standalone YZ is a descriptive series, not one of the four forecasting models,
  so its window doesn't need tuning.
- **Counted in bars, as in f1.** 22 bars ≈ 3 weeks for crypto (24/7),
  ≈ 1 month for QQQ/XAUUSD.

**Caveat:** the squared-return target is provisional (not decided yet).
Re-run this check once the target is fixed.

## Overnight term by asset (train 2021–2023)

| Asset | Overnight² share of close-to-close variance |
|---|---:|
| BTC | 0.000 |
| ETH | 0.000 |
| QQQ | 0.120 |
| XAUUSD | 0.013 |

24/7 crypto has no real overnight gap, so YZ there reduces to open-to-close plus
Rogers–Satchell. Only QQQ uses the overnight term in a meaningful way.

## YZ data — `yz.py` → `yz_data/<SYM>-yz-1d.csv`

Run `python yz.py`. Computed on the full history (2019 →): YZ has no fitted
parameters, so it needs no train/test split.

| Column | Meaning |
|---|---|
| `yz_var_daily` | Per-day YZ variance: o² + k·c² + (1−k)·RS, zero mean, k = 0.34/2.34. HAR input (HAR takes the 1/5/22 averages itself) |
| `yz_var_22` | Standalone YZ over 22 bars (`yang-zhang.md` formula, demeaned, k(22)). For the historical plot |
| `r` | This bar's close-to-close log return (not ×100). GARCH-family input, known at this bar's close |
| `r2_next` | Next bar's squared close-to-close log return. Provisional target, **future value: never an input** |

- Units: daily log-return variance, not annualized.
- Each row's YZ is known at that bar's close and forecasts the next bar.
- XAUUSD timestamps are tz-naive; the other three are UTC (as in the source parquet).

## Walk-forward convention: annual folds (decided 2026-11-01)

Applies to every fitted model in f2 (HAR-YZ now, GARCH / EGARCH / GJR later), so all models forecast the same days with the same information.

- **Fold Y** = forecasts whose target day falls in calendar year Y.
- **Refit:** once, at the first forecast origin of fold Y, on every row whose target day ≤ 31 Dec of Y−1. Expanding window from 2019. Parameters are held fixed through Y.
- **Forecast:** each day of Y uses the fold's fixed parameters × that day's inputs (known at the close of the day before the target).
- Scoring joins all fold forecasts into one daily series per model and scores each day. Refits stay inside each model.

| Fold | Fit on targets | Role |
|---|---|---|
| 2021 | 2019 → 2020 | Train |
| 2022 | 2019 → 2021 | Train |
| 2023 | 2019 → 2022 | Train |
| 2024 | 2019 → 2023 | Test |
| 2025 | 2019 → 2024 | Test |
| 2026 (Jan–Sep) | 2019 → 2025 | Test (ends 2026-09-30) |

Train folds may also compare other refit schedules (monthly, daily) as a diagnostic; only the annual scheme is scored on test.

## Forecast files — `forecasts/<SYM>-<model>.csv`

Written by each model notebook (`f2-HAR-YZ.ipynb` → `HAR-YZ`, `f2-GARCH11.ipynb` → `GARCH11`, `f2-EGARCH11.ipynb` → `EGARCH11`, `f2-GJRGARCH11.ipynb` → `GJRGARCH11`) for the cross-model comparison.
Index `timestamp` = forecast origin (close of day t); `target_date` = day t+1; `h` = forecast variance in %² (log-return variance × 1e4); `split` = train / test; `fold` = target year.
Annual walk-forward only. Train targets 2021–2023, test targets 2024-01-01 → 2026-09-30.

## Scoring target: what RMSE and QLIKE are measured against (provisional)

**Every RMSE and QLIKE so far (naive, HAR-YZ, GARCH; train and test) scores each forecast against one value: the next day's squared close-to-close log return.**

- Forecast: h, made at the close of day t (%²).
- Realized: RV = (100 · ln(C_{t+1} / C_t))², known at the close of day t+1. This is `r2_next` × 1e4.
- RMSE = √ mean((h − RV)²)
- QLIKE = mean(ln h + RV / h)

Same RV and the same days for every model, so the comparisons are fair.

**True variance is never observed.** RV is only a stand-in for it:
- **Right on average:** with zero mean, E[r²_{t+1}] = σ²_{t+1}, so forecasting the true variance gives the best expected score.
- **Very noisy:** under normal returns, the standard deviation of r² is √2 × σ². One day says almost nothing; only averages over hundreds of days rank models. The noise costs power: small gaps can't be told apart from luck without a significance test (Diebold–Mariano, pending).

**Status: provisional.** Possible upgrades:

| Stand-in | Noise | Note |
|---|---|---|
| Squared daily return (current) | Very high | Works with daily bars for every asset |
| Intraday realized variance (sum of squared 5-minute returns) | Much lower | Data exists (5m crypto, 1m QQQ). QQQ needs the overnight gap added |
| Day t+1's own YZ variance | Lower | Would favour HAR-YZ (built from YZ): not a fair judge |

Changing the target changes every score. Re-run all model notebooks after deciding.

## Standardized innovation check B: lag k = 22 (decided 2026-11-01)

Z_t = r_t / √h_t. Check B (remaining volatility clustering, [validation guide](../../docs/study-guide/P2-f2-validation.md) §5) uses **k = 22**:

- ACF of Z² for lags 1–22, with raw r² overlaid as the baseline. What counts is how much of the raw-r² clustering the model removes, not whether the p-value is above some cutoff.
- Ljung–Box on Z² at lags 5 and 22.
- Why 22: it matches HAR's monthly horizon and the 22-bar YZ window. Convenience, not tuning.
- Crypto: also check |Z|, since a few extreme Z values can dominate the Z² ACF.

Evaluation period: pooled test, 2024-01-01 → 2026-09-30. Ljung–Box is not run per year (≈ 250–365 days is too few for 22 lags); per-year stability uses mean Z² instead. Notebook: `f2-standardize-sd.ipynb`.
