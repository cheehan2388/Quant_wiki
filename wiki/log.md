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
