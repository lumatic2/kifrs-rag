"""AE2 Step 4 — DART 공개 사업보고서에서 리스 주석 요구항목 존재를 태깅한다.

DART Open API(`document.xml`)로 상장사 최신 사업보고서를 받아 태그를 제거하고, [1116-53]+[58]
요구항목 키워드가 실제 주석에 등장하는지 확인한다. 주석 원문은 `data/dart_lease_notes/`
(gitignored)에만 저장하고, 커밋 가능한 산출물은 **항목 존재 요약(사실)**뿐이다 — 원문 표현은
커밋하지 않는다(저작권 경계).

용례: DART_API_KEY 환경변수 필요.
  python scripts/fetch_dart_lease_notes.py
"""
from __future__ import annotations

import io
import json
import os
import re
import urllib.request
import zipfile
from pathlib import Path

# 파일럿 대상 — 리스 강도가 다른 대형 상장사(교차검증 다양성)
COMPANIES = [
    ("삼성전자", "00126380"),
    ("현대자동차", "00164742"),
    ("LG전자", "00401731"),
    ("롯데쇼핑", "00426472"),
]

# [1116-53]+[58] 요구항목 → 주석 존재 판정 키워드
ITEM_KEYWORDS = {
    "53(1) 감가상각비": ["사용권자산", "감가상각"],
    "53(2) 이자비용": ["리스부채", "이자"],
    "53(3) 단기리스": ["단기리스"],
    "53(4) 소액자산": ["소액"],
    "53(5) 변동리스료": ["변동리스료"],
    "53(6) 전대리스": ["전대리스"],
    "53(7) 총 현금유출": ["현금유출"],
    "53(8) 사용권자산 추가": ["사용권자산", "증가"],
    "53(9) 판매후리스": ["판매후리스"],
    "53(10) 기말장부": ["사용권자산", "장부금액"],
    "58 만기분석": ["만기"],
}

DATA_DIR = Path("data/dart_lease_notes")


def _api(url: str, timeout: int = 60) -> bytes:
    return urllib.request.urlopen(url, timeout=timeout).read()


def latest_business_report(key: str, corp_code: str) -> str | None:
    url = (
        f"https://opendart.fss.or.kr/api/list.json?crtfc_key={key}"
        f"&corp_code={corp_code}&bgn_de=20240101&pblntf_ty=A&page_count=10"
    )
    data = json.loads(_api(url).decode("utf-8"))
    if data.get("status") != "000":
        return None
    for it in data.get("list", []):
        if it["report_nm"].startswith("사업보고서"):
            return it["rcept_no"]
    return None


def filing_text(key: str, rcept_no: str) -> str:
    raw = _api(f"https://opendart.fss.or.kr/api/document.xml?crtfc_key={key}&rcept_no={rcept_no}")
    z = zipfile.ZipFile(io.BytesIO(raw))
    main = next(n for n in z.namelist() if n == f"{rcept_no}.xml")
    xml = z.read(main).decode("utf-8", "ignore")
    text = re.sub(r"<[^>]+>", " ", xml)
    text = re.sub(r"&[a-zA-Z]+;", " ", text)
    return re.sub(r"\s+", " ", text)


def tag_items(text: str) -> dict[str, bool]:
    """요구항목별 존재 여부 — 키워드 전부 등장하면 존재로 판정."""
    return {item: all(kw in text for kw in kws) for item, kws in ITEM_KEYWORDS.items()}


def main() -> None:
    key = os.environ.get("DART_API_KEY")
    if not key:
        raise SystemExit("DART_API_KEY 환경변수 필요 (opendart.fss.or.kr 무료 발급)")
    DATA_DIR.mkdir(parents=True, exist_ok=True)

    summary: list[dict] = []
    for name, corp in COMPANIES:
        rcept = latest_business_report(key, corp)
        if not rcept:
            print(f"  {name}: 사업보고서 없음, skip")
            continue
        text = filing_text(key, rcept)
        tags = tag_items(text)
        # 원문(태그 제거 텍스트)은 gitignored data/ 에만 — 커밋 금지
        (DATA_DIR / f"{corp}_{rcept}.txt").write_text(text, encoding="utf-8")
        summary.append({"name": name, "corp_code": corp, "rcept_no": rcept, "items": tags})
        present = sum(tags.values())
        print(f"  {name}: {rcept} — 요구항목 {present}/{len(tags)} 존재")

    out = DATA_DIR / "coverage_summary.json"
    out.write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"요약 저장: {out} ({len(summary)}개사)")


if __name__ == "__main__":
    main()
