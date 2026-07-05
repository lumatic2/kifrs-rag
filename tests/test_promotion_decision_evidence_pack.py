from __future__ import annotations

from scripts.promotion_decision_evidence_pack import build_evidence_pack, render_markdown


def test_promotion_decision_evidence_pack_defers_without_authorization() -> None:
    pack = build_evidence_pack()

    assert pack["ok"] is True
    assert pack["decision"] == "defer"
    assert pack["promote_to_default"] is False
    assert "explicit promotion authorization is absent" in pack["blockers"]
    assert pack["current_default"] == "hybrid"


def test_promotion_decision_evidence_pack_links_quality_guard_and_failures() -> None:
    pack = build_evidence_pack()

    assert pack["evidence"]["rag_quality_ok"] is True
    assert pack["evidence"]["default_guard_ok"] is True
    assert pack["evidence"]["failure_matrix_ok"] is True
    assert "default_promotion" in pack["evidence"]["failure_categories"]


def test_promotion_decision_evidence_pack_report_is_public_safe() -> None:
    rendered = render_markdown(build_evidence_pack())

    assert "Default retriever promotion remains deferred" in rendered
    assert "explicit authorization" in rendered
    assert "api_key" not in rendered
    assert "source_body" not in rendered
