"""S0 Buy & Hold vs S1 monthly DCA on 1D bars, gross (no fees, no dividends, cash earns 0).

Run with `python -m helpers.passive_benchmarks` from the study folder.
Both start with the same capital. Buy & Hold buys everything at the first bar's open.
DCA splits capital into one equal tranche per calendar month, bought at the open of
each month's first bar; uninvested capital stays in cash. Equity is marked at each close.
"""
from __future__ import annotations

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from .replayer_bars import draw_ohlc, period_bars

CAPITAL = 900.0


def simulate(price: pd.DataFrame, capital: float = CAPITAL) -> pd.DataFrame:
    """Daily equity of Buy & Hold and monthly DCA over the bars given."""
    month = price.index.tz_localize(None).to_period("M")
    buy_day = ~month.duplicated()
    tranche = capital / buy_day.sum()

    bh_units = capital / price["open"].iloc[0]
    dca_units = np.cumsum(np.where(buy_day, tranche / price["open"], 0.0))
    dca_cash = capital - tranche * np.cumsum(buy_day)
    return pd.DataFrame({
        "buy_hold": bh_units * price["close"],
        "dca": dca_units * price["close"] + dca_cash,
        "dca_invested": capital - dca_cash,
        "dca_units": dca_units,
        "dca_buy": buy_day,
    }, index=price.index)


def max_drawdown(equity: pd.Series) -> float:
    return (equity / equity.cummax() - 1).min()


def summary(equity: pd.DataFrame, capital: float = CAPITAL) -> pd.DataFrame:
    rows = {}
    for name in ("buy_hold", "dca"):
        e = equity[name]
        rows[name] = {
            "final": e.iloc[-1],
            "return": e.iloc[-1] / capital - 1,
            "max_dd": max_drawdown(e),
            "worst_equity": e.min(),
        }
    return pd.DataFrame(rows).T


def plot_buy_hold(price: pd.DataFrame, title: str, ylabel: str, capital: float = CAPITAL):
    """Candles on top, Buy & Hold position value in USD below, on the same bar axis."""
    value = simulate(price, capital)["buy_hold"]
    x = np.arange(len(price))
    fig, (top, bottom) = plt.subplots(2, 1, figsize=(24, 13), sharex=True, height_ratios=[3, 2])
    draw_ohlc(top, price, ylabel, xlabel="")
    top.scatter([0], [price["open"].iloc[0]], marker="^", s=160, color="#1565c0", zorder=4,
                label=f"buy {capital / price['open'].iloc[0]:.6g} units @ {price['open'].iloc[0]:,.2f}")
    top.legend(loc="upper left")
    top.set_title(title, loc="left", fontsize=13, fontweight="bold")

    gain = value >= capital
    bottom.plot(x, value, color="#1565c0", lw=1.6)
    bottom.axhline(capital, color="#616161", lw=1, ls="--")
    bottom.fill_between(x, value, capital, where=gain, color="#26a69a", alpha=.25, interpolate=True)
    bottom.fill_between(x, value, capital, where=~gain, color="#ef5350", alpha=.25, interpolate=True)
    final = value.iloc[-1]
    bottom.annotate(f"${final:,.2f} ({final / capital - 1:+.1%})", (x[-1], final),
                    xytext=(-10, 10), textcoords="offset points", ha="right", fontweight="bold")
    bottom.set_ylabel(f"position value, USD (start ${capital:,.0f})")
    bottom.set_xlabel("1D bar open"); bottom.grid(alpha=.18)
    fig.tight_layout()
    plt.show()


def plot_dca(price: pd.DataFrame, title: str, ylabel: str, capital: float = CAPITAL):
    """Candles with each monthly buy marked on top; DCA holdings value vs dollars invested below."""
    sim = simulate(price, capital)
    held = sim["dca_units"] * price["close"]
    invested = sim["dca_invested"]
    buys = np.flatnonzero(sim["dca_buy"])
    x = np.arange(len(price))
    fig, (top, bottom) = plt.subplots(2, 1, figsize=(24, 13), sharex=True, height_ratios=[3, 2])
    draw_ohlc(top, price, ylabel, xlabel="")
    top.scatter(buys, price["open"].iloc[buys], marker="^", s=160, color="#1565c0", zorder=4,
                label=f"buy ${invested.iloc[buys[0]]:,.0f} at each month's first open")
    avg_cost = invested.iloc[-1] / sim["dca_units"].iloc[-1]
    top.axhline(avg_cost, color="#1565c0", lw=1, ls=":", label=f"average cost {avg_cost:,.2f}")
    top.legend(loc="upper left")
    top.set_title(title, loc="left", fontsize=13, fontweight="bold")

    gain = (held >= invested).to_numpy()
    bottom.plot(x, held, color="#1565c0", lw=1.6, label="holdings value")
    bottom.step(x, invested, color="#616161", lw=1, ls="--", where="post", label="dollars invested")
    bottom.fill_between(x, held, invested, where=gain, color="#26a69a", alpha=.25, interpolate=True)
    bottom.fill_between(x, held, invested, where=~gain, color="#ef5350", alpha=.25, interpolate=True)
    final = held.iloc[-1]
    bottom.annotate(f"${final:,.2f} ({final / invested.iloc[-1] - 1:+.1%})", (x[-1], final),
                    xytext=(-10, 10), textcoords="offset points", ha="right", fontweight="bold")
    bottom.set_ylabel("USD"); bottom.legend(loc="upper left")
    bottom.set_xlabel("1D bar open"); bottom.grid(alpha=.18)
    fig.tight_layout()
    plt.show()


if __name__ == "__main__":
    for symbol in ["BTC", "ETH", "XAUT", "QQQ"]:
        price = period_bars(symbol, "1d", "2026Q1", "2026Q3")
        eq = simulate(price)
        s = summary(eq)
        print(f"\n{symbol}: {price.index[0]:%Y-%m-%d} open {price['open'].iloc[0]:,.2f} -> "
              f"{price.index[-1]:%Y-%m-%d} close {price['close'].iloc[-1]:,.2f}")
        print(s.to_string(formatters={"final": "{:,.0f}".format, "return": "{:+.1%}".format,
                                      "max_dd": "{:.1%}".format, "worst_equity": "{:,.0f}".format}))
