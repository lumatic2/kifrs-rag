"""(C) 벤치마크 회계 문항이 인용한 [기준서-문단]만 핀포인트 검증.
인용 locator 가 DB에 존재하는지 + 본문이 원본 PDF에 등장하는지 확인.
인용목록은 stdin(JSON: [[std,no],...]) 으로 받는다.
실행: python -m ... < cites.json  또는  python validate_cited_paragraphs.py cites.json
"""
from __future__ import annotations
import json, glob, os, re, sys
import fitz
from kifrs import store

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PDFS = {os.path.basename(p): p for p in glob.glob(os.path.join(ROOT, "data", "standards", "**", "*.pdf"), recursive=True)}
ws = re.compile(r"\s+")
sw = lambda s: ws.sub("", s or "")

_cache = {}
def pdf_text_for(std: str) -> str:
    if std in _cache:
        return _cache[std]
    f = os.path.join(ROOT, "data", "standards", "parsed", f"{std}.json")
    src = json.load(open(f, encoding="utf-8")).get("source") if os.path.exists(f) else None
    txt = ""
    if src and src in PDFS:
        doc = fitz.open(PDFS[src])
        txt = sw("".join(p.get_text() for p in doc)); doc.close()
    _cache[std] = txt
    return txt

def main():
    raw = open(sys.argv[1], encoding="utf-8").read() if len(sys.argv) > 1 else sys.stdin.read()
    cites = json.loads(raw)
    seen = set()
    ok = missing = mismatch = 0
    problems = []
    for std, no in cites:
        key = (std, no)
        if key in seen:
            continue
        seen.add(key)
        p = store.get_paragraph(std, no)
        if not p or not (p.get("body") or "").strip():
            missing += 1
            problems.append(("MISSING", std, no, "DB에 문단 없음/빈본문"))
            continue
        body = sw(p["body"])
        pt = pdf_text_for(std)
        probe = body[:40] if len(body) >= 40 else body
        if pt and len(probe) >= 12 and probe not in pt and (body[len(body)//2:len(body)//2+40] not in pt):
            mismatch += 1
            problems.append(("MISMATCH", std, no, (p["body"] or "")[:60]))
        else:
            ok += 1
    print(f"인용 고유 문단 {len(seen)}개 검증")
    print(f"  ✅ 존재+본문일치: {ok}")
    print(f"  ❌ MISSING(없음/빈): {missing}")
    print(f"  ⚠ MISMATCH(PDF 불일치): {mismatch}")
    if problems:
        print("=== 문제 문단 ===")
        for kind, std, no, detail in problems:
            print(f"  [{kind}] {std} 문단 {no}: {detail}")

if __name__ == "__main__":
    main()
