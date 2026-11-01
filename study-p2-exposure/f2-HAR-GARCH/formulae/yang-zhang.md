
# Yang-Zhang Volatility Estimator Guide

The Yang-Zhang volatility estimator (introduced in 2000) is a historical volatility measure for OHLC (Open, High, Low, Close) price data. It is widely considered the gold standard of range-based estimators because it is drift-independent and explicitly accounts for overnight price gaps.

## 1. The Core Formula

The daily Yang-Zhang variance 
$$\sigma _{YZ}^{2}$$
is a weighted combination of overnight variance, open-to-close variance, and the range-based Rogers-Satchell variance:

$$\sigma _{YZ}^{2}=\sigma _{o}^{2}+k\cdot \sigma _{c}^{2}+(1-k)\cdot \sigma _{RS}^{2}$$
To get the daily volatility (standard deviation), take the square root:
$$\sigma _{YZ}=\sqrt{\sigma _{YZ}^{2}}$$

## 2. Component Breakdowns & Formulas

For a lookback window of n trading days, the individual elements are calculated as follows:

### A. Overnight Return Variance $\sigma _{o}^{2}$

Measures the variance of the price gaps between the previous day's close and today's open.
$$\sigma _{o}^{2}=\frac{1}{n-1}\sum _{i=1}^{n}(o_{i}-\={o})^{2}$$
• Log Overnight Return $o_{i}$: $$\ln\left(\frac{\text{Open}_i}{\text{Close}_{i-1}}\right)$$
• Mean Overnight Return ō: $$\frac{1}{n}\sum o_i$$

### B. Open-to-Close Variance $\sigma _{c}^{2}$

Measures the variance of the price movement from the open to the close of the same trading session.
$$\sigma _{c}^{2}=\frac{1}{n-1}\sum _{i=1}^{n}(c_{i}-\={c})^{2}$$
• Log Intraday Return ($$c_{i}$$): $$\ln\left(\frac{\text{Close}_i}{\text{Open}_i}\right)$$
• Mean Intraday Return (c̄): $$\frac{1}{n}\sum c_i$$

### C. Rogers-Satchell Variance $\sigma _{RS}^{2}$

A range-based variance estimator that captures intraday price action (High and Low) and remains valid even when the asset has a non-zero drift (a strong trend).
$$\sigma _{RS}^{2}=\frac{1}{n}\sum _{i=1}^{n}\left[\ln \left(\frac{H_{i}}{C_{i}}\right)\ln \left(\frac{H_{i}}{O_{i}}\right)+\ln \left(\frac{L_{i}}{C_{i}}\right)\ln \left(\frac{L_{i}}{O_{i}}\right)\right]$$
• Where $$O_i, H_i, L_i, C_i$$ represent the Open, High, Low, and Close prices for day i.

### D. The Weighting Constant (k)

An analytical weight optimized by Yang and Zhang to minimize the overall estimator variance over your lookback window n:
$$k=\frac{0.34}{1.34+\frac{n+1}{n-1}}$$

## 3. Why It Matters: Key Properties

- Overnight Gap Capture: Standard range estimators (like Parkinson or Garman-Klass) assume continuous trading and ignore overnight jumps. Yang-Zhang bridges this gap.
- Drift-Independent: Range estimators such as Parkinson and Garman-Klass are biased when a stock trends steadily up or down (price drift). Yang-Zhang is not, because its overnight and open-to-close parts are demeaned and Rogers-Satchell is drift-free. (Corrected 2026-11-01: the original blamed close-to-close estimators; a demeaned close-to-close variance is already drift-independent, just inefficient.)
- Maximum Efficiency: In theory it is up to about 14 times more efficient than the close-to-close estimator, so it needs much less history for the same accuracy. (Corrected 2026-11-01: this is a best case under ideal assumptions, i.e. a continuous, frictionless price path inside the session. Real data with discrete ticks and jumps gets less.)

# 4. Annualization

To convert your daily Yang-Zhang volatility to an annualized metric, multiply the daily variance by the number of trading periods in a year (typically 252 for daily stock data; **365 for 24/7 crypto**, added 2026-11-01) before taking the square root:
$$\sigma _{\text{annual}}=\sqrt{\sigma _{YZ}^{2}\times 252}$$
Would you like a copy-pasteable Python script using pandas and numpy to calculate this over a rolling window, or should we look at an example table calculation?
