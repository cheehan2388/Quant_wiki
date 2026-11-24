#!/usr/bin/env python3
"""產生兩張常態分布的示意圖（依公式精確畫出，不是隨機資料）：
- tools/figures/normal-bell.svg：一條鐘形曲線，標出平均、±1 和 ±2 個標準差的範圍
- tools/figures/normal-fuse.svg：預測（甲）和量測（乙）兩條曲線，相乘後得到更窄的新曲線

用法：python3 tools/make_normal_figures.py
"""
import math
from pathlib import Path

FIG = Path(__file__).resolve().parent / "figures"


def pdf(x, m, v):
    return math.exp(-(x - m) ** 2 / (2 * v)) / math.sqrt(2 * math.pi * v)


def curve(m, v, X, Y, lo, hi, n=240):
    pts = [(lo + (hi - lo) * i / n) for i in range(n + 1)]
    return "M" + " L".join(f"{X(x):.1f},{Y(pdf(x, m, v)):.1f}" for x in pts)


# 圖一：鐘形曲線
W, H, L, R, T, B = 760, 360, 30, 30, 30, 70
lo, hi = -3.6, 3.6
peak = pdf(0, 0, 1)
X = lambda x: L + (W - L - R) * (x - lo) / (hi - lo)
Y = lambda y: H - B - (H - B - T) * y / peak


def band(a, b, cls):
    n = 80
    xs = [a + (b - a) * i / n for i in range(n + 1)]
    top = " L".join(f"{X(x):.1f},{Y(pdf(x, 0, 1)):.1f}" for x in xs)
    return f'<path d="M{X(a):.1f},{Y(0):.1f} L{top} L{X(b):.1f},{Y(0):.1f} Z" class="{cls}"/>'


parts = [f'<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" role="img" class="fig-svg nb" '
         'aria-label="常態分布的鐘形曲線：中間最高，約 68% 的值落在平均加減 1 個標準差內，約 95% 落在加減 2 個標準差內">',
         band(-2, 2, "nb-2"), band(-1, 1, "nb-1"),
         f'<path d="{curve(0, 1, X, Y, lo, hi)}" class="nb-c"/>',
         f'<line x1="{X(lo):.1f}" x2="{X(hi):.1f}" y1="{Y(0):.1f}" y2="{Y(0):.1f}" class="nb-ax"/>']
for k, lab in [(-2, "平均 − 2σ"), (-1, "平均 − 1σ"), (0, "平均"), (1, "平均 + 1σ"), (2, "平均 + 2σ")]:
    parts.append(f'<line x1="{X(k):.1f}" x2="{X(k):.1f}" y1="{Y(0):.1f}" y2="{Y(0) + 6:.1f}" class="nb-ax"/>')
    parts.append(f'<text x="{X(k):.1f}" y="{Y(0) + 24:.1f}" text-anchor="middle" class="nb-t">{lab}</text>')
parts.append(f'<text x="{X(0):.1f}" y="{Y(0.17):.1f}" text-anchor="middle" class="nb-big">約 68%</text>')
parts.append(f'<text x="{X(2.15):.1f}" y="{Y(0.16):.1f}" text-anchor="start" class="nb-t">到 ±2σ：合計約 95%</text>')
parts.append(f'<text x="{X(0):.1f}" y="{Y(peak) - 8:.1f}" text-anchor="middle" class="nb-t">最常出現：靠近平均</text>')
parts.append(f'<text x="{X(-3.2):.1f}" y="{Y(0.05):.1f}" text-anchor="middle" class="nb-t">很少出現</text>')
parts.append(f'<text x="{W - R}" y="{H - 8}" text-anchor="end" class="nb-n">σ ＝ 標準差。曲線越高，代表那個值越常出現</text>')
parts.append("</svg>")
(FIG / "normal-bell.svg").write_text("\n".join(parts), encoding="utf-8")

# 圖二：兩條曲線相乘（甲：預測 100、變異數 1.5；乙：量測 102、變異數 2）
m1, v1, m2, v2 = 100.0, 1.5, 102.0, 2.0
mf = m1 + v1 / (v1 + v2) * (m2 - m1)
vf = v1 * v2 / (v1 + v2)
W, H, L, R, T, B = 760, 360, 30, 30, 40, 60
lo, hi = 95.5, 106.5
peak = pdf(mf, mf, vf)
X = lambda x: L + (W - L - R) * (x - lo) / (hi - lo)
Y = lambda y: H - B - (H - B - T) * y / peak
parts = [f'<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" role="img" class="fig-svg nb" '
         'aria-label="兩條鐘形曲線相乘：預測在 100，量測在 102，結合後的曲線落在 100.86，而且比兩條都窄">',
         f'<line x1="{X(lo):.1f}" x2="{X(hi):.1f}" y1="{Y(0):.1f}" y2="{Y(0):.1f}" class="nb-ax"/>',
         f'<path d="{curve(m1, v1, X, Y, lo, hi)}" class="nf-a"/>',
         f'<path d="{curve(m2, v2, X, Y, lo, hi)}" class="nf-b"/>',
         f'<path d="{curve(mf, vf, X, Y, lo, hi)}" class="nf-f"/>']
for v in range(96, 107, 2):
    parts.append(f'<text x="{X(v):.1f}" y="{Y(0) + 22:.1f}" text-anchor="middle" class="nb-t">{v}</text>')
parts.append(f'<text x="{X(m1) - 70:.1f}" y="{Y(pdf(m1, m1, v1)) - 6:.1f}" text-anchor="middle" class="nf-ta">甲：預測 100（變異數 1.5）</text>')
parts.append(f'<text x="{X(m2) + 80:.1f}" y="{Y(pdf(m2, m2, v2)) - 6:.1f}" text-anchor="middle" class="nf-tb">乙：看到 102（變異數 2）</text>')
parts.append(f'<text x="{X(mf):.1f}" y="{Y(peak) - 10:.1f}" text-anchor="middle" class="nf-tf">相乘後：{mf:.2f}（變異數 {vf:.2f}，更窄）</text>')
parts.append(f'<line x1="{X(mf):.1f}" x2="{X(mf):.1f}" y1="{Y(0):.1f}" y2="{Y(peak):.1f}" class="nf-mid"/>')
parts.append(f'<text x="{W - R}" y="{H - 8}" text-anchor="end" class="nb-n">依公式畫出；數字和概念頁的例子相同</text>')
parts.append("</svg>")
(FIG / "normal-fuse.svg").write_text("\n".join(parts), encoding="utf-8")
print(f"已產生 normal-bell.svg、normal-fuse.svg（相乘後中心 {mf:.2f}，變異數 {vf:.3f}）")
