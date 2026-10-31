---
name: xaut-proxy-known-constraint
description: XAUT uses MT5 XAUUSD spot gold as a stand-in; user documents it, so don't re-flag it in every answer
metadata:
  type: feedback
---

XAUT has no XAUTUSDT bars yet; the P1 study uses MT5 XAUUSD spot gold instead. The user treats this as a known, documented constraint (noted in the study-p1-baseline README).

**Why:** The user flagged that I kept repeating the caveat after every result.
**How to apply:** Don't footnote XAUT results with the proxy caveat in chat replies. Keep the label in chart titles/notebook notes. Raise it again only if XAUTUSDT data appears or the proxy materially changes a conclusion.
