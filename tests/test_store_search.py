"""Retrieval logic safety net — kifrs/embed.py + kifrs/mcp_server.py dual-backend paths.

Runs against the real local `data/kifrs.db` (gitignored per the K-IFRS copyright
boundary). Skips cleanly wherever that DB is absent (fresh clone, CI).
"""
from __future__ import annotations

import pytest

from kifrs import store

pytestmark = pytest.mark.skipif(
    not store.DB_PATH.exists(), reason="local data/kifrs.db not present"
)


def _rrf_scores(results):
    return [r["rrf"] for r in results]


def test_search_hybrid_sorted_by_rrf_descending():
    from kifrs.embed import search_hybrid

    results = search_hybrid("공정가치", limit=10)
    assert results
    scores = _rrf_scores(results)
    assert scores == sorted(scores, reverse=True)
    assert len(results) <= 10


def test_search_hybrid_respects_standard_filter():
    from kifrs.embed import search_hybrid

    results = search_hybrid("자산", standard="1115", limit=10)
    assert results
    assert all(r["standard"] == "1115" for r in results)


def test_search_hierarchical_sorted_by_rrf_descending():
    from kifrs.embed import search_hierarchical

    results = search_hierarchical("리스", limit=10)
    assert results
    scores = _rrf_scores(results)
    assert scores == sorted(scores, reverse=True)
    assert len(results) <= 10


def test_search_hierarchical_falls_back_to_hybrid_when_no_embeddings():
    from kifrs.embed import search_hierarchical, search_hybrid

    # A standard id with no rows in `embedding` forces mat is None -> fallback path.
    fallback = search_hierarchical("자산", standard="__nonexistent_standard__", limit=5)
    hybrid = search_hybrid("자산", standard="__nonexistent_standard__", limit=5)
    assert fallback == hybrid


def test_search_reranked_sorted_by_rerank_score_and_within_limit():
    from kifrs.embed import search_reranked

    results = search_reranked("금융자산 분류", limit=5, candidates=10)
    assert results
    assert len(results) <= 5
    assert all("rerank_score" in r for r in results)
    scores = [r["rerank_score"] for r in results]
    assert scores == sorted(scores, reverse=True)


def test_search_reranked_candidate_pool_can_be_smaller_than_requested():
    """Documents current behavior: the reranker's actual candidate pool comes from
    search_hybrid(limit=candidates), which itself unions two independent top-50
    lists (lexical/semantic) capped at `candidates` — the pool is not guaranteed
    to reach `candidates` items even when the corpus has far more matches."""
    from kifrs.embed import search_hybrid

    pool = search_hybrid("공정가치", limit=50)
    assert len(pool) <= 50


def test_mcp_server_json_fallback_raises_tool_error():
    """With USE_SQLITE=False, search(mode=...) for the four embedding-backed modes
    (semantic/hybrid/hierarchical/reranked) and get_user_notes raise a typed fastmcp
    ToolError instead of returning an `[{"error": ...}]` sentinel a caller would have
    to pattern-match. mode="lexical" is excluded — it has a real JSON fallback."""
    from fastmcp.exceptions import ToolError

    from kifrs import mcp_server

    original = mcp_server.USE_SQLITE
    mcp_server.USE_SQLITE = False
    try:
        for mode in ["semantic", "hybrid", "hierarchical", "reranked"]:
            with pytest.raises(ToolError):
                mcp_server.search("공정가치", mode=mode)
        with pytest.raises(ToolError):
            mcp_server.get_user_notes("공정가치")
    finally:
        mcp_server.USE_SQLITE = original


def test_mcp_server_search_rejects_unknown_mode():
    from fastmcp.exceptions import ToolError

    from kifrs import mcp_server

    with pytest.raises(ToolError):
        mcp_server.search("자산", mode="bogus")


def test_mcp_server_search_lexical_mode_matches_store_search_fts():
    from kifrs import mcp_server

    assert mcp_server.USE_SQLITE is True
    via_tool = mcp_server.search("자산", limit=5, mode="lexical")
    via_store = store.search_fts("자산", limit=5)
    assert via_tool == via_store


def test_mcp_server_search_reranked_mode_matches_embed_search_reranked():
    from kifrs import mcp_server
    from kifrs.embed import search_reranked

    via_tool = mcp_server.search("금융자산 분류", limit=5, mode="reranked")
    via_embed = search_reranked("금융자산 분류", limit=5, candidates=50)
    assert via_tool == via_embed


def test_store_has_paragraphs_true_for_local_db():
    assert store.has_paragraphs() is True


def test_get_paragraphs_batch_matches_individual_lookups():
    pairs = [("1115", "5"), ("1115", "9")]
    batch = store.get_paragraphs_batch(pairs)
    for std, no in pairs:
        assert batch[(std, no)] == store.get_paragraph(std, no)


def test_get_paragraphs_batch_empty_input():
    assert store.get_paragraphs_batch([]) == {}


# ── ib4: search() section/exclude_bc 후보 필터링 ──────────────────────────
# 결함: 공시 절 수집 쿼리에서 search(reranked/hierarchical) 가 BC·측정 절 문단에
# 희석되어 회수율이 낮다 (BACKLOG 2026-07-12(b) H10 C8-2). 랭킹은 그대로 두고 후보만
# 필터링 — _apply_candidate_filter 는 순수 함수라 로컬 DB 없이도 단위 테스트 가능.


def test_apply_candidate_filter_section_substring():
    from kifrs import mcp_server

    hits = [
        {"section": "공시", "appendix": None},
        {"section": "인식과 측정", "appendix": None},
        {"section": "질적 공시", "appendix": None},
    ]
    out = mcp_server._apply_candidate_filter(hits, section="공시", exclude_bc=False, limit=10)
    assert [h["section"] for h in out] == ["공시", "질적 공시"]
    assert all(h["filter_applied"] == {"section": "공시", "exclude_bc": False} for h in out)


def test_apply_candidate_filter_exclude_bc():
    from kifrs import mcp_server

    hits = [{"section": "x", "appendix": "BC"}, {"section": "x", "appendix": None}]
    out = mcp_server._apply_candidate_filter(hits, section=None, exclude_bc=True, limit=10)
    assert len(out) == 1
    assert out[0]["appendix"] is None


def test_apply_candidate_filter_honest_short_result_not_backfilled():
    """필터 통과분이 limit 보다 적으면 필터 전 결과로 채우지 않고 정직하게 적게 반환."""
    from kifrs import mcp_server

    hits = [{"section": "공시", "appendix": None}, {"section": "측정", "appendix": None}]
    out = mcp_server._apply_candidate_filter(hits, section="공시", exclude_bc=False, limit=10)
    assert len(out) == 1


def test_apply_candidate_filter_noop_without_filters():
    """필터 파라미터 미지정 시 순서·내용 완전 불변(filter_applied 필드도 안 붙음)."""
    from kifrs import mcp_server

    hits = [{"section": "x", "appendix": "BC"}]
    out = mcp_server._apply_candidate_filter(hits, section=None, exclude_bc=False, limit=10)
    assert out == hits
    assert "filter_applied" not in out[0]


def test_mcp_server_search_default_unaffected_by_new_filter_params():
    """기존 호출부(파라미터 미지정) 는 완전 불변 — section/exclude_bc 기본값 None/False."""
    from kifrs import mcp_server

    via_default = mcp_server.search("금융자산 분류", limit=5, mode="reranked")
    via_explicit_none = mcp_server.search(
        "금융자산 분류", limit=5, mode="reranked", section=None, exclude_bc=False
    )
    assert via_default == via_explicit_none


def test_mcp_server_search_section_filter_only_returns_matching_section():
    from kifrs import mcp_server

    results = mcp_server.search("유형자산 공시", limit=10, mode="hybrid", section="공시")
    assert results
    assert all("공시" in (r.get("section") or "") for r in results)
    assert all(r.get("filter_applied") for r in results)


def test_mcp_server_search_exclude_bc_removes_bc_hits():
    from kifrs import mcp_server

    results = mcp_server.search("공정가치", limit=10, mode="hybrid", exclude_bc=True)
    assert all(r.get("appendix") != "BC" for r in results)
