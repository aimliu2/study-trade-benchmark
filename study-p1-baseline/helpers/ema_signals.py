"""EMA(12/26) cross signals on 1D bars, evaluated on completed candles.

A buy signal is the close where EMA fast moves from <= slow to > slow; a sell signal is the reverse.
Signals are known only after that bar closes, so the earliest fill is the next bar's open.
"""
from __future__ import annotations

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from .replayer_bars import draw_ohlc, period_bars
from ta import ema  # noqa: E402  (src/ is put on sys.path by replayer_bars)

FAST, SLOW = 12, 26


def ema_cross(symbol: str, start: str, end: str, warmup: str, fast: int = FAST, slow: int = SLOW) -> pd.DataFrame:
    """Bars for `start`..`end` with EMA columns and +1 buy / -1 sell signals; EMAs warm up from `warmup`."""
    bars = period_bars(symbol, "1d", warmup, end)
    bars = bars.assign(ema_fast=ema(bars["close"], fast), ema_slow=ema(bars["close"], slow))
    above = bars["ema_fast"] > bars["ema_slow"]
    ready = bars["ema_slow"].notna() & bars["ema_slow"].shift().notna()
    cross = above.astype(int).diff().where(ready, 0).fillna(0).astype(int)
    bars["signal"] = cross
    bars["fill_open"] = bars["open"].shift(-1).where(cross != 0)
    first = pd.Period(start).start_time.tz_localize("UTC")
    return bars[bars.index >= first]


def signal_table(bars: pd.DataFrame) -> pd.DataFrame:
    """One row per signal: signal bar, its close, and the next bar's open where it could be filled."""
    hits = bars[bars["signal"] != 0]
    fill_time = pd.Series(bars.index, index=bars.index).shift(-1)[hits.index]
    return pd.DataFrame({
        "side": np.where(hits["signal"] > 0, "buy", "sell"),
        "signal_close": hits["close"],
        "fill_bar": fill_time.dt.strftime("%Y-%m-%d"),
        "fill_open": hits["fill_open"],
    }, index=hits.index.strftime("%Y-%m-%d"))


def simulate_ema(bars: pd.DataFrame, capital: float) -> tuple[pd.DataFrame, pd.DataFrame]:
    """All-in / all-out on EMA cross signals, gross.

    Buys all capital at the first bar's open regardless of trend. A sell signal while holding
    sells every unit at the next bar's open; a buy signal while flat buys with all cash at the
    next bar's open. Signals that don't change the position are ignored. Equity is marked at
    each close. Returns (daily equity, one row per completed or open trade).
    """
    opens, closes, signals = bars["open"].to_numpy(), bars["close"].to_numpy(), bars["signal"].to_numpy()
    cash, units, pending = capital, 0.0, +1  # first bar: forced buy at its open
    equity, held, trades = np.empty(len(bars)), np.empty(len(bars)), []
    for i in range(len(bars)):
        if pending > 0 and units == 0:
            units, cash = cash / opens[i], 0.0
            trades.append({"entry": bars.index[i], "entry_open": opens[i], "cost": units * opens[i]})
        elif pending < 0 and units > 0:
            cash, units = units * opens[i], 0.0
            trades[-1].update(exit=bars.index[i], exit_open=opens[i], proceeds=cash)
        pending = signals[i]
        equity[i], held[i] = cash + units * closes[i], units
    if units > 0:
        trades[-1].update(exit=pd.NaT, exit_open=np.nan, proceeds=units * closes[-1])
    daily = pd.DataFrame({"equity": equity, "units": held}, index=bars.index)
    trades = pd.DataFrame(trades)
    trades["pnl"] = trades["proceeds"] - trades["cost"]
    trades["return"] = trades["proceeds"] / trades["cost"] - 1
    trades["days"] = ((trades["exit"].fillna(bars.index[-1]) - trades["entry"]).dt.days)
    return daily, trades


def plot_ema_trades(bars: pd.DataFrame, daily: pd.DataFrame, buy_hold: pd.Series, title: str, ylabel: str,
                    capital: float, fast: int = FAST, slow: int = SLOW):
    """Candles + EMAs with actual fills on top; EMA strategy equity vs Buy & Hold below."""
    x = np.arange(len(bars))
    held = (daily["units"] > 0).to_numpy()
    entered = held & ~np.r_[False, held[:-1]]
    exited = ~held & np.r_[False, held[:-1]]
    fig, (top, bottom) = plt.subplots(2, 1, figsize=(24, 13), sharex=True, height_ratios=[3, 2])
    draw_ohlc(top, bars, ylabel, xlabel="")
    top.plot(x, bars["ema_fast"], color="#fb8c00", lw=1.4, label=f"EMA {fast}")
    top.plot(x, bars["ema_slow"], color="#6a1b9a", lw=1.4, label=f"EMA {slow}")
    lo, hi = top.get_ylim()
    top.fill_between(x, lo, hi, where=held, color="#1565c0", alpha=.06, step="mid", label="holding")
    top.set_ylim(lo, hi)
    top.scatter(x[entered], bars["open"][entered], marker="^", s=170, color="#1565c0", zorder=4,
                label=f"buy fill at open ({entered.sum()})")
    top.scatter(x[exited], bars["open"][exited], marker="v", s=170, color="#d81b60", zorder=4,
                label=f"sell fill at open ({exited.sum()})")
    top.legend(loc="upper left")
    top.set_title(title, loc="left", fontsize=13, fontweight="bold")

    bottom.plot(x, daily["equity"], color="#1565c0", lw=1.6, label=f"EMA {fast}/{slow} all-in/all-out")
    bottom.plot(x, buy_hold, color="#9e9e9e", lw=1.2, label="Buy & Hold")
    bottom.axhline(capital, color="#616161", lw=1, ls="--")
    for series, color in ((daily["equity"], "#1565c0"), (buy_hold, "#757575")):
        final = series.iloc[-1]
        bottom.annotate(f"${final:,.2f} ({final / capital - 1:+.1%})", (x[-1], final), color=color,
                        xytext=(-10, 8), textcoords="offset points", ha="right", fontweight="bold")
    bottom.set_ylabel(f"equity, USD (start ${capital:,.0f})"); bottom.legend(loc="upper left")
    bottom.set_xlabel("1D bar open"); bottom.grid(alpha=.18)
    fig.tight_layout()
    plt.show()


def plot_ema_signals(bars: pd.DataFrame, title: str, ylabel: str, fast: int = FAST, slow: int = SLOW):
    """Candles with EMA lines and cross markers placed on the signal bar."""
    x = np.arange(len(bars))
    fig, ax = plt.subplots(figsize=(24, 10))
    draw_ohlc(ax, bars, ylabel)
    ax.plot(x, bars["ema_fast"], color="#fb8c00", lw=1.4, label=f"EMA {fast}")
    ax.plot(x, bars["ema_slow"], color="#6a1b9a", lw=1.4, label=f"EMA {slow}")
    buy = (bars["signal"] > 0).to_numpy()
    sell = (bars["signal"] < 0).to_numpy()
    pad = (bars["high"].max() - bars["low"].min()) * .02
    ax.scatter(x[buy], bars["low"][buy] - pad, marker="^", s=170, color="#1565c0", zorder=4,
               label=f"buy: EMA {fast} crosses above {slow} ({buy.sum()})")
    ax.scatter(x[sell], bars["high"][sell] + pad, marker="v", s=170, color="#d81b60", zorder=4,
               label=f"sell: EMA {fast} crosses below {slow} ({sell.sum()})")
    ax.legend(loc="upper left")
    ax.set_title(title, loc="left", fontsize=13, fontweight="bold")
    fig.tight_layout()
    plt.show()
