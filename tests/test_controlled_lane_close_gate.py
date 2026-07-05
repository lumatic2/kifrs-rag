from __future__ import annotations

from scripts.controlled_lane_close_gate import build_controlled_lane_close_gate, render_markdown


def test_controlled_lane_close_gate_passes() -> None:
    gate = build_controlled_lane_close_gate()

    assert gate["ok"], gate["errors"]
    assert gate["close_status"] == "closed"
    assert gate["completed_milestone"] == "SBI5"
    assert gate["selected_source_class"] == "interpretive_accounting_material"
    assert gate["implementation_mode"] == "synthetic_body_only"
    assert gate["checks"]["sbi1_source_selection"] is True
    assert gate["checks"]["sbi2_policy_record"] is True
    assert gate["checks"]["sbi3_parser_chunker"] is True
    assert gate["checks"]["sbi4_retrieval_gate"] is True
    assert gate["checks"]["primary_evidence_preserved"] is True
    assert gate["next_horizon"] == "workflow-coverage-expansion"


def test_controlled_lane_close_gate_report_is_public_safe() -> None:
    rendered = render_markdown(build_controlled_lane_close_gate())

    assert "Source Body Ingestion Controlled Lane Close Gate" in rendered
    assert "synthetic-only interpretive lane" in rendered
    assert "workflow-coverage-expansion" in rendered
    assert "api_key" not in rendered
    assert "token" not in rendered
    assert "source_body" not in rendered
