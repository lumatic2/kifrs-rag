from __future__ import annotations

from scripts.demo_rehearsal_script import build_rehearsal_script, render_markdown


def test_demo_rehearsal_script_defines_stages_and_timing_gate() -> None:
    result = build_rehearsal_script()

    assert result["ok"] is True
    assert result["horizon"] == "demo-rehearsal-quality-loop"
    assert result["completed_milestone"] == "DRQ1"
    assert len(result["stages"]) >= 8
    assert result["total_budget_seconds"] > 0
    assert all(stage["operator_command"] for stage in result["stages"])
    assert all(stage["expected_output"].startswith("docs/reports/") for stage in result["stages"])
    assert result["next_leaf"] == "DRQ2_demo_run_quality_checklist"


def test_demo_rehearsal_script_markdown_is_public_safe() -> None:
    rendered = render_markdown(build_rehearsal_script())

    assert "DRQ1 Demo Rehearsal Script And Timing Gate" in rendered
    assert "Timing Gate" in rendered
    assert "api_key" not in rendered
    assert "secret" not in rendered
    assert "source_body" not in rendered
    assert "packaging" not in rendered.lower()
    assert "external accountant feedback" not in rendered.lower()
