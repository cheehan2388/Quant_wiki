#!/usr/bin/env python3
"""自動產生 wiki/index.md（目錄）。不要手改 index.md，改了也會被覆蓋。

用法：python3 tools/gen_index.py（build_site.py 會自動先跑）
依每頁開頭的 type 分組，來源頁依年份排序，其他依標題排序。
"""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
WIKI = ROOT / "wiki"
GROUPS = [("source", "來源（sources）"), ("strategy", "策略（strategies）"), ("case", "案例（cases）"),
          ("player", "玩家（players）"), ("concept", "概念（concepts）")]
OTHER = [("pairs-guide", "配對交易導覽"), ("who-pays", "總覽：誰在付錢"), ("me", "我的程度（AI 解釋新知識前要先讀）"),
         ("log", "收錄紀錄"), ("todo", "待寫清單")]

pages = {}
for p in WIKI.rglob("*.md"):
    if p.stem == "index":
        continue
    meta = re.match(r"^---\n(.*?)\n---", p.read_text(encoding="utf-8"), re.S).group(1)
    title = re.search(r"^title:\s*(.+)$", meta, re.M).group(1).strip()
    ptype = re.search(r"^type:\s*(\S+)", meta, re.M).group(1)
    pages[p.stem] = (title, ptype)

out = ["---", "title: 目錄", "type: overview", "sources: []", "updated: 自動產生", "---", "",
       "# 開心的 Quant Wiki", "",
       "核心問題：**交易策略到底在賺誰的錢？** 先看總覽 [[who-pays]]，或從第一個主題版本 [[pairs-guide]] 開始。", "",
       "> 這一頁由 `tools/gen_index.py` 自動產生，請不要手改。", ""]
for key, label in GROUPS:
    items = [s for s, (_, t) in pages.items() if t == key]
    if key == "source":
        items.sort(key=lambda s: (s.rsplit("-", 1)[-1], s))
    else:
        items.sort(key=lambda s: pages[s][0])
    out.append(f"## {label}")
    out += [f"- [[{s}]]：{pages[s][0]}" for s in items] or ["（還沒有）"]
    out.append("")
out.append("## 其他")
out += [f"- [[{s}]]：{label}" for s, label in OTHER if s in pages]
(WIKI / "index.md").write_text("\n".join(out) + "\n", encoding="utf-8")
print(f"已產生 wiki/index.md（{len(pages)} 頁）")
