---
title: 收錄紀錄
type: overview
sources: []
updated: 2026-11-23
---

# 收錄紀錄

每次收錄、健檢都記一筆。格式：日期、動作、新增或更新的頁面、檢查抓到什麼、怎麼修。

## 2026-11-23 #0 建立骨架
- 新增：AGENTS.md、CLAUDE.md、tools/check.py、raw/sources.md、index、who-pays、todo、log。

## 2026-11-23 #1 收錄 momentum-1993
- 讀：期刊全文。
- 新增：[[momentum-1993]]、[[momentum]]。
- 更新：index、who-pays、todo。
- 分支判斷：超額報酬、交易成本、bps 只出現在 1 篇，依規則先進 todo，不建概念頁。
- 檢查：一次通過。

## 2026-11-23 #2 收錄 overtrading-2000
- 讀：期刊版全文。
- 新增：[[overtrading-2000]]、[[retail]]、[[brokers-exchanges]]、[[transaction-costs]]。
- 更新：index、who-pays（新增「反過來：誰在付錢」表）、todo。
- 分支判斷：交易成本、超額報酬都到 2 篇。但這輪已新增 3 個非來源頁，碰到「一次超過 3 頁要先問」的上限，所以超額報酬延到下一輪。
- 檢查第一次失敗，7 個問題：
  - 來源頁連到還不存在的 market-makers 和 bid-ask-spread。論文沒有直接說價差被誰收走，做市商頁沒有來源支持；價差也只出現在 1 篇。→ 拿掉兩個連結，改記進 todo。
  - index 漏列 4 頁、log 漏記本篇。→ 補上。
- 第二次檢查通過。

## 2026-11-23 #3 收錄 pairs-trading-2006
- 讀：2006 年工作論文全文，期刊版只讀摘要。兩個版本都有年化數字：期刊摘要寫「最高約 11%」，NBER 1999 年版摘要寫「最高約 12%」，來源頁採用期刊版的 11%。
- 新增：[[pairs-trading-2006]]、[[pairs-trading]]、[[bid-ask-spread]]、[[excess-return]]（上一輪延後的）。
- 更新：[[momentum]]（加上方向相反的對照）、[[momentum-1993]]、[[overtrading-2000]]（價差連結補回來）、[[transaction-costs]]（加放空成本與新例子）、[[retail]]（散戶難借券）、index、who-pays、todo。
- 分支判斷：bps 到 2 篇、套利者有直接來源，但這輪已新增 3 個非來源頁，延到下一輪。
- 檢查：腳本一次通過。人工比對數字（162 bps、113–225 bps、118→38 bps）與工作論文一致。

## 2026-11-23 #4 收錄 hft-race-2015
- 讀：NBER 會議版全文前半部；期刊版沒有另外核對。
- 新增：[[hft-race-2015]]、[[hft-latency-arb]]、[[market-makers]]、[[arbitrageurs]]。
- 更新：[[overtrading-2000]]（做市商連結補上，但保留「推論」標示）、[[bid-ask-spread]]（價差為什麼存在）、[[transaction-costs]]（速度成本）、[[pairs-trading]]、index、who-pays、todo。
- 分支判斷：本來想建「高頻交易者」玩家頁，但它和策略頁 [[hft-latency-arb]] 內容幾乎重複，改成併進 [[arbitrageurs]] 的「快速版」。一價定律到 2 篇、bps 第二次延後，都因 3 頁上限。
- 檢查：腳本一次通過。人工檢查發現 [[who-pays]] 的高頻列寫了「論文原話」，對照來源頁確認論文確實直接說成本轉嫁給一般投資人，保留。
