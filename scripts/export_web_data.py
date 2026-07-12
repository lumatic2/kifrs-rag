"""포트폴리오 사이트용 메타데이터 export — DB → web/src/data/*.json.

**저작권 하드 경계**: 기준서 본문·문단 텍스트는 어떤 형태로도 내보내지 않는다.
번호·제목(KASB 공개 목록 메타)·개수·구조·지표만. export 후 반드시
`python scripts/check_web_data_safety.py` gate 를 통과해야 커밋/배포 가능.

실행:
  .venv/Scripts/python scripts/export_web_data.py
"""
from __future__ import annotations

import io
import json
import sqlite3
import sys
from datetime import datetime
from pathlib import Path

if sys.stdout.encoding and sys.stdout.encoding.lower() != "utf-8":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from kifrs import drift
from kifrs.download import Standard

DB_PATH = ROOT / "data" / "kifrs.db"
EVAL_DIR = ROOT / "data" / "eval" / "results"
OUT_DIR = ROOT / "web" / "src" / "data"


def _title_map() -> dict[str, dict]:
    """drift snapshot(KASB 공개 목록 메타) → {db_id: {title, category}}."""
    snap = drift.load_snapshot()
    local = drift.load_local(DB_PATH)
    out: dict[str, dict] = {}
    for e in (snap.get("entries") or {}).values():
        std = Standard(gubun="", seq=e["seq"], number=e["number"], title=e["title"])
        db_id = next((c for c in drift._id_candidates(e["category"], std) if c in local), None)
        if db_id:
            out[db_id] = {"title": e["title"], "category": e["category"]}
    return out


def export_standards(conn: sqlite3.Connection) -> list[dict]:
    titles = _title_map()
    rows = conn.execute("""
        SELECT p.standard,
               COUNT(*) AS paragraphs,
               SUM(CASE WHEN p.appendix IS NULL THEN 1 ELSE 0 END) AS body,
               SUM(CASE WHEN p.appendix IN ('BC','DO','IN') THEN 1 ELSE 0 END) AS basis,
               SUM(CASE WHEN p.appendix IS NOT NULL
                         AND p.appendix NOT IN ('BC','DO','IN') THEN 1 ELSE 0 END) AS appendix,
               COUNT(DISTINCT p.section) AS sections,
               SUM(p.ko_added) AS ko_added
        FROM paragraph p GROUP BY p.standard ORDER BY p.standard
    """).fetchall()
    return [
        {
            "id": r[0],
            "title": titles.get(r[0], {}).get("title"),
            "category": titles.get(r[0], {}).get("category", "kifrs"),
            "paragraphs": r[1], "body": r[2], "basis": r[3],
            "appendix": r[4], "sections": r[5], "ko_added": r[6],
        }
        for r in rows
    ]


def export_eval_history() -> list[dict]:
    """retrieval eval 이력 — retriever별 aggregate 만 (goldset 쿼리·gold 문단 제외)."""
    history = []
    for f in sorted(EVAL_DIR.glob("retrieval_*.json")):
        try:
            d = json.loads(f.read_text(encoding="utf-8"))
        except Exception:
            continue
        history.append({
            "timestamp": d.get("timestamp"),
            "n_items": d.get("n_items"),
            "retrievers": {
                name: r.get("aggregate", {})
                for name, r in (d.get("retrievers") or {}).items()
            },
        })
    return history


def export_pipeline_stats(conn: sqlite3.Connection) -> dict:
    n_std, n_para = conn.execute(
        "SELECT COUNT(DISTINCT standard), COUNT(*) FROM paragraph").fetchone()
    n_emb = conn.execute("SELECT COUNT(*) FROM embedding").fetchone()[0]
    n_amend = conn.execute("SELECT COUNT(*) FROM amendment").fetchone()[0]
    n_notes = conn.execute("SELECT COUNT(*) FROM user_note_v2 WHERE active=1").fetchone()[0]
    snap = drift.load_snapshot()
    return {
        "standards": n_std,
        "paragraphs": n_para,
        "embeddings": n_emb,
        "embedding_model": "bge-m3 (1024d)",
        "lexical_index": "SQLite FTS5 trigram",
        "mcp_tools": 9,
        "amendments_tracked": n_amend,
        "user_notes": n_notes,
        "last_drift_check": snap.get("checked_at"),
        "exported_at": datetime.now().isoformat(timespec="seconds"),
    }


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    with sqlite3.connect(DB_PATH) as conn:
        outputs = {
            "standards.json": export_standards(conn),
            "eval_history.json": export_eval_history(),
            "pipeline.json": export_pipeline_stats(conn),
        }
    for name, data in outputs.items():
        p = OUT_DIR / name
        p.write_text(json.dumps(data, ensure_ascii=False, indent=1), encoding="utf-8")
        size = p.stat().st_size
        n = len(data) if isinstance(data, list) else len(data.keys())
        print(f"  ✓ {name}: {n} items, {size//1024} KB")
    print(f"\nexport 완료 → {OUT_DIR}")
    print("다음: python scripts/check_web_data_safety.py (gate 통과 후에만 커밋)")


if __name__ == "__main__":
    main()
