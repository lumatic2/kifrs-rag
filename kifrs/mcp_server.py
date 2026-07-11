"""K-IFRS RAG MCP 서버 (Phase 1+2).

data/standards/parsed/*.json + SQLite + 임베딩(bge-m3) 인덱스를 MCP tool 로 노출한다.

실행:
  uv run python -m kifrs.mcp_server
등록 (Claude Code):
  claude mcp add kifrs -- uv --directory /path/to/kifrs-rag run python -m kifrs.mcp_server
"""
from __future__ import annotations

import os
import sys

# fastmcp 는 stdio 로 JSON-RPC 통신. transformers/huggingface 라이브러리의
# stdout 출력은 통신 메시지를 corrupt 시키므로 import 전에 노이즈 차단.
os.environ.setdefault("HF_HUB_DISABLE_PROGRESS_BARS", "1")
os.environ.setdefault("HF_HUB_DISABLE_TELEMETRY", "1")
os.environ.setdefault("TRANSFORMERS_VERBOSITY", "error")
os.environ.setdefault("TQDM_DISABLE", "1")

import json
import re
from pathlib import Path
from typing import Any

from fastmcp import FastMCP
from fastmcp.exceptions import ToolError

from kifrs import store as _store

ROOT = Path(__file__).resolve().parent.parent
PARSED_DIR = ROOT / "data" / "standards" / "parsed"

# 백엔드: kifrs.db 가 있으면 SQLite, 없으면 JSON 파일 로더 fallback
USE_SQLITE = _store.DB_PATH.exists()

mcp = FastMCP("kifrs")


# ── 스토어 (JSON 파일 → 메모리) ────────────────────────────────────────────
def _load_all() -> dict[str, dict[str, Any]]:
    store: dict[str, dict[str, Any]] = {}
    if not PARSED_DIR.exists():
        return store
    for path in sorted(PARSED_DIR.glob("*.json")):
        if path.stem.endswith("_view") or path.stem == "index":
            continue
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except Exception as e:
            print(f"[WARN] load 실패 {path.name}: {e}")
            continue
        std = data.get("standard") or path.stem
        store[str(std)] = data
    return store


STORE = _load_all()


def _standard(standard: str) -> dict[str, Any] | None:
    return STORE.get(str(standard))


def _dispatch(sqlite_fn, json_fn):
    """SQLite/JSON dual-backend dispatch — single shared branch instead of one
    `if USE_SQLITE: ... else: ...` per tool."""
    return sqlite_fn() if USE_SQLITE else json_fn()


def _require_sqlite(feature: str) -> None:
    """Embedding-backed tools (semantic/hybrid/hierarchical/reranked search, user_note)
    have no JSON-fallback implementation — raise a typed tool error instead of returning
    a `[{"error": ...}]` sentinel the caller has to pattern-match."""
    if not USE_SQLITE:
        raise ToolError(f"{feature} 검색은 SQLite 모드만 지원. data/kifrs.db 필요")


# ── MCP tools ────────────────────────────────────────────────────────────
@mcp.tool(output_schema=None)
def list_standards() -> list[dict[str, Any]]:
    """인덱싱된 기준서 목록."""
    return _dispatch(
        lambda: _store.list_standards(),
        lambda: [
            {"standard": std, "total_paragraphs": data.get("total_paragraphs", len(data.get("paragraphs", []))), "source": data.get("source")}
            for std, data in sorted(STORE.items())
        ],
    )


def _get_paragraph_json(standard: str, no: str) -> dict[str, Any] | None:
    data = _standard(standard)
    if not data:
        return None
    for p in data.get("paragraphs", []):
        if p.get("no") == no:
            return {"standard": standard, **p}
    return None


@mcp.tool(output_schema=None)
def get_paragraph(standard: str, no: str) -> dict[str, Any] | None:
    """기준서·문단 번호로 단일 문단 반환. 예: ('1115','5'), ('1115','한4.1'), ('1115','B5')."""
    return _dispatch(
        lambda: _store.get_paragraph(standard, no),
        lambda: _get_paragraph_json(standard, no),
    )


def _list_paragraphs_json(standard: str, appendix: str | None, section: str | None, limit: int) -> list[dict[str, Any]]:
    data = _standard(standard)
    if not data:
        return []
    out: list[dict[str, Any]] = []
    for p in data.get("paragraphs", []):
        if appendix is not None and p.get("appendix") != (appendix if appendix != "본문" else None):
            continue
        if section is not None and (p.get("section") or "") != section:
            continue
        out.append({"no": p["no"], "appendix": p.get("appendix"), "section": p.get("section"),
                    "ko_added": p.get("ko_added", False), "page": p.get("page"),
                    "preview": (p.get("body") or "")[:80]})
        if len(out) >= limit:
            break
    return out


@mcp.tool(output_schema=None)
def list_paragraphs(standard: str, appendix: str | None = None, section: str | None = None, limit: int = 50) -> list[dict[str, Any]]:
    """문단 목록(본문 미포함, 메타+preview). appendix='A'/'B'/'C'/'본문'(=None), section 필터."""
    app_arg = None if appendix in (None, "본문") else appendix
    return _dispatch(
        # __any__ 는 전체, 그 외는 정확 매칭
        lambda: _store.list_paragraphs(standard, appendix=app_arg if appendix is not None else "__any__", section=section, limit=limit),
        lambda: _list_paragraphs_json(standard, appendix, section, limit),
    )


def _list_sections_json(standard: str) -> list[dict[str, Any]]:
    data = _standard(standard)
    if not data:
        return []
    buckets: dict[tuple[str | None, str | None], list[str]] = {}
    for p in data.get("paragraphs", []):
        key = (p.get("appendix"), p.get("section"))
        buckets.setdefault(key, []).append(p["no"])
    return [{"appendix": a, "section": s, "paragraph_count": len(nos), "first_no": nos[0]} for (a, s), nos in buckets.items()]


@mcp.tool(output_schema=None)
def list_sections(standard: str) -> list[dict[str, Any]]:
    """섹션 소제목 목록."""
    return _dispatch(
        lambda: _store.list_sections(standard),
        lambda: _list_sections_json(standard),
    )


def _search_lexical_json(query: str, standard: str | None, limit: int, case_sensitive: bool = False) -> list[dict[str, Any]]:
    flags = 0 if case_sensitive else re.IGNORECASE
    try:
        pat = re.compile(query, flags)
    except re.error:
        pat = re.compile(re.escape(query), flags)
    hits: list[dict[str, Any]] = []
    targets = [_standard(standard)] if standard else list(STORE.values())
    for data in targets:
        if not data:
            continue
        std = data.get("standard")
        for p in data.get("paragraphs", []):
            body = p.get("body") or ""
            m = pat.search(body)
            if not m:
                continue
            snippet = body[max(0, m.start() - 40): min(len(body), m.end() + 80)]
            hits.append({"standard": std, "no": p["no"], "appendix": p.get("appendix"),
                         "section": p.get("section"), "page": p.get("page"), "snippet": snippet})
            if len(hits) >= limit:
                return hits
    return hits


def _get_context_json(standard: str, no: str, around: int) -> list[dict[str, Any]]:
    data = _standard(standard)
    if not data:
        return []
    paragraphs = data.get("paragraphs", [])
    for i, p in enumerate(paragraphs):
        if p.get("no") == no:
            lo, hi = max(0, i - around), min(len(paragraphs), i + around + 1)
            return [{"standard": standard, **paragraphs[j]} for j in range(lo, hi)]
    return []


@mcp.tool(output_schema=None)
def get_context(standard: str, no: str, around: int = 2) -> list[dict[str, Any]]:
    """문단 앞뒤 around 개 포함 맥락 반환."""
    return _dispatch(
        lambda: _store.get_context(standard, no, around),
        lambda: _get_context_json(standard, no, around),
    )


_SEARCH_MODES = ("lexical", "semantic", "hybrid", "hierarchical", "reranked")


@mcp.tool(output_schema=None)
def search(query: str, standard: str | None = None, limit: int = 20, mode: str = "hybrid") -> list[dict[str, Any]]:
    """K-IFRS 본문 검색. `mode` 로 알고리즘 선택 (단일 지표 기준의 절대 우위 모드는 없음 — 목적별로 고른다).

    - **"reranked"** (정밀 인용 1순위) — hybrid top-50 을 cross-encoder(bge-reranker-v2-m3)로
      재점수. top-5 정밀도 최고. 정확한 조항 1~2개를 집어 인용할 때. per-query ~0.4s(GPU).
    - **"hierarchical"** (넓은 recall 1순위) — 조·항·호 **섹션**을 1차 단위로, hybrid(lexical+
      semantic) + 섹션 membership 3-way RRF. 섹션 제목이 쿼리와 일치하는 정답을 끌어올림.
      hybrid 대비 전 지표 비퇴행/개선. 여러 후보를 폭넓게 보거나 reranked 가 놓친 후보 보강.
    - **"hybrid"** — lexical(FTS5)+semantic RRF. hierarchical/reranked 의 baseline·대조군.
    - **"lexical"** — FTS5 trigram 정확 매칭(SQLite) / 정규식 substring fallback(JSON 모드,
      쿼리 정규화 없음). 조항 번호·정확 용어 검색, SQLite 없어도 동작하는 유일한 mode.
    - **"semantic"** — bge-m3 cosine. 순수 의미 매칭, lexical 0건이 명백할 때.

    recall@k/MRR 실측치는 시점에 따라 바뀐다 — 최신 수치는 `python -m kifrs.eval.retrieval`
    재실행으로 확인(하드코딩하지 않음, docstring-eval drift 방지).

    **`standard` 필터 주의** — 정답이 다른 기준서에 있으면 필터가 실패 원인이 된다
    (예: '리픽싱' 실체 규정은 1032가 아니라 1001-한138.5). top score가 낮거나 기대한
    문단이 안 보이면 **필터를 해제하고 재검색**하라. 필터 없이 1차 탐색 후 좁히는
    순서가 더 안전하다.
    """
    if mode == "lexical":
        return _dispatch(
            lambda: _store.search_fts(query, standard, limit=limit),
            lambda: _search_lexical_json(query, standard, limit),
        )
    if mode not in _SEARCH_MODES:
        raise ToolError(f"unknown mode {mode!r} — choose one of {_SEARCH_MODES}")
    _require_sqlite(mode)
    if mode == "semantic":
        # lazy import — 모델 로드는 첫 호출 시
        from kifrs.embed import semantic_search
        return semantic_search(query, standard, limit)
    if mode == "hybrid":
        from kifrs.embed import search_hybrid
        return search_hybrid(query, standard, limit)
    if mode == "hierarchical":
        from kifrs.embed import search_hierarchical
        return search_hierarchical(query, standard, limit)
    from kifrs.embed import search_reranked
    return search_reranked(query, standard, limit=limit, candidates=50)


@mcp.tool(output_schema=None)
def get_user_notes(query: str, standard: str | None = None, note_type: str | None = None, limit: int = 20) -> list[dict[str, Any]]:
    """사용자 해설/user_note 조회. exam_convention·interpretation_note를 답변 작성 전 checklist로 확인한다."""
    _require_sqlite("user_note")
    return _store.get_user_notes(query, standard=standard, note_type=note_type, limit=limit)


@mcp.tool(output_schema=None)
def reload_store() -> dict[str, Any]:
    """디스크에서 파싱 JSON 다시 로드하고 임베딩 행렬/centroid 캐시를 무효화한다.
    SQLite 모드에서는 paragraph/embedding 테이블 자체를 재조회하지 않는다 — 재기동 없이
    반영되는 건 쿼리 시점 캐시뿐이며, `USE_SQLITE`(백엔드 선택)는 재계산되지 않는다."""
    global STORE
    STORE = _load_all()
    if USE_SQLITE:
        from kifrs.embed import invalidate_caches
        invalidate_caches()
    return {"loaded": sorted(STORE.keys()), "count": len(STORE)}


def _redirect_stderr_to_logfile():
    """Codex's MCP client hands the child an stderr handle that becomes
    unwritable on Windows mid-startup (OSError(EINVAL) on the first write after
    the heavy torch/transformers import), which kills the server before it can
    answer `initialize` -> the client reports "connection closed". Route fd 2
    and sys.stderr to a logfile so neither our diagnostics nor FastMCP's startup
    banner can crash the process. stdout (the JSON-RPC channel) is untouched."""
    import tempfile

    try:
        f = open(os.path.join(tempfile.gettempdir(), "kifrs_mcp.log"),
                 "a", encoding="utf-8", buffering=1)
    except Exception:
        return
    try:
        os.dup2(f.fileno(), 2)
    except Exception:
        pass
    sys.stderr = f


def main():
    _redirect_stderr_to_logfile()
    backend = "sqlite" if USE_SQLITE else "json"
    loaded = [s["standard"] for s in _store.list_standards()] if USE_SQLITE else sorted(STORE.keys())
    print(f"[kifrs-mcp] backend={backend} | standards={loaded}", file=sys.stderr)

    # 빈/손상된 data/kifrs.db 는 여기서 잡지 않으면 각 tool 호출 내부 SQL 실행에서야
    # 실패한다. 존재하지만 비어 있으면 시작 시점에 바로 실패 메시지를 남긴다.
    if USE_SQLITE and not _store.has_paragraphs():
        print(
            f"[kifrs-mcp] FATAL: {_store.DB_PATH} exists but has no paragraph rows — "
            "run `python scripts/ingest.py` before starting the server",
            file=sys.stderr,
        )
        sys.exit(1)

    # 무거운 C-확장 import(sentence_transformers→sklearn→scipy)는 반드시 **메인 스레드**에서.
    # 백그라운드 스레드에서 처음 import 하면 CPython import-lock 교착으로 영구 hang 한다
    # (scipy#13985 등 — 이전엔 warmup 스레드가 _model_lock 쥔 채 여기서 멈춰 tool 호출까지
    # 같이 멈췄다). 핸드셰이크는 이 import(~5초)만큼만 늦어지며 타임아웃 한참 이내.
    # 가중치 로딩(느림)은 import 완료 후 warmup 데몬 스레드로 돌려 첫 search 를 빠르게 한다.
    if USE_SQLITE:
        import threading

        from kifrs.embed import eager_import
        eager_import()
        print("[kifrs-mcp] heavy imports done (main thread)", file=sys.stderr)

        def _warmup() -> None:
            try:
                from kifrs.embed import _load_model, _load_reranker
                _load_model()
                print("[kifrs-mcp] embed model loaded (warmup)", file=sys.stderr)
                _load_reranker()
                print("[kifrs-mcp] reranker loaded (warmup)", file=sys.stderr)
            except Exception as e:
                print(f"[kifrs-mcp] warmup skipped: {e}", file=sys.stderr)

        if os.environ.get("KIFRS_MCP_DISABLE_WARMUP") == "1":
            print("[kifrs-mcp] warmup disabled", file=sys.stderr)
        else:
            threading.Thread(target=_warmup, name="embed-warmup", daemon=True).start()

    mcp.run()


if __name__ == "__main__":
    main()
