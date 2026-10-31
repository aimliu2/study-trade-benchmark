# ADF failure is a sign of regime, not a reason to drop d

Date: 2026-11-01
Setting: fixed-width window FFD on `log(close)`, daily, τ = 1e-4, **d = 0.25** for
BTC, ETH, QQQ and XAUUSD (445-bar window), with rolling Z over 445 bars as the
feature. d was chosen on 2021–2023 (smallest d with ADF p < 0.01). See
[fracdiff README](../m1-fracdiff/README.md) §3.

## Conclusion

**A temporary ADF failure on FFD does not permanently invalidate d.** It marks a
regime: a strong, lasting trend that d = 0.25 cannot absorb. When the trend ends,
FFD passes again with no change to d. During the failure, **Z stops reverting to
its centre**, so any use of Z that expects mean reversion breaks for that period.

## Evidence — XAUUSD with d = 0.25 held fixed

| Period | What gold did | ADF on FFD (d = 0.25) | Rolling Z |
|---|---|---|---|
| Train 2021–23 | Range-bound | Pass (p < 0.001) | Around 0 |
| 2024–25 | Strong rally | **Fail**: 2024 p ≈ 0.067, 2025 p ≈ 0.088, 2024–25 p ≈ 0.26 | Stuck at about +1 to +2 for two years |
| 2025 → 2026 Q3 | Peak 2026-01-28 (≈ 5,420), back to ≈ 4,160 by September | **Pass again**: p ≈ 0.005 | Fell from about +2 to about −1 |

Sources: [ffd-z-plot2](../m1-fracdiff/ffd-z-plot2.ipynb) (2023–25 health check),
[ffd-z-plot3](../m1-fracdiff/ffd-z-plot3.ipynb) (d = 0.25 held to 2026 Q3).

## Raising d would have chased the trend

Simulated review on 2024-12-31 ([ffd-z-plot-xau03](../m1-fracdiff/ffd-z-plot-xau03.ipynb)),
re-running the selection rule on the last 3 years:

| Review | d asked for | What happened next |
|---|---|---|
| End-2024 (data 2022–24) | 0.30 (only just passes, p ≈ 0.009) | Failed again in 2024–25 (p ≈ 0.079) |
| End-2025 (data 2023–25) | ≈ 0.40 | The trend ended in 2026; d = 0.25 passed again |

- d = 0.30 is almost the same feature as 0.25: FFD and Z both correlate at 0.99.
- Each change costs a retrain and a Z reset. Two changes would have followed a
  trend that then reversed.

## Why it happens

FFD at d = 0.25 keeps about 18% of the log-price level (weight sum 0.178). That
retained level is the memory the feature is meant to keep. In a strong, lasting
trend the retained level trends too, so ADF fails. When the trend stops, FFD
comes back and passes. This is the expected behaviour of a memory-keeping
feature, not a fault.

## What a failure means — and doesn't

| Means | Doesn't mean |
|---|---|
| Z's pull back toward the centre is suspended (Z can stay high or low for a long time) | d is permanently wrong |
| The market is in a trend regime strong enough that d = 0.25 can't absorb it | The feature is broken or has lost its predictive value |
| Sometimes nothing: one-year ADF is a weak test (BTC single years p = 0.02–0.03 are noise) | That passing ADF guarantees Z or price will revert |

- Evidence so far is clearest for **rallies** (gold 2024–25). For drops it is
  weaker: BTC in 2022 was borderline (p ≈ 0.04) rather than failing.

## Implications

1. **Keep d = 0.25 through temporary failures.** Re-select d only for a structural
   change, not for a trend phase. The yearly ADF check stays as a warning label.
2. **Don't read Z as a mean-reversion signal during a failure.** That is where
   expecting reversion from Z hurts.
3. **Whether a model is hurt depends:**
   - Is rolling Z still inside its training range? Gold yes (0% outside);
     QQQ 2026 partly not (7% of days above its train max of +2.35).
   - Did training contain trend regimes? Crypto yes (2021 rally, 2022 drop);
     gold no (2021–23 was calm), so gold is the riskier case.
   - Model type: tree-based models cap at the edge of what they've seen; linear
     models extend the trend.
   - Only the model's out-of-sample error answers this (Stage B).
4. **Possible regime feature.** Since a failure marks "trend regime, don't expect
   Z to revert", a rolling ADF statistic or a trend-persistence measure could be
   a candidate feature. It is noisy and overlaps with momentum / trend-strength
   features, so it must prove incremental value in Stage B like any other.

## Open

- ADF threshold for the yearly check (proposal: 5%; 1% stays for selecting d).
- What counts as a "structural change" that justifies re-selecting d. Not yet defined.
