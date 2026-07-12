"""기준서 간 상호참조 추출 — 문단 본문 → cross_reference 테이블 + 그래프 JSON.

문단 본문의 "기업회계기준서 제NNNN호" / "기업회계기준해석서 제NNNN호" 언급을 파싱해
`cross_reference` 에 문단 단위로 적재한다(context 주변 스니펫 포함 — **DB 로컬 전용**,
export 대상 아님). 그래프 JSON(web/src/data/crossref.json)은 기준서 쌍 aggregate
(from/to/weight)만 담는다 — 본문 텍스트 비노출.

실행: .venv/Scripts/python scripts/build_cross_references.py   (idempotent — 테이블 rebuild)
"""
from __future__ import annotations

import io
import json
import re
import sqlite3
import sys
from pathlib import Path

if sys.stdout.encoding and sys.stdout.encoding.lower() != "utf-8":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

ROOT = Path(__file__).resolve().parent.parent
DB_PATH = ROOT / "data" / "kifrs.db"
OUT_PATH = ROOT / "web" / "src" / "data" / "crossref.json"

# "기업회계기준서 제1109호", "한국채택국제회계기준 기준서 제1103호", "기업회계기준해석서 제2101호" 등.
# bare "제NNNN호" 는 자기 문단 번호·법령 조항과 혼동될 수 있어 기준서/해석서 접두를 요구한다.
_REF_RE = re.compile(r"(?:기준서|해석서)\s*제(\d{4})호")

CONTEXT = 40  # 참조 주변 스니펫 길이 (DB 로컬 전용)


def build(db_path: Path = DB_PATH) -> dict:
    with sqlite3.connect(db_path) as db:
        standard_ids = {r[0] for r in db.execute("SELECT id FROM standard")}
        rows = db.execute("SELECT standard, no, body FROM paragraph").fetchall()

        refs: list[tuple[str, str, str, str, str]] = []
        seen: set[tuple[str, str, str]] = set()
        for std, no, body in rows:
            for m in _REF_RE.finditer(body):
                target = m.group(1)
                if target == std or target not in standard_ids:
                    continue
                key = (std, no, target)
                if key in seen:  # 같은 문단 내 중복 언급은 1회
                    continue
                seen.add(key)
                start = max(0, m.start() - CONTEXT // 2)
                context = body[start:m.end() + CONTEXT // 2]
                refs.append((std, no, target, "", context))

        db.execute("DELETE FROM cross_reference")
        db.executemany(
            "INSERT OR IGNORE INTO cross_reference "
            "(from_standard, from_no, to_standard, to_no, context) VALUES (?, ?, ?, ?, ?)",
            refs,
        )
        db.commit()

        # aggregate 그래프 (본문 비노출 — from/to/weight 만)
        edges = db.execute("""
            SELECT from_standard, to_standard, COUNT(*) AS weight
            FROM cross_reference GROUP BY from_standard, to_standard
            ORDER BY weight DESC
        """).fetchall()

    graph = {
        "edges": [{"from": f, "to": t, "weight": w} for f, t, w in edges],
        "paragraph_refs": len(refs),
        "standard_pairs": len(edges),
    }
    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUT_PATH.write_text(json.dumps(graph, ensure_ascii=False, indent=1), encoding="utf-8")
    return graph


def main() -> None:
    g = build()
    print(f"  ✓ cross_reference: {g['paragraph_refs']} 문단 참조 → {g['standard_pairs']} 기준서 쌍")
    top = g["edges"][:8]
    for e in top:
        print(f"    {e['from']} → {e['to']}  ({e['weight']})")
    print(f"  ✓ {OUT_PATH}")
    print("다음: python scripts/check_web_data_safety.py")


if __name__ == "__main__":
    main()
