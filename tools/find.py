#!/usr/bin/env python3
"""在 Wiki 裡找跟關鍵字有關的頁面。收錄新資料前先跑這個，只讀找到的頁面，不靠記憶。

用法：python3 tools/find.py 卡爾曼 移動平均 [--top 10]
計分：標題或別名命中 5 分、檔名命中 3 分、內文每出現一次 1 分（每個關鍵字最多 5 分）。
"""
import argparse
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ap = argparse.ArgumentParser()
ap.add_argument("words", nargs="+")
ap.add_argument("--top", type=int, default=10)
args = ap.parse_args()

rows = []
for p in sorted((ROOT / "wiki").rglob("*.md")):
    if p.stem in ("log", "todo", "index"):
        continue
    text = p.read_text(encoding="utf-8")
    m = re.match(r"^---\n(.*?)\n---\n(.*)$", text, re.S)
    meta, body = (m.group(1), m.group(2)) if m else ("", text)
    title = re.search(r"^title:\s*(.+)$", meta, re.M)
    title = title.group(1) if title else p.stem
    aliases = re.search(r"^aliases:\s*\[(.*)\]$", meta, re.M)
    aliases = [a.strip().lower() for a in aliases.group(1).split(",")] if aliases else []
    ptype = re.search(r"^type:\s*(\S+)", meta, re.M)
    score, hits = 0, []
    for w in args.words:
        lw = w.lower()
        s = 0
        if lw in title.lower() or any(lw in a or a in lw for a in aliases if a):
            s += 5
        if lw in p.stem:
            s += 3
        s += min(5, body.lower().count(lw))
        if s:
            hits.append(w)
        score += s
    if score:
        rows.append((score, p.stem, ptype.group(1) if ptype else "?", title, hits))

rows.sort(reverse=True)
if not rows:
    print("找不到相關頁面：這可能是全新的主題。")
for score, slug, ptype, title, hits in rows[:args.top]:
    print(f"{score:>3}  [[{slug}]]  {ptype:<8} {title}（命中：{'、'.join(hits)}）")
