"""K-IFRS SQLite 스토어.

tax-agent `tax_store.py` 의 `_conn()` + `init_db()` 패턴을 포팅.
Phase 1: standard, paragraph 테이블만 활성. FTS5·cross_reference·amendment 는 스캐폴드.

DB 파일: data/kifrs.db
"""
from __future__ import annotations

import json
import sqlite3
from datetime import datetime
from pathlib import Path
from typing import Any, Iterable

ROOT = Path(__file__).resolve().parent.parent
DB_PATH = ROOT / "data" / "kifrs.db"


def _conn() -> sqlite3.Connection:
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


# ── 스키마 ────────────────────────────────────────────────────────────────
SCHEMA = """
CREATE TABLE IF NOT EXISTS standard (
    id               TEXT PRIMARY KEY,   -- '1115', '1116', ...
    source           TEXT,               -- 원본 PDF 파일명
    total_paragraphs INTEGER,
    parsed_at        TEXT,
    ingested_at      TEXT
);

CREATE TABLE IF NOT EXISTS paragraph (
    standard    TEXT NOT NULL,
    no          TEXT NOT NULL,           -- '5', '한4.1', 'B5', '부록A'
    appendix    TEXT,                    -- 'A' / 'B' / 'C' / NULL(본문)
    ko_added    INTEGER NOT NULL DEFAULT 0,
    page        INTEGER,
    section     TEXT,
    body        TEXT NOT NULL,
    ord         INTEGER NOT NULL,        -- 파일 내 순서 (get_context 용)
    PRIMARY KEY (standard, no),
    FOREIGN KEY (standard) REFERENCES standard(id) ON DELETE CASCADE
);

CREATE INDEX IF NOT EXISTS idx_paragraph_ord       ON paragraph(standard, ord);
CREATE INDEX IF NOT EXISTS idx_paragraph_section   ON paragraph(standard, section);
CREATE INDEX IF NOT EXISTS idx_paragraph_appendix  ON paragraph(standard, appendix);

-- Phase 2: 하이브리드 검색용 FTS5 가상 테이블 (한글 trigram)
CREATE VIRTUAL TABLE IF NOT EXISTS paragraph_fts USING fts5(
    standard, no, section, body,
    content='paragraph', content_rowid='rowid',
    tokenize='trigram'
);

-- Phase 2: 조항 간 상호참조
CREATE TABLE IF NOT EXISTS cross_reference (
    from_standard TEXT NOT NULL,
    from_no       TEXT NOT NULL,
    to_standard   TEXT NOT NULL,
    to_no         TEXT NOT NULL,
    context       TEXT,                  -- 참조 주변 텍스트 20-50자
    PRIMARY KEY (from_standard, from_no, to_standard, to_no)
);

-- Phase 3: 개정 이력
CREATE TABLE IF NOT EXISTS amendment (
    id            INTEGER PRIMARY KEY AUTOINCREMENT,
    standard      TEXT NOT NULL,
    no            TEXT NOT NULL,
    revised_on    TEXT,                  -- 'YYYY-MM-DD'
    previous_body TEXT,
    new_body      TEXT,
    note          TEXT
);

-- Phase 3: 사용자 자체 해설(저작권 안전한 창작물)
CREATE TABLE IF NOT EXISTS user_note (
    id         INTEGER PRIMARY KEY AUTOINCREMENT,
    standard   TEXT NOT NULL,
    no         TEXT NOT NULL,
    note       TEXT NOT NULL,
    created_at TEXT
);
"""


def init_db() -> None:
    with _conn() as conn:
        conn.executescript(SCHEMA)


# ── ingest (parsed JSON → DB) ────────────────────────────────────────────
def upsert_from_json(path: Path) -> dict[str, Any]:
    """parse.py 산출 JSON 한 개를 읽어 standard + paragraph 테이블에 저장."""
    data = json.loads(path.read_text(encoding="utf-8"))
    std = str(data["standard"])
    paragraphs = data.get("paragraphs", [])
    now = datetime.now().isoformat(timespec="seconds")

    with _conn() as conn:
        conn.execute(
            """
            INSERT INTO standard (id, source, total_paragraphs, parsed_at, ingested_at)
            VALUES (?, ?, ?, ?, ?)
            ON CONFLICT(id) DO UPDATE SET
                source=excluded.source,
                total_paragraphs=excluded.total_paragraphs,
                parsed_at=excluded.parsed_at,
                ingested_at=excluded.ingested_at
            """,
            (std, data.get("source"), data.get("total_paragraphs", len(paragraphs)),
             data.get("parsed_at"), now),
        )
        conn.execute("DELETE FROM paragraph WHERE standard=?", (std,))
        # 중복 no 디듀플리케이트 (예: 부록A 헤더가 여러 섹션에서 반복)
        seen: dict[str, int] = {}
        rows = []
        for i, p in enumerate(paragraphs):
            no = p["no"]
            seen[no] = seen.get(no, 0) + 1
            if seen[no] > 1:
                no = f"{no}#{seen[no]}"
            rows.append((
                std, no, p.get("appendix"),
                1 if p.get("ko_added") else 0,
                p.get("page"), p.get("section"),
                p.get("body") or "", i,
            ))
        conn.executemany(
            """
            INSERT INTO paragraph (standard, no, appendix, ko_added, page, section, body, ord)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            rows,
        )
        # FTS5 contentless-external 동기화: 전체 rebuild (단순·안전)
        conn.execute("INSERT INTO paragraph_fts(paragraph_fts) VALUES('rebuild')")
    return {"standard": std, "paragraphs": len(paragraphs)}


# ── query 헬퍼 ───────────────────────────────────────────────────────────
def get_paragraph(standard: str, no: str) -> dict[str, Any] | None:
    with _conn() as conn:
        row = conn.execute(
            "SELECT * FROM paragraph WHERE standard=? AND no=?", (standard, no)
        ).fetchone()
        return dict(row) if row else None


def list_paragraphs(
    standard: str,
    appendix: str | None = "__any__",
    section: str | None = None,
    limit: int = 50,
) -> list[dict[str, Any]]:
    q = "SELECT standard, no, appendix, ko_added, page, section, substr(body,1,80) AS preview FROM paragraph WHERE standard=?"
    params: list[Any] = [standard]
    if appendix != "__any__":
        q += " AND appendix IS ?" if appendix is None else " AND appendix=?"
        if appendix is not None:
            params.append(appendix)
    if section is not None:
        q += " AND section=?"
        params.append(section)
    q += " ORDER BY ord LIMIT ?"
    params.append(limit)
    with _conn() as conn:
        return [dict(r) for r in conn.execute(q, params).fetchall()]


def _like_snippet(body: str, query: str, window: int = 40) -> str:
    import re as _re
    m = _re.search(_re.escape(query), body, _re.IGNORECASE)
    if not m:
        return body[:120]
    s, e = max(0, m.start() - window), min(len(body), m.end() + window * 2)
    return f"{body[s:m.start()]}[{body[m.start():m.end()]}]{body[m.end():e]}"


def search_fts(query: str, standard: str | None = None, limit: int = 20) -> list[dict[str, Any]]:
    """본문 검색. FTS5 trigram 우선, 결과 없으면 LIKE substring fallback.
    FTS5 trigram 은 3자 미만 단어를 인덱싱하지 않음 → 2글자 한글 단어용 fallback 필수."""
    q = """
        SELECT p.standard, p.no, p.appendix, p.section, p.page,
               snippet(paragraph_fts, 3, '[', ']', '…', 16) AS snippet
        FROM paragraph_fts
        JOIN paragraph p ON p.rowid = paragraph_fts.rowid
        WHERE paragraph_fts MATCH ?
    """
    params: list[Any] = [query]
    if standard:
        q += " AND p.standard=?"
        params.append(standard)
    q += " LIMIT ?"
    params.append(limit)
    with _conn() as conn:
        try:
            rows = conn.execute(q, params).fetchall()
        except sqlite3.OperationalError:
            rows = []
        if rows:
            return [dict(r) for r in rows]

        # Fallback: LIKE substring. query 에 공백 있으면 첫 토큰으로 스캔 후 전체 포함 필터.
        tokens = [t for t in query.split() if t]
        if not tokens:
            return []
        probe = max(tokens, key=len)
        like_q = "SELECT standard, no, appendix, section, page, body FROM paragraph WHERE body LIKE ?"
        like_params: list[Any] = [f"%{probe}%"]
        if standard:
            like_q += " AND standard=?"
            like_params.append(standard)
        like_q += " LIMIT ?"
        like_params.append(limit * 3)
        out = []
        for r in conn.execute(like_q, like_params).fetchall():
            body = r["body"] or ""
            if not all(t.lower() in body.lower() for t in tokens):
                continue
            out.append({
                "standard": r["standard"], "no": r["no"],
                "appendix": r["appendix"], "section": r["section"],
                "page": r["page"],
                "snippet": _like_snippet(body, probe),
            })
            if len(out) >= limit:
                break
        return out


def get_context(standard: str, no: str, around: int = 2) -> list[dict[str, Any]]:
    with _conn() as conn:
        row = conn.execute(
            "SELECT ord FROM paragraph WHERE standard=? AND no=?", (standard, no)
        ).fetchone()
        if not row:
            return []
        lo, hi = row["ord"] - around, row["ord"] + around
        rows = conn.execute(
            "SELECT * FROM paragraph WHERE standard=? AND ord BETWEEN ? AND ? ORDER BY ord",
            (standard, lo, hi),
        ).fetchall()
        return [dict(r) for r in rows]


def list_standards() -> list[dict[str, Any]]:
    with _conn() as conn:
        return [dict(r) for r in conn.execute(
            "SELECT id AS standard, source, total_paragraphs, parsed_at, ingested_at FROM standard ORDER BY id"
        ).fetchall()]


def list_sections(standard: str) -> list[dict[str, Any]]:
    with _conn() as conn:
        rows = conn.execute(
            """
            SELECT appendix, section, COUNT(*) AS paragraph_count, MIN(no) AS first_no
            FROM paragraph
            WHERE standard=?
            GROUP BY appendix, section
            ORDER BY MIN(ord)
            """,
            (standard,),
        ).fetchall()
        return [dict(r) for r in rows]
