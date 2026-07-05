from __future__ import annotations

from scripts.demo_rehearsal_quality_close_gate import build_close_gate, render_markdown


def test_demo_rehearsal_quality_close_gate_closes_horizon() -> None:
    result = build_close_gate()

    assert result["ok"] is True
    assert result["horizon"] == "demo-rehearsal-quality-loop"
    assert result["completed_milestone"] == "DRQ5"
    assert result["close_result"] == "demo_rehearsal_quality_loop_closed"
    assert result["next_leaf"] == "objective_gap_queue_complete"
    assert result["checks"]["all_evidence_exists"] is True
    assert result["checks"]["all_required_phrases_present"] is True
    assert result["checks"]["objective_gap_queue_closed"] is True
    assert {item["status"] for item in result["objective_gap_status"]} == {"closed"}


def test_demo_rehearsal_quality_close_gate_markdown_is_public_safe() -> None:
    rendered = render_markdown(build_close_gate())

    assert "Demo Rehearsal Quality Loop Close Report" in rendered
    assert "demo_rehearsal_quality_loop_closed" in rendered
    assert "objective_gap_queue_complete" in rendered
    assert "api_key" not in rendered
    assert "secret" not in rendered
    assert "source_body" not in rendered
    assert "packaging" not in rendered.lower()
    assert "external accountant feedback" not in rendered.lower()
