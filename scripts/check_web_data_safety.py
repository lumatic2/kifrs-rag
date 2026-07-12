"""public-safe gate — web/src/data/ 산출물에 기준서 본문이 없는지 기계 검증.

검사 2중:
  1) 길이 상한 — JSON 내 어떤 문자열 값도 MAX_LEN(200자) 초과 금지
     (제목·라벨은 짧다; 문단 본문은 수백~수만 자).
  2) 직접 대조 — **전체** 문단(17,899)의 선두 스니펫이 산출물에 문자 그대로
     포함돼 있으면 FAIL (표본 방식은 주입 검증에서 누락 적발 — 전수로 강화).

실행: .venv/Scripts/python scripts/check_web_data_safety.py   (exit 0 = PASS)
"""
from __future__ import annotations

import io
import json
import sqlite3
import sys
from pathlib import Path

if sys.stdout.encoding and sys.stdout.encoding.lower() != "utf-8":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

ROOT = Path(__file__).resolve().parent.parent
DB_PATH = ROOT / "data" / "kifrs.db"
DATA_DIR = ROOT / "web" / "src" / "data"
UNIVERSE_GRAPH = ROOT / "web" / "public" / "universe" / "graph.json"

MAX_LEN = 200
SNIPPET = 30          # 대조 스니펫 길이 (이보다 짧은 본문은 소제목 수준 — 대조 제외)


def _iter_strings(x):
    if isinstance(x, str):
        yield x
    elif isinstance(x, dict):
        for k, v in x.items():
            yield k
            yield from _iter_strings(v)
    elif isinstance(x, list):
        for v in x:
            yield from _iter_strings(v)


def main() -> int:
    files = sorted(DATA_DIR.glob("*.json"))
    if UNIVERSE_GRAPH.exists():
        files.append(UNIVERSE_GRAPH)
    if not files:
        print(f"FAIL: 산출물 없음 — {DATA_DIR}")
        return 2
    errors: list[str] = []

    # 1) 길이 상한
    blobs: dict[str, str] = {}
    for f in files:
        raw = f.read_text(encoding="utf-8")
        blobs[f.name] = raw
        for s in _iter_strings(json.loads(raw)):
            if len(s) > MAX_LEN:
                errors.append(f"{f.name}: 문자열 값 {len(s)}자 (> {MAX_LEN}) — 본문 의심: {s[:50]!r}…")

    # 2) 직접 대조 — 전체 문단 선두 스니펫 포함 여부 (전수)
    with sqlite3.connect(DB_PATH) as db:
        rows = db.execute(
            "SELECT standard, no, substr(body, 1, ?) FROM paragraph "
            "WHERE LENGTH(body) >= ?", (SNIPPET, SNIPPET)
        ).fetchall()
    for std, no, snippet in rows:
        for name, raw in blobs.items():
            if snippet in raw:
                errors.append(f"{name}: 문단 본문 포함 ({std}-{no})")
                break

    if errors:
        print(f"FAIL — {len(errors)}건:")
        for e in errors[:10]:
            print(f"  ! {e}")
        return 1
    print(f"PASS — {len(files)} 파일, 길이 상한 {MAX_LEN}자 + 본문 표본 {len(rows)}건 비포함 확인")
    return 0


if __name__ == "__main__":
    sys.exit(main())
