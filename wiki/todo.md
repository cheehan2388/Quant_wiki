---
title: 待寫清單
type: overview
sources: []
updated: 2026-11-25
---

# 待寫清單

新點子只記在這裡，這一輪不展開。「出現次數」是提到它的來源頁數量，到 2 就可以拆成概念頁（AGENTS.md 第 7 節）。

## 概念

| 概念 | 出現在 | 出現次數 | 狀態 |
|---|---|---|---|
| 交易成本 | [[momentum-1993]]、[[overtrading-2000]]、[[pairs-trading-2006]] | 3 | 已拆成 [[transaction-costs]] |
| 超額報酬 | [[momentum-1993]]、[[overtrading-2000]]、[[pairs-trading-2006]] | 3 | 已拆成 [[excess-return]] |
| 買賣價差 | [[overtrading-2000]]、[[pairs-trading-2006]] | 2 | 已拆成 [[bid-ask-spread]] |
| bps（基點） | [[momentum-1993]]、[[pairs-trading-2006]] | 2 | 已拆成 [[bps]]（#5） |
| 一價定律 | [[pairs-trading-2006]]、[[hft-race-2015]]、[[crypto-arb-2020]] | 3 | 已拆成 [[law-of-one-price]]（#5） |
| 資本管制 | [[crypto-arb-2020]] | 1 | 先寫在來源頁裡 |
| 套利的極限 | [[limits-arbitrage-1997]]、[[twin-shares-2009]]、[[pairs-decline-2010]]、[[ltcm-2006]] | 4 | 已拆成 [[limits-of-arbitrage]]（配對篇） |
| 槓桿 | [[ltcm-2006]]、[[twin-shares-2009]]、[[limits-arbitrage-1997]] | 3 | 已拆成 [[leverage]]（配對篇） |
| 共整合（cointegration） | [[pairs-review-2015]]、[[crypto-pairs-2020]]、[[statarb-ou-2010]] | 3 | 已拆成模型頁 [[cointegration]]（#13–#18） |
| 迴歸、避險比例 | [[fpp3-2021]]、[[pairs-review-2015]]、[[statarb-ou-2010]]、[[crypto-pairs-2020]] | 4 | 已拆成模型頁 [[regression]] |
| 平穩、單根檢定 | [[fpp3-2021]]、[[pairs-review-2015]]、[[statarb-ou-2010]] | 3 | 已拆成模型頁 [[stationarity]]。待補：ADF 檢定的虛無假設（和 KPSS 相反）還沒有來源 |
| 均值回歸、OU、半衰期 | [[statarb-ou-2010]]、[[pairs-review-2015]]、[[fpp3-2021]] | 3 | 已拆成模型頁 [[mean-reversion]] |
| 資金費率 | [[perpetual-futures-2024]] | 1 | 先寫在來源頁和 [[transaction-costs]]、[[pairs-trading]] 裡 |
| 停損 | [[crypto-pairs-2020]]、[[pairs-review-2015]] | 2 | 可以拆頁；這輪新增頁數已到上限，下次再問 |
| 多重檢定（測很多組時的假警報） | [[pairs-review-2015]]、[[backtest-overfitting-2014]] | 2 | 先寫在 [[cointegration]] 裡；可以和過度配適合成一頁 |
| 移動平均 | [[kalman-trend-2016]] | 1 | 先寫在來源頁裡 |
| 卡爾曼濾波器 | [[kalman-trend-2016]]、[[kalman-course-2001]]、[[kalman-gaussian-2012]] | 3 | 已拆成 [[kalman-filter]] |
| 變異數、常態分布 | [[kalman-course-2001]]、[[kalman-gaussian-2012]] | 2 | 已拆成 [[variance-normal]]（使用者說沒有直覺，作為前置知識） |
| 過度配適（同一段資料調參又測試） | [[kalman-trend-2016]]、[[backtest-overfitting-2014]]、[[pairs-review-2015]]、[[crypto-pairs-2020]] | 4 | 已收錄專門的來源 [[backtest-overfitting-2014]]；使用者 2026-11-25 決定先不拆概念頁（下次可再問） |
| 夏普比率、最大回撤 | [[kalman-trend-2016]]、[[statarb-ou-2010]]、[[crypto-pairs-2020]]、[[backtest-overfitting-2014]]、[[perpetual-futures-2024]] | 5 | 可以拆頁，還沒問使用者 |
| 頻繁批次拍賣 | [[hft-race-2015]] | 1 | 先寫在來源頁裡 |
| 放空成本 | [[pairs-trading-2006]]、[[crypto-pairs-2020]]、[[perpetual-futures-2024]] | 3 | 已拆成 [[transaction-costs]] 裡的一段（加密貨幣的借幣年費與資金費率） |

## 玩家

| 玩家 | 狀態 |
|---|---|
| 套利者 | 已建 [[arbitrageurs]]（#4） |
| 做市商 | 已建 [[market-makers]]（#4） |
| 高頻交易者 | 先併在 [[arbitrageurs]] 裡（快速版套利者），避免和 [[hft-latency-arb]] 重複 |

## 你自己的實驗（等你提供資料）

- **OKX–Binance 比特幣永續價差回測**：之前跑出的 IC 很強，但還沒確認扣完 10 bps 成本後是否還有利潤。[[crypto-arb-2020]] 說同一國內交易所價差通常不到 1%，可以拿來對照。要建「實驗紀錄」頁，需要你提供回測結果。

## 待你確認的推論

這些推論出現在總覽或導覽頁。請逐條告訴我：保留（改成「推論，已確認」）、修改，或拿掉。

| # | 推論 | 出現在 | 根據 |
|---|---|---|---|
| 1 | 動量賺的是「對消息反應慢的人」的錢 | [[who-pays]] | [[momentum-1993]] 說價格對公司消息反應延遲，但沒點名是誰 |
| 2 | 配對交易賺的是「把價格暫時推歪的人」的錢 | [[who-pays]]、[[pairs-guide]] | [[pairs-trading-2006]] 說是暫時定錯；[[pairs-decline-2010]] 說危機時賺最多 |
| 3 | 跨交易所套利賺的是「在溢價市場買幣的人」的錢 | [[who-pays]] | [[crypto-arb-2020]] 的價差方向：美歐以外幾乎總是溢價 |
| 4 | 散戶付的買賣價差流到做市商 | [[who-pays]] | [[overtrading-2000]] 沒說誰收走價差；[[hft-race-2015]] 說做市商靠價差賺錢 |
| 5 | 卡爾曼濾波趨勢策略「可能和動量一樣」賺反應慢的人的錢 | [[who-pays]] | [[kalman-trend-2016]] 沒討論；只是想法相近 |
| 6 | 配對交易近年扣完成本「可能所剩無幾」 | [[pairs-guide]] | 拿 [[pairs-trading-2006]] 的成本估計對照 [[pairs-decline-2010]] 的近年報酬，兩篇口徑不一定相同 |
| 7 | 用永續合約做配對，兩腳的資金費率平靜時大致抵銷，某一檔被炒熱時空它的成本可能大增 | [[pairs-trading]] | 依 [[perpetual-futures-2024]] 的幣安算法推出；論文沒有研究配對交易 |

## 還沒有來源支持的問題

- 動量策略在 1990 年以後、參與者變多之後還剩多少？
- 「反應慢的人」「把價格推開的人」具體是誰？
- 零佣金時代，散戶頻繁交易的代價變多少？
- Do & Faff（2012）專門研究配對交易扣成本後還剩多少，可收錄。
- 卡爾曼濾波器拿來追蹤配對交易的避險比例（論文提到 Chan 2013），可收錄；正好對應你加密配對篩選時 beta 一直跳的問題。2026-11-25 這輪沒找到可公開讀取的來源，[[regression]] 先說明了滾動估計為什麼會跳。
- ADF 單根檢定的虛無假設：要找一份來源確認（[[stationarity]] 目前標為待確認）。
- 共整合的正式理論：[[cointegration]] 目前只到直覺和 Engle-Granger 兩步驟的做法；正式定義（「整合階數」）、為什麼對殘差做檢定要用不同的臨界值、Johansen 方法都還沒有來源。候選：Engle & Granger（1987）原始論文，或時間序列教科書的共整合章節。
- 論文常用的數學符號（Σ 加總、下標、隨機微分方程的 $dt$、$dW$）：使用者讀論文時卡住，可考慮做一頁「讀論文需要的符號」，要先找來源。
- 永續合約上的配對交易：兩腳都要付或收資金費率，實際淨成本多少？還沒有來源研究。
- 把 Benhamou 2016 的模型 1 用樣本外資料重跑一次，看績效還剩多少。
- 加密貨幣的配對交易：你 11 月做的大型幣配對篩選（6 組都沒通過協整檢定、APT/SUI 單邊發散）可以整理成實驗紀錄頁。
- 2018 年以後，加密貨幣跨國價差還有多大？
- 資金費率套利（永續合約）在賺誰的錢？
