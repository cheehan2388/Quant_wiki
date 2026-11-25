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
    # 模型、公式類知識：以後要會用、會算、知道何時不能用（AGENTS.md 第 5 節）
    "model": ["一句話", "需要先懂什麼", "白話解釋", "公式逐項白話", "手算一次",
              "靠什麼假設", "什麼時候不能用", "出現在哪些來源", "相關頁面"],
}
FOLDER_TYPE = {"sources": "source", "strategies": "strategy",
               "players": "player", "concepts": "concept", "cases": "case",
               "models": "model"}
BANNED = ["穩賺", "必勝", "保證獲利", "穩定獲利"]
ONE_LINER_MAX = 50
MAX_READ_CHARS = 3000          # 讀者看到的字數上限，超過就提醒拆頁（AGENTS.md 第 7 節）
NO_LENGTH_LIMIT = {"log", "todo", "index"}
INFERENCE_PAGES = {"who-pays", "pairs-guide"}   # 給讀者看的整理：推論要標確認狀態
MAX_RELATED = 5
MIN_LINKS = 2
LINK_RE = re.compile(r"\[\[([a-z0-9\-]+)\]\]")


def readable_len(body):
    """讀者實際看到的字數：去掉連結語法、markdown 符號和 LaTeX 指令，不算空白。"""
    t = LINK_RE.sub(r"\1", body)
    t = re.sub(r"\\(text|operatorname|mathbf|hat|dfrac|tfrac|frac|left|right|underbrace|begin|end|"
               r"bmatrix|quad|qquad|sqrt|times|cdots|top|approx|to|sigma|mu|cdot)\b", "", t)
    t = re.sub(r"[\\{}^_$|#*>\-]", "", t)
    return len(re.sub(r"\s", "", t))

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
    if ptype in ("strategy", "player", "concept", "case", "model") and not meta.get("sources"):
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
        for sec in ["在賺誰的錢", "靠什麼假設", "什麼時候失效", "扣成本後剩多少", "什麼時候不能用"]:
            if sec in want:
                m = re.search(rf"^## {sec}\n(.*?)(?=^## |\Z)", body, re.M | re.S)
                if m and len(m.group(1).strip()) < 15:
                    errors.append(f"{where}：「{sec}」幾乎是空的")
    # 概念頁、模型頁的「出現在哪些來源」要和開頭的 sources 欄位一致
    if ptype in ("concept", "model"):
        m = re.search(r"^## 出現在哪些來源\n(.*?)(?=^## |\Z)", body, re.M | re.S)
        if m:
            listed, declared = set(LINK_RE.findall(m.group(1))), set(meta.get("sources", []))
            if listed != declared:
                errors.append(f"{where}：「出現在哪些來源」和 sources 欄位不一致"
                              f"（只在段落裡：{sorted(listed - declared)}；只在欄位裡：{sorted(declared - listed)}）")
    # 相關頁面：最多 5 條，每條一個連結加一句原因（AGENTS.md 第 3 節）
    m = re.search(r"^## 相關頁面\n(.*?)(?=^---$|^## |\Z)", body, re.M | re.S)
    if m and ptype in SECTIONS:
        items = [l for l in m.group(1).splitlines() if l.strip().startswith("- ")]
        if len(items) > MAX_RELATED:
            errors.append(f"{where}：相關頁面有 {len(items)} 條，最多 {MAX_RELATED} 條（其他關係交給自動產生的「可能相關」）")
        for l in items:
            mm = re.match(r"^- \[\[([a-z0-9\-]+)\]\]：(.+)$", l.strip())
            if not mm or LINK_RE.search(mm.group(2)) or len(mm.group(2).strip()) < 4:
                errors.append(f"{where}：相關頁面這條格式不對，要寫成「- [[頁面]]：為什麼相關」：{l.strip()[:40]}")
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
    # 數學公式：$ 要成對，而且每個公式都要能轉成 MathML
    try:
        sys.path.insert(0, str(ROOT / "tools"))
        from latex2mathml.converter import convert as _tex
        _nc = re.sub(r"`[^`\n]*`", "", body)
        for tex in re.findall(r"\$\$(.+?)\$\$", _nc, re.S) + re.findall(r"(?<!\$)\$(?!\$)(.+?)(?<!\$)\$(?!\$)", re.sub(r"\$\$.+?\$\$", "", _nc, flags=re.S)):
            try:
                _tex(tex.strip())
            except Exception as e:
                errors.append(f"{where}：公式轉換失敗：{tex.strip()[:40]}（{e}）")
    except ImportError:
        warnings.append("沒有安裝 latex2mathml，略過公式檢查（pip install latex2mathml）")
    nocode = re.sub(r"`[^`\n]*`", "", body)
    if (nocode.count("$") - 2 * nocode.count("$$")) % 2:
        errors.append(f"{where}：$ 沒有成對（公式要寫成 $...$ 或 $$...$$）")
    if slug not in NO_LENGTH_LIMIT and (n := readable_len(body)) > MAX_READ_CHARS:
        warnings.append(f"{where}：{n} 字，超過 {MAX_READ_CHARS} 字，考慮拆成兩頁")
    if slug in INFERENCE_PAGES:
        for bad in re.findall(r"推論(?![，,]\s*(待確認|已確認))[）)]", body):
            errors.append(f"{where}：總覽／導覽頁裡的推論要標成「推論，待確認」或「推論，已確認（日期）」")
            break
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
HUB_AT = 15
for slug, inc in incoming.items():
    meta = pages[slug]["meta"] or {}
    real = inc - {"index", "log", "todo", "me"}
    if pages[slug]["folder"] in FOLDER_TYPE and len(real) > HUB_AT and not meta.get("hub"):
        warnings.append(f"{pages[slug]['path']}：被 {len(real)} 頁連到，考慮做一頁主題導覽（像 pairs-guide），"
                        f"做好後在這頁開頭加 hub: 導覽頁檔名")
    if meta.get("hub") and meta["hub"] not in pages:
        errors.append(f"{pages[slug]['path']}：hub 欄位指向不存在的頁面 {meta['hub']}")
for slug, inc in incoming.items():
    if pages[slug]["folder"] in FOLDER_TYPE and not (inc - {"index"}):
        warnings.append(f"{pages[slug]['path']}：除了目錄以外，沒有其他頁面連到它")

for ed in sorted((ROOT / "editions").glob("*.txt")) if (ROOT / "editions").exists() else []:
    for s in [l.strip() for l in ed.read_text(encoding="utf-8").splitlines() if l.strip()]:
        if s not in pages:
            errors.append(f"{ed.relative_to(ROOT)}：列了不存在的頁面 {s}")

# 數字只住在來源頁（AGENTS.md 第 8 節）
NUM_RE = re.compile(r"(?<![A-Za-z\d.])[−-]?\d[\d,]*(?:\.\d+)?")
CHECK_ALL = {"strategy", "player", "case"}
CHECK_OVERVIEW = {"who-pays", "pairs-guide"}


def numbers(text):
    out = []
    for m in NUM_RE.findall(text):
        try:
            out.append(abs(float(m.replace(",", "").replace("−", "-"))))
        except ValueError:
            pass
    return out


def strip_for_numbers(text):
    text = re.sub(r"\$\$.+?\$\$|\$[^$\n]+\$|`[^`\n]*`|\{\{figure:[^}]+\}\}", " ", text, flags=re.S)
    # 章節、式子、表格、圖的編號不是事實數字
    text = re.sub(r"第\s*[\d.]+\s*(節|章|頁)|式\s*[\d.–、\-]+|表\s*[\d.–\-]+|(Table|Figure|EQ)\s*[\d.–\-]+", " ", text)
    return LINK_RE.sub(" ", text)


source_numbers = {s: numbers(d["body"]) for s, d in pages.items() if d["folder"] == "sources"}
for slug, d in pages.items():
    meta, ptype = d["meta"] or {}, (d["meta"] or {}).get("type")
    if not (ptype in CHECK_ALL or ptype in ("concept", "model") or slug in CHECK_OVERVIEW):
        continue
    allowed = [n for s in meta.get("sources", []) for n in source_numbers.get(s, [])]
    section = ""
    for line in d["body"].splitlines():
        if line.startswith("## "):
            section = line[3:].strip()
        if line.startswith("#") or "算術" in line or "示意" in line:
            continue  # 標明「Wiki 的算術」或「示意」的句子不檢查
        if (ptype == "concept" and section == "例子") or (ptype == "model" and section == "手算一次"):
            continue  # 概念頁的例子、模型頁的手算是教學用的示意數字
        line_allowed = allowed + [n for s in LINK_RE.findall(line) for n in source_numbers.get(s, [])]
        if ptype in ("concept", "model") and not any(s in source_numbers for s in LINK_RE.findall(line)):
            continue  # 概念頁只檢查有標出處的句子；其他多半是示意數字
        clean = strip_for_numbers(line)
        for m in NUM_RE.finditer(clean):
            try:
                n = abs(float(m.group(0).replace(",", "").replace("−", "-")))
            except ValueError:
                continue
            unit = re.match(r"\s*(%|％|倍|bps|個百分點|美元|億|萬|毫秒|指數點)", clean[m.end():])
            if n <= 20 and n == int(n) and not unit:
                continue  # 沒帶單位的小整數多半是步驟、天數、「2 個標準差」這類
            if not any(abs(w - n) < 1e-9 or (n == int(n) and abs(w - n) < 0.5) for w in line_allowed):
                errors.append(f"{d['path']}：數字 {n:g} 在它引用的來源頁 {meta.get('sources', [])} 裡找不到：{line.strip()[:50]}")

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
