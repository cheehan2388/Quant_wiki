#!/usr/bin/env python3
"""一個指令產生整個網站（docs/），GitHub Pages 直接發布這個資料夾。

用法：python3 tools/build_site.py

步驟
1. 健檢：tools/check.py（Wiki）、tools/check_slides.py（簡報），任一沒過就停止。
2. docs/wiki.html：完整版 Wiki；docs/pairs.html：配對交易篇。
3. docs/slides.html：簡報（站內相對連結）；slides/pairs-trading/index.html：同一份簡報，
   連結指向 GitHub Pages 網址，方便從 repo 或別處直接打開。
4. docs/process.html：流程說明（slides/pairs-trading/PROCESS.md）。
5. docs/index.html：首頁，「最新更新」欄來自 site/updates.md。
"""
import html
import re
import subprocess
import sys
from pathlib import Path

import markdown

ROOT = Path(__file__).resolve().parent.parent
DOCS = ROOT / "docs"
SITE_URL = "https://cheehan2388.github.io/Quant_wiki/"
REPO_URL = "https://github.com/cheehan2388/Quant_wiki"
DECK = ROOT / "slides" / "pairs-trading" / "deck.md"
PY = sys.executable


def run(*cmd):
    r = subprocess.run([PY, *map(str, cmd)], cwd=ROOT)
    if r.returncode != 0:
        sys.exit(f"停止：{' '.join(map(str, cmd))} 沒有通過")


# 1. 健檢
run("tools/check.py")
run("tools/check_slides.py", DECK)

# 2–3. Wiki 與簡報
run("tools/build_viewer.py", "--out", DOCS / "wiki.html")
run("tools/build_viewer.py", "--edition", "pairs", "--out", DOCS / "pairs.html")
run("tools/build_slides.py", DECK, "--out", DOCS / "slides.html")
run("tools/build_slides.py", DECK, "--base", SITE_URL)

# 4. 流程說明
proc_md = (ROOT / "slides" / "pairs-trading" / "PROCESS.md").read_text(encoding="utf-8")
proc_html = markdown.markdown(proc_md, extensions=["tables", "fenced_code"])
proc_tpl = (ROOT / "tools" / "process_template.html").read_text(encoding="utf-8")
(DOCS / "process.html").write_text(proc_tpl.replace("__BODY__", proc_html), encoding="utf-8")
print("已產生 process.html")

# 5. 首頁
entries = []
cur = None
for line in (ROOT / "site" / "updates.md").read_text(encoding="utf-8").splitlines():
    m = re.match(r"^## (\d{4}-\d{2}-\d{2}) \| (.+?) \| (.+)$", line)
    if m:
        cur = {"date": m.group(1), "title": m.group(2).strip(), "href": m.group(3).strip(), "desc": []}
        entries.append(cur)
    elif cur is not None and line.strip() and not line.startswith("#"):
        cur["desc"].append(line.strip())
if not entries:
    sys.exit("site/updates.md 沒有任何更新紀錄")
for e in entries:
    page = e["href"].split("#")[0]
    if not page.startswith("http") and not (DOCS / page).exists():
        sys.exit(f"更新紀錄「{e['title']}」連到不存在的頁面 {e['href']}")

feed = "".join(
    f'<li><time datetime="{e["date"]}">{e["date"]}</time>'
    f'<a href="{html.escape(e["href"])}">{html.escape(e["title"])}'
    f'{"<span class=new>最新</span>" if i == 0 else ""}</a>'
    f'<p>{html.escape(" ".join(e["desc"]))}</p></li>'
    for i, e in enumerate(entries))
toggle = ('<button class="toggle" id="more" aria-expanded="false" aria-controls="feed">看全部更新</button>'
          if len(entries) > 5 else "")


def count(edition=None):
    if edition:
        return len((ROOT / "editions" / f"{edition}.txt").read_text(encoding="utf-8").split())
    return sum(1 for _ in (ROOT / "wiki").rglob("*.md"))


home = (ROOT / "tools" / "home_template.html").read_text(encoding="utf-8")
home = (home.replace("__FEED__", feed).replace("__TOGGLE__", toggle)
        .replace("__LAST__", entries[0]["date"]).replace("__REPO__", REPO_URL)
        .replace("__PAIRS_N__", str(count("pairs"))).replace("__WIKI_N__", str(count())))
(DOCS / "index.html").write_text(home, encoding="utf-8")
print(f"已產生 index.html（最新更新 {len(entries)} 筆）")
print(f"網站完成：{DOCS.relative_to(ROOT)}/ → {SITE_URL}")
