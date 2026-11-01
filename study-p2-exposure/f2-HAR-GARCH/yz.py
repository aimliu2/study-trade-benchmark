"""Yang-Zhang variance per asset -> yz_data/<SYM>-yz-1d.csv

Columns (daily log-return variance units, not annualized):
  yz_var_daily  per-day YZ: o^2 + k*c^2 + (1-k)*RS, zero mean, k = 0.34/2.34 (large-n limit). HAR input.
  yz_var_22     standalone YZ over 22 bars (yang-zhang.md formula, demeaned, k(22)). Historical plot.
  r             this bar's close-to-close log return (GARCH-family input; known at this bar's close).
  r2_next       next bar's squared close-to-close log return (provisional target) = r.shift(-1)**2.

Each row's YZ values are known at that bar's close and forecast the next bar.
r2_next is the future value on the same row; never use it as an input.
"""
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
DATA = HERE.parents[1] / 'data'
OUT = HERE / 'yz_data'
ASSETS = ['BTC', 'ETH', 'QQQ', 'XAUUSD']
N = 22
K_DAILY = 0.34 / 2.34


def yz_frame(df):
    o, h, l, c = (np.log(df[x]) for x in ('open', 'high', 'low', 'close'))
    on = o - c.shift()                       # overnight
    oc = c - o                               # open-to-close
    rs = (h - c) * (h - o) + (l - c) * (l - o)
    k = 0.34 / (1.34 + (N + 1) / (N - 1))
    r = c.diff()
    return pd.DataFrame({
        'yz_var_daily': on**2 + K_DAILY * oc**2 + (1 - K_DAILY) * rs,
        'yz_var_22': on.rolling(N).var() + k * oc.rolling(N).var() + (1 - k) * rs.rolling(N).mean(),
        'r': r,
        'r2_next': (r**2).shift(-1),
    })


def main():
    OUT.mkdir(exist_ok=True)
    for sym in ASSETS:
        df = pd.read_parquet(DATA / sym / f'{sym}-sorted-1d.parquet')
        ts = pd.to_datetime(df['timestamp'])
        assert ts.is_monotonic_increasing and ts.is_unique, sym
        out = yz_frame(df.set_index(ts))
        out.index.name = 'timestamp'
        out.to_csv(OUT / f'{sym}-yz-1d.csv')
        print(sym, len(out), out.index[0], '->', out.index[-1])


if __name__ == '__main__':
    main()
