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


def test_mcp_server_json_fallback_error_sentinels():
    """Current behavior (pre-CS-3): with USE_SQLITE=False, the search_semantic/
    hybrid/hierarchical/reranked/get_user_notes tools all short-circuit to an
    `[{"error": ...}]` sentinel list instead of raising. This test pins that
    contract so CS-3's structured-error refactor has a known baseline to change."""
    from kifrs import mcp_server

    original = mcp_server.USE_SQLITE
    mcp_server.USE_SQLITE = False
    try:
        for fn, kwargs in [
            (mcp_server.search_semantic, {}),
            (mcp_server.search_hybrid, {}),
            (mcp_server.search_hierarchical, {}),
            (mcp_server.search_reranked, {}),
            (mcp_server.get_user_notes, {}),
        ]:
            result = fn("공정가치", **kwargs)
            assert isinstance(result, list)
            assert len(result) == 1
            assert "error" in result[0]
    finally:
        mcp_server.USE_SQLITE = original


def test_mcp_server_search_lexical_matches_store_search_fts():
    from kifrs import mcp_server

    assert mcp_server.USE_SQLITE is True
    via_tool = mcp_server.search_lexical("자산", limit=5)
    via_store = store.search_fts("자산", limit=5)
    assert via_tool == via_store
