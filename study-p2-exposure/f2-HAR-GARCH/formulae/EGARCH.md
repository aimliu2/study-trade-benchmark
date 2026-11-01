The EGARCH (Exponential GARCH) model differs from standard GARCH(1,1) by solving its biggest real-world flaw: asymmetry (the leverage effect).
In standard GARCH, the shock term is squared ($\epsilon _{t-1}^{2}$). Because it is squared, a positive shock (+5% gain) and a negative shock (-5% crash) have the exact same impact on tomorrow's volatility.
In real stock markets, this is completely unrealistic. Bad news (a crash) panics investors and drives volatility up much faster than good news. EGARCH handles this by modeling the log of variance and tracking the sign (positive or negative) of the shock.

### 1. The EGARCH Formula vs. GARCH(1,1)

Instead of modeling variance ($\sigma _{t}^{2}$) directly, EGARCH models the natural logarithm of variance ($\ln(\sigma_t^2)$). This is Nelson's (1991) EGARCH(1,1) and matches `arch`'s parameterization. Note: $\sqrt{2/\pi}$ is E|z| for a **normal** z only (with Student's t it is not exact):

$$\ln (\sigma _{t}^{2})=\omega +\beta \ln (\sigma _{t-1}^{2})+\alpha \left(\left|{}\frac{\epsilon _{t-1}}{\sigma _{t-1}}\right|{}-\sqrt{\frac{2}{\pi }}\right)+\gamma \left(\frac{\epsilon _{t-1}}{\sigma _{t-1}}\right)$$

Here is how the components directly compare:

|Feature	|Standard GARCH(1,1)	|EGARCH	|Why EGARCH does it|
|--|--|--|--|
|Target Metric|	$\sigma _{t}^{2}$ (Raw Variance)|	$\ln(\sigma_t^2)$ (Log Variance)|	No sign constraints needed on ω, α, γ. Because $e^{x}$ is always positive, variance can never accidentally drop below zero during optimization. (Corrected 2026-11-01:) stationarity still needs \|β\| < 1; half-life = ln 0.5 / ln β.|
|Shock Impact|	$\alpha \epsilon_{t-1}^2$ (Size only)|	$\alpha \left\vert{} \frac{\epsilon_{t-1}}{\sigma_{t-1}} \right\vert{}$ (Magnitude)|	Measures how big the market surprise was, regardless of direction. It standardizes the shock by dividing it by current volatility.
|Asymmetry Term	|None|	$\gamma \left( \frac{\epsilon_{t-1}}{\sigma_{t-1}} \right)$ (Direction / Leverage)|	Captures the sign of the shock. If γ is negative **and statistically significant**, the data show that bad news increases volatility more than good news (an estimate alone doesn't prove it; corrected 2026-11-01).|


### 2. How the Leverage Effect (γ) Works

The γ (gamma) parameter is the asymmetric heart of the model.
• If γ < 0 (which is typical for equities): Yesterday's negative return multiplies a negative by a negative, creating a positive boost to tomorrow's log variance.
• Yesterday's positive return retains a negative impact, muting the spike in volatility.

### 3. How to Fit EGARCH in Python

Switching from GARCH to EGARCH in the arch library is simple. You change the vol parameter from 'Garch' to 'EGARCH' **and add `o=1`** for the asymmetry term.

```python
import numpy as np
import pandas as pd
from arch import arch_model

# Assume df['Return'] is already scaled (multiplied by 100)
# Switch vol='Garch' to vol='EGARCH'.
# Corrected 2026-11-01: o=1 is required for the gamma (asymmetry) term. Without it arch fits
# only omega, alpha[1], beta[1] and there is no gamma[1] to read.
# dist='normal' is the regular case; switch to 't' only if the fit fails (GARCH.md §3).
egarch_model = arch_model(df['Return'], p=1, o=1, q=1, vol='EGARCH', dist='normal')

# Fit the model
res_egarch = egarch_model.fit(disp='off')

# View the parameters (Look closely at 'gamma[1]')
print(res_egarch.summary())
```

### 4. How to Read the EGARCH Summary

When you review the summary table, look for the row labeled gamma[1]:
- If gamma[1] is statistically significant and negative, you have confirmed the leverage effect—bad news creates more volatility in your asset than good news.
- If gamma[1] is close to zero, the asset reacts symmetrically to shocks (common in some currency markets), and a standard GARCH model might suffice.

