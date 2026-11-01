# Fracdiff mini guide — how τ and d were chosen

Recap of the NDX reference work in
`py-fracdiff/notebook/analysis/NDX-part1.ipynb` and `NDX-part2.ipynb`
(`NDX-part3.ipynb` is empty). Use this as the starting recipe for P2-M1.

---

## 1. Recipe (what was done)

| Step | Choice |
|---|---|
| Input | `log(close)`, daily NDX bars |
| Method | Fixed-width window FFD (López de Prado, Ch. 5) |
| τ (weight cutoff) | **1e-4**, fixed up front — not tuned |
| d sweep | {0.4, 0.5, 0.6} |
| Stationarity test | ADF, `regression='c', maxlag=1, autolag=None` (Snippet 5.4), α = 0.05 |
| Rule | Pick the **smallest d that rejects the unit root** → keeps the most memory |
| Result | **d = 0.4, τ = 1e-4 → 282-bar window** (current bar + 281 lags) |

### Weights

```python
def ffd_weights(d, tau):
    w = [1.0]                      # lag 0 first
    while True:
        k = len(w)
        nxt = -w[-1] * (d - k + 1) / k
        if abs(nxt) < tau:
            return np.asarray(w)
        w.append(nxt)

w = ffd_weights(0.4, 1e-4)        # len(w) == 282
ffd = np.log(close).rolling(len(w)).apply(lambda x: np.dot(w, x[::-1]), raw=True)
```

τ decides the window length: smaller d → slower weight decay → longer window.

## 2. Evidence (NDX, 2020-02-07 → 2026-10-09, 1,727 common bars)

| Series | Window | ADF stat | p-value | Unit root rejected? |
|---|---:|---:|---:|---|
| Raw close | – | 0.46 | 0.98 | No |
| Log close | – | −0.51 | 0.89 | No |
| FFD log, d=0.4 | 282 | −7.37 | 9e-11 | Yes |
| FFD log, d=0.5 | 200 | −10.97 | 8e-20 | Yes |
| FFD log, d=0.6 | 140 | −15.08 | 8e-28 | Yes |
| FFD raw close, d=0.4 | 282 | −6.57 | 8e-09 | Yes |

- FFD on raw close vs. log close: correlation 0.96 → the input choice matters little for shape; log is scale-free, so prefer it.
- Z-score: `z = (ffd − μ) / σ`, with μ and σ taken over the **full sample** (ddof=0).

### AR(1) half-life of the FFD series

`x_t = c + φ·x_{t−1} + ε`, half-life = `log(0.5)/log(φ)` bars.

| Sample | FFD.raw | FFD.log |
|---|---:|---:|
| Full (2020–2026) | 6.6 bars | 4.9 bars |
| 2026 only | 2.4 bars | 2.5 bars |

Ljung–Box at lag 10 still finds residual autocorrelation, so treat the half-life as rough. It's the decay time of the **feature**, not of the price.

> **Unconfirmed:** the "T=4,5" note in the P2-M1 guide may be this ~5-bar
> half-life. Nothing in the notebooks confirms that.

## 3. P2 decisions

### τ = 1e-4 (confirmed 2026-10-31)

| Item | Setting |
|---|---|
| Method | **Fixed-width window FFD** (López de Prado, Ch. 5): one constant weight vector, cut at τ, applied causally to every bar — not expanding-window FD |
| Assets | BTC, ETH, QQQ, XAUUSD — `data/<SYM>/<SYM>-sorted-1d.parquet`, all from 2019-01 |
| Warm-up | 2019-01 → 2020-12, used only to fill the FFD window |
| Train (d-selection / ADF) | **2021-01-01 → 2023-12-31** (confirmed 2026-10-31); test 2024-01-01 onward |
| τ | **1e-4** |

Why 1e-4 over 5e-4 (evidence: ADF p-value per d, 2021–2023, warm-up from 2019–20):

- **τ hardly moves d.** The smallest d that passes at 5% is about the same for
  both τ values (BTC 0.20, QQQ 0.20, XAUUSD 0.10). τ mainly sets the window length.
- **The warm-up is free.** At τ = 1e-4 the longest window is 527 bars (d = 0.15).
  Warm-up has 731 crypto bars and about 505–517 QQQ/XAUUSD bars, so FFD values
  exist by early 2021. Only QQQ/XAUUSD at d ≈ 0.15 leave about the first month
  of 2021 empty.
- **Less price leaks through.** A truncated window keeps a share of the
  log-price level (the sum of the weights; e.g. at d = 0.2 it is 0.25 at 1e-4
  and 0.33 at 5e-4). Under 5e-4, ETH "passes" at d = 0.05 even though that
  series is almost the log price itself (correlation 1.00), so the pass reflects
  leaked price level rather than real stationarity. At the same d, 1e-4 is less
  tied to price.
- It matches the NDX reference, so results stay comparable.

| d | 0.05 | 0.10 | 0.15 | 0.20 | 0.25 | 0.30 | 0.40 | 0.50 | 0.60 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Window at τ=1e-4 | 362 | 503 | 527 | 497 | 445 | 388 | 282 | 200 | 140 |

### d sweep {0.20, 0.25, 0.30} on train (2026-10-31) — `ffd-d-sweep.ipynb`

Rule: the smallest d with ADF p < 0.01. Log price fails ADF on every asset (p from 0.05 to 0.61).

**Why 1% and not 5% (the NDX reference used 5%)**

- **5% never decided anything in NDX.** Its grid started at d = 0.4, where
  p = 9e-11, so every tested d passed by a huge margin and the threshold didn't
  matter. Our finer grid (0.05–0.60) runs into the boundary, so there the
  threshold does decide the pick.
- **The smallest passing d always sits at the threshold.** At 5% the picks only
  just passed: BTC p = 0.041 and QQQ p = 0.027 at d = 0.20. A d that only just
  passes on train is fragile, and a small change in the data moves it.
- **The 5% pick was unstable.** In the τ comparison, the smallest d passing at
  5% shifted between τ settings, which looked like noise.
- **The sweep runs many tests.** Taking the first pass over many d values (and
  four assets) makes a lucky pass more likely. A stricter bar offsets that.
- **1% is a judgment, not a standard.** It was proposed after seeing the
  2021–23 train results (train data only, so no test leakage). Later, d = 0.20
  failed on 2022–24 (BTC p = 0.30, QQQ p = 0.19), which agrees with the choice,
  but that is test-period hindsight and is not the reason for it.
- **1% is for selecting d, not for monitoring it.** A one-year ADF is weak, so
  holding yearly health checks to 1% flags noise (see the 2023 → 2025 health
  check below). The monitoring threshold is still open; the proposal is 5%
  ("strict to get in, lenient to stay in", so d doesn't flip between reviews).

| Asset | d | Window | ADF p | corr(FFD, log P) |
|---|---:|---:|---:|---:|
| BTC | 0.25 | 445 | 0.006 | 0.86 |
| ETH | 0.25 | 445 | 0.001 | 0.71 |
| QQQ | 0.25 | 445 | 0.004 | 0.88 |
| XAUUSD | 0.20 (grid floor; 0.15 also passes) | 497 | 0.0002 | 0.93 |

At d = 0.20 BTC (p = 0.041) and QQQ (p = 0.027) pass only at 5%, and ETH does
not pass at 1% (p = 0.011). **Decision: one shared d = 0.25 for all four assets** (window 445). At 0.25 XAUUSD has p < 0.0001 and corr 0.89. Not yet checked: whether d holds after 2023. In the
plot, QQQ and XAUUSD FFD drift upward through 2024–26.

### Warm-up end at d = 0.25 (445-bar window)

The first FFD value appears on the 445th bar, i.e. after 444 bars of history:

| Asset | Data starts | First FFD value | Calendar span |
|---|---|---|---|
| BTC | 2019-01-01 | 2020-03-20 | ~1.2 yr (trades every day) |
| ETH | 2019-01-01 | 2020-03-20 | ~1.2 yr |
| QQQ | 2019-01-02 | 2020-10-06 | ~1.8 yr (weekdays only) |
| XAUUSD | 2019-01-02 | 2020-09-21 | ~1.8 yr |

- Warm-up finishes before train starts (2021-01-01) for every asset, so all
  train bars have a value. FFD values from the warm-up end to 2020-12-31 exist
  but are not used for d-selection.
- Each FFD value depends only on its own last 445 bars. Dropping old history
  (e.g. 2019) does not change any later FFD value; trimming history only matters
  for the Z reference (μ/σ) and for which period ADF is tested on.

### Z reference = expanding, anchored at warm-up end — `ffd-z-plot1.ipynb`

`Z_t = (FFD_t − μ_t) / σ_t`, where μ_t and σ_t use **every FFD value from the anchor up to and including bar t** (ddof = 0). The start is fixed; the end moves forward with each bar.

| Reference type | μ/σ window on day t | Status |
|---|---|---|
| Fixed (train-only) | 2021-01-01 → 2023-12-31, the same for every day | Used only as a one-off check (gave XAUUSD Z ≈ +6 in 2024–26); not in any notebook |
| **Expanding** | anchor → t | **Current, used in `ffd-z-plot1.ipynb`** (3rd panel; the 4th panel shows rolling 445 bars next to it) |
| Rolling | t − N → t | Candidate, plotted in `ffd-z-rolling-plot-test.ipynb` (N = 100, 200, 445 bars, 1y, 2y); N not chosen. See next section |

- Anchor = each asset's first FFD value (warm-up end table above): BTC/ETH 2020-03-20,
  QQQ 2020-10-06, XAUUSD 2020-09-21. Z is left empty for the first 60 FFD bars
  (`Z_MIN`), so the first Z is BTC/ETH 2020-05-18, QQQ 2020-12-30, XAUUSD 2020-12-11.
- Causal: Z_t uses no data after t.
- Early Z is noisy because μ/σ rest on a few months of data (BTC Z ≈ +4 in early 2021).
- The anchor period never leaves μ/σ, so after a lasting level shift Z re-centres
  only slowly. FFD at d = 0.25 keeps about 18% of the log-price level (weight
  sum 0.178), so a lasting price move shifts the FFD level.
- Open: keep expanding (reset the anchor only on a d / data / timeframe change),
  or switch to rolling. Rolling answers "vs the last N years" and forgets real
  extremes after N years. Choose based on Stage B, not on how the 2024+ charts look.

### Z reference = rolling (candidate) — `ffd-z-rolling-plot-test.ipynb`

`Z_t = (FFD_t − μ_t) / σ_t`, where μ_t and σ_t use **only the FFD values in the last N calendar days up to and including bar t** (ddof = 0). Both ends of the window move forward, so old data drops out.

| Setting | Value |
|---|---|
| FFD | Same as above: fixed-width window, τ = 1e-4, d = 0.25, 445 bars |
| Anchor | Same as expanding: each asset's first FFD value |
| N | **445 bars (= FFD window)**, **100 bars**, **200 bars**, **1 year (`365D`)**, **2 years (`730D`)**; not chosen yet |
| Layout | Five comparison sets, Z only, one panel per asset: (1) expanding vs 445; (2) expanding vs 1y, 2y; (3) expanding vs 100, 200; (4) 445 vs 100, 200; (5) 100, 200 vs 1y, 2y |
| Burn-in | 60 FFD bars (`Z_MIN`), same as expanding |
| Plot range | Data start → 2022-12-31, same as `ffd-z-plot1.ipynb` |

How it works:
- **N = 445 bars (the FFD window) adds no new parameter.** It follows d and τ, so
  there is nothing to tune. It counts **bars**, like FFD: about 1.2 years for
  crypto and 1.8 years for QQQ/XAUUSD. Matching the two windows is a convenience,
  not a derivation: the FFD window is how far back the weights reach, and the Z
  window is what counts as "normal". Z then reaches back about 890 price bars in
  total (445 FFD values, each using a 445-bar FFD window).
- **N = 100 / 200 bars** are short fixed bar counts: 100 bars ≈ 3.3 months of
  crypto or ≈ 4.8 months of QQQ/XAUUSD; 200 bars ≈ 6.6 or ≈ 9.5 months.
- **N = 1y / 2y count calendar days.** 1 year ≈ 365 crypto bars, ≈ 252 QQQ bars
  and ≈ 258 XAUUSD bars; 2 years ≈ 730 / 503 / 516 bars. Every asset looks back
  over the same span of time.
- **Before the window fills, it holds everything since the anchor** (it behaves
  like an expanding reference).

  | Asset | Anchor | 100 bars full | 200 bars full | 445 bars full | 1y full | 2y full |
  |---|---|---|---|---|---|---|
  | BTC / ETH | 2020-03-20 | 2020-06-27 | 2020-10-05 | 2021-06-07 | 2021-03-20 | 2022-03-20 |
  | QQQ | 2020-10-06 | 2021-03-01 | 2021-07-22 | 2022-07-13 | 2021-10-06 | 2022-10-06 |
  | XAUUSD | 2020-09-21 | 2021-02-09 | 2021-06-30 | 2022-06-10 | 2021-09-21 | 2022-09-21 |

  In the 2022 plot, the 2y Z is truly rolling for only the last ~3 months of
  QQQ/XAUUSD. Most of what's shown is still expanding.
- **Causal.** Z_t uses no data after t.
- **Trade-off.** Rolling forgets old levels after N, so Z re-centres after a
  lasting level shift (the problem with expanding). It also forgets real extremes:
  after a trend lasting N, rolling Z calls it normal. N defines what "normal" means.

First look (2022 yearly mean Z):

| Asset | Expanding | 100 bars | 200 bars | 445 bars | 1y | 2y |
|---|---:|---:|---:|---:|---:|---:|
| BTC | −0.63 | −0.50 | −0.92 | −1.27 | −1.19 | −0.89 |
| ETH | −0.29 | −0.50 | −0.82 | −1.18 | −1.17 | −0.63 |
| QQQ | −1.58 | −0.71 | −1.14 | −1.53 | −1.26 | −1.57 |
| XAUUSD | −0.32 | −0.01 | −0.15 | −0.27 | −0.16 | −0.30 |

- **Very short windows (100 bars) re-centre fastest.** Z stays closest to 0 and
  absorbs a drawdown within months (QQQ 2022: −0.71 vs −1.58 expanding).
- **Medium windows (445 bars, 1y) push the 2022 crypto drawdown lowest.** Their
  reference holds mostly the high 2021 levels, while expanding still includes 2020.
- The 445-bar window tracks 1y for crypto (445 bars ≈ 1.2 years) and 2y for
  QQQ/XAUUSD (445 bars ≈ 1.8 years), because it counts bars, not days.
- Choose N on train (2021–2023) or by Stage B, not by how 2024+ looks.

### Z reference for the feature: expanding or rolling 445 bars (decided 2026-10-31)

Also in the last cell of `ffd-z-rolling-plot-test.ipynb`.

**Use either expanding Z or rolling Z over 445 bars (= FFD window). Both go into
Stage B. 100 / 200 bars and 1y / 2y are dropped.**

| Reference | Why it stays | Weak point |
|---|---|---|
| **Expanding** (anchor → t) | No free parameter; stable; Z means "vs everything since the anchor" | Re-centres slowly after a lasting level shift; early Z is noisy |
| **Rolling 445 bars** (= FFD window) | No free parameter (follows d, τ); re-centres after a level shift; Z judges FFD over the same span its memory covers | 445 bars ≈ 1.2y crypto vs ≈ 1.8y QQQ/XAUUSD; fills late (crypto 2021-06-07, QQQ 2022-07-13, XAUUSD 2022-06-10) |

- **Dropped: 100 / 200 bars.** They judge a 445-bar-memory feature against only
  3–9 months, which turns Z into a short-term oscillator, closer to RSI or
  momentum, the baselines it must beat. And 100/200 have no basis beyond the plots.
- **Dropped: 1y / 2y.** They add a free parameter with no advantage over 445 bars.
- **Expanding anchor reset:** only on a setup change (new d, data source or
  timeframe). Never in reaction to Z drifting.
- **Rolling 445 starts late. Cost accepted as is (2026-11-01).** The window is
  not full until 2021-06-07 for crypto, 2022-07-13 for QQQ and 2022-06-10 for
  XAUUSD. Before that, rolling 445 equals expanding, so the early part of train
  (2021 to mid-2022 for QQQ/XAUUSD) gives the same Z under both references.
  Stage B can only separate the two on data after those dates.
- FFD itself is the same on every asset: one 445-bar window (τ = 1e-4, d = 0.25).

### Maintenance rule — when to re-check ADF, τ, d and Z (decided 2026-10-31, d rule revised 2026-11-01)

Also in the last cell of `ffd-z-plot1.ipynb` (updated to match). The original
2026-10-31 version raised d on a persistent ADF failure. **That part is removed:**
see the d row below and [ADF failure is a sign of regime](../reports/r1-fracdiff-adf-failure.md).

| What | When | Action |
|---|---|---|
| **ADF** | Every year, on the last 1 year and the last 2–3 years; also track FFD mean/σ | **Warning label / regime sign only.** A failure, even a persistent one, does not change d. It marks a trend regime in which Z does not revert to its centre. |
| **τ** | Only if the setup changes: bar timeframe, new asset with a short history, FFD method | Otherwise keep τ = 1e-4. τ was never tuned to market behaviour. |
| **d** | **Keep d = 0.25.** No re-selection triggered by ADF failure (removed 2026-11-01) | Re-selecting d for a structural change is possible later, but "structural change" is not defined yet. If d ever changes: re-select on past data only, start a new Z anchor, retrain; old and new Z are not comparable. |
| **Z reference** | ADF passes but Z sits off-centre for long stretches | Fix the reference (e.g. rolling Z). Keep d. |

- An ADF failure changes nothing about d. Why: gold failed through the 2024–25
  rally and passed again in 2025–26 Q3 with d unchanged. Raising d at end-2024
  (0.30) and end-2025 (≈ 0.40) would have chased a trend that then ended.
- During a failure, don't read Z as a mean-reversion signal.
- Set this rule before looking further at 2024+, so the response isn't tuned to the test period.

### ADF health check 2023 → 2025 (d = 0.25, τ = 1e-4) — `ffd-z-plot2.ipynb`

The notebook plots price, FFD and **rolling-445 Z only** for 2023-01-01 → 2025-12-31.
Values are computed causally from 2019 data. ADF runs on FFD, not Z. 2023 is the
last train year and 2024–25 are test years. d is not re-selected here.

ADF p-values on FFD:

| Asset | Train 2021–23 | 2023 | 2024 | 2025 | 2023–24 | 2024–25 | 2023–25 |
|---|---:|---:|---:|---:|---:|---:|---:|
| BTC | 0.006 | 0.016 | 0.028 | 0.016 | 0.033 | 0.000 | 0.005 |
| ETH | 0.001 | 0.000 | 0.010 | 0.082 | 0.001 | 0.001 | 0.000 |
| QQQ | 0.004 | 0.040 | 0.000 | 0.175 | 0.008 | 0.002 | 0.005 |
| XAUUSD | 0.000 | 0.004 | 0.067 | 0.088 | 0.110 | 0.264 | 0.458 |

- **XAUUSD: d = 0.25 does not hold.** FFD trends up with gold's 2024–25 rally,
  and ADF fails on every 2–3-year window and in both 2024 and 2025. That is a
  persistent failure at either 1% or 5%. This corrects an earlier reading that
  gold's problem was only a stale Z level: on 2023–25 the FFD itself fails.
  **Follow-up (`ffd-z-plot3.ipynb`):** with d = 0.25 kept, gold passes again on
  2025–26 Q3 (p ≈ 0.005) after the rally ended, so the failure was a regime, not
  a wrong d. d stays at 0.25 (maintenance rule above).
- **BTC is flagged only at 1%.** Single years score p = 0.016–0.028, close to its
  single train years (0.02–0.04), and the 2024–25 and 2023–25 windows pass
  (p ≤ 0.005). At 5% nothing fails.
- **ETH and QQQ** have single-year dips only (2025). All 2–3-year windows pass at 1%.
- **Rolling Z doesn't fix a trending FFD.** Gold's rolling-445 Z sits at about
  +1 to +2 through 2024–25 (25–27% of days above 2).
- **Open:** the maintenance rule does not set the ADF threshold. 1% on one-year
  windows flags BTC on noise; 5% flags only gold.

## 4. Pitfalls — fix these before using fracdiff in P2

1. **Leakage:** d and the Z-score μ/σ were both fit on the full history. For P2,
   choose d **on the training window only**, and use an expanding (causal)
   Z reference.
2. **Coarse d grid:** nothing below 0.4 was tested, so 0.4 isn't proven to be
   the minimum. Sweep finer next time, e.g. 0.1–0.6 in steps of 0.05.
3. **Warm-up:** a 282-bar window means the first 281 bars have no value. Shorter
   histories (XAUT, ETH) lose a larger share of their data.
4. **Stationarity ≠ mean reversion of price.** Z ≈ −1 can persist while price
   keeps falling. Never read negative Z as "buy" or positive Z as "sell".
5. ADF rejection is evidence against a unit root under this specification,
   not proof of stationarity.

## 5. Re-run checklist (new asset or new period)

1. Take log close and check that timestamps are sorted and unique.
2. Split train/test **first**.
3. On train: sweep d with τ = 1e-4 (see §3) and run ADF with the settings above.
4. Pick the smallest d that rejects at **1%** (p < 0.01), and note the window length.
   (The NDX reference project in §1–2 used 5%; P2 uses 1%.)
5. Apply FFD causally to the full series and drop the warm-up bars.
6. **Check that d holds over time:** run ADF (same settings) and track the FFD
   mean/σ on a rolling one-year window. See P2-M1 guide, Stage A, and the
   maintenance rule in §3 for when to act.
   - FFD fails ADF in a period → the market is in a trend regime that d can't
     absorb → **keep d**; treat it as a regime sign and don't expect Z to revert
     during it (see the maintenance rule in §3).
   - FFD passes but its level or spread shifts (e.g. Z stuck near −1) → the
     Z reference is stale → change the anchor or use an expanding/rolling window.
   - The anchor applies only to Z; FFD has none. After a d change, old and
     new Z values aren't comparable. ADF on one year of data is a weak test.
7. Z-score with an expanding (or train-fixed) μ/σ, never full-sample.
8. Plot price / FFD / Z together, then go to the predictive tests
   (P2-M1 Stage B).
