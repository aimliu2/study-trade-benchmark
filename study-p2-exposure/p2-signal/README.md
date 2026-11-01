# P2 signal — FFD Z and ITR/LTR structure on the P1 anchor period

| Notebook | What it shows |
|---|---|
| [p2-ffd-signal.ipynb](p2-ffd-signal.ipynb) | BTC, ETH, XAUT, QQQ 1D candles for 2026 Q1–Q3 (same bars as [P1 buy-hold-1d](../../study-p1-baseline/buy-hold-1d.ipynb)), with the replayer's ITR/LTR structure drawn on the candles and FFD rolling Z (d = 0.25, 445 bars) below. Marks the first signal: ITR low (HL or LL) confirmed with Z ≤ −1 on the pivot bar (BTC ≤ −2, a hindsight special case drawn in cyan); dashed line = confirmation bar, earliest fill = next bar's open (the confirmation bar's open would leak). Third panel: $900 all in at that fill, held to the last Q3 close (P1 S0 Buy & Hold with a signal entry; gross) |

Run with this folder as the working directory.

## Wiring

```
p2-ffd-signal.ipynb
 ├─ ../../study-p1-baseline/helpers/replayer_bars.py   (added to sys.path)
 │    ├─ period_bars, draw_ohlc, DATA_ROOT, DATA_SYMBOL
 │    └─ puts ../../src on sys.path
 ├─ src/bar_replayer/data_source.py  load_bars          (raw bars, indexed by bar close)
 ├─ src/smc  StructureReducer, DEFAULT_ENGINE_CONFIG    (ITR/LTR structure engine)
 └─ ../../data/<SYMBOL>/<SYMBOL>-sorted-1d.parquet      (XAUT reads XAUUSD)
```

- **Do not rename or move `study-p1-baseline/`.** The notebook imports its bar loader and candle drawing from there.
- `src` is the symlink to the replayer repo (`py-historical-bar-replayer/src`); see the root [README](../../README.md#setup).
- FFD and rolling Z are defined inside the notebook, copied from [f1-fracdiff/ffd-z-plot3.ipynb](../f1-fracdiff/ffd-z-plot3.ipynb). Change one, change both.

## Warm-up — everything replays from the first bar

Nothing is cached and no anchor file is used. Each run reads each asset's full 1D history (from 2019-01-01/02) and then cuts to 2026 Q1–Q3.

| Piece | How it starts | Ready from |
|---|---|---|
| FFD (445-bar weights) | First value on bar 445 | 2020-03 (BTC, ETH), 2020-09/10 (XAUT, QQQ) |
| Rolling Z (445 bars, min 60) | Full 445-bar window | 2021-06 (BTC, ETH), 2022-06/07 (XAUT, QQQ) |
| ITR/LTR structure | Fresh `StructureReducer` (1D default config, conservative, `str_bars` = 2), low-first genesis seed, stepped bar by bar from the first bar | 1,760–2,557 bars of history before 2026 |

The replayer's terrain anchors are saved reducer states it loads to skip that replay. Without a matching anchor it also replays from the first bar, which is what this notebook does. The engine's `warmup_start` (2020-01-01) only flags earlier bars in its output; the notebook ignores it.

## Plot conventions

- Engine timestamps are bar close; the anchor bars are keyed by bar open, so every structure timestamp is shifted back one day.
- Pivots are triangles (▼ high, ▲ low; LTR larger, labelled `LTR`), styled after py-3TFSMC V30 `2020_q3_1h_over2.ipynb`. A pivot is drawn on its own bar but is known only on its confirmation bar. Pivots confirmed after the last bar of the period are left out.
- Break lines run from the broken level's pivot to the first bar that closed through it: `ichoch` / `lchoch` against the prior structure, `isb` / `lsb` with it.
