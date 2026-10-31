"""Load and plot replayer bars for a study period without touching the replayer repo.

The replayer is reached through this repo's `src` symlink. Bars are read from
this repo's `data/` folder, whose symbol folders link into the replayer's data.
"""
from __future__ import annotations

import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
DATA_ROOT = ROOT / "data"
if str(ROOT / "src") not in sys.path:
    sys.path.insert(0, str(ROOT / "src"))

from bar_replayer.data_source import TIMEFRAME_DURATIONS, load_bars  # noqa: E402

# Study name -> replayer data symbol. XAUT has no XAUTUSDT bars yet; MT5 XAUUSD spot gold stands in.
DATA_SYMBOL = {"QQQ": "QQQ", "BTC": "BTC", "ETH": "ETH", "XAUT": "XAUUSD"}


def period_bars(symbol: str, timeframe: str, start: str, end: str | None = None) -> pd.DataFrame:
    """OHLC bars whose open time falls in periods `start`..`end` (e.g. "2026Q1".."2026Q3"), indexed by bar open (UTC)."""
    bars = load_bars(DATA_SYMBOL.get(symbol, symbol), timeframe, root=DATA_ROOT)
    bars.index = bars.index - TIMEFRAME_DURATIONS[timeframe.lower()]
    bars.index.name = "bar_open_time"
    first = pd.Period(start).start_time.tz_localize("UTC")
    last = pd.Period(end or start).end_time.tz_localize("UTC")
    return bars[(bars.index >= first) & (bars.index <= last)]


def plot_ohlc(price: pd.DataFrame, title: str, ylabel: str, xlabel: str = "1D bar open"):
    """Plain candles on a gap-free bar axis, styled after the py-3TFSMC V30 structure notebook."""
    fig, ax = plt.subplots(figsize=(24, 10))
    draw_ohlc(ax, price, ylabel, xlabel)
    ax.set_title(title, loc="left", fontsize=13, fontweight="bold")
    fig.tight_layout()
    plt.show()


def draw_ohlc(ax, price: pd.DataFrame, ylabel: str, xlabel: str = "1D bar open"):
    """Draw candles onto `ax`, one x slot per bar, Monday ticks."""
    x = np.arange(len(price))
    ax.vlines(x, price["low"], price["high"], color="#616161", lw=.8, zorder=2)
    up = (price["close"] >= price["open"]).to_numpy()
    body_lw = max(1.0, min(10.0, 600 / len(price)))
    ax.vlines(x[up], price["open"][up], price["close"][up], color="#26a69a", lw=body_lw, zorder=3)
    ax.vlines(x[~up], price["open"][~up], price["close"][~up], color="#ef5350", lw=body_lw, zorder=3)
    mondays = np.flatnonzero(price.index.dayofweek == 0)
    ax.set_xticks(mondays)
    ax.set_xticklabels([price.index[i].strftime("%m-%d") for i in mondays], rotation=45, ha="right", fontsize=8)
    ax.set_xlim(-1, len(price)); ax.grid(alpha=.18)
    ax.set_ylabel(ylabel); ax.set_xlabel(xlabel)
