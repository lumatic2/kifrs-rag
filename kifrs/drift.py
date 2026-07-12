"""KASB 기준서 제·개정 drift 감지.

로컬 DB(`standard.source` — 인제스트 당시 현행 PDF 파일명, 개정 정보 포함)와
KASB 게시판의 현재 현행 PDF 파일 목록을 대조해 제·개정 공표(drift)를 감지한다.
fetch 는 `kifrs.download` 의 목록/상세 파서를 재사용한다.

감지 신호 (drifts — 인제스트된 기준서의 staleness, actionable):
  filename_changed  KASB 현행 PDF 파일명이 DB source 와 다름 → 개정 공표 (정본 신호)
  fileref_changed   파일명은 같지만 file_no/file_seq 가 직전 스냅샷과 다름 → 재게시
  fetch_empty       인제스트된 기준서인데 상세 페이지에 PDF 없음 → 게시 변경 의심
참고 신호 (uncovered — DB 미등재 KASB 항목, 신규 제정 후보):
  not_in_db

실행:
  .venv/Scripts/python -m kifrs.drift                        # kifrs+gaap+special 전체
  .venv/Scripts/python -m kifrs.drift --category kifrs --only 1115
"""
from __future__ import annotations

import argparse
import io
import json
import re
import sqlite3
import sys
import time
from datetime import datetime
from pathlib import Path

if sys.stdout.encoding and sys.stdout.encoding.lower() != "utf-8":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")

from kifrs import download
from kifrs.download import CATEGORIES, Standard, _slug

ROOT = Path(__file__).resolve().parent.parent
DB_PATH = ROOT / "data" / "kifrs.db"
DRIFT_DIR = ROOT / "data" / "drift"
SNAPSHOT_PATH = DRIFT_DIR / "snapshot.json"

DEFAULT_CATEGORIES = ["kifrs", "gaap", "special"]  # DB 에 인제스트된 카테고리

_SANITIZE_RE = re.compile(r'[<>:"/\\|?*]')


def _sanitize(filename: str) -> str:
    """download.download_file 과 동일한 Windows-safe 파일명 정리 (대조용)."""
    return _SANITIZE_RE.sub("_", filename).strip()


def _id_candidates(category: str, std: Standard) -> list[str]:
    """KASB 목록 항목 → DB standard.id 후보 (ingest 시 id 파생 규칙의 관측 변형들).

    관측된 id 형태: kifrs='1115'/'재무보고를_위한_개념체계', gaap='gaap_01'(제NN장),
    special='special_5002'(제N호).
    """
    slug = _slug(std.title)
    nums = [std.number]
    # download 의 number 는 제N호만 잡음 — 제N장(gaap) 등은 제목에서 직접 추출
    m = re.search(r"제(\d+)[호장]", std.title)
    if m:
        nums += [m.group(1), m.group(1).zfill(2)]
    cands = nums + [slug]
    if category != "kifrs":
        cands = [f"{category}_{n}" for n in nums] + [f"{category}_{slug}"] + cands
    # 순서 유지 중복 제거
    seen: set[str] = set()
    return [c for c in cands if not (c in seen or seen.add(c))]


def load_local(db_path: Path = DB_PATH) -> dict[str, str]:
    """DB standard 테이블 → {id: source 파일명}."""
    if not db_path.exists():
        raise FileNotFoundError(f"DB 없음: {db_path}")
    with sqlite3.connect(db_path) as db:
        return dict(db.execute("SELECT id, source FROM standard"))


def fetch_current(
    categories: list[str],
    *,
    only: str | None = None,
    delay: float = 0.2,
) -> tuple[list[dict], list[str]]:
    """KASB 에서 카테고리별 기준서 목록 + 현행(첫) PDF 파일 참조를 수집.

    Returns: (entries, errors). entry 키: category, number, seq, title,
    filename(sanitized), file_no, file_seq.
    """
    session = download.build_session()
    entries: list[dict] = []
    errors: list[str] = []
    for category in categories:
        try:
            standards = download.fetch_list(session, category)
        except Exception as e:
            errors.append(f"{category}: 목록 조회 실패 — {e}")
            continue
        if not standards:
            errors.append(f"{category}: 목록 0건 — 게시판 포맷 변경 의심")
            continue
        if only:
            standards = [s for s in standards if s.number.startswith(only)]
        for std in standards:
            try:
                refs = download.fetch_detail_files(session, std, category)
            except Exception as e:
                errors.append(f"{category}/{std.number}: 상세 조회 실패 — {e}")
                continue
            pdfs = [r for r in refs if r.ext == "pdf"]
            entries.append({
                "category": category,
                "number": std.number,
                "seq": std.seq,
                "title": std.title,
                "filename": _sanitize(pdfs[0].filename) if pdfs else None,
                "file_no": pdfs[0].file_no if pdfs else None,
                "file_seq": pdfs[0].file_seq if pdfs else None,
            })
            if delay:
                time.sleep(delay)
    return entries, errors


def load_snapshot(path: Path = SNAPSHOT_PATH) -> dict:
    if path.exists():
        return json.loads(path.read_text(encoding="utf-8"))
    return {}


def save_snapshot(entries: list[dict], path: Path = SNAPSHOT_PATH) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    snap = {
        "checked_at": datetime.now().isoformat(timespec="seconds"),
        "entries": {f"{e['category']}:{e['number']}": e for e in entries},
    }
    path.write_text(json.dumps(snap, ensure_ascii=False, indent=1), encoding="utf-8")


def compare(
    entries: list[dict],
    local: dict[str, str],
    prev_snapshot: dict | None = None,
) -> dict:
    """KASB 현재 상태 vs 로컬 DB(+직전 스냅샷) 대조 → drift 리포트 dict."""
    prev_entries = (prev_snapshot or {}).get("entries", {})
    drifts: list[dict] = []       # 인제스트된 기준서의 staleness — actionable
    uncovered: list[dict] = []    # DB 에 없는 KASB 항목 — 참고 (신규 제정 후보)
    matched = 0
    for e in entries:
        std = Standard(gubun="", seq=e["seq"], number=e["number"], title=e["title"])
        db_id = next((c for c in _id_candidates(e["category"], std) if c in local), None)
        base = {
            "category": e["category"], "number": e["number"], "title": e["title"],
            "standard_id": db_id, "kasb_filename": e["filename"],
        }
        if db_id is None:
            uncovered.append({**base, "kind": "not_in_db",
                              "detail": "KASB 목록에 있으나 DB 미등재 — 신규 제정 또는 id 매핑 미스"})
            continue
        matched += 1
        if e["filename"] is None:
            drifts.append({**base, "kind": "fetch_empty", "db_source": local[db_id],
                           "detail": "인제스트된 기준서인데 상세 페이지에 PDF 없음 — 게시 변경 의심"})
            continue
        if local[db_id] != e["filename"]:
            drifts.append({**base, "kind": "filename_changed", "db_source": local[db_id],
                           "detail": "현행 PDF 파일명 변경 — 개정 공표 가능성. 단위 갱신 필요"})
            continue
        prev = prev_entries.get(f"{e['category']}:{e['number']}")
        if prev and (prev.get("file_no"), prev.get("file_seq")) != (e["file_no"], e["file_seq"]):
            drifts.append({**base, "kind": "fileref_changed", "db_source": local[db_id],
                           "detail": "파일명 동일하나 file_no/file_seq 변경 — 재게시. 내용 확인 권장"})
    checked_ids = {
        c for e in entries
        for c in _id_candidates(e["category"], Standard("", e["seq"], e["number"], e["title"]))
    }
    return {
        "checked_at": datetime.now().isoformat(timespec="seconds"),
        "kasb_entries": len(entries),
        "db_standards": len(local),
        "matched": matched,
        "db_unmatched": sorted(set(local) - checked_ids),
        "drifts": drifts,
        "uncovered": uncovered,
    }


def run_check(
    categories: list[str] | None = None,
    *,
    only: str | None = None,
    delay: float = 0.2,
    db_path: Path = DB_PATH,
    update_snapshot: bool = True,
) -> dict:
    """감지 전체 실행: fetch → 대조 → 리포트 저장(+스냅샷 갱신). 리포트 dict 반환."""
    categories = categories or DEFAULT_CATEGORIES
    unknown = [c for c in categories if c not in CATEGORIES]
    if unknown:
        raise ValueError(f"unknown category: {unknown} (choose from {list(CATEGORIES)})")
    local = load_local(db_path)
    entries, errors = fetch_current(categories, only=only, delay=delay)
    report = compare(entries, local, load_snapshot())
    report["categories"] = categories
    report["only"] = only
    report["errors"] = errors
    if not entries and errors:
        report["fatal"] = "모든 카테고리 fetch 실패 — 네트워크 또는 게시판 포맷 변경"
    DRIFT_DIR.mkdir(parents=True, exist_ok=True)
    stamp = report["checked_at"].replace(":", "").replace("-", "").replace("T", "-")
    report_path = DRIFT_DIR / f"report-{stamp}.json"
    report_path.write_text(json.dumps(report, ensure_ascii=False, indent=1), encoding="utf-8")
    report["report_path"] = str(report_path)
    # only 필터 실행은 부분 상태라 스냅샷을 덮어쓰지 않는다 (전체 대조 기준 유지)
    if update_snapshot and entries and not only:
        save_snapshot(entries)
    return report


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description="KASB 기준서 제·개정 drift 감지")
    p.add_argument("--category", action="append", choices=list(CATEGORIES),
                   help="반복 지정 가능 (기본: kifrs gaap special)")
    p.add_argument("--only", help="기준서번호 prefix 필터 (예: 1115) — 스냅샷 갱신 안 함")
    p.add_argument("--delay", type=float, default=0.2, help="상세 요청 간 sleep(초)")
    p.add_argument("--json", action="store_true", help="리포트 JSON 전체 출력")
    args = p.parse_args(argv)

    report = run_check(args.category, only=args.only, delay=args.delay)
    if args.json:
        print(json.dumps(report, ensure_ascii=False, indent=1))
    else:
        print(f"[drift] {report['checked_at']}  KASB {report['kasb_entries']}건 / "
              f"DB {report['db_standards']}건 / 대조 {report['matched']}건")
        for d in report["drifts"]:
            print(f"  ! {d['kind']:16s} {d['category']}/{d['number']} {d['title']}")
            print(f"    {d['detail']}")
            if d.get("db_source"):
                print(f"    DB:   {d['db_source']}")
                print(f"    KASB: {d['kasb_filename']}")
        for e in report["errors"]:
            print(f"  x {e}")
        if report["uncovered"]:
            print(f"  (참고) DB 미등재 KASB 항목 {len(report['uncovered'])}건 — 리포트 JSON 참조")
        if not report["drifts"] and not report.get("fatal"):
            print("  drift 없음 — DB 는 KASB 현행과 일치")
        print(f"  리포트: {report['report_path']}")
    if report.get("fatal"):
        print(f"[drift] FATAL: {report['fatal']}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
