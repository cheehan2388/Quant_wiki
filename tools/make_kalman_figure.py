#!/usr/bin/env python3
"""產生示意圖：tools/figures/kf-vs-ma.svg（卡爾曼濾波器 vs 12 天移動平均）

模擬資料，圖上標「示意，非真實資料」。卡爾曼濾波器用最簡單的「位置＋速度」模型（類似論文的模型 1）。
用法：python3 tools/make_kalman_figure.py
"""
import random
from pathlib import Path

OUT = Path(__file__).resolve().parent / "figures" / "kf-vs-ma.svg"
random.seed(11)
N = 120
# 真實走勢：先上漲、第 60 天轉頭向下、第 95 天後走平
true, v = [100.0], 0.35
for t in range(1, N):
    if t == 60:
        v = -0.45
    if t == 95:
        v = 0.0
    true.append(true[-1] + v)
price = [x + random.gauss(0, 1.4) for x in true]

ma = [None] * N
for t in range(11, N):
    ma[t] = sum(price[t - 11:t + 1]) / 12

# 卡爾曼濾波器：狀態 = [價格, 速度]
q_pos, q_vel, r = 0.05, 0.01, 1.4 ** 2
x = [price[0], 0.0]
P = [[4.0, 0.0], [0.0, 1.0]]
kf = []
for y in price:
    # 預測
    x = [x[0] + x[1], x[1]]
    P = [[P[0][0] + 2 * P[0][1] + P[1][1] + q_pos, P[0][1] + P[1][1]],
         [P[1][0] + P[1][1], P[1][1] + q_vel]]
    # 修正
    s = P[0][0] + r
    k0, k1 = P[0][0] / s, P[1][0] / s
    innov = y - x[0]
    x = [x[0] + k0 * innov, x[1] + k1 * innov]
    P = [[(1 - k0) * P[0][0], (1 - k0) * P[0][1]],
         [P[1][0] - k1 * P[0][0], P[1][1] - k1 * P[0][1]]]
    kf.append(x[0])

W, H, L, R, TOP, BOT = 760, 380, 40, 20, 40, 320
lo, hi = min(price) - 1, max(price) + 1
X = lambda t: L + (W - L - R) * t / (N - 1)
Y = lambda v: BOT - (v - lo) / (hi - lo) * (BOT - TOP)


def path(vals):
    pts = [(X(t), Y(v)) for t, v in enumerate(vals) if v is not None]
    return "M" + " L".join(f"{a:.1f},{b:.1f}" for a, b in pts)


dots = "".join(f'<circle cx="{X(t):.1f}" cy="{Y(p):.1f}" r="2.2" class="k-dot"/>' for t, p in enumerate(price))
tx = X(60)
svg = f'''<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" role="img" class="fig-svg" aria-label="示意圖：雜訊很多的價格點、12 天移動平均線和卡爾曼濾波器線。價格在中間轉頭向下時，卡爾曼濾波器比移動平均更早跟著轉彎">
<line x1="{tx:.1f}" x2="{tx:.1f}" y1="{TOP - 10}" y2="{BOT}" class="k-turn"/>
<text x="{tx + 6:.1f}" y="{TOP - 14}" class="f-lab">真實走勢在這裡轉頭向下</text>
{dots}
<path d="{path(ma)}" class="k-ma"/>
<path d="{path(kf)}" class="k-kf"/>
<g class="f-lab"><circle cx="{L + 6}" cy="{H - 34}" r="4" class="k-dot"/><text x="{L + 16}" y="{H - 30}">每天的價格（有雜訊）</text>
<line x1="{L + 190}" x2="{L + 220}" y1="{H - 34}" y2="{H - 34}" class="k-ma"/><text x="{L + 228}" y="{H - 30}">12 天移動平均：慢半拍</text>
<line x1="{L + 410}" x2="{L + 440}" y1="{H - 34}" y2="{H - 34}" class="k-kf"/><text x="{L + 448}" y="{H - 30}">卡爾曼濾波器：較早轉彎</text></g>
<text x="{W - R}" y="{H - 6}" text-anchor="end" class="f-note">示意，非真實資料（模擬產生）</text>
</svg>'''
OUT.write_text(svg, encoding="utf-8")
pk = lambda s: next(t for t in range(61, N) if s[t] < max(v for v in s[50:t] if v is not None) - 1.5)
lag_ma = pk(ma)
lag_kf = pk(kf)
print(f"已產生 {OUT.name}：真實第 60 天轉頭；從高點回落 1.5 的那天，移動平均第 {lag_ma} 天，卡爾曼第 {lag_kf} 天")
