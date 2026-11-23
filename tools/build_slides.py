#!/usr/bin/env python3
"""把簡報稿（deck.md）轉成單一 HTML 簡報。

用法：python3 tools/build_slides.py slides/pairs-trading/deck.md
輸出：同一資料夾的 index.html。會先跑 check_slides.py，沒過就不產生。
"""
import html
import json
import re
import subprocess
import sys
from pathlib import Path

import markdown

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))
from check_slides import parse  # noqa: E402

deck = Path(sys.argv[1]).resolve()
r = subprocess.run([sys.executable, str(ROOT / "tools" / "check_slides.py"), str(deck)])
if r.returncode != 0:
    sys.exit("簡報檢查沒過，不產生 HTML。")

titles = {}
for p in (ROOT / "wiki").rglob("*.md"):
    m = re.search(r"^title:\s*(.+)$", p.read_text(encoding="utf-8"), re.M)
    titles[p.stem] = re.sub(r"（.*?）$", "", m.group(1).strip()) if m else p.stem


def figure(name):
    for ext in (".svg", ".html"):
        f = ROOT / "tools" / "figures" / f"{name}{ext}"
        if f.exists():
            return f'<div class="fig">{f.read_text(encoding="utf-8")}</div>'
    return ""


def quiz(body):
    out, qi = [], 0
    blocks = re.split(r"^\?\? ", body, flags=re.M)
    head = markdown.markdown(blocks[0])
    for b in blocks[1:]:
        lines = b.strip().splitlines()
        q = lines[0]
        opts = [(l[6:], l[3] == "x") for l in lines if l.startswith("- [")]
        why = next((l[3:] for l in lines if l.startswith("!! ")), "")
        btns = "".join(f'<button class="opt" data-ok="{int(ok)}">{html.escape(t)}</button>' for t, ok in opts)
        out.append(f'<div class="q" data-q="{qi}"><p class="qq">{qi + 1}. {html.escape(q)}</p>'
                   f'<div class="opts">{btns}</div><p class="why" hidden>{html.escape(why)}</p></div>')
        qi += 1
    return head + '<div class="quiz">' + "".join(out) + '</div><p class="score" aria-live="polite"></p>'


def render(s):
    body = s["body"]
    if s["layout"] == "quiz":
        return quiz(body)
    figs = re.findall(r"\{\{figure:([a-z0-9\-]+)\}\}", body)
    body = re.sub(r"\{\{figure:([a-z0-9\-]+)\}\}", r"FIGTOKEN\1FIGTOKEN", body)
    body = re.sub(r"^(> .*)$", r"\n\1\n", body, flags=re.M)      # 每行定義各自成一張卡
    out = markdown.markdown(body, extensions=["tables"])
    for f in figs:
        out = out.replace(f"<p>FIGTOKEN{f}FIGTOKEN</p>", figure(f))
    return out


slides = []
for s in parse(deck):
    slides.append({"id": s["id"], "layout": s["layout"], "html": render(s),
                   "cites": [titles.get(c, c) for c in s["cites"]],
                   "illustrative": "illustrative" in s["flags"]})

tpl = (ROOT / "tools" / "slides_template.html").read_text(encoding="utf-8")
title = re.sub(r"<.*?>", "", slides[0]["html"].split("</h1>")[0])
out = deck.parent / "index.html"
out.write_text(tpl.replace("__TITLE__", html.escape(title))
               .replace("/*__SLIDES__*/null", json.dumps(slides, ensure_ascii=False).replace("</", "<\\/")),
               encoding="utf-8")
print(f"已產生 {out.relative_to(ROOT)}，共 {len(slides)} 頁")
