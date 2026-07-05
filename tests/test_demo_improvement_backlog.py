from __future__ import annotations

from scripts.demo_improvement_backlog import build_improvement_backlog, render_markdown


def test_demo_improvement_backlog_prioritizes_internal_fixes() -> None:
    result = build_improvement_backlog()

    assert result["ok"] is True
    assert result["horizon"] == "demo-rehearsal-quality-loop"
    assert result["completed_milestone"] == "DRQ4"
    assert len(result["findings"]) >= 3
    assert len(result["backlog"]) >= 3
    assert all(item["dependency"] == "internal" for item in result["backlog"])
    assert result["backlog"][0]["priority_score"] >= result["backlog"][-1]["priority_score"]
    assert result["next_leaf"] == "DRQ5_horizon_close_and_objective_gap_audit"


def test_demo_improvement_backlog_markdown_is_public_safe() -> None:
    rendered = render_markdown(build_improvement_backlog())

    assert "DRQ4 Demo Improvement Backlog" in rendered
    assert "internal fixes" in rendered
    assert "api_key" not in rendered
    assert "secret" not in rendered
    assert "source_body" not in rendered
    assert "packaging" not in rendered.lower()
    assert "outreach" not in rendered.lower()
