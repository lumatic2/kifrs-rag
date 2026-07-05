from __future__ import annotations

from scripts.demo_run_quality_checklist import build_quality_checklist, render_markdown


def test_demo_run_quality_checklist_has_failure_and_recovery_per_stage() -> None:
    result = build_quality_checklist()

    assert result["ok"] is True
    assert result["horizon"] == "demo-rehearsal-quality-loop"
    assert result["completed_milestone"] == "DRQ2"
    assert result["source_stage_count"] >= 8
    assert all(item["pass_checks"] for item in result["stage_checks"])
    assert all(item["failure_note"] for item in result["stage_checks"])
    assert all(item["recovery_route"] for item in result["stage_checks"])
    assert result["checks"]["has_timing_check"] is True
    assert result["next_leaf"] == "DRQ3_rehearsal_evidence_capture"


def test_demo_run_quality_checklist_markdown_is_public_safe() -> None:
    rendered = render_markdown(build_quality_checklist())

    assert "DRQ2 Demo Run Quality Checklist" in rendered
    assert "failure note" in rendered.lower()
    assert "api_key" not in rendered
    assert "secret" not in rendered
    assert "source_body" not in rendered
    assert "packaging" not in rendered.lower()
    assert "external accountant feedback" not in rendered.lower()
