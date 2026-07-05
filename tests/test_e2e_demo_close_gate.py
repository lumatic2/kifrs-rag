from __future__ import annotations

from scripts.e2e_demo_close_gate import build_demo_close_gate, render_markdown


def test_e2e_demo_close_gate_marks_demo_ready() -> None:
    result = build_demo_close_gate()

    assert result["ok"] is True
    assert result["horizon"] == "end-to-end-demo-scenario"
    assert result["completed_milestone"] == "E2E5"
    assert result["close_result"] == "demo_ready"
    assert result["demo_packet"] == "docs/reports/end-to-end-demo/INDEX.md"
    assert result["next_horizon_candidate"] == "demo-rehearsal-or-packaging-readiness"
    assert all(item["exists"] for item in result["evidence"])
    assert all(item["gate_ok"] for item in result["evidence"])


def test_e2e_demo_close_gate_markdown_is_public_safe_and_boundary_explicit() -> None:
    rendered = render_markdown(build_demo_close_gate())

    assert "End-to-End Demo Scenario Close Report" in rendered
    assert "demo_ready" in rendered
    assert "not production packaging" in rendered
    assert "not final accounting judgment" in rendered
    assert "api_key" not in rendered
    assert "token" not in rendered
    assert "kifrs.db" not in rendered
