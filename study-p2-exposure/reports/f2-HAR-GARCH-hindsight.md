# P2-f2 volatility forecasting: HAR-YZ vs GARCH, EGARCH, GJR-GARCH

Date: 2026-11-01
Setting: one-day-ahead variance forecasts, daily bars, BTC, ETH, QQQ, XAUUSD.
Annual walk-forward, expanding window from 2019. Train targets 2021–2023, test
targets 2024-01-01 → 2026-09-30. See [f2 README](../f2-HAR-GARCH/README.md) and
the [P2-f2 guide](../../docs/study-guide/P2-f2-guide.md).

## Conclusion

**No model wins on every asset, and the gaps between the best models are small.**
On test, the best model per asset is GJR-GARCH for BTC and gold, and HAR-YZ for
QQQ and (narrowly) ETH. The winner changes from year to year, and the train and
test rankings disagree. So the picks below are **provisional**: they need a
significance test, and the scoring target is still provisional.

| Asset | Provisional pick | Why |
|---|---|---|
| BTC | GJR-GARCH or GARCH | HAR-YZ fails in calm years; GJR ≈ GARCH on test |
| ETH | HAR-YZ or GJR-GARCH | Within 0.004 QLIKE of each other on test |
| QQQ | HAR-YZ, then GJR / EGARCH | Significant leverage effect; asymmetric GARCH clearly beats plain GARCH |
| XAUUSD | GJR-GARCH | Best on test; significant *reverse* asymmetry |

By the guide's rule ("prefer the simplest when similar"), plain GARCH stays a
reasonable default where the gaps are not significant.

## Setup

| Item | Setting |
|---|---|
| Data | `yz_data/<SYM>-yz-1d.csv`, from [`yz.py`](../f2-HAR-GARCH/yz.py): YZ variances, return, target, one file per asset |
| HAR-YZ | OLS on per-day YZ variance and its 5- and 22-day averages; target r²_{t+1}; variance levels |
| GARCH family | Zero mean, normal likelihood (the regular case), returns in %; `arch` 8.0.0 |
| Folds | Fold Y forecasts year Y with parameters fitted on data up to 31 Dec of Y−1, held fixed through Y |
| Naive benchmark | Carry forward the 22-bar YZ variance |
| Target | Next day's squared close-to-close return, (100 · ln C_{t+1}/C_t)² (**provisional**) |
| Scores | QLIKE (main) and RMSE, same days and same target for every model |

Notebooks: [HAR-YZ](../f2-HAR-GARCH/f2-HAR-YZ.ipynb) ·
[GARCH](../f2-HAR-GARCH/f2-GARCH11.ipynb) ·
[EGARCH](../f2-HAR-GARCH/f2-EGARCH11.ipynb) ·
[GJR-GARCH](../f2-HAR-GARCH/f2-GJRGARCH11.ipynb). Forecasts in
`f2-HAR-GARCH/forecasts/<SYM>-<model>.csv`.

## Results

### Test (2024 → 2026-09): QLIKE vs naive, lower = better

| Asset | HAR-YZ | GARCH | EGARCH | GJR |
|---|---:|---:|---:|---:|
| BTC | +0.058 | −0.021 | −0.006 | **−0.025** |
| ETH | **−0.098** | −0.086 | −0.079 | −0.094 |
| QQQ | **−0.100** | −0.047 | −0.086 | −0.088 |
| XAUUSD | −0.047 | −0.042 | −0.043 | **−0.055** |

RMSE vs naive tells the same broad story (every model 0–6% below naive, except
HAR-YZ on BTC at +2%).

### Train (2021–2023): QLIKE vs naive

| Asset | HAR-YZ | GARCH | EGARCH | GJR |
|---|---:|---:|---:|---:|
| BTC | −0.027 | −0.032 | **−0.053** | −0.024 |
| ETH | +0.063 | +0.029 | **+0.018** | +0.057 |
| QQQ | +0.044 | +0.045 | **+0.010** | +0.024 |
| XAUUSD | **−0.041** | −0.007 | 0.000 | −0.002 |

On train, EGARCH led for three assets; on test it leads none. On train, ETH and QQQ
couldn't beat naive at all.

### Best model each year (lowest QLIKE of all five, naive included)

| Asset | 2021 | 2022 | 2023 | 2024 | 2025 | 2026 |
|---|---|---|---|---|---|---|
| BTC | HAR-YZ | GJR | EGARCH | GJR | naive | GJR |
| ETH | HAR-YZ | HAR-YZ | naive | EGARCH | HAR-YZ | GJR |
| QQQ | HAR-YZ | naive | naive | EGARCH | HAR-YZ | HAR-YZ |
| XAUUSD | HAR-YZ | HAR-YZ | GARCH | EGARCH | GJR | HAR-YZ |

The 2021–23 columns are train years; 2024–26 are test years. No model wins more
than half the years on any asset.

### How big the gaps are

Extra QLIKE grows with the ratio between the true variance and the forecast.
**About 0.05 is roughly the cost of being ~30% further off in variance every day.**
Most gaps between the top two models are ≤ 0.02.

## What each model showed

**HAR-YZ.** For crypto it is close to a flat line: the horizon weights sum to only
0.2–0.4, so the constant term does most of the work. It wins in high-vol years and
loses badly in calm ones (BTC 2023 +0.095, 2025 +0.141 vs naive). For QQQ the
weights sum to about 0.8, and it is the best model on test. Yearly refits barely move
the coefficients. Using a rolling 22-day YZ as the HAR input would make the daily
and weekly inputs almost identical (correlation 0.98–0.99), hence the per-day YZ
construction.

**GARCH(1,1).** Converges cleanly on all 24 fits; α + β = 0.91–0.99. A shock halves
in about 8–16 days for BTC (ETH 10–56), 22–53 for QQQ and 12–27 for gold. It reacts to each
day's return, which fixes HAR's calm-year problem on crypto.

**Asymmetry (EGARCH, GJR).** Both models agree on the direction:

| Asset | Asymmetry | Significant? |
|---|---|---|
| QQQ | Down moves raise vol more (leverage) | Yes, from the 2022–23 folds onward |
| XAUUSD | **Up** moves raise vol more (GJR: ~3× more) | Yes, in almost every fold |
| BTC, ETH | Slight down-move tilt | No |

Asymmetry pays off clearly only for QQQ (GJR beats GARCH in all 6 QQQ years).
GJR beats GARCH in 10 of 12 test asset-years; EGARCH less consistently.

## Fitting notes

- **Every GARCH-family fit converged** (72 fits across 3 models × 4 assets × 6 folds),
  and restarts from 9–18 starting points always reached the same peak. Scaling
  returns to % was the only fix needed.
- **The Student-t version was dropped.** It was only meant as a fallback if the normal
  fit failed (`GARCH.md` §3), and the normal fit never failed. When tried, it pushed
  BTC to α + β = 1 (shocks never fade).
- **Guide corrections:**
  - `EGARCH.md`, fixed in the file: its code omitted `o=1`, so it fit no asymmetry term.
    Also: |β| < 1 is still needed for stability, and γ needs significance to "prove" leverage.
  - `GARCH.md`, fixed in the file: `fit(method='L-BFGS-B')` doesn't exist in `arch` (TypeError).
    The IGARCH case (α + β = 1) and the "log-likelihood → −∞" claim were overstated.
  - `GJR-GARCH.md`, fixed in the file: the p/q comment was swapped, the constraint row
    wrongly required γ > 0, and the stationarity condition α + γ/2 + β < 1 was missing.
  - `HAR.md` and `yang-zhang.md`: wording fixes only (target vs forecast in HAR; which
    estimators drift biases in YZ). The formulas were correct.

## Limits and open items

1. **No significance test yet.** The gaps (mostly ≤ 0.05) may be noise. Next step:
   a Diebold–Mariano test on daily QLIKE differences, with standard errors robust
   to autocorrelation.
2. **The target is provisional.** A single day's squared return is right on average but
   very noisy (its spread is √2 × the true variance), which limits how sharply models
   can be separated. Intraday realized variance (5m crypto, 1m QQQ, plus QQQ's
   overnight gap) would be a much less noisy judge. Changing the target means
   re-running every notebook.
3. **Untested variants:** log-HAR (might fix crypto HAR's shrunken weights); a monthly
   instead of yearly refit (it mattered only in regime shifts on train).
4. **This is a forecasting result, not a trading result.** Whether any of these
   representations improves P2 top/bottom forecasting is a separate test.
