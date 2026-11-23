# 簡報稿：配對交易：賭雙胞胎會回來
#
# 格式：每頁用一行 `=== id | 版型 | 引用的 Wiki 頁 | 選項 ===` 開頭。
# - 引用：用逗號分隔的 Wiki 檔名。這頁出現的每個數字，都必須能在引用頁裡找到。
# - 選項：illustrative（示意頁，數字不檢查）、define:名詞（這頁負責解釋這個名詞）。
# - 版型：cover、statement、bullets、figure、table、quiz、flow、sources
# 檢查：python3 tools/check_slides.py slides/pairs-trading/deck.md

=== cover | cover | pairs-guide | ===
# 配對交易：賭雙胞胎會回來

交易策略到底在賺誰的錢？

開心的 Quant Wiki・配對交易篇

=== question | statement | who-pays, pairs-guide | ===
## 先問一個問題
你在市場上賺到的每一塊錢，都是某個人付的。

這份簡報要回答：**配對交易賺的是誰的錢？**最後那個人，可能就是你自己。

=== twins | bullets | pairs-trading, law-of-one-price | define:配對交易, define:一價定律, define:放空, define:平倉 ===
## 什麼是配對交易
- 找兩檔走勢像**雙胞胎**的股票，平常一起漲、一起跌。
- 某天兩者突然拉開：買落後的那檔，同時**放空**領先的那檔。
- 等兩者靠回來，兩邊一起平倉，賺中間拉開的那段。
> **放空**：先借股票來賣，之後再買回來還。股價下跌時賺錢。
> **平倉**：把手上的部位結清，賺賠就此確定。
> **一價定律**：同樣的東西，價格應該一樣。配對交易賭的就是「暫時不一樣」會回到「一樣」。

=== how | figure | pairs-trading | define:標準差 ===
## 一張圖看懂
{{figure:pairs-spread}}
> **標準差**：衡量平常晃動幅度的尺。超過 2 個標準差，代表「比平常拉開得多很多」。

=== example | bullets | pairs-trading | illustrative ===
## 一個數字例子（示意）
- A 和 B 過去一年幾乎同步。某天 A 比平常多跌了 6%，超過 2 個標準差。
- 你買 10 萬元的 A，放空 10 萬元的 B。大盤漲跌時，兩邊互相抵銷。
- 兩週後兩者回到同步：賺約 6,000 元，再扣手續費和價差。
- **但如果 A 是因為公司真的出事才跌的**，那 6% 不會回來，還可能越拉越開。

=== evidence | statement | pairs-trading-2006 | ===
## 它真的賺錢嗎？
Gatev 等人用 1962–2002 年的美股測試：最像的前 20 對，**年化最高約 11%**。

用隨機配對當對照組，幾乎賺不到錢，所以不是運氣。

=== decline | table | pairs-decline-2010, excess-return | define:超額報酬 ===
## 但越來越難賺
| 期間 | 前 20 對每月超額報酬 |
|---|---|
| 1962–1988 | 0.86% |
| 1989–2002 | 0.37% |
| 2003–2009 | 0.24% |

有趣的是：2007–09 年金融危機時，它反而賺得特別多。恐慌讓價格走得更歪。
> **超額報酬**：扣掉「什麼都不做也拿得到」的基準之後，多賺的部分。

=== perfect | bullets | twin-shares-2009, ltcm-2006 | ===
## 最完美的雙胞胎：Royal Dutch 和 Shell
- 同一個集團，現金流按 60：40 分給兩家公司，一家在荷蘭上市、一家在英國上市。
- 照理說，兩檔股價應該永遠維持固定比例。
- 實際上，1980–2002 年間偏離最多到 **−36%**。
- 做這種套利，有些部位要等**將近 9 年**才收斂。

=== ltcm1 | figure | ltcm, ltcm-2006 | define:槓桿 ===
## LTCM：最會算的人
{{figure:ltcm-timeline}}
> **槓桿**：借錢放大部位。27 倍槓桿，代表用 1 元本錢做 27 元的生意。

=== ltcm2 | bullets | ltcm, ltcm-2006 | define:相關性 ===
## 1998 年：價差反而拉開
- 1997 年 Royal Dutch 貴了約 8%，LTCM 賭它會回來。
- 俄羅斯違約後，溢價一度超過 **17%**，LTCM 單月虧掉 44% 的資本。
- 平常互不相關的部位，相關性從 0.1 跳到 0.7：所有交易一起出事。
- 14 家銀行出資 36 億美元接管。價差到 2001 年才消失。

**他們賭對了方向，但撐不到那一天。**
> **相關性**：兩件事一起動的程度。0 是各走各的，1 是完全同步。

=== limits | bullets | limits-of-arbitrage, limits-arbitrage-1997, leverage | define:套利的極限, define:保證金 ===
## 為什麼撐不住：套利的極限
- **時間**：最後會回來，但不知道是哪一天。
- **錢不是自己的**：出資人看到虧損就撤資，偏偏那時機會最好。
- **被迫平倉**：保證金被追繳，只能在最差的價位認賠。
- **大家都在做**：一個人被迫賣，所有人一起虧。
- **關係真的變了**：價差永遠不回來。
> **保證金**：借錢交易時押在帳上的錢。虧到不夠就要補，補不出來就被強制平倉。

=== answers | table | pairs-guide, pairs-trading, bps | define:bps ===
## 回到四個問題
| 問題 | 配對交易的答案 |
|---|---|
| 在賺誰的錢？ | 把價格暫時推歪的人（推論） |
| 靠什麼假設？ | 兩檔關係穩定，而且你撐得到價差回來 |
| 什麼時候失效？ | 做的人變多、公司關係改變、價差先拉得更開 |
| 扣成本後剩多少？ | 早年每半年仍有 113–225 bps；近年可能所剩無幾（推論） |

> **bps**：萬分之一，100 bps = 1%。

=== quiz | quiz | pairs-trading, ltcm, pairs-decline-2010 | ===
## 小測驗
?? A 比 B 多跌了很多，超過 2 個標準差。配對交易會怎麼做？
- [ ] 買 A 也買 B
- [x] 買 A、放空 B
- [ ] 放空 A、買 B
!! 買落後的（A）、放空領先的（B），賭兩者會靠回來。
?? LTCM 的 Royal Dutch／Shell 判斷，最後怎麼了？
- [ ] 判斷錯了，價差從沒回來
- [x] 判斷對了，但價差在 LTCM 被接管後才消失
- [ ] LTCM 及時平倉賺到錢
!! 價差到 2001 年才消失，LTCM 1998 年就被接管了。
?? 為什麼市場恐慌時，配對交易反而賺比較多？
- [ ] 手續費變便宜
- [x] 恐慌讓價格走得更歪，錯價變多
- [ ] 大家都不交易了
!! 研究發現危機期間風險變大，但錯價變多的效果更大。

=== takeaway | statement | pairs-guide | ===
## 一句話帶走
**「最後會收斂」和「你撐得到收斂」是兩件事。**

配對交易賺的錢，很大一部分是承擔「撐不撐得住」這個風險的報酬。

=== process | flow | log | ===
## 附錄：這份簡報怎麼做出來的
{{figure:loop-graph}}

=== run | bullets | log | ===
## 附錄：一次實際執行的紀錄
- **收錄第 2 篇**：檢查失敗 7 項。來源頁連到「做市商」，但論文沒說價差被誰收走，沒有根據 → 拿掉連結，等有來源再建頁。
- **收錄加密貨幣那篇**：抓到 3 個版本矛盾的數字 → 全部寫進頁面，註明採用哪個版本。
- **收錄 LTCM**：檢查失敗 11 項（目錄漏列、紀錄漏寫）→ 補上後通過。
- **簡報第 1 次檢查**：失敗 7 項，其中 6 項是術語沒先解釋 → 補上白話解釋後通過。
- **測試檢查器**：故意改錯 2 個數字，2 個都被抓到。

=== reflect | bullets | log | ===
## 附錄：反思
- **最常出錯的是 ③ 更新相關頁**：目錄漏列、紀錄漏寫、連到沒根據的頁。這類機械性錯誤，下一步該讓程式自動產生，不靠事後檢查。
- **其次是 ① 取得資料**：讀不到全文、二手數字互相矛盾。所以加了「讀了什麼」欄位，可信度低的頁面一眼就看得出來。
- **檢查器本身也會錯**：參考資料頁被字數規則誤判，所以調整了規則；也故意塞錯數字，確認它真的會抓。
- **簡報會反過來推動 Wiki**：想講 LTCM 時 Wiki 沒有資料，就回到收錄迴圈補了 4 篇。

=== sources | sources | pairs-trading-2006, pairs-decline-2010, twin-shares-2009, limits-arbitrage-1997, ltcm-2006 | ===
## 參考資料
- Gatev, Goetzmann & Rouwenhorst (2006). Pairs Trading. *Review of Financial Studies*.
- Do & Faff (2010). Does Simple Pairs Trading Still Work? *Financial Analysts Journal*.（只讀摘要）
- de Jong, Rosenthal & van Dijk (2009). The Risk and Return of Arbitrage in Dual-Listed Companies. *Review of Finance*.
- Shleifer & Vishny (1997). The Limits of Arbitrage. *Journal of Finance*.
- MacKenzie (2006). *An Engine, Not a Camera*, Ch. 8. MIT Press.

所有內容都來自「開心的 Quant Wiki・配對交易篇」。
