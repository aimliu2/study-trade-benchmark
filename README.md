# study-trader

Research notebooks testing whether simple trading strategies add value over passive exposure (Buy & Hold, DCA) on BTC, ETH, gold and QQQ.

## Studies

| Folder | Study |
|---|---|
| [study-p1-baseline/](study-p1-baseline/) | P1 baseline: Buy & Hold vs DCA vs EMA 12/26 on 1D bars, 2026 Q1–Q3. See its [README](study-p1-baseline/README.md) and [report](study-p1-baseline/reports/P1-baseline.md) |

## Setup

### 1. Replayer engine (`src`)

The notebooks load bars and indicators through [historical-bar-replayer](https://github.com/aimliu2/historical-bar-replayer). Clone it and link its `src` folder here:

```sh
git clone https://github.com/aimliu2/historical-bar-replayer ../historical-bar-replayer
ln -s ../historical-bar-replayer/src src
```

### 2. Market data (`data`)

Data is not included; bring your own. This study used:

| Symbol folder | Instrument | Source |
|---|---|---|
| `BTC`, `ETH` | BTCUSDT, ETHUSDT spot | Bybit |
| `QQQ` | QQQ ETF | Databento |
| `XAUUSD` | XAUUSD spot gold (stand-in for XAUT) | CFD broker (MT5) |

Each symbol needs one parquet file per timeframe at `data/<SYMBOL>/<SYMBOL>-sorted-<timeframe>.parquet` (e.g. `data/BTC/BTC-sorted-1d.parquet`) with columns `timestamp` (bar close, UTC), `open`, `high`, `low`, `close`. Symbol folders can be symlinks into wherever the data actually lives.

Both `src` and `data` are git-ignored.

### 3. Python

Python 3 with `pandas`, `numpy`, `numba`, `pyarrow`, `matplotlib` and Jupyter. Run notebooks with the study folder as the working directory.
