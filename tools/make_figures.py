#!/usr/bin/env python3
"""產生示意圖：tools/figures/pairs-spread.svg

這是模擬資料畫的示意圖，圖上會標「示意，非真實資料」。
用法：python3 tools/make_figures.py
"""
import math
import random
from pathlib import Path

OUT = Path(__file__).resolve().parent / "figures" / "pairs-spread.svg"
random.seed(77)
N = 220
W, H = 760, 452
L, R = 56, 20          # 左右邊界
TOP1, BOT1 = 34, 190   # 上圖：兩檔價格
TOP2, BOT2 = 250, 392  # 下圖：價差

# 模擬：B 是隨機漫步，A = B + 會回歸的價差；第 120 天左右注入一次偏離
b, s = [100.0], [0.0]
for t in range(1, N):
    b.append(b[-1] * (1 + random.gauss(0.0004, 0.011)))
    shock = -2.6 if t in (118, 119, 120) else 0.0
    s.append(0.86 * s[-1] + random.gauss(0, 0.55) + shock)
a = [bb * (1 + ss / 100) for bb, ss in zip(b, s)]
sd = (sum(x * x for x in s[:110]) / 110) ** 0.5

entry = next(t for t in range(110, N) if s[t] < -2 * sd)
exit_ = next(t for t in range(entry + 1, N) if s[t] >= 0)


def x(t):
    return L + (W - L - R) * t / (N - 1)


def path(vals, lo, hi, top, bot):
    return "M" + " L".join(f"{x(t):.1f},{bot - (v - lo) / (hi - lo) * (bot - top):.1f}" for t, v in enumerate(vals))


plo, phi = min(a + b) - 1, max(a + b) + 1
slo, shi = -3.6 * sd, 3.6 * sd
ys = lambda v: BOT2 - (v - slo) / (shi - slo) * (BOT2 - TOP2)

parts = [f'<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" role="img" class="fig-svg" '
         f'aria-label="配對交易示意圖：上方是兩檔股票的價格，下方是兩者的價差與正負兩個標準差的界線">']
parts.append(f'<rect x="{x(entry):.1f}" y="{TOP1 - 8}" width="{x(exit_) - x(entry):.1f}" height="{BOT2 - TOP1 + 16}" class="f-hold"/>')
parts.append(f'<text x="{L}" y="20" class="f-h">兩檔股票的價格</text>')
parts.append(f'<path d="{path(b, plo, phi, TOP1, BOT1)}" class="f-b"/>')
parts.append(f'<path d="{path(a, plo, phi, TOP1, BOT1)}" class="f-a"/>')
parts.append(f'<text x="{W - R}" y="{TOP1 + 4}" text-anchor="end" class="f-lab"><tspan class="f-ka">━ A</tspan>　<tspan class="f-kb">━ B</tspan></text>')
parts.append(f'<text x="{L}" y="{TOP2 - 14}" class="f-h">價差（A 減 B）</text>')
for k, lab in ((2, "+2 標準差"), (0, "平常水準"), (-2, "−2 標準差")):
    cls = "f-zero" if k == 0 else "f-band"
    parts.append(f'<line x1="{L}" x2="{W - R}" y1="{ys(k * sd):.1f}" y2="{ys(k * sd):.1f}" class="{cls}"/>')
    parts.append(f'<text x="{L - 6}" y="{ys(k * sd) + 4:.1f}" text-anchor="end" class="f-tick">{"+2σ" if k == 2 else ("0" if k == 0 else "−2σ")}</text>')
parts.append(f'<path d="{path(s, slo, shi, TOP2, BOT2)}" class="f-s"/>')
ex, ey = x(entry), ys(s[entry])
qx, qy = x(exit_), ys(s[exit_])
parts.append(f'<circle cx="{ex:.1f}" cy="{ey:.1f}" r="6" class="f-in"/>')
parts.append(f'<circle cx="{qx:.1f}" cy="{qy:.1f}" r="6" class="f-out"/>')
parts.append(f'<text x="{ex - 10:.1f}" y="{BOT2 + 22}" text-anchor="end" class="f-lab">① 跌破 −2σ：買 A、空 B</text>')
parts.append(f'<text x="{qx + 10:.1f}" y="{BOT2 + 22}" class="f-lab">② 回到 0：平倉</text>')
parts.append(f'<text x="{W - R}" y="{H - 4}" text-anchor="end" class="f-note">示意，非真實資料（模擬產生）</text>')
parts.append("</svg>")
OUT.parent.mkdir(exist_ok=True)
OUT.write_text("\n".join(parts), encoding="utf-8")
print(f"已產生 {OUT.name}：進場第 {entry} 天，出場第 {exit_} 天")
