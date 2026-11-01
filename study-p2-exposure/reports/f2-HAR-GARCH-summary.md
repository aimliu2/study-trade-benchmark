# P2-f2 volatility forecasting: HAR-YZ vs GARCH, EGARCH, GJR-GARCH

See [f2 README](../f2-HAR-GARCH/README.md) and the
[P2-f2 validation guide](../../docs/study-guide/P2-f2-validation.md).

## Round 1 validation — QLIKE on test (2024-01-01 → 2026-09-30)

Date: 2026-11-01

### What was validated against

| Item | Setting |
|---|---|
| Forecast | h_{t+1}: next-day variance of % log returns, made at the close of day t |
| Realized (validation target) | RV = (100 · ln(C_{t+1} / C_t))², known at the close of day t+1. This is `r2_next` × 1e4 in `yz_data/<SYM>-yz-1d.csv` |
| Score | QLIKE = mean(ln h + RV / h). Lower is better |
| Period | Target days 2024-01-01 → 2026-09-30. Days: BTC/ETH 1004, QQQ 689, XAUUSD 710 |
| Folds | Annual walk-forward: fold Y is fitted on all targets up to 31 Dec of Y−1 (expanding from 2019), parameters fixed through Y |
| Benchmark (naive) | Carry forward the 22-bar Yang–Zhang variance (`yz_var_22`) |
| Fairness | Same RV and same days for every model of an asset |

**The target is provisional.** RV is a single day's squared return: correct on
average (E[r²] = true variance under zero mean) but very noisy. Changing the
target means re-scoring everything.

**Reading the gaps.** A forecast that is off by a ratio ρ from the true variance
costs ρ − ln ρ − 1 extra QLIKE per day. **A gap of about 0.05 ≈ being ~30% off in
variance every day.** Raw QLIKE depends on each asset's variance level, so compare
models within an asset, not across assets.

**What "best" means here.** Round 1 only measures the **lowest pooled QLIKE**:
the average over every test day, all three years together. That is not the
same as:

1. **Best in every period.** No model is best in all three test years on any asset.
2. **Significantly better.** Not tested yet (Diebold–Mariano pending).

A pooled average can be carried by one strong year, so each pooled result below
is shown next to the number of years in which that model was also best.

### QLIKE, pooled test period

Raw QLIKE (**bold** = lowest pooled):

| Asset | naive | HAR-YZ | GARCH | EGARCH | GJR |
|---|---:|---:|---:|---:|---:|
| BTC | 2.818 | 2.876 | 2.796 | 2.812 | **2.793** |
| ETH | 3.631 | **3.534** | 3.545 | 3.553 | 3.537 |
| QQQ | 1.477 | **1.377** | 1.430 | 1.390 | 1.389 |
| XAUUSD | 1.459 | 1.413 | 1.417 | 1.416 | **1.404** |

Difference from naive (negative = better than naive):

| Asset | HAR-YZ | GARCH | EGARCH | GJR | Gap, 1st vs 2nd pooled |
|---|---:|---:|---:|---:|---:|
| BTC | +0.058 | −0.021 | −0.006 | **−0.025** | 0.004 |
| ETH | **−0.098** | −0.086 | −0.079 | −0.094 | 0.004 |
| QQQ | **−0.100** | −0.047 | −0.086 | −0.088 | 0.012 |
| XAUUSD | −0.047 | −0.042 | −0.043 | **−0.055** | 0.008 |

Lowest pooled QLIKE vs years that model was also best (out of all five, naive included):

| Asset | Lowest pooled | Years also best | Reading |
|---|---|---|---|
| BTC | GJR | 2 of 3 (2024, 2026) | Fairly steady |
| ETH | HAR-YZ | **1 of 3** (2025, −0.165) | Carried by one year |
| QQQ | HAR-YZ | 2 of 3 (2025, 2026) | Fairly steady |
| XAUUSD | GJR | **1 of 3** (2025) | Carried by one year |

### By target year: difference from naive

| Asset | Year | HAR-YZ | GARCH | EGARCH | GJR | Best of all five |
|---|---|---:|---:|---:|---:|---|
| BTC | 2024 | +0.033 | +0.001 | +0.012 | **−0.003** | GJR |
| | 2025 | +0.141 | +0.021 | +0.042 | +0.028 | **naive** |
| | 2026 | −0.018 | −0.107 | −0.094 | **−0.124** | GJR |
| ETH | 2024 | +0.017 | −0.001 | **−0.018** | −0.004 | EGARCH |
| | 2025 | **−0.165** | −0.121 | −0.115 | −0.124 | HAR-YZ |
| | 2026 | −0.161 | −0.155 | −0.111 | **−0.176** | GJR |
| QQQ | 2024 | −0.058 | −0.044 | **−0.061** | −0.057 | EGARCH |
| | 2025 | **−0.153** | −0.086 | −0.147 | −0.145 | HAR-YZ |
| | 2026 | **−0.084** | −0.001 | −0.039 | −0.052 | HAR-YZ |
| XAUUSD | 2024 | −0.052 | −0.058 | **−0.078** | −0.075 | EGARCH |
| | 2025 | −0.064 | −0.062 | −0.086 | **−0.095** | GJR |
| | 2026 | **−0.017** | +0.008 | +0.061 | +0.024 | HAR-YZ |

### Per model

- **HAR-YZ.** Lowest pooled QLIKE on QQQ (−0.100) and, narrowly, ETH (−0.098).
  The ETH result rests on 2025 alone. Highest pooled QLIKE on BTC, and the only
  model worse than naive there (+0.058), driven by 2024–25 (+0.033, +0.141).
  It swings the most from year to year: best in 4 of 12 asset-years, but also
  has the largest single loss to naive.
- **GARCH(1,1).** Beats naive on every asset over the pooled period, but never
  has the lowest pooled QLIKE. Last of the four on QQQ (−0.047, about half the
  gain of the others) and on gold. Close to GJR on BTC (0.004 behind).
- **EGARCH(1,1).** Middle of the pack, pooled, on every asset. Best in 2024 on
  ETH, QQQ and gold, then fades. On gold in 2026 it is the worst (+0.061 vs naive).
  Weakest model on BTC apart from HAR-YZ (−0.006).
- **GJR-GARCH(1,1).** Lowest pooled QLIKE on BTC and gold, second on ETH and QQQ.
  The gold result rests on 2025 alone. Never worse than third pooled on any
  asset, which makes it the steadiest of the four on this measure. Beats plain
  GARCH in 10 of the 12 asset-years.
- **Naive.** Beaten by every model on ETH, QQQ and gold. On BTC it beats HAR-YZ,
  and it is the best model of all five in 2025.

### Round 1 reading

- **No model has the lowest pooled QLIKE on every asset.** GJR is lowest on BTC
  and gold, HAR-YZ on QQQ and ETH.
- **Two of those four results rest on a single year** (ETH HAR-YZ, gold GJR).
- **The pooled leader is often not far ahead.** On BTC and ETH, first and second
  are 0.004 apart, well inside the ~0.05 that corresponds to a 30% variance error.
- **Year-to-year rankings change.** Only BTC (GJR) and QQQ (HAR-YZ) have a
  model that is best in 2 of the 3 test years. ETH and gold have a different
  best model in each year.
- **Not yet tested:** whether any gap is significant (Diebold–Mariano on daily
  QLIKE differences, pending). Until then, the pooled ranking is a description,
  not a selection.

## Round 2 validation — standardized innovations on test (2024-01-01 → 2026-09-30)

Date: 2026-11-01 · Notebook: [`f2-standardize-sd.ipynb`](../f2-HAR-GARCH/f2-standardize-sd.ipynb)

### What was computed

| Item | Setting |
|---|---|
| Standardized innovation | Z_{t+1} = r_{t+1} / √h_{t+1}, with r_{t+1} = 100 · ln(C_{t+1} / C_t) (signed). Z² = RV / h, the same ratio QLIKE uses |
| Mean assumption | Zero conditional mean (μ = 0), as in the validation guide and the GARCH fits |
| Forecasts, period, days | Same as round 1 |
| A. Calibration | mean Z² (≈ 1 if the variance level is right), per test year and pooled |
| B. Remaining clustering | Ljung–Box on Z² and \|Z\| at lags 5 and 22, pooled only; ACF of Z² for lags 1–22 against raw r² |
| C. Distribution | Skew, excess kurtosis, max \|Z\|, share \|Z\| > 3, QQ plot |

Ljung–Box is pooled because one year (≈ 250–365 days) is too few for 22 lags
to have useful power. Per-year stability uses mean Z² instead.

### A. Calibration: mean Z²

mean Z² < 1: forecast variance too **high**. mean Z² > 1: too **low**.

| Asset | Model | 2024 | 2025 | 2026 | Pooled |
|---|---|---:|---:|---:|---:|
| BTC | naive | 0.99 | 0.94 | 1.23 | 1.04 |
| | HAR-YZ | 0.66 | 0.47 | 0.61 | 0.58 |
| | GARCH | 0.75 | 0.57 | 0.71 | 0.68 |
| | EGARCH | 0.73 | 0.54 | 0.68 | 0.65 |
| | GJR | 0.77 | 0.55 | 0.68 | 0.66 |
| ETH | naive | 1.01 | 1.09 | 1.30 | 1.11 |
| | HAR-YZ | 0.66 | 0.87 | 0.68 | 0.75 |
| | GARCH | 0.89 | 1.02 | 0.87 | 0.93 |
| | EGARCH | 0.86 | 1.01 | 0.97 | 0.94 |
| | GJR | 0.88 | 1.01 | 0.82 | 0.91 |
| QQQ | naive | 1.27 | 1.18 | 1.19 | 1.22 |
| | HAR-YZ | 0.86 | 0.86 | 0.96 | 0.89 |
| | GARCH | 0.92 | 0.98 | 1.05 | 0.98 |
| | EGARCH | 0.91 | 0.96 | 1.03 | 0.96 |
| | GJR | 0.91 | 0.90 | 1.08 | 0.95 |
| XAUUSD | naive | 1.26 | 1.27 | 1.19 | 1.24 |
| | HAR-YZ | 1.18 | 1.28 | 1.52 | 1.31 |
| | GARCH | 1.07 | 1.21 | 1.51 | 1.24 |
| | EGARCH | 0.98 | 1.10 | 1.69 | 1.22 |
| | GJR | 1.03 | 1.09 | 1.56 | 1.19 |

- **BTC: every model forecasts too much variance, in every year** (mean Z² 0.47–0.77,
  about 1.3–2× too high). Naive is the only calibrated forecast. The fits carry
  the high-volatility 2019–23 history into calmer 2024–26.
- **ETH:** the GARCH family is close (0.91–0.94 pooled). HAR-YZ is too high (0.75).
- **QQQ:** all four models are close to 1 (0.89–0.98). Naive is too low (1.22).
- **XAUUSD: everything forecasts too little**, worst in 2026 (1.5–1.7). Volatility
  rose and every forecast lagged behind it.
- **Link to round 1:** QLIKE penalises a too-high forecast less than a too-low
  one. That is how BTC models beat a calibrated naive on QLIKE while being
  ~1.5× too high.

### Zero-mean assumption, by test year

Z is built with μ = 0. If returns actually drift, mean Z ≈ μ / σ (a daily
Sharpe ratio), and that drift is counted as variance: mean Z² = Var(Z) + (mean Z)².

Mean Z (GJR shown; the other models are within ±0.02) and its t-statistic:

| Asset | 2024 | 2025 | 2026 | Pooled |
|---|---:|---:|---:|---:|
| BTC | 0.068 (t 1.5) | −0.005 (t −0.1) | −0.001 (t 0.0) | 0.022 (t 0.9) |
| ETH | 0.030 (t 0.6) | −0.006 (t −0.1) | −0.002 (t 0.0) | 0.008 (t 0.3) |
| QQQ | 0.071 (t 1.2) | 0.036 (t 0.6) | 0.067 (t 0.9) | 0.057 (t 1.5) |
| XAUUSD | 0.112 (t 1.8) | **0.213 (t 3.3)** | −0.027 (t −0.3) | **0.111 (t 2.7)** |

What this implies:

- **The zero-mean assumption holds for crypto and QQQ in every year.** No mean Z
  differs from 0 significantly (|t| < 2).
- **It fails only for gold in 2025** (mean Z 0.21, t 3.3): the gold rally was a
  drift large enough to show up in daily standardized returns. It also makes the
  pooled gold mean significant (t 2.7).
- **It barely matters for the variance checks.** (mean Z)² is at most 4% of mean Z²
  (gold 2025) and below 1.3% everywhere else. So gold's mean Z² of 1.1–1.3 in
  2025 is still mostly genuine under-forecasting, not drift. Gold 2026
  (mean Z² 1.5–1.7) has a mean Z near zero, so that miss is entirely variance.
- Modelling a non-zero mean is not needed for f2. It would change mean Z² by
  ≤ 0.04 in the worst year.

### B. Remaining volatility clustering (pooled)

Ljung–Box Q at lag 22 (p-value). "raw" = squared or absolute return, i.e. what a
constant-variance forecast would leave. Lower Q = more clustering removed.

| Asset | Series | raw | naive | HAR-YZ | GARCH | EGARCH | GJR |
|---|---|---:|---:|---:|---:|---:|---:|
| BTC | Z² | 89 (<.001) | 62 (<.001) | **51 (<.001)** | 20 (.56) | 29 (.14) | 23 (.39) |
| | \|Z\| | 83 (<.001) | 45 (.003) | **36 (.03)** | 18 (.68) | 21 (.52) | 21 (.54) |
| ETH | Z² | 33 (.06) | 13 (.94) | 12 (.96) | 11 (.97) | 11 (.97) | 11 (.98) |
| | \|Z\| | 43 (.005) | 54 (<.001) | 18 (.70) | 18 (.70) | 25 (.28) | 18 (.73) |
| QQQ | Z² | 101 (<.001) | 33 (.06) | 25 (.32) | 28 (.16) | 25 (.31) | 23 (.38) |
| | \|Z\| | 160 (<.001) | 44 (.004) | 25 (.32) | 22 (.43) | 21 (.52) | 22 (.44) |
| XAUUSD | Z² | 214 (<.001) | 33 (.06) | 18 (.71) | 16 (.80) | 21 (.55) | 18 (.71) |
| | \|Z\| | 331 (<.001) | 44 (.008) | 23 (.38) | 24 (.33) | 26 (.27) | 24 (.33) |

Lag 5 gives the same picture. One exception: BTC EGARCH Z² at lag 5 is
significant (p .004) but \|Z\| is not (p .39), so a few extreme days drive it.

- **GARCH, EGARCH and GJR remove the clustering on every asset.** Nothing
  significant is left at lag 22 on either Z² or \|Z\|.
- **BTC HAR-YZ does not.** It leaves more than half of the raw clustering
  (Q 51 vs 89), close to naive. Its forecast is nearly flat for crypto, so it
  cannot follow BTC's volatility swings. This matches its round 1 losses in
  2024–25.
- **ETH is a weak test:** raw r² is only borderline clustered (p .06), so ETH
  cannot separate the models on this check.
- **QQQ:** every model shows a Z² ACF spike near lag 22 (≈ 0.10) that is also in raw
  r². Possibly monthly macro releases. Not investigated.

### C. Distribution (pooled)

| Asset | Skew (models) | Excess kurtosis (models) | % \|Z\| > 3 (normal: 0.27%) |
|---|---|---|---|
| BTC | +0.06 to +0.20 | 2.0–2.8 | 0.2–0.5 |
| ETH | +0.49 to +0.83 | 4.6–7.8 | 0.8–1.2 |
| QQQ | −0.45 to −0.53 | 1.4–1.9 | 0.6–1.0 |
| XAUUSD | −0.47 to −0.52 | 1.5–1.7 | 1.5–2.0 |

- Heavy tails on every asset, even after scaling by the forecast. Normality is not
  required, but a ±2σ normal band would undercover.
- Skew is negative for QQQ and gold (bigger down days) and positive for crypto.
- ETH has the fattest tails (max \|Z\| 5.5–7.5). Gold's left tail is the heaviest
  relative to normal (Z down to about −5).

### Round 2 reading

- **Timing (B):** the GARCH family tracks volatility through time on all four
  assets. HAR-YZ fails on BTC.
- **Level (A):** no model is calibrated everywhere. BTC is over-forecast by every
  model, gold is under-forecast by every model, and QQQ and ETH (GARCH family) are
  close.
- **Zero mean:** safe for f2. The only significant drift (gold 2025) moves mean Z²
  by at most 0.04.
- **Compared with round 1:** the lowest pooled QLIKE does not guarantee
  calibration. GJR has the lowest pooled QLIKE on BTC yet over-forecasts BTC
  variance by ~1.5×.

## Round 3 validation — RMSE on test, by year (2024-01-01 → 2026-09-30)

Date: 2026-11-01

### What was computed

| Item | Setting |
|---|---|
| Score | RMSE = √ mean((h − RV)²), in %² (variance units). Lower is better |
| Realized, forecasts, days | Same as round 1: RV = (100 · ln(C_{t+1} / C_t))² = `r2_next` × 1e4 |
| Role | Secondary metric (validation guide §5): RMSE does not decide model selection by itself |

### RMSE relative to naive (< 1 = better than naive)

| Asset | Year | HAR-YZ | GARCH | EGARCH | GJR | naive RMSE | Best of all five |
|---|---|---:|---:|---:|---:|---:|---|
| BTC | 2024 | 1.014 | 1.013 | 1.007 | 1.001 | 15.01 | **naive** |
| | 2025 | 1.070 | **0.998** | 1.024 | 1.010 | 10.26 | GARCH |
| | 2026 | 0.992 | 0.986 | **0.966** | 0.972 | 17.79 | EGARCH |
| | pooled | 1.016 | 0.999 | 0.994 | **0.991** | 14.37 | GJR |
| ETH | 2024 | 1.007 | 1.005 | **0.993** | 1.003 | 26.29 | EGARCH |
| | 2025 | 0.964 | 0.945 | **0.942** | 0.944 | 37.88 | EGARCH |
| | 2026 | **0.982** | 0.995 | 0.990 | 0.988 | 28.42 | HAR-YZ |
| | pooled | 0.979 | 0.971 | **0.966** | 0.969 | 31.52 | EGARCH |
| QQQ | 2024 | 1.022 | 1.003 | **0.985** | 0.991 | 2.25 | EGARCH |
| | 2025 | **0.931** | 0.997 | 0.961 | 0.958 | 10.87 | HAR-YZ |
| | 2026 | 0.984 | 1.008 | 0.972 | **0.966** | 3.15 | GJR |
| | pooled | **0.937** | 0.998 | 0.962 | 0.960 | 6.89 | HAR-YZ |
| XAUUSD | 2024 | 0.990 | 0.995 | **0.983** | 0.986 | 1.60 | EGARCH |
| | 2025 | 0.985 | 0.978 | 0.964 | **0.961** | 2.96 | GJR |
| | 2026 | **0.937** | 0.941 | 0.957 | 0.946 | 8.27 | HAR-YZ |
| | pooled | **0.946** | 0.949 | 0.959 | 0.950 | 4.77 | HAR-YZ |

### What it implies

- **RMSE barely separates the models.** Every model is within −7% to +7% of naive
  in every year, and most are within ±3%. Even a hindsight constant equal to each
  year's true average RV would score about the same as the models (e.g. BTC 2024:
  14.90 vs 15.0–15.2). Most of the RMSE is the noise of single-day r², not the
  forecast's error.
- **RMSE is decided by a handful of crash days.** The largest 1% of RV days
  (1–3 days in a year) make up 27–86% of GARCH's squared error; QQQ 2025 is 86%
  (April 2025: the sell-off and the +12% rebound day on 9 April). So an RMSE ranking mostly reflects who forecast
  highest just before the few biggest moves.
- **The pooled RMSE leader matches QLIKE on BTC (GJR) and QQQ (HAR-YZ), and
  differs on ETH and gold.**

| Asset | Lowest pooled QLIKE | Lowest pooled RMSE |
|---|---|---|
| BTC | GJR | GJR (0.991, effectively a tie with naive) |
| ETH | HAR-YZ | EGARCH (HAR-YZ is 4th of 4 models) |
| QQQ | HAR-YZ | HAR-YZ |
| XAUUSD | GJR | HAR-YZ (GJR 0.004 behind) |

- **BTC is a tie on RMSE.** Every model is within 2% of naive. The models
  over-forecast BTC variance by ~1.5× (round 2), and RMSE tolerates that
  because over-forecasting on calm days costs little in absolute %².
- **The best-per-year column changes almost every year**, as with QLIKE. No model
  is best in more than one of the three years on any asset except EGARCH on ETH (2 of 3).

### How RMSE differs from QLIKE

| | QLIKE | RMSE |
|---|---|---|
| Error measured as | Ratio RV / h (scale-free) | Difference h − RV in %² |
| Which days dominate | Every day counts about equally | High-volatility days dominate (errors are squared in variance units) |
| Too high vs too low | Penalises a too-low forecast more | Symmetric in absolute terms; too high on a calm day is nearly free |
| Sensitivity to a few extreme RV days | Low | Very high (27–86% of error from 1% of days) |
| Power to separate models on noisy r² | Higher | Low: differences sit inside the noise |
| Role here | Primary ranking | Secondary check |

Both are valid with a noisy target: a forecast equal to the true variance gets
the best expected score under either. They answer different questions. QLIKE
asks whether the forecast is in proportion on a typical day. RMSE asks how close
it was in absolute size, which comes down to the crash days.

### Round 3 reading

- RMSE does not overturn round 1. Where it disagrees (ETH, gold), the gaps are
  ≤ 1.3%, which is noise by RMSE's own standard.
- RMSE adds one thing: on the days that matter most in absolute size, no model
  is clearly better than carrying forward the 22-bar YZ on BTC.
