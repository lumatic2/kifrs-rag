"""K-IFRS SQLite 스토어.

tax-agent `tax_store.py` 의 `_conn()` + `init_db()` 패턴을 포팅.
Phase 1: standard, paragraph 테이블만 활성. FTS5·cross_reference·amendment 는 스캐폴드.

DB 파일: data/kifrs.db
"""
from __future__ import annotations

import json
import re
import sqlite3
from datetime import datetime
from pathlib import Path
from typing import Any, Iterable

from kifrs.user_notes import format_user_note, note_field as _note_field, parse_user_note, parse_user_note_v2

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

-- Engine Quality Ops: typed projection of user_note. Additive and idempotent.
CREATE TABLE IF NOT EXISTS user_note_v2 (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    legacy_id   INTEGER,
    standard    TEXT NOT NULL,
    no          TEXT NOT NULL,
    type        TEXT NOT NULL,
    trigger     TEXT NOT NULL,
    expansion   TEXT NOT NULL,
    source      TEXT,
    rationale   TEXT,
    active      INTEGER NOT NULL DEFAULT 1,
    confidence  REAL NOT NULL DEFAULT 1.0,
    created_at  TEXT,
    migrated_at TEXT,
    UNIQUE(legacy_id),
    FOREIGN KEY (legacy_id) REFERENCES user_note(id)
);

-- Phase 2: 임베딩 인덱스 (kifrs/embed.py)
CREATE TABLE IF NOT EXISTS embedding (
    standard    TEXT NOT NULL,
    no          TEXT NOT NULL,
    model       TEXT NOT NULL,
    dim         INTEGER NOT NULL,
    vector      BLOB NOT NULL,
    indexed_at  TEXT,
    PRIMARY KEY (standard, no, model),
    FOREIGN KEY (standard, no) REFERENCES paragraph(standard, no) ON DELETE CASCADE
);
CREATE INDEX IF NOT EXISTS idx_embedding_model ON embedding(model);
"""


def init_db() -> None:
    with _conn() as conn:
        conn.executescript(SCHEMA)


def _table_exists(conn: sqlite3.Connection, table: str) -> bool:
    row = conn.execute(
        "SELECT 1 FROM sqlite_master WHERE type='table' AND name=?", (table,)
    ).fetchone()
    return row is not None


def _has_v2_notes(conn: sqlite3.Connection) -> bool:
    if not _table_exists(conn, "user_note_v2"):
        return False
    row = conn.execute("SELECT 1 FROM user_note_v2 WHERE active=1 LIMIT 1").fetchone()
    return row is not None


def add_user_note_v2(
    standard: str,
    no: str,
    note_type: str,
    trigger: str,
    expansion: str,
    source: str | None,
    rationale: str | None,
    created_at: str | None = None,
    *,
    mirror_legacy: bool = True,
) -> dict[str, Any]:
    """Insert a typed user note, optionally mirroring to legacy `user_note`.

    The legacy mirror keeps older query paths and local DB snapshots compatible.
    Existing legacy rows are reused and never mutated.
    """
    init_db()
    note = format_user_note(note_type, trigger, expansion, source, rationale)
    now = datetime.now().isoformat(timespec="seconds")
    created = created_at or now

    with _conn() as conn:
        legacy_id = None
        if mirror_legacy:
            legacy = conn.execute(
                "SELECT id FROM user_note WHERE standard=? AND no=? AND note=?",
                (standard, no, note),
            ).fetchone()
            if legacy:
                legacy_id = legacy["id"]
            else:
                cur = conn.execute(
                    "INSERT INTO user_note (standard, no, note, created_at) VALUES (?, ?, ?, ?)",
                    (standard, no, note, created),
                )
                legacy_id = cur.lastrowid

        existing = conn.execute(
            """
            SELECT id FROM user_note_v2
            WHERE standard=? AND no=? AND type=? AND trigger=? AND expansion=?
              AND COALESCE(source, '')=COALESCE(?, '')
              AND COALESCE(rationale, '')=COALESCE(?, '')
            """,
            (standard, no, note_type, trigger, expansion, source, rationale),
        ).fetchone()
        if existing:
            return {"inserted": False, "id": existing["id"], "legacy_id": legacy_id}

        cur = conn.execute(
            """
            INSERT INTO user_note_v2
            (legacy_id, standard, no, type, trigger, expansion, source, rationale, active, confidence, created_at, migrated_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, 1, 1.0, ?, ?)
            """,
            (legacy_id, standard, no, note_type, trigger, expansion, source, rationale, created, now),
        )
        return {"inserted": True, "id": cur.lastrowid, "legacy_id": legacy_id}


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


# ── 쿼리 정상화 (M3a) ────────────────────────────────────────────────────
# 질문형(긴 문장) 쿼리를 키워드 OR 검색으로 바꾼다. FTS5 trigram 은 전 토큰을
# AND 로 묶어 긴 문장에 0 hits → 본문에 어휘로 존재하는 키워드만 뽑아 OR 결합.
# 신규 의존성 없이 순수 휴리스틱 (konlpy/mecab 은 Windows/Smart App Control 마찰).

_FTS_STOPWORDS = frozenset({
    "무엇", "무엇인가", "무엇인가요", "어떻게", "어떤", "경우", "대한", "대하여", "대해",
    "위한", "위하여", "위해", "따라", "또는", "그리고", "있는", "하는", "한다", "한가",
    "설명", "서술", "기술", "약술", "제시", "각각", "모두", "관련", "관하여", "관한",
    "이란", "이며", "인가", "되는", "되는가", "해야", "하며", "어디", "언제", "얼마",
    "이를", "이것", "그것", "있다", "한다면", "보유", "회사", "고객", "기준", "근거",
    "조항", "처리", "회계처리", "기준서", "어느", "그리", "몇개", "이내", "이후", "이전",
})

# 조사·어미 (최장일치로 strip)
_JOSA = (
    "으로서", "으로써", "이라고", "에서는", "에게는", "으로", "로서", "로써", "라고",
    "이라", "에서", "에게", "에는", "까지", "부터", "처럼", "만큼", "보다", "조차",
    "마저", "이나", "거나", "든지", "라도", "이든", "에", "은", "는", "이", "가",
    "을", "를", "의", "와", "과", "도", "만", "로", "라", "며", "고", "나", "들",
)


def _strip_josa(tok: str) -> str:
    for j in _JOSA:
        if tok.endswith(j) and len(tok) - len(j) >= 2:
            return tok[: -len(j)]
    return tok


def extract_keywords(query: str) -> list[str]:
    """질문형 쿼리에서 검색 키워드만 추출 (한글 어절 조사 strip + 불용어 제거)."""
    out: list[str] = []
    seen: set[str] = set()
    for tok in re.findall(r"[가-힣]+|[A-Za-z0-9]+", query):
        stem = tok if re.fullmatch(r"[A-Za-z0-9]+", tok) else _strip_josa(tok)
        if len(stem) < 2 or stem in _FTS_STOPWORDS:
            continue
        if stem not in seen:
            seen.add(stem)
            out.append(stem)
    return out


# 시험표현 → 본문표현 브리지 (M3b). 시험 답안 표현이 본문에 어휘로 없을 때, 본문에
# 실제 존재하는 표현을 검색 전 쿼리에 덧붙여 lexical·semantic 양쪽 신호를 보강한다.
# 실사용(dogfood) 마찰에서 누적 — 각 value 는 *본문에 실제 존재하는* 표현이어야 함.
TERM_BRIDGE: dict[str, list[str]] = {
    "할부판매": ["유의적 금융요소", "화폐의 시간가치", "현금판매가격"],
    "현재가치 할인": ["유의적 금융요소", "화폐의 시간가치"],
    "측정기준일": ["부여일"],
    "재측정요소": ["보험수리적손익"],
    "공매도": ["당기손익-공정가치 측정 금융부채", "단기매매항목"],  # 한계 #1 (goldset 밖)
}


def expand_query(query: str) -> str:
    """시험표현을 본문표현으로 확장 (M3b). 매칭된 시험표현마다 본문 용어를 쿼리에 덧붙임."""
    extra: list[str] = []
    for exam_term, body_terms in TERM_BRIDGE.items():
        if exam_term in query:
            extra.extend(body_terms)
    extra.extend(_user_note_expansions(query))
    deduped = list(dict.fromkeys(extra))
    return f"{query} {' '.join(deduped)}" if deduped else query


def _user_note_expansions(query: str) -> list[str]:
    """Use Phase 4 user_note rows as local query-expansion hints.

    Only term bridges and retriever policies are search-time signals. Exam
    conventions and interpretation notes are answer-time checklist material.
    """
    if not DB_PATH.exists():
        return []

    try:
        with _conn() as conn:
            if _has_v2_notes(conn):
                rows = conn.execute(
                    """
                    SELECT trigger, expansion FROM user_note_v2
                    WHERE active=1 AND type IN ('term_bridge', 'retriever_policy')
                    ORDER BY id
                    """
                ).fetchall()
                return _expansions_from_typed_rows(query, rows)

            rows = conn.execute(
                """
                SELECT note FROM user_note
                WHERE note LIKE 'type=term_bridge;%'
                   OR note LIKE 'type=retriever_policy;%'
                """
            ).fetchall()
    except sqlite3.Error:
        return []

    return _expansions_from_legacy_rows(query, rows)


def _expansions_from_typed_rows(query: str, rows: Iterable[sqlite3.Row]) -> list[str]:
    out: list[str] = []
    seen: set[str] = set()
    for row in rows:
        trigger = row["trigger"]
        expansion = row["expansion"]
        if not trigger or not expansion or trigger not in query:
            continue
        for term in expansion.split(";"):
            term = term.strip()
            if term and term not in seen:
                seen.add(term)
                out.append(term)
    return out


def _expansions_from_legacy_rows(query: str, rows: Iterable[sqlite3.Row]) -> list[str]:
    out: list[str] = []
    seen: set[str] = set()
    for (note,) in rows:
        trigger = _note_field(note, "trigger")
        expansion = _note_field(note, "expansion")
        if not trigger or not expansion or trigger not in query:
            continue
        for term in expansion.split(";"):
            term = term.strip()
            if term and term not in seen:
                seen.add(term)
                out.append(term)
    return out


def get_user_notes(
    query: str,
    standard: str | None = None,
    note_type: str | None = None,
    limit: int = 20,
) -> list[dict[str, Any]]:
    """Return user-authored notes whose trigger appears in the query.

    Search-time expansion intentionally uses only term_bridge/retriever_policy.
    This helper exposes exam_convention and interpretation_note at answer time.
    """
    if not DB_PATH.exists():
        return []

    try:
        with _conn() as conn:
            if _has_v2_notes(conn):
                return _get_user_notes_v2(conn, query, standard, note_type, limit)
            rows = _get_user_notes_legacy_rows(conn, standard, note_type)
    except sqlite3.Error:
        return []

    out: list[dict[str, Any]] = []
    for row in rows:
        note = row["note"]
        parsed = parse_user_note(
            row["standard"], row["no"], note, row["created_at"],
            note_id=row["id"], legacy_id=row["id"],
        )
        if not parsed.trigger or parsed.trigger not in query:
            continue
        out.append(parsed.to_dict())
        if len(out) >= limit:
            break
    return out


def _get_user_notes_v2(
    conn: sqlite3.Connection,
    query: str,
    standard: str | None,
    note_type: str | None,
    limit: int,
) -> list[dict[str, Any]]:
    sql = """
        SELECT id, legacy_id, standard, no, type, trigger, expansion, source, rationale,
               active, confidence, created_at, migrated_at
        FROM user_note_v2
        WHERE active=1
    """
    params: list[Any] = []
    if standard:
        sql += " AND standard=?"
        params.append(standard)
    if note_type:
        sql += " AND type=?"
        params.append(note_type)
    sql += " ORDER BY id"

    out: list[dict[str, Any]] = []
    for row in conn.execute(sql, params).fetchall():
        parsed = parse_user_note_v2(row)
        if not parsed.trigger or parsed.trigger not in query:
            continue
        out.append(parsed.to_dict())
        if len(out) >= limit:
            break
    return out


def _get_user_notes_legacy_rows(
    conn: sqlite3.Connection,
    standard: str | None,
    note_type: str | None,
) -> list[sqlite3.Row]:
    sql = "SELECT id, standard, no, note, created_at FROM user_note"
    clauses: list[str] = []
    params: list[Any] = []
    if standard:
        clauses.append("standard=?")
        params.append(standard)
    if note_type:
        clauses.append("note LIKE ?")
        params.append(f"type={note_type};%")
    if clauses:
        sql += " WHERE " + " AND ".join(clauses)
    sql += " ORDER BY id"
    return conn.execute(sql, params).fetchall()


def search_fts(query: str, standard: str | None = None, limit: int = 20) -> list[dict[str, Any]]:
    """본문 검색. 쿼리에서 키워드를 뽑아 FTS5 OR(bm25 정렬) 검색, 결과 없으면 LIKE fallback.
    FTS5 trigram 은 3자 미만 단어를 인덱싱하지 않음 → 2글자 한글 단어용 fallback 필수."""
    keywords = extract_keywords(expand_query(query))
    # FTS5 trigram 은 3자 미만 phrase 에 토큰을 못 만듦 → ≥3자만 MATCH, 나머지는 fallback 으로.
    fts_terms = [k for k in keywords if len(k) >= 3]
    match_str = " OR ".join(f'"{k}"' for k in fts_terms) if fts_terms else None

    with _conn() as conn:
        rows = []
        if match_str:
            q = """
                SELECT p.standard, p.no, p.appendix, p.section, p.page,
                       snippet(paragraph_fts, 3, '[', ']', '…', 16) AS snippet
                FROM paragraph_fts
                JOIN paragraph p ON p.rowid = paragraph_fts.rowid
                WHERE paragraph_fts MATCH ?
            """
            params: list[Any] = [match_str]
            if standard:
                q += " AND p.standard=?"
                params.append(standard)
            q += " ORDER BY rank LIMIT ?"   # rank = bm25 (rare 한 변별 키워드에 가중)
            params.append(limit)
            try:
                rows = conn.execute(q, params).fetchall()
            except sqlite3.OperationalError:
                rows = []
        if rows:
            return [dict(r) for r in rows]

        # Fallback: 키워드 OR LIKE 스캔 → 본문에 포함된 키워드 수로 점수 매겨 정렬.
        terms = keywords or [t for t in query.split() if t]
        if not terms:
            return []
        where = " OR ".join("body LIKE ?" for _ in terms)
        like_q = f"SELECT standard, no, appendix, section, page, body FROM paragraph WHERE ({where})"
        like_params: list[Any] = [f"%{t}%" for t in terms]
        if standard:
            like_q += " AND standard=?"
            like_params.append(standard)
        scored = []
        for r in conn.execute(like_q, like_params).fetchall():
            body = r["body"] or ""
            low = body.lower()
            hits = [t for t in terms if t.lower() in low]
            if hits:
                scored.append((len(hits), r, max(hits, key=len)))
        scored.sort(key=lambda x: -x[0])
        return [{
            "standard": r["standard"], "no": r["no"],
            "appendix": r["appendix"], "section": r["section"],
            "page": r["page"],
            "snippet": _like_snippet(r["body"] or "", probe),
        } for _, r, probe in scored[:limit]]


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
