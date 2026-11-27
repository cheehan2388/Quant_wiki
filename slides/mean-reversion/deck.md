# 簡報稿：均值回歸配對交易：把價差當彈簧來量
#
# 格式同 slides/pairs-trading/deck.md：每頁 `=== id | 版型 | 引用的 Wiki 頁 | 選項 ===`。
# 檢查：python3 tools/check_slides.py slides/mean-reversion/deck.md
# 主要來源：Avellaneda & Lee（2010），見 wiki/sources/statarb-ou-2010.md

=== cover | cover | statarb-ou-2010, mean-reversion | ===
# 均值回歸配對交易：把價差當彈簧來量

從「拉太開就進場」，到「算出價差多快回來」

開心的 Quant Wiki・論文導讀：Avellaneda & Lee (2010)

=== recap | bullets | pairs-trading | define:做空, define:標準差, define:平倉 ===
## 先複習：入門版配對交易
- 找一對平常一起動的，每天算兩者的差距。
- 差距超過 2 個**標準差**：買落後的、**做空**領先的。
- 差距回到 0 就**平倉**；6 個月還沒回來，強制平倉。
> **標準差**：差距「平常晃多大」的尺。
> **做空**：先借來賣掉，之後買回來還；價格跌就賺。
> **平倉**：把買的賣掉、空的買回，結束這筆交易。

=== why | bullets | pairs-trading, pairs-review-2015 | ===
## 為什麼需要更好的方法：入門版有三個盲點
- **不知道會不會回來**：只看過去像不像，挑到的配對容易一路發散。
- **不知道要等多久**：6 個月一刀切，回得快和回得慢的配對被一樣對待。
- **一把尺量所有配對**：每一對都用 2 個標準差，不管它平常怎麼晃。

美股的簡單版配對交易，每月多賺的報酬從 0.86% 降到 0.24%，越來越不能只靠簡單規則。

=== idea | statement | statarb-ou-2010, mean-reversion | ===
## Avellaneda & Lee 的想法
先用一條式子描述「價差怎麼動」，再決定怎麼交易。

只要知道價差拉回多快、平常晃多大，就能回答：何時進場、要等多久、何時放棄。

=== spring | bullets | mean-reversion, statarb-ou-2010 | define:OU 過程 ===
## 一個比喻：彈簧
- 價差拉離平均，像拉開一條彈簧：拉得越遠，往回拉的力越大。
- 每天只回去「距離的一部分」，所以一開始回得快，越接近平均越慢。
- 旁邊一直有人隨機推它，這就是每天的雜訊。
> **OU 過程**：論文用來描述價差的模型。「彈簧」是 Wiki 的比喻，論文裡沒有這個詞。

=== ar1 | bullets | stationarity, mean-reversion, fpp3-2021 | define:迴歸, define:自我迴歸 ===
## 第一塊積木：AR(1)，用昨天猜今天
$$X_{n+1} = a + b\,X_n + \zeta_{n+1}$$
- $X_n$：第 $n$ 天的價差。
- $b$：昨天的偏離，今天還留下幾成。**最重要的數字。**
- $a$：決定平衡點在哪；$\zeta$：今天新的隨機推擠。
> **迴歸**：在散點圖上找一條最貼近的直線。
> **自我迴歸 AR(1)**：拿自己「昨天的值」當迴歸裡的 x。

=== bvalue | table | mean-reversion, stationarity, fpp3-2021 | define:半衰期 ===
## $b$ 決定一切
| $b$ | 像什麼 | 半衰期 |
|---|---|---|
| 0 | 沒有記憶，每天都是全新的雜訊 | — |
| 0.8 | 繩子很緊的狗 | 約 3.1 天 |
| 0.99 | 繩子很鬆的狗 | 約 69 天 |
| 1 | 沒拴的狗（隨機漫步），不會回來 | 永遠 |

要會回來，$b$ 必須在 −1 和 1 之間。
> **半衰期**：偏離縮成一半要幾天，$h = \ln 2 / (-\ln b)$。

=== halflife | figure | mean-reversion | illustrative ===
## 看得見的差別
{{figure:ou-halflife}}

=== ou | bullets | statarb-ou-2010, mean-reversion | ===
## 第二塊積木：OU 過程，連續時間的彈簧
$$dX = \kappa\,(m - X)\,dt + \sigma\,dW$$
- $m$：平衡點。$m - X$：被拉開多遠，在下面就往上拉。
- $\kappa$：彈簧多硬，也就是拉回的速度。
- $\sigma\,dW$：一小段時間裡的隨機推擠，$\sigma$ 是推擠的大小。

=== bridge | bullets | mean-reversion, statarb-ou-2010 | ===
## AR(1) 和 OU 是同一件事
- OU 是「每一瞬間」的寫法；AR(1) 是「每天看一次」的寫法。
- 由論文式 13：$b = e^{-\kappa \Delta t}$，所以 $\kappa = -\ln(b) \times 252$。
- 所以**不用解微分方程**：對價差做一次 AR(1) 迴歸，就能算出 $\kappa$。
- 252 是一年大約的交易日數；加密貨幣全年無休，可改用 365。

=== sscore | bullets | statarb-ou-2010, mean-reversion | define:s 分數 ===
## 每一對都有自己的尺
$$m = \frac{a}{1-b} \qquad s = \frac{X - m}{\sigma_{eq}}$$
$$\sigma_{eq} = \sqrt{\frac{\mathrm{Var}(\zeta)}{1-b^2}}$$
- $\sigma_{eq}$：這條彈簧長期下來平常晃多大，由每一對自己的資料算出。
- 所以同樣是「偏離 2 塊錢」，在很穩的配對可能很誇張，在很亂的配對可能很平常。
> **s 分數**：現在離平衡點幾個「平常的晃動」。

=== steps | bullets | statarb-ou-2010, regression | ===
## 論文的五個步驟（每天收盤後做一次）
1. 用過去 60 天，把股票報酬對它的產業 ETF 做迴歸，斜率 $\beta$ 就是要做空多少 ETF。
2. 把扣掉產業後剩下的部分累加起來，得到價差 $X$。
3. 對 $X$ 做 AR(1)，得到 $a$、$b$。
4. 換算 $\kappa$、$m$、$\sigma_{eq}$，算出 s 分數。
5. 照規則進出場。

=== rules | table | statarb-ou-2010 | ===
## 進出場規則
| 情況 | 動作 |
|---|---|
| s < −1.25 | 買進價差（買股票、做空 $\beta$ 倍的 ETF） |
| s > +1.25 | 賣出價差（反過來） |
| 多單的 s 回到 −0.50 以上 | 平倉 |
| 空單的 s 回到 0.75 以下 | 平倉 |
| $\kappa$ < 8.4（回歸時間超過 1.5 個月） | 不開新倉，已開的平倉 |

門檻是用 2000–2004 年的資料挑的。最後一列就是「何時放棄」：看彈簧多硬，不看價格虧多少。

=== signals | figure | mean-reversion | illustrative ===
## 看一次完整的進出場
{{figure:ou-signals}}

=== handcalc | table | mean-reversion | illustrative ===
## 手算一次（示意）
估出 $a = 0.1$、$b = 0.8$、$\mathrm{Var}(\zeta) = 0.36$ → $m = 0.5$、$\sigma_{eq} = 1$。今天價差 −1.0 → $s = -1.5$，**進場**。$\kappa \approx 56.2 > 8.4$，可以做；半衰期約 3.1 天。

| 天 | 0 | 1 | 2 | 3 | 4 | 5 |
|---|---|---|---|---|---|---|
| s 分數 | −1.5 | −1.2 | −0.96 | −0.77 | −0.61 | −0.49 |
| 動作 | 進場 | 持有 | 持有 | 持有 | 持有 | **平倉** |

（沒有雜訊時的平均走法：每天乘 0.8）

=== results | table | statarb-ou-2010, bps | define:夏普比率, define:主成分, define:bps ===
## 結果：扣成本後有賺，但越來越難
| 版本 | 期間 | 夏普比率 |
|---|---|---|
| 主成分 | 1997–2007 | 1.44 |
| 主成分 | 2003–2007 | 0.9 |
| 產業 ETF | 1997–2007 | 1.1 |
| 產業 ETF＋成交量 | 2003–2007 | 1.51 |

已扣每筆一來一回 10 bps 的成本。
> **夏普比率**：賺的錢除以帳戶起伏的大小，越高越穩。
> **主成分**：不用產業 ETF，改從所有股票的共同走勢裡找出幾個「共同因子」當夥伴。
> **bps**：萬分之一，10 bps 就是 0.1%。

=== risks | bullets | statarb-ou-2010, crypto-pairs-2020 | define:回撤 ===
## 什麼時候會出事
- **回得太慢**：$b$ 接近 1，模型不成立，直接不做。
- **大家同時平倉**：2007 年 8 月，所有策略突然大幅回撤（主成分版 5%、ETF 版 10%），約 10 天後才回升。
- **門檻是歷史挑的**：1.25 等數字來自美股 2000–2004 年，換市場要重新驗證。
- **加密貨幣日線**：簡單配對每月只有 −0.07% 到 1.36%。
> **回撤**：帳戶從最高點往下掉了多少。

=== crypto | bullets | mean-reversion, perpetual-futures-2024, statarb-ou-2010 | ===
## 想套到加密貨幣上（推論，待確認）
- 把「股票對產業 ETF」換成「幣對幣」，或「幣對一籃子大幣」。
- 252 改成 365。
- 用永續合約做空，成本是資金費率：幣安每 8 小時付一次，平靜時 0.01%。
- 這些是 Wiki 的想法，論文只做了美股。

=== answers | table | statarb-ou-2010, mean-reversion | define:參數 ===
## 回到四個問題
| 問題 | 這篇的答案 |
|---|---|
| 在賺誰的錢？ | 原文：市場反應過度，資產暫時被高估或低估，之後會修正 |
| 靠什麼假設？ | 價差能用最簡單的 OU 過程描述；參數在 60 天內不變 |
| 什麼時候失效？ | 回得太慢；大家同時平倉；2003 年以後績效下降 |
| 扣成本後剩多少？ | 扣一來一回 10 bps 後，夏普比率 0.9 到 1.51 |

> **參數**：模型裡要從資料估出來的數字，例如 $a$、$b$、$\kappa$。

=== quiz | quiz | mean-reversion, statarb-ou-2010 | ===
## 小測驗
?? 某組配對估出 b = 0.99，照論文的規則該怎麼辦？
- [ ] 馬上進場，因為它很穩
- [x] 不做：κ 約 2.5，低於 8.4，回得太慢
- [ ] 把門檻放寬到 2 個標準差
!! 回歸太慢，半衰期約 69 天，模型的「參數不變」假設撐不住，論文直接不交易。
?? s 分數是 −1.5，代表什麼？
- [x] 價差在平衡點下方 1.5 個「平常的晃動」，可以買進價差
- [ ] 價差每天會跌 1.5%
- [ ] 還要 1.5 天才會回來
!! s 分數是「偏離 ÷ 長期平常的晃動」；低於 −1.25 就買進價差。
?? 為什麼論文可以用一次 AR(1) 迴歸，就估出 OU 過程的拉回速度？
- [ ] 因為 OU 過程只能用在股票上
- [x] 每天看一次的 OU 過程就是 AR(1)，b 和 κ 可以互相換算
- [ ] 因為迴歸可以消除所有雜訊
!! b = e^(−κΔt)，所以 κ = −ln(b) × 252。

=== takeaway | statement | mean-reversion, statarb-ou-2010 | ===
## 一句話帶走
**先量出價差這條彈簧有多硬、平常晃多大，再決定何時進場、等多久、何時放棄。**

這套方法讓每一組配對都有自己的尺，但門檻和參數都要在你自己的市場上重新驗證。

=== sources | sources | statarb-ou-2010 | ===
## 參考資料
- Avellaneda, M. & Lee, J.-H. (2010). Statistical arbitrage in the US equities market. *Quantitative Finance*, 10(7), 761–782. 本簡報讀的是 2009 年 6 月 15 日的工作論文版。
- Hyndman, R. J. & Athanasopoulos, G. (2021). *Forecasting: Principles and Practice*, 3rd ed. OTexts.（AR(1) 的平穩條件）
- Krauss, C. (2015). Statistical arbitrage pairs trading strategies: Review and outlook. FAU Discussion Papers 09/2015.
- Fil, M. & Kristoufek, L. (2020). Pairs trading in cryptocurrency markets. *IEEE Access*, 8.
- He, S., Manela, A., Ross, O. & von Wachter, V. (2024). Fundamentals of perpetual futures. arXiv:2212.06888.
- 兩張示意圖用模擬資料畫成，不是論文的資料。

所有內容都來自「開心的 Quant Wiki」的模型頁「均值回歸與半衰期」「平穩」「迴歸」與相關來源頁。
