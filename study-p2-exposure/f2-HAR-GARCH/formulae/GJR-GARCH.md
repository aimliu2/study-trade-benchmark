Like EGARCH, the GJR-GARCH model (named after its creators Glosten, Jagannathan, and Runkle) was designed to fix standard GARCH's biggest blind spot: its inability to see that bad news causes a much bigger volatility spike than good news.
However, while EGARCH uses complex natural logarithms to handle this asymmetry, GJR-GARCH keeps things simple. It takes the standard GARCH(1,1) formula and adds a mathematical "on/off switch" (an indicator function) that activates only when yesterday's return was negative.

## 1. The GJR-GARCH Formula Comparison

Let's look at the formulas side-by-side to see exactly how GJR-GARCH modifies the standard version:

Standard GARCH(1,1):

$$\sigma _{t}^{2}=\omega +\alpha \epsilon _{t-1}^{2}+\beta \sigma _{t-1}^{2}$$

GJR-GARCH(1,1):

$$\sigma _{t}^{2}=\omega +\alpha \epsilon _{t-1}^{2}+\gamma \epsilon _{t-1}^{2}I_{t-1}+\beta \sigma _{t-1}^{2}$$

The "On/Off Switch" ($I_{t-1}$):

The variable $I_{t-1}$ is a dummy variable that looks at yesterday's shock ($\epsilon _{t-1}$):
• If yesterday was a down day ($\epsilon_{t-1} < 0$), the switch turns ON ($I_{t-1} = 1$).
• If yesterday was an up day ($\epsilon_{t-1} \ge 0$), the switch turns OFF ($I_{t-1} = 0$).

## 2. The Direct Impact on Volatility

Because of this switch, market shocks are funneled into two completely different paths depending on whether the day was green or red:
• If yesterday was a Good Day (Green):
The asymmetry term disappears completely because multiplying by zero cancels it out. Tomorrow's variance is driven strictly by alpha:
$\text{Impact}=\alpha \epsilon _{t-1}^{2}$
• If yesterday was a Bad Day (Red):
The switch turns to 1, meaning both parameters are added together. Tomorrow's variance gets a double-whammy penalty:
$\text{Impact}=(\alpha +\gamma )\epsilon _{t-1}^{2}$
(These are the shock contributions only; ω and βσ²_{t−1} are added on both days.)
If γ > 0 (typical for stock markets) **and statistically significant**, a down move raises volatility more than an up move of the same size. An estimate alone doesn't prove it. γ may also be negative (up moves raise volatility more); the model only needs α + γ ≥ 0.

**Stationarity / persistence** (corrected 2026-11-01; missing before): with symmetric shocks, I = 1 half the time on average, so persistence = α + γ/2 + β < 1, and the long-run variance = ω / (1 − α − γ/2 − β).

## 3. Key Differences: GARCH vs. GJR-GARCH vs. EGARCH


|Feature	|Standard GARCH(1,1)|	GJR-GARCH(1,1)|	EGARCH(1,1)|
|--|--|--|--|
|Asymmetry (Leverage Effect)?|	❌ No. Treats up and down days identically.|	Yes. Adds γε² on down days.|	Yes. Uses the sign and magnitude of shocks separately.|
|How it treats Shocks|	Squared ($\epsilon _{t-1}^{2}$)	|Squared ($\epsilon _{t-1}^{2}$)|	Absolute value & linear ratio|
|Target Variable|	Raw Variance ($\sigma _{t}^{2}$)|	Raw Variance ($\sigma _{t}^{2}$)|	Log Variance ($\ln(\sigma_t^2)$)|
|Constraints|	ω > 0, α ≥ 0, β ≥ 0, α + β < 1|	ω > 0, α ≥ 0, **α + γ ≥ 0** (γ may be negative), β ≥ 0, α + γ/2 + β < 1|	None for positivity; \|β\| < 1 for stationarity|


## 4. How to Fit GJR-GARCH in Python

In Python’s arch library, GJR-GARCH isn't a completely separate model name. Instead, you use the standard 'Garch' framework but set the parameter o=1 (which stands for asymmetric order).
```python
import numpy as np
import pandas as pd
from arch import arch_model

# Assume df['Return'] is your calculated log returns multiplied by 100
# In arch: p=1 -> alpha (shock / ARCH term), o=1 -> gamma (GJR asymmetry), q=1 -> beta (lagged variance / GARCH term)
# (corrected 2026-11-01: the original comment had p and q swapped)
# dist='normal' is the regular case; switch to 't' only if the fit fails (GARCH.md §3)
gjr_model = arch_model(df['Return'], p=1, o=1, q=1, vol='Garch', dist='normal')

# Fit the model
res_gjr = gjr_model.fit(disp='off')

# Print the results to see the 'gamma' coefficient
print(res_gjr.summary())
```

## 5. How to read the GJR-GARCH Summary

When looking at your Python terminal printout:
- Find the row labeled gamma[1].
- If gamma[1] is positive and its p-value is small (e.g. < 0.05), the data show a leverage effect.
- To find out exactly how much worse a market crash is compared to a market pump, calculate α + γ to see the total crash impact versus just α for the pump impact.
Now that you have seen standard GARCH, EGARCH, and GJR-GARCH, would you like to run a quick backtest script to see which of these three models historically gives the most accurate volatility forecasts for your specific OHLC data?
