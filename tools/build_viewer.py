#!/usr/bin/env python3
"""把 wiki/ 轉成單一 HTML 檔（docs/index.html），方便瀏覽。

用法：python3 tools/build_viewer.py
每頁的 [[slug]] 會變成可點的連結，側欄依類型分組，每頁底部列出「誰連到這頁」。
"""
import html
import json
import re
from pathlib import Path

import markdown

ROOT = Path(__file__).resolve().parent.parent
WIKI = ROOT / "wiki"
OUT = ROOT / "docs" / "index.html"
LINK_RE = re.compile(r"\[\[([a-z0-9\-]+)\]\]")
GROUPS = [("overview", "總覽"), ("source", "來源"), ("strategy", "策略"),
          ("player", "玩家"), ("concept", "概念")]


def parse(p):
    m = re.match(r"^---\n(.*?)\n---\n(.*)$", p.read_text(encoding="utf-8"), re.S)
    meta = {}
    for line in m.group(1).splitlines():
        if ":" in line:
            k, v = line.split(":", 1)
            meta[k.strip()] = v.split("#")[0].strip()
    return meta, m.group(2)


raw = {}
for p in sorted(WIKI.rglob("*.md")):
    meta, body = parse(p)
    raw[p.stem] = {"title": meta.get("title", p.stem), "type": meta.get("type", "overview"),
                   "updated": meta.get("updated", ""), "body": body}

backlinks = {s: [] for s in raw}
for s, d in raw.items():
    for t in set(LINK_RE.findall(d["body"])):
        if t in backlinks and t != s and s not in ("index", "log", "todo"):
            backlinks[t].append(s)


def short(slug):
    t = re.sub(r"（.*?）$", "", raw[slug]["title"])
    if raw[slug]["type"] == "source":
        t += " " + slug.rsplit("-", 1)[-1]
    return t


pages = {}
for s, d in raw.items():
    body = re.sub(r"^# .*\n", "", d["body"].lstrip(), count=1)
    body = LINK_RE.sub(lambda m: f'<a class="wl" href="#{m.group(1)}">{html.escape(short(m.group(1)))}</a>'
                       if m.group(1) in raw else m.group(0), body)
    pages[s] = {"title": d["title"], "type": d["type"], "updated": d["updated"],
                "html": markdown.markdown(body, extensions=["tables"]),
                "back": sorted(backlinks[s])}

nav = []
for key, label in GROUPS:
    items = [s for s, d in raw.items() if d["type"] == key]
    if key == "source":
        items.sort(key=lambda s: s.rsplit("-", 1)[-1])
    if key == "overview":
        order = ["who-pays", "index", "todo", "log"]
        items = [s for s in order if s in items]
    nav.append({"label": label, "items": [{"slug": s, "title": short(s)} for s in items]})

counts = {label: sum(1 for d in raw.values() if d["type"] == key) for key, label in GROUPS[1:]}
data = json.dumps({"pages": pages, "nav": nav, "counts": counts}, ensure_ascii=False)

TEMPLATE = (ROOT / "tools" / "viewer_template.html").read_text(encoding="utf-8")
OUT.parent.mkdir(exist_ok=True)
OUT.write_text(TEMPLATE.replace("/*__DATA__*/null", data.replace("</", "<\\/")), encoding="utf-8")
print(f"已產生 {OUT.relative_to(ROOT)}，共 {len(pages)} 頁")
