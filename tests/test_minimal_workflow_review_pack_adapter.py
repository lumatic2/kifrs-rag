from __future__ import annotations

from scripts.minimal_workflow_review_pack_adapter import (
    build_minimal_review_pack_adapter,
    render_markdown,
)


def test_minimal_review_pack_adapter_emits_structured_output() -> None:
    result = build_minimal_review_pack_adapter()
    output = result["output"]
    summary = output["structured_summary"]

    assert result["ok"], result["errors"]
    assert result["horizon"] == "workflow-coverage-expansion"
    assert result["completed_milestone"] == "WCE3"
    assert result["workflow_id"] == "1037_provisions"
    assert result["input_mode"] == "structured_local_facts"
    assert summary["recognition_assessment"] == "review_ready"
    assert summary["measurement_summary"] == "estimate_basis_supplied"
    assert "journal entry" in summary["journal_entry_cue"]
    assert output["human_review_checklist"]
    assert output["confidence"] == "medium"
    assert any(role["role"] == "primary_kifrs" for role in summary["authority_panel"])


def test_minimal_review_pack_adapter_marks_missing_required_inputs() -> None:
    result = build_minimal_review_pack_adapter({"obligating_event": "event exists"})

    assert not result["ok"]
    assert "obligation_type" in result["output"]["structured_summary"]["missing_facts"]
    assert result["output"]["confidence"] == "low"


def test_minimal_review_pack_adapter_report_is_public_safe() -> None:
    rendered = render_markdown(build_minimal_review_pack_adapter())

    assert "WCE3 Minimal Review-Pack Adapter" in rendered
    assert "structured review-pack draft" in rendered
    assert "api_key" not in rendered
    assert "token" not in rendered
    assert "source_body" not in rendered
