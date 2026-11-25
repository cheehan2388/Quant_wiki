#!/usr/bin/env python3
"""每週健檢報告：只讀、只回報，不改任何檔案。

用法：python3 tools/lint_report.py
內容
1. check.py 的結果（錯誤與警告）
2. 單向連結：A 的「相關頁面」連到 B，B 卻完全沒提到 A
3. 可能相關：引用 2 篇以上相同來源、卻互不相連的頁面
4. 太長的頁（超過 3,000 字）與被連太多的頁（超過 15 頁）
5. 待寫清單裡已經可以拆頁的概念（出現次數 ≥ 2、還沒拆）
6. 可能過期：引用的來源頁比這頁晚更新
"""
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
WIKI = ROOT / "wiki"
LINK = re.compile(r"\[\[([a-z0-9\-]+)\]\]")
SKIP = {"index", "log", "todo", "me"}

pages = {}
for p in WIKI.rglob("*.md"):
    t = p.read_text(encoding="utf-8")
    m = re.match(r"^---\n(.*?)\n---\n(.*)$", t, re.S)
    meta, body = m.group(1), m.group(2)
    get = lambda k: (re.search(rf"^{k}:\s*(.+)$", meta, re.M) or [None, ""])[1].strip()
    src = re.search(r"^sources:\s*\[(.*)\]", meta, re.M)
    rel = re.search(r"^## 相關頁面\n(.*?)(?=^---$|^## |\Z)", body, re.M | re.S)
    pages[p.stem] = {"title": get("title"), "type": get("type"), "updated": get("updated"), "hub": get("hub"),
                     "sources": {x.strip() for x in src.group(1).split(",") if x.strip()} if src else set(),
                     "body": body, "links": set(LINK.findall(body)),
                     "related": LINK.findall(rel.group(1)) if rel else []}

out = ["# Quant Wiki 每週健檢報告", ""]

r = subprocess.run([sys.executable, str(ROOT / "tools" / "check.py")], capture_output=True, text=True, cwd=ROOT)
out += ["## 1. check.py", "", "結果：" + ("**通過**" if r.returncode == 0 else "**失敗**"), "", "```", r.stdout.strip(), "```", ""]

backcount = {s: sum(1 for x, d in pages.items() if x not in SKIP and s in d["links"] and x != s) for s in pages}
oneway = [(a, b) for a, d in pages.items() for b in d["related"]
          if b in pages and b not in SKIP and a not in pages[b]["links"] and pages[b]["type"] != "overview"
          and not pages[b]["hub"] and backcount[b] <= 10]
out += [f"## 2. 單向連結（{len(oneway)}）", "",
        "（不列出連到熱門頁的：熱門頁不可能每頁都連回去，瀏覽頁會自動顯示「連到這一頁的頁面」。）", ""]
out += [f"- [[{a}]] 連到 [[{b}]]，但 [[{b}]] 沒提到 [[{a}]]" for a, b in oneway] or ["沒有"]
out.append("")

maybe = [(len(pages[a]["sources"] & pages[b]["sources"]), a, b)
         for a in pages for b in pages
         if a < b and pages[a]["type"] != "overview" and pages[b]["type"] != "overview"
         and len(pages[a]["sources"] & pages[b]["sources"]) >= 2
         and b not in pages[a]["links"] and a not in pages[b]["links"]]
out += [f"## 3. 可能相關、卻互不相連（{len(maybe)}）", ""]
out += [f"- [[{a}]] ↔ [[{b}]]（共用 {n} 篇來源）" for n, a, b in sorted(maybe, reverse=True)] or ["沒有"]
out.append("")

warn = [l[3:] for l in r.stdout.splitlines() if l.startswith("警告：")]
long_ = [w for w in warn if "字，超過" in w]
hubs = [w for w in warn if "考慮做一頁主題導覽" in w]
out += ["## 4. 太長或太熱門的頁", ""] + [f"- {w}" for w in long_ + hubs] + ([] if long_ or hubs else ["沒有"]) + [""]

ready = []
todo = (WIKI / "todo.md").read_text(encoding="utf-8")
for line in todo.splitlines():
    cells = [c.strip() for c in line.strip("|").split("|")]
    if len(cells) >= 4 and cells[2].isdigit() and int(cells[2]) >= 2 and "已拆" not in cells[3]:
        ready.append(f"- {cells[0]}：出現在 {cells[2]} 篇來源（{cells[3]}）")
out += [f"## 5. 待寫清單裡可以拆頁的概念（{len(ready)}）", ""] + (ready or ["沒有"]) + [""]

stale = []
for s, d in pages.items():
    if d["type"] in ("source", "overview") or not re.match(r"\d{4}-\d{2}-\d{2}", d["updated"]):
        continue
    newer = [x for x in d["sources"] if x in pages and pages[x]["updated"] > d["updated"]]
    if newer:
        stale.append(f"- [[{s}]]（{d['updated']}）引用的 {', '.join(f'[[{x}]]' for x in newer)} 比它晚更新")
out += [f"## 6. 可能過期（{len(stale)}）", ""] + (stale or ["沒有"]) + [""]

out += ["---", "這份報告只回報、不修改。要修哪一項，請告訴 AI「照健檢報告修第 N 項」。"]
print("\n".join(out))
