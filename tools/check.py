#!/usr/bin/env python3
"""開心的 Quant Wiki 健檢腳本。

用法：python3 tools/check.py
任何一項錯誤都會讓腳本以非 0 結束，並列出問題。警告不影響結果。
規則來源：AGENTS.md 第 3–8 節。
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
WIKI = ROOT / "wiki"

SECTIONS = {
    "source": ["一句話", "資料", "方法", "結果", "在賺誰的錢", "靠什麼假設",
               "什麼時候失效", "扣成本後剩多少", "原文與推論", "讀了什麼", "相關頁面"],
    "strategy": ["一句話", "怎麼做", "在賺誰的錢", "靠什麼假設", "什麼時候失效",
                 "扣成本後剩多少", "證據", "相關頁面"],
    "player": ["一句話", "他在哪裡賺錢", "他在哪裡付錢", "相關頁面"],
    "concept": ["一句話", "白話解釋", "例子", "出現在哪些來源", "相關頁面"],
    "case": ["一句話", "發生了什麼", "跟策略的關係", "學到什麼", "相關頁面"],
}
FOLDER_TYPE = {"sources": "source", "strategies": "strategy",
               "players": "player", "concepts": "concept", "cases": "case"}
BANNED = ["穩賺", "必勝", "保證獲利", "穩定獲利"]
ONE_LINER_MAX = 50
MIN_LINKS = 2
LINK_RE = re.compile(r"\[\[([a-z0-9\-]+)\]\]")

errors, warnings = [], []


def parse(path):
    text = path.read_text(encoding="utf-8")
    m = re.match(r"^---\n(.*?)\n---\n(.*)$", text, re.S)
    if not m:
        return None, text
    meta = {}
    for line in m.group(1).splitlines():
        if ":" in line:
            k, v = line.split(":", 1)
            meta[k.strip()] = v.split("#")[0].strip()
    if "sources" in meta:
        meta["sources"] = [s.strip() for s in meta["sources"].strip("[]").split(",") if s.strip()]
    return meta, m.group(2)


pages = {}
for p in sorted(WIKI.rglob("*.md")):
    slug = p.stem
    if slug in pages:
        errors.append(f"檔名重複：{slug}（{pages[slug]['path']} 與 {p}）")
    meta, body = parse(p)
    pages[slug] = {"path": p.relative_to(ROOT), "meta": meta, "body": body,
                   "folder": p.parent.name}

source_slugs = {s for s, d in pages.items() if d["folder"] == "sources"}
incoming = {s: set() for s in pages}

for slug, d in pages.items():
    where, meta, body = d["path"], d["meta"], d["body"]
    if meta is None:
        errors.append(f"{where}：缺少 frontmatter")
        continue
    for f in ["title", "type", "sources", "updated"]:
        if f not in meta:
            errors.append(f"{where}：frontmatter 缺少 {f}")
    ptype = meta.get("type")
    expect = FOLDER_TYPE.get(d["folder"])
    if expect and ptype != expect:
        errors.append(f"{where}：type 應為 {expect}，實際是 {ptype}")
    for s in meta.get("sources", []):
        if s not in source_slugs:
            errors.append(f"{where}：sources 列了不存在的來源頁 {s}")
    if ptype in ("strategy", "player", "concept", "case") and not meta.get("sources"):
        errors.append(f"{where}：沒有任何來源支持（sources 是空的）")

    # 段落順序
    if ptype in SECTIONS:
        found = re.findall(r"^## (.+)$", body, re.M)
        want = SECTIONS[ptype]
        if found != want:
            missing = [s for s in want if s not in found]
            if missing:
                errors.append(f"{where}：缺少段落 {missing}")
            else:
                errors.append(f"{where}：段落順序不對，應為 {want}")
        m = re.search(r"^## 一句話\n+(.+?)\n", body, re.M)
        if m:
            n = len(re.sub(r"\s", "", m.group(1)))
            if n > ONE_LINER_MAX:
                errors.append(f"{where}：一句話有 {n} 字，超過 {ONE_LINER_MAX} 字")
        # 四問題不能是空的
        for sec in ["在賺誰的錢", "靠什麼假設", "什麼時候失效", "扣成本後剩多少"]:
            if sec in want:
                m = re.search(rf"^## {sec}\n(.*?)(?=^## |\Z)", body, re.M | re.S)
                if m and len(m.group(1).strip()) < 15:
                    errors.append(f"{where}：「{sec}」幾乎是空的")
    if ptype == "source":
        m = re.search(r"^## 原文與推論\n(.*?)(?=^## |\Z)", body, re.M | re.S)
        if m and not ("原文" in m.group(1) and "推論" in m.group(1)):
            errors.append(f"{where}：原文與推論沒有分開列")

    # 連結
    links = set(LINK_RE.findall(body))
    for t in links:
        if t not in pages:
            errors.append(f"{where}：連結 [[{t}]] 找不到頁面")
        elif t != slug:
            incoming[t].add(slug)
    if ptype in SECTIONS and len(links - {slug}) < MIN_LINKS:
        errors.append(f"{where}：只連到 {len(links - {slug})} 個頁面，至少要 {MIN_LINKS} 個")

    for fig in re.findall(r"\{\{figure:([a-z0-9\-]+)\}\}", body):
        if not any((ROOT / "tools" / "figures" / f"{fig}{ext}").exists() for ext in (".svg", ".html")):
            errors.append(f"{where}：找不到圖 {fig}")
    for w in BANNED:
        if w in body:
            errors.append(f"{where}：出現禁用字「{w}」")

# 目錄與紀錄
index_body = pages.get("index", {}).get("body", "")
log_body = pages.get("log", {}).get("body", "")
for slug, d in pages.items():
    if d["folder"] in FOLDER_TYPE and f"[[{slug}]]" not in index_body:
        errors.append(f"index.md 沒有列出 [[{slug}]]")
for s in source_slugs:
    if s not in log_body:
        errors.append(f"log.md 沒有 {s} 的收錄紀錄")
for slug, inc in incoming.items():
    if pages[slug]["folder"] in FOLDER_TYPE and not (inc - {"index"}):
        warnings.append(f"{pages[slug]['path']}：除了目錄以外，沒有其他頁面連到它")

for ed in sorted((ROOT / "editions").glob("*.txt")) if (ROOT / "editions").exists() else []:
    for s in [l.strip() for l in ed.read_text(encoding="utf-8").splitlines() if l.strip()]:
        if s not in pages:
            errors.append(f"{ed.relative_to(ROOT)}：列了不存在的頁面 {s}")

counts = {k: sum(1 for d in pages.values() if d["folder"] == k) for k in FOLDER_TYPE}
print("頁數：" + "、".join(f"{k} {v}" for k, v in counts.items()))
for w in warnings:
    print("警告：" + w)
if errors:
    print(f"\n健檢失敗，共 {len(errors)} 個問題：")
    for e in errors:
        print(" - " + e)
    sys.exit(1)
print("健檢通過")
