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


# ── MCP tools ────────────────────────────────────────────────────────────
@mcp.tool()
def list_standards() -> list[dict[str, Any]]:
    """인덱싱된 기준서 목록."""
    if USE_SQLITE:
        return _store.list_standards()
    return [
        {"standard": std, "total_paragraphs": data.get("total_paragraphs", len(data.get("paragraphs", []))), "source": data.get("source")}
        for std, data in sorted(STORE.items())
    ]


@mcp.tool()
def get_paragraph(standard: str, no: str) -> dict[str, Any] | None:
    """기준서·문단 번호로 단일 문단 반환. 예: ('1115','5'), ('1115','한4.1'), ('1115','B5')."""
    if USE_SQLITE:
        return _store.get_paragraph(standard, no)
    data = _standard(standard)
    if not data:
        return None
    for p in data.get("paragraphs", []):
        if p.get("no") == no:
            return {"standard": standard, **p}
    return None


@mcp.tool()
def list_paragraphs(standard: str, appendix: str | None = None, section: str | None = None, limit: int = 50) -> list[dict[str, Any]]:
    """문단 목록(본문 미포함, 메타+preview). appendix='A'/'B'/'C'/'본문'(=None), section 필터."""
    if USE_SQLITE:
        app_arg = None if appendix in (None, "본문") else appendix
        # __any__ 는 전체, 그 외는 정확 매칭
        return _store.list_paragraphs(standard, appendix=app_arg if appendix is not None else "__any__", section=section, limit=limit)
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


@mcp.tool()
def list_sections(standard: str) -> list[dict[str, Any]]:
    """섹션 소제목 목록."""
    if USE_SQLITE:
        return _store.list_sections(standard)
    data = _standard(standard)
    if not data:
        return []
    buckets: dict[tuple[str | None, str | None], list[str]] = {}
    for p in data.get("paragraphs", []):
        key = (p.get("appendix"), p.get("section"))
        buckets.setdefault(key, []).append(p["no"])
    return [{"appendix": a, "section": s, "paragraph_count": len(nos), "first_no": nos[0]} for (a, s), nos in buckets.items()]


@mcp.tool()
def search_lexical(query: str, standard: str | None = None, limit: int = 20, case_sensitive: bool = False) -> list[dict[str, Any]]:
    """본문 검색. SQLite 모드에서는 FTS5 trigram, JSON 모드는 정규식 substring."""
    if USE_SQLITE:
        return _store.search_fts(query, standard, limit=limit)
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


@mcp.tool()
def get_context(standard: str, no: str, around: int = 2) -> list[dict[str, Any]]:
    """문단 앞뒤 around 개 포함 맥락 반환."""
    if USE_SQLITE:
        return _store.get_context(standard, no, around)
    data = _standard(standard)
    if not data:
        return []
    paragraphs = data.get("paragraphs", [])
    for i, p in enumerate(paragraphs):
        if p.get("no") == no:
            lo, hi = max(0, i - around), min(len(paragraphs), i + around + 1)
            return [{"standard": standard, **paragraphs[j]} for j in range(lo, hi)]
    return []


@mcp.tool()
def search_semantic(query: str, standard: str | None = None, limit: int = 20) -> list[dict[str, Any]]:
    """임베딩 cosine top-k. 동의어·표현 차이에 강함 (예: '환매약정' → '재매입약정' 매칭).
    SQLite + embedding 인덱스 필요. 미인덱싱 기준서는 결과 없음."""
    if not USE_SQLITE:
        return [{"error": "semantic 검색은 SQLite 모드만 지원. data/kifrs.db 필요"}]
    # lazy import — 모델 로드는 첫 호출 시
    from kifrs.embed import semantic_search
    return semantic_search(query, standard, limit)


@mcp.tool()
def search_hybrid(query: str, standard: str | None = None, limit: int = 20) -> list[dict[str, Any]]:
    """RRF (Reciprocal Rank Fusion) 하이브리드 검색 — lexical(FTS5) + semantic.
    각 검색 결과의 순위에 1/(60+rank) 점수를 합산해 top-k 반환.
    lexical 정확 매칭과 semantic 동의어 매칭 모두 활용."""
    if not USE_SQLITE:
        return [{"error": "hybrid 검색은 SQLite 모드만 지원. data/kifrs.db 필요"}]
    from kifrs.embed import search_hybrid as _hybrid
    return _hybrid(query, standard, limit)


@mcp.tool()
def search_hierarchical(query: str, standard: str | None = None, limit: int = 20) -> list[dict[str, Any]]:
    """계층 검색 — 조·항·호 **섹션**을 1차 단위로. hybrid(lexical+semantic) + 섹션 membership 3-way RRF.
    **넓은 recall 1순위**: hybrid 전 지표 비퇴행/개선(recall@5 0.597→0.627, @10 0.763→0.827, @20 0.907→0.917,
    MRR 0.509→0.542). 섹션 제목이 쿼리와 일치하는 정답을 끌어올림. 정밀 인용 top-5는 search_reranked."""
    if not USE_SQLITE:
        return [{"error": "hierarchical 검색은 SQLite 모드만 지원. data/kifrs.db 필요"}]
    from kifrs.embed import search_hierarchical as _hier
    return _hier(query, standard, limit)


@mcp.tool()
def search_reranked(query: str, standard: str | None = None, limit: int = 10) -> list[dict[str, Any]]:
    """Cross-encoder 리랭킹 검색 — hybrid top-50 후보를 bge-reranker-v2-m3로 재점수.
    **정밀 인용 1순위**: top-5 정밀도가 hybrid보다 높음(recall@5 0.640 vs 0.597, MRR 0.612 vs 0.509).
    매우 깊은 recall(@20)이 필요하면 search_hybrid(0.907 > reranked 0.853). per-query ~0.4s(GPU)."""
    if not USE_SQLITE:
        return [{"error": "reranked 검색은 SQLite 모드만 지원. data/kifrs.db 필요"}]
    from kifrs.embed import search_reranked as _reranked
    return _reranked(query, standard, limit=limit, candidates=50)


@mcp.tool()
def reload_store() -> dict[str, Any]:
    """디스크에서 파싱 JSON 다시 로드. ingest 파이프라인 갱신 후 재기동 없이 반영."""
    global STORE
    STORE = _load_all()
    return {"loaded": sorted(STORE.keys()), "count": len(STORE)}


def main():
    backend = "sqlite" if USE_SQLITE else "json"
    loaded = [s["standard"] for s in _store.list_standards()] if USE_SQLITE else sorted(STORE.keys())
    print(f"[kifrs-mcp] backend={backend} | standards={loaded}", file=sys.stderr)

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

        threading.Thread(target=_warmup, name="embed-warmup", daemon=True).start()

    mcp.run()


if __name__ == "__main__":
    main()
