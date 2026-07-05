from __future__ import annotations

from scripts.demo_rehearsal_improvement_close_gate import build_close_gate, render_markdown


def test_demo_rehearsal_improvement_close_gate_closes_horizon() -> None:
    result = build_close_gate()

    assert result["ok"] is True
    assert result["horizon"] == "demo-rehearsal-improvement-hardening"
    assert result["completed_milestone"] == "DRI4"
    assert result["close_result"] == "demo_rehearsal_improvements_hardened"
    assert result["implemented_items"] == ["DRQ4-1", "DRQ4-2", "DRQ4-3"]
    assert result["checks"]["timing_threshold_present"] is True
    assert result["checks"]["freshness_metadata_present"] is True
    assert result["checks"]["operator_summary_present"] is True


def test_demo_rehearsal_improvement_close_gate_markdown_is_public_safe() -> None:
    rendered = render_markdown(build_close_gate())

    assert "Demo Rehearsal Improvement Hardening Close Report" in rendered
    assert "demo_rehearsal_improvements_hardened" in rendered
    assert "DRQ4-1" in rendered
    assert "api_key" not in rendered
    assert "secret" not in rendered
    assert "source_body" not in rendered
    assert "packaging" not in rendered.lower()
    assert "external accountant feedback" not in rendered.lower()
