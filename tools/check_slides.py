#!/usr/bin/env python3
"""簡報檢查：確認簡報內容都來自 Wiki，而且新手看得懂。

用法：python3 tools/check_slides.py slides/pairs-trading/deck.md

檢查項目
1. 每頁至少引用一個 Wiki 頁面，而且引用的頁面存在。
2. 數字可追溯：非示意頁裡的每個數字，都要能在「這頁引用的 Wiki 頁」裡找到
   （整數允許四捨五入，例如 −36 對得上 Wiki 的 −36.2）。
3. 術語先解釋：術語第一次出現的那一頁，必須在負責解釋它的頁（define:）之後或同一頁。
4. 字數：每頁正文（不含表格、圖、測驗）不超過 MAX_CHARS 個字；參考資料頁除外。
限制：數字檢查只比對數值，不保證語意正確，語意仍需人工看過。
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
WIKI = ROOT / "wiki"
MAX_CHARS = 200
JARGON = ["放空", "平倉", "標準差", "槓桿", "一價定律", "套利的極限", "保證金",
          "bps", "超額報酬", "相關性",
          "移動平均", "卡爾曼濾波器", "卡爾曼增益", "參數", "做多", "做空", "期貨",
          "回撤", "夏普比率"]
NUM_RE = re.compile(r"(?<![A-Za-z])[−-]?\d[\d,]*(?:\.\d+)?")


def nums(text):
    out = []
    for m in NUM_RE.findall(text):
        try:
            out.append(abs(float(m.replace(",", "").replace("−", "-"))))
        except ValueError:
            pass
    return out


def parse(path):
    slides, cur = [], None
    for line in path.read_text(encoding="utf-8").splitlines():
        m = re.match(r"^=== (.+?) ===$", line)
        if m:
            sid, layout, cites, flags = [x.strip() for x in m.group(1).split("|")]
            cur = {"id": sid, "layout": layout,
                   "cites": [c.strip() for c in cites.split(",") if c.strip()],
                   "flags": [f.strip() for f in flags.split(",") if f.strip()], "body": []}
            slides.append(cur)
        elif cur is not None:
            cur["body"].append(line)
        # 檔頭的 # 註解行（第一頁之前）略過
    for s in slides:
        s["body"] = "\n".join(s["body"]).strip()
    return slides


def main(deck):
    pages = {p.stem: p.read_text(encoding="utf-8") for p in WIKI.rglob("*.md")}
    slides = parse(Path(deck))
    errors = []
    defined_at, first_use = {}, {}
    for i, s in enumerate(slides):
        tag = f"第 {i + 1} 頁（{s['id']}）"
        if not s["cites"]:
            errors.append(f"{tag}：沒有引用任何 Wiki 頁面")
        for c in s["cites"]:
            if c not in pages:
                errors.append(f"{tag}：引用的 Wiki 頁面 {c} 不存在")
        body = re.sub(r"\{\{figure:[a-z0-9\-]+\}\}", "", s["body"])
        text_no_title = "\n".join(l for l in body.splitlines() if not l.startswith("#"))

        if "illustrative" not in s["flags"] and s["layout"] not in ("sources",):
            source_nums = [n for c in s["cites"] if c in pages for n in nums(pages[c])]
            for n in nums(text_no_title):
                ok = any(abs(w - n) < 1e-9 for w in source_nums) or (
                    n == int(n) and any(abs(w - n) < 0.5 for w in source_nums))
                if not ok:
                    errors.append(f"{tag}：數字 {n:g} 在引用的頁面 {s['cites']} 裡找不到")

        for f in s["flags"]:
            if f.startswith("define:"):
                defined_at[f[7:]] = i
        for t in JARGON:
            if t in body and t not in first_use:
                first_use[t] = i

        if re.search(r"推論(?![，,]\s*(待確認|已確認))", body):
            errors.append(f"{tag}：推論要標成「推論，待確認」或「推論，已確認」（AGENTS.md 第 8 節）")
        prose = [l for l in text_no_title.splitlines()
                 if not re.match(r"^\s*(\||\?\?|!!|- \[)", l)]
        n = len(re.sub(r"[\s*>#\-]", "", "".join(prose)))
        if n > MAX_CHARS and s["layout"] != "sources":
            errors.append(f"{tag}：正文 {n} 字，超過 {MAX_CHARS} 字，新手讀不完")

    for t, i in first_use.items():
        if t not in defined_at:
            errors.append(f"術語「{t}」在第 {i + 1} 頁（{slides[i]['id']}）出現，但沒有任何一頁解釋它")
        elif defined_at[t] > i:
            errors.append(f"術語「{t}」在第 {i + 1} 頁先出現，第 {defined_at[t] + 1} 頁才解釋")

    print(f"共 {len(slides)} 頁")
    if errors:
        print(f"簡報檢查失敗，共 {len(errors)} 個問題：")
        for e in errors:
            print(" - " + e)
        sys.exit(1)
    print("簡報檢查通過")


if __name__ == "__main__":
    main(sys.argv[1])
