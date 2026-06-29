"""(A) 결정론 파싱 검증 — 원본 PDF를 PyMuPDF로 독립 재추출해 parsed JSON 대조.

기존 파서를 재사용하지 않는다(같은 버그 물려받지 않기 위해). 측정:
  - fidelity: 파싱 본문(공백제거)이 원본 PDF 텍스트(공백제거)에 실제로 등장하는 비율
  - 가짜 문단번호: 날짜/연도(\d{4}) 또는 본문정수 200 초과 = 헤더·날짜 오파싱 의심
  - 빈/초단문 본문, 중복 no
실행: .venv/Scripts/python.exe scripts/validate_parse_against_pdf.py
"""
from __future__ import annotations
import json, glob, os, re, sys, collections
import fitz  # PyMuPDF

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PARSED = os.path.join(ROOT, "data", "standards", "parsed")
PDFS = {os.path.basename(p): p for p in glob.glob(os.path.join(ROOT, "data", "standards", "**", "*.pdf"), recursive=True)}

ws = re.compile(r"\s+")
def strip_ws(s: str) -> str:
    return ws.sub("", s or "")

def pdf_text(path: str):
    doc = fitz.open(path)
    try:
        raw = "".join(page.get_text() for page in doc)
        npages = max(1, doc.page_count)
    finally:
        doc.close()
    # 페이지당 평균 50자 미만이면 PyMuPDF 추출 실패(이미지·인코딩) → 검증 불가 표시
    extractable = (len(raw) / npages) >= 50
    return strip_ws(raw), extractable

def found_in(body: str, pt: str) -> bool:
    """공백제거 본문 일부가 PDF 텍스트에 등장하는지. 읽기순서 뒤섞임에 관대하게
    앞·중간 두 군데서 40자 슬라이스를 시도."""
    b = strip_ws(body)
    if not b:
        return True
    for probe in {b[:40], b[len(b)//2: len(b)//2 + 40]}:
        if len(probe) >= 20 and probe in pt:
            return True
    return False

def main():
    rows = []
    files = [f for f in sorted(glob.glob(os.path.join(PARSED, "*.json")))
             if not f.endswith("_view.json") and "index" not in os.path.basename(f)]
    for f in files:
        d = json.load(open(f, encoding="utf-8"))
        std = d.get("standard") or os.path.basename(f)[:-5]
        src = d.get("source")
        ps = d.get("paragraphs", [])
        pt, extractable = pdf_text(PDFS[src]) if src in PDFS else ("", False)
        found = miss = empty = 0
        missing_samples = []
        for p in ps:
            b = strip_ws(p.get("body"))
            if not b:
                empty += 1
                continue
            if found_in(p.get("body"), pt):
                found += 1
            else:
                miss += 1
                if len(missing_samples) < 3:
                    missing_samples.append((p.get("no"), (p.get("body") or "")[:50]))
        nonempty = found + miss
        fidelity = found / nonempty if nonempty else 1.0
        nos = [p.get("no") for p in ps]
        dups = len(nos) - len(set(nos))
        fake = sum(1 for n in nos if isinstance(n, str) and (re.fullmatch(r"\d{4}", n) or (n.isdigit() and int(n) > 200)))
        rows.append(dict(std=std, total=len(ps), empty=empty, miss=miss, fidelity=fidelity,
                         dups=dups, fake=fake, samples=missing_samples, extractable=extractable))

    ext = [r for r in rows if r["extractable"]]
    noext = [r for r in rows if not r["extractable"]]
    ext.sort(key=lambda r: (r["fidelity"], -r["miss"]))

    print(f"=== 추출가능 기준서 fidelity (PyMuPDF 신뢰구간) — {len(ext)}개 ===")
    print(f"{'기준서':>6} {'문단':>4} {'fidelity':>8} {'불일치':>5} {'빈':>3} {'중복':>4} {'가짜no':>5}")
    for r in ext:
        flag = "  ⚠" if (r["fidelity"] < 0.97 or r["fake"] or r["empty"]) else ""
        print(f"{r['std']:>6} {r['total']:>4} {r['fidelity']*100:>7.1f}% {r['miss']:>5} {r['empty']:>3} {r['dups']:>4} {r['fake']:>5}{flag}")

    tot_p = sum(r["total"] for r in ext)
    tot_miss = sum(r["miss"] for r in ext)
    tot_empty = sum(r["empty"] for r in ext)
    print(f"\n=== 요약 (추출가능 {len(ext)}개 기준) ===")
    print(f"문단 {tot_p} · 본문일치 {tot_p - tot_miss - tot_empty} → fidelity {(tot_p - tot_miss - tot_empty)/max(1,tot_p)*100:.1f}%")
    print(f"본문불일치 {tot_miss} · 빈본문 {tot_empty}")
    print(f"fidelity<97% 기준서: {sum(1 for r in ext if r['fidelity']<0.97)}")
    print(f"가짜 no(날짜오파싱) 보유: {sum(1 for r in rows if r['fake'])}기준서 / 총 {sum(r['fake'] for r in rows)}개")
    print(f"번호중복 보유: {sum(1 for r in rows if r['dups'])}기준서 / 총 {sum(r['dups'] for r in rows)}개")
    print(f"\n=== 검증불가 (PyMuPDF 추출실패=이미지/인코딩 PDF) — {len(noext)}개 ===")
    print("  " + ", ".join(r["std"] for r in noext))
    print(f"\n=== 추출가능 중 최악 8개 불일치 샘플 ===")
    for r in [x for x in ext if x['miss']][:8]:
        print(f"[{r['std']}] fidelity {r['fidelity']*100:.0f}% miss={r['miss']}")
        for no, txt in r["samples"]:
            print(f"    no={no}: {txt!r}")

if __name__ == "__main__":
    main()
