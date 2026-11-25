# Quant_wiki：開心的 Quant Wiki

用白話整理量化交易研究的 LLM Wiki。核心問題：**交易策略到底在賺誰的錢？**

## 網站
**https://cheehan2388.github.io/Quant_wiki/** （首頁是唯一入口）
- 第一次來 → 教學簡報「配對交易：賭雙胞胎會回來」（`slides.html`）
- 想深入或查證 → Wiki 配對交易篇（`pairs.html`）；完整版（`wiki.html`）
- 想知道怎麼做出來的 → 流程說明（`process.html`，原文在 [slides/pairs-trading/PROCESS.md](slides/pairs-trading/PROCESS.md)）
- 最新更新寫在 [site/updates.md](site/updates.md)，首頁會自動顯示

## 結構
- 規則：[AGENTS.md](AGENTS.md)（AI 協作規則：收錄、提問、健檢三種模式）
- 原始資料清單：[raw/sources.md](raw/sources.md)
- Wiki 內容：`wiki/`（從 [wiki/pairs-guide.md](wiki/pairs-guide.md) 或 [wiki/who-pays.md](wiki/who-pays.md) 開始讀）
- 收錄紀錄：[wiki/log.md](wiki/log.md)

## 指令
```bash
python3 tools/build_site.py                              # 檢查並重新產生整個網站 docs/（平常只要這一行）
python3 tools/check.py                                   # Wiki 健檢
python3 tools/check_slides.py slides/pairs-trading/deck.md  # 簡報檢查
python3 tools/build_viewer.py --edition pairs            # 產生配對交易篇 → docs/pairs.html
python3 tools/build_slides.py slides/pairs-trading/deck.md  # 產生簡報（檢查沒過就不產生）
```
需要 Python 3 與兩個套件：`pip install markdown latex2mathml`。
