#!/usr/bin/env python3
"""把 wiki/ 轉成單一 HTML 檔（docs/index.html），方便瀏覽。

用法：
  python3 tools/build_viewer.py                 完整版 → docs/wiki.html
  python3 tools/build_viewer.py --edition pairs  只放 editions/pairs.txt 列的頁 → docs/pairs.html
每頁的 [[slug]] 會變成可點的連結（版本外的頁面變成純文字），側欄依類型分組，
每頁底部列出「誰連到這頁」，{{figure:名稱}} 會換成 tools/figures 裡的圖。
"""
import argparse
import html
import json
import re
from pathlib import Path

import markdown
from latex2mathml.converter import convert as latex_to_mathml

ROOT = Path(__file__).resolve().parent.parent
WIKI = ROOT / "wiki"
LINK_RE = re.compile(r"\[\[([a-z0-9\-]+)\]\]")
FIG_RE = re.compile(r"\{\{figure:([a-z0-9\-]+)\}\}")
# 數學公式：$$...$$ 是獨立一行的公式，$...$ 是句子裡的公式；產生網站時轉成 MathML，瀏覽器直接排版
MATH_BLOCK_RE = re.compile(r"\$\$(.+?)\$\$", re.S)
MATH_INLINE_RE = re.compile(r"(?<!\$)\$(?!\$)(.+?)(?<!\$)\$(?!\$)")


def protect_math(text):
    """把公式先換成記號，免得 markdown 把底線、星號、反斜線當成格式。回傳 (新文字, 記號→MathML)。"""
    store = {}

    def keep(tex, display):
        key = f"MATHTOKEN{len(store)}MATHTOKEN"
        mathml = latex_to_mathml(tex.strip(), display="block" if display else "inline")
        store[key] = f'<div class="mathblock">{mathml}</div>' if display else mathml
        return key

    text = MATH_BLOCK_RE.sub(lambda m: "\n\n" + keep(m.group(1), True) + "\n\n", text)
    text = MATH_INLINE_RE.sub(lambda m: keep(m.group(1), False), text)
    return text, store
GROUPS = [("overview", "總覽"), ("strategy", "策略"), ("case", "案例"), ("source", "來源"),
          ("player", "玩家"), ("concept", "概念")]

ap = argparse.ArgumentParser()
ap.add_argument("--edition")
ap.add_argument("--base", default="", help="網站根目錄網址；站內用空字串（相對路徑）")
ap.add_argument("--out")
args = ap.parse_args()
if args.edition:
    lines = (ROOT / "editions" / f"{args.edition}.txt").read_text(encoding="utf-8").splitlines()
    ONLY = [l.strip() for l in lines if l.strip() and not l.startswith("#")]
    OUT = ROOT / "docs" / f"{args.edition}.html"
else:
    ONLY = None
    OUT = ROOT / "docs" / "wiki.html"
if args.out:
    OUT = Path(args.out).resolve()


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
    if ONLY is not None and p.stem not in ONLY:
        continue
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


ALL_TITLES = {}
for p in WIKI.rglob("*.md"):
    ALL_TITLES[p.stem] = re.sub(r"（.*?）$", "", parse(p)[0].get("title", p.stem))


def figure(name):
    for ext in (".svg", ".html"):
        f = ROOT / "tools" / "figures" / f"{name}{ext}"
        if f.exists():
            return f'<figure class="fig">{f.read_text(encoding="utf-8")}</figure>'
    return ""


def link(m):
    s = m.group(1)
    if s in raw:
        return f'<a class="wl" href="#{s}">{html.escape(short(s))}</a>'
    return f'<span class="nl">{html.escape(ALL_TITLES.get(s, s))}</span>'


pages = {}
for s, d in raw.items():
    body = re.sub(r"^# .*\n", "", d["body"].lstrip(), count=1)
    body = LINK_RE.sub(link, body)
    figs = FIG_RE.findall(body)
    body = FIG_RE.sub(lambda m: f"FIGTOKEN{m.group(1)}FIGTOKEN", body)
    body, maths = protect_math(body)
    # python-markdown 要求清單前面空一行；寫 Wiki 時常省略，這裡自動補上
    body = re.sub(r"(?m)^(?!\s*(?:[-*] |\d+\. |\|)).+\n(?=(?:[-*] |\d+\. ))", lambda m: m.group(0) + "\n", body)
    out = markdown.markdown(body, extensions=["tables"])
    for key, mathml in maths.items():
        out = out.replace(f"<p>{key}</p>", mathml).replace(key, mathml)
    for f in figs:
        out = out.replace(f"<p>FIGTOKEN{f}FIGTOKEN</p>", figure(f)).replace(f"FIGTOKEN{f}FIGTOKEN", figure(f))
    pages[s] = {"title": d["title"], "type": d["type"], "updated": d["updated"],
                "html": out, "back": sorted(backlinks[s])}

nav = []
for key, label in GROUPS:
    items = [s for s, d in raw.items() if d["type"] == key]
    if key == "source":
        items.sort(key=lambda s: s.rsplit("-", 1)[-1])
    if key == "overview":
        order = ["pairs-guide", "who-pays", "index", "todo", "log"]
        items = [s for s in order if s in items]
    if not items:
        continue
    nav.append({"label": label, "items": [{"slug": s, "title": short(s)} for s in items]})

counts = {label: n for key, label in GROUPS[1:]
          if (n := sum(1 for d in raw.values() if d["type"] == key))}
home = ONLY[0] if ONLY else "who-pays"
subtitle = "配對交易篇" if args.edition == "pairs" else "完整版"
data = json.dumps({"pages": pages, "nav": nav, "counts": counts, "home": home,
                   "subtitle": subtitle, "site": args.base + "index.html"}, ensure_ascii=False)

TEMPLATE = (ROOT / "tools" / "viewer_template.html").read_text(encoding="utf-8")
OUT.parent.mkdir(exist_ok=True)
OUT.write_text(TEMPLATE.replace("/*__DATA__*/null", data.replace("</", "<\\/")), encoding="utf-8")
print(f"已產生 {OUT.name}，共 {len(pages)} 頁")
