# Fracdiff as a model feature — good to know

Notes from the XAUUSD 2024–25 case (`ffd-z-plot2.ipynb`, `ffd-z-plot-xau03.ipynb`).
Setting: fixed-width window FFD on `log(close)`, τ = 1e-4, d = 0.25, rolling Z over
445 bars (= FFD window). See `README.md` §3 for how these were chosen.

## Does ADF matter?

| Use | Role of ADF |
|---|---|
| **Choosing d** | **Yes.** It makes sure FFD isn't just price under another name. Without it, a model can learn a link to the price level that later turns out to be spurious. Use 1% here. |
| **Running check (model live)** | **Only a proxy.** ADF asks "is there a unit root?", not "can the model still use this?". A 1% vs 5% result (e.g. gold 2025: p ≈ 0.023 at d = 0.30) says nothing about whether the model still works. |

## What actually matters to the model

| Risk | Better check |
|---|---|
| Inputs leave the training range | Share of days where Z falls outside its train range. For gold in 2024–25 it was 0%, even though FFD failed ADF. |
| Z's distribution drifts | Rolling mean and σ of Z compared with train |
| The feature-to-target link changes | The model's own error on recent data. Only this one shows real harm |

- Raw FFD for gold was outside its train range on 49% of days in 2024 and 100% of
  days in 2025. Rolling Z stayed inside it (train range −3.1 to +4.1). Rolling Z
  keeps the input in range; raw FFD does not.
- What changes in a trend is the **meaning** of Z: in train, Z ≈ +1.5 was a
  short-lived high; in 2024–25 it was a lasting trending-up state. Whether that
  hurts is a model question, not an ADF question.

## Bounding the input

- **Rolling Z** already keeps values in range. That's why gold stayed inside it.
- **Clip** (e.g. at ±4, about gold's train extreme) as a cheap guard against rare
  spikes. If many days pile up at the clip, Z has turned into an on/off flag, and
  that pile-up is itself a warning.
- **Percentile rank** within the rolling window is bounded between 0 and 1 by
  construction and is robust to outliers. Worth considering if you want a fully
  bounded input.
- Clipping matters more for raw FFD or expanding Z than for rolling Z.

## Changing d doesn't change much (gold, end-2024 review)

- Re-running the selection rule on 2022–24 moves gold from d = 0.25 to 0.30
  (388-bar window). The new d only just passes (p ≈ 0.009).
- The two features are nearly identical: FFD correlates at 0.99 and so does Z
  (mean |Z diff| ≈ 0.15–0.19).
- d = 0.30 starts failing in 2025, the first year after the change (2024–25
  p ≈ 0.079), and the end-2025 review would ask for about 0.40. Raising d lags
  the trend by one review each time.
- Each change still costs a retrain and a Z reset.

## Which period to test at a review

- Use the **last 3 years** at the review date (e.g. 2022–24 at end-2024), the same
  length as the original train window.
- Not all history: over 2019–2024 gold passes even at d = 0.25 (p ≈ 0.008),
  because the quiet years outweigh the rally, so it would never flag the change.

## Working recommendation

- Use ADF only when choosing d.
- For the running check, watch the share of Z outside its train range, the drift
  in Z, and the model's error.
- Clip Z at about ±4 as a guard.
- For a lasting trend (gold 2024–25), prefer keeping d = 0.25 and watching the
  model over raising d.
