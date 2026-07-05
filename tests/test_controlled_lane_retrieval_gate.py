from __future__ import annotations

from scripts.controlled_lane_retrieval_gate import (
    build_controlled_lane_retrieval_gate,
    render_markdown,
    retrieve_controlled_chunks,
)


def test_controlled_lane_retrieval_gate_finds_supporting_chunk() -> None:
    gate = build_controlled_lane_retrieval_gate()

    assert gate["ok"], gate["errors"]
    assert gate["completed_milestone"] == "SBI4"
    assert gate["next_leaf"] == "SBI5_controlled_lane_close_gate"
    assert gate["retrieved_count"] >= 1
    assert gate["primary_evidence_preserved"] is True
    assert any("Lease guidance" in item["text"] for item in gate["retrieved"])


def test_controlled_lane_retrieval_marks_supporting_role_only() -> None:
    retrieved = retrieve_controlled_chunks("lease payment pattern")

    assert retrieved
    assert all(item["retrieval_lane"] == "controlled_supporting_interpretation" for item in retrieved)
    assert all(item["citation_role"] == "supporting_interpretation" for item in retrieved)
    assert all(item["primary_evidence_replacement_allowed"] is False for item in retrieved)


def test_controlled_lane_retrieval_returns_empty_for_unrelated_query() -> None:
    retrieved = retrieve_controlled_chunks("unrelated crypto mining tokenomics")

    assert retrieved == []


def test_controlled_lane_retrieval_report_is_public_safe() -> None:
    rendered = render_markdown(build_controlled_lane_retrieval_gate())

    assert "SBI4 Controlled Lane Retrieval Gate" in rendered
    assert "supporting interpretation only" in rendered
    assert "does not change the default retriever" in rendered
    assert "api_key" not in rendered
    assert "token" not in rendered
    assert "source_body" not in rendered
