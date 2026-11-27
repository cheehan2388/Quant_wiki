#!/usr/bin/env python3
"""產生兩張示意圖（均值回歸簡報用）：

- tools/figures/ou-halflife.svg：b = 0.8 和 b = 0.99 的偏離，每天剩多少（沒有雜訊）
- tools/figures/ou-signals.svg：模擬一條 b = 0.8 的價差，照 Avellaneda & Lee 的門檻進出場

模擬資料，圖上標「示意，非真實資料」。
用法：python3 tools/make_ou_figures.py
"""
import math
import random
from pathlib import Path

FIG = Path(__file__).resolve().parent / "figures"
W, H, L, R, TOP, BOT = 760, 380, 48, 20, 40, 316


def path(xs, ys, X, Y):
    return "M" + " L".join(f"{X(a):.1f},{Y(b):.1f}" for a, b in zip(xs, ys))


# ---------- 圖 1：半衰期 ----------
D = 30
X = lambda t: L + (W - L - R) * t / D
Y = lambda v: BOT - v * (BOT - TOP)
days = list(range(D + 1))
fast = [0.8 ** t for t in days]
slow = [0.99 ** t for t in days]
h_fast = math.log(2) / -math.log(0.8)
ticks = "".join(f'<text x="{X(t):.1f}" y="{BOT + 18}" text-anchor="middle" class="f-tick">{t}</text>' for t in range(0, D + 1, 5))
yt = "".join(f'<text x="{L - 8}" y="{Y(v) + 4:.1f}" text-anchor="end" class="f-tick">{int(v * 100)}%</text>' for v in (0, 0.5, 1))
svg1 = f'''<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" role="img" class="fig-svg" aria-label="示意圖：偏離從 100% 開始，b 等於 0.8 時大約 3 天剩一半、十幾天就幾乎歸零；b 等於 0.99 時 30 天後還剩約四分之三">
<line x1="{L}" x2="{W - R}" y1="{Y(0.5):.1f}" y2="{Y(0.5):.1f}" class="f-band"/>
<text x="{W - R}" y="{Y(0.5) - 6:.1f}" text-anchor="end" class="f-lab">剩一半</text>
<line x1="{L}" x2="{W - R}" y1="{BOT}" y2="{BOT}" class="f-zero"/>
{ticks}{yt}
<text x="{(L + W - R) / 2:.0f}" y="{BOT + 38}" text-anchor="middle" class="f-tick">天數</text>
<path d="{path(days, slow, X, Y)}" class="k-ma"/>
<path d="{path(days, fast, X, Y)}" class="k-kf"/>
<circle cx="{X(h_fast):.1f}" cy="{Y(0.5):.1f}" r="6" class="f-in"/>
<text x="{X(7):.1f}" y="{Y(0.5) + 24:.1f}" class="f-lab">b = 0.8（紅）：約 3.1 天剩一半</text>
<text x="{X(D) - 4:.1f}" y="{Y(0.64):.1f}" text-anchor="end" class="f-lab">b = 0.99（藍）：30 天後還剩約 74%，要 69 天才剩一半</text>
<text x="{L + 4}" y="{TOP - 14}" class="f-lab">離平衡點的距離（第 0 天 = 100%）</text>
<text x="{W - R}" y="{H - 6}" text-anchor="end" class="f-note">示意，沒有雜訊時的平均走法</text>
</svg>'''
(FIG / "ou-halflife.svg").write_text(svg1, encoding="utf-8")

# ---------- 圖 2：進出場 ----------
N = 120
b, sd = 0.8, math.sqrt(1 - 0.8 ** 2)       # 平衡時標準差 = 1，所以價差本身就是 s 分數
OPEN, CLOSE_LONG, CLOSE_SHORT = 1.25, -0.50, 0.75


def simulate(seed):
    random.seed(seed)
    s = [0.0]
    for _ in range(N - 1):
        s.append(b * s[-1] + random.gauss(0, sd))
    trades, pos, start = [], 0, None
    for t, v in enumerate(s):
        if pos == 0 and v < -OPEN:
            pos, start = 1, t
        elif pos == 0 and v > OPEN:
            pos, start = -1, t
        elif pos == 1 and v > CLOSE_LONG:
            trades.append((start, t, 1)); pos = 0
        elif pos == -1 and v < CLOSE_SHORT:
            trades.append((start, t, -1)); pos = 0
    return s, trades, pos


seed = next(k for k in range(1, 500)
            if (lambda r: 3 <= len(r[1]) <= 5 and r[2] == 0 and {d for *_, d in r[1]} == {1, -1}
                and max(abs(x) for x in r[0]) < 2.9)(simulate(k)))
s, trades, _ = simulate(seed)
lo, hi = -3, 3
X2 = lambda t: L + (W - L - R) * t / (N - 1)
Y2 = lambda v: BOT - (v - lo) / (hi - lo) * (BOT - TOP)
holds = "".join(f'<rect x="{X2(a):.1f}" y="{TOP}" width="{X2(c) - X2(a):.1f}" height="{BOT - TOP}" class="f-hold"/>' for a, c, _ in trades)
marks = "".join(f'<circle cx="{X2(a):.1f}" cy="{Y2(s[a]):.1f}" r="6" class="f-in"/><circle cx="{X2(c):.1f}" cy="{Y2(s[c]):.1f}" r="6" class="f-out"/>' for a, c, _ in trades)


def hline(v, cls, label):
    return (f'<line x1="{L}" x2="{W - R}" y1="{Y2(v):.1f}" y2="{Y2(v):.1f}" class="{cls}"/>'
            f'<text x="{L - 8}" y="{Y2(v) + 4:.1f}" text-anchor="end" class="f-tick">{label}</text>')


svg2 = f'''<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" role="img" class="fig-svg" aria-label="示意圖：一條模擬的 s 分數在 0 附近上下晃動。跌破負 1.25 時買進價差、回到負 0.5 以上平倉；漲破 1.25 時賣出價差、回到 0.75 以下平倉。圖上共有 {len(trades)} 筆交易">
{holds}
{hline(OPEN, "f-band", "+1.25")}{hline(-OPEN, "f-band", "−1.25")}
{hline(CLOSE_SHORT, "k-turn", "0.75")}{hline(CLOSE_LONG, "k-turn", "−0.5")}
{hline(0, "f-zero", "0")}
<path d="{path(range(N), s, X2, Y2)}" class="f-s"/>
{marks}
<g class="f-lab"><circle cx="{L + 6}" cy="{H - 34}" r="6" class="f-in"/><text x="{L + 18}" y="{H - 30}">進場：s 超過 ±1.25</text>
<circle cx="{L + 200}" cy="{H - 34}" r="6" class="f-out"/><text x="{L + 212}" y="{H - 30}">平倉：多單回到 −0.5 以上、空單回到 0.75 以下</text></g>
<text x="{L + 4}" y="{TOP - 14}" class="f-lab">s 分數（價差離平衡點幾個「平常的晃動」）</text>
<text x="{W - R}" y="{H - 6}" text-anchor="end" class="f-note">示意，非真實資料（模擬 b = 0.8 的價差）</text>
</svg>'''
(FIG / "ou-signals.svg").write_text(svg2, encoding="utf-8")
print(f"已產生 ou-halflife.svg（半衰期 {h_fast:.2f} 天；b=0.99 第 30 天剩 {slow[-1]:.3f}）")
print(f"已產生 ou-signals.svg（seed {seed}，{len(trades)} 筆交易：{trades}）")
