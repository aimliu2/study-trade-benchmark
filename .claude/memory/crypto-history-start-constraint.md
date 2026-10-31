---
name: crypto-history-start-constraint
description: BTC/ETH daily data (Bybit spot USDT) starts 2021-07-05; Binance-before-2022-01-01 stitch passed the overlap check on 2026-10-31
metadata:
  type: project
---

BTC and ETH daily bars in `data/` come from Bybit spot USDT pairs (symlinked from py-historical-bar-replayer/data-spot). They start on 2021-07-05, when Bybit spot launched. QQQ and XAUUSD start on 2019-01-02.

As of 2026-10-31 the user proposes stitching Binance spot USDT history before a year boundary (likely 2022-01-01) onto the Bybit series, excluding volume because it is venue-specific. This was first accepted as a hard no-stitch constraint, then reopened.

**Why:** Without earlier history, the FFD warm-up and the Z warm-up both consume the crypto training set. With low d, the 2022 crash drops out of Z-train.

**How to apply:** Accept the stitch only after the 2021-07-05..2021-12-31 overlap shows a small close-level basis and near-identical daily returns. Record a `source` column and the seam date. Early Bybit spot bars are very thin (a 4h bar of about 0.16 BTC), so the Bybit data from 2021 is less trustworthy than Binance. Related: [[xaut-proxy-known-constraint]].


**Overlap check result (2026-10-31):** Binance daily (`data-binance/`, 2019-01-01..2026-10-29, no gaps) vs Bybit daily. Close basis across 2021-07-05..2021-12-31 has a median of 3–4bp and a p95 of 11–13bp. Daily-return correlation is above 0.999. At the 2021-12-31 seam, the basis is under 5bp for both BTC and ETH. In 2021H2, Bybit has bad prints that Binance doesn't have: ETH high +11.5% on 2021-07-05, ETH close +110bp on 2021-10-27, and a few 50–190bp high/low wicks. Bybit volume was under 1% of Binance's. So using Binance for all of 2021 is better than switching to Bybit at 2021-07-05. The stitch at 2021-12-31 is accepted on evidence.
