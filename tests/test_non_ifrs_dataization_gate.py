from __future__ import annotations

from scripts.non_ifrs_dataization_gate import build_gate, render_close_markdown, render_gate_markdown


def test_non_ifrs_dataization_gate_hands_off_to_runtime_horizon() -> None:
    gate = build_gate()

    assert gate["ok"], gate["errors"]
    assert gate["milestone"] == "NIS5"
    assert gate["next_horizon"] == "multi-authority-runtime-hardening"
    assert all(row["exists"] for row in gate["required_reports"])
    assert gate["records_snapshot"]["total"] == 4
    assert gate["chunking_snapshot"]["total_lanes"] == 4
    assert gate["default_guard_snapshot"]["default_mode"] == "hybrid"
    assert gate["default_guard_snapshot"]["promote_to_default"] is False


def test_non_ifrs_dataization_gate_markdown_is_actionable() -> None:
    gate = build_gate()
    rendered = render_gate_markdown(gate)
    close_rendered = render_close_markdown(gate)

    assert "NIS5 Dataization Gate" in rendered
    assert "Regression Commands" in rendered
    assert "multi-authority-runtime-hardening" in rendered
    assert "Non-IFRS Source Dataization Close Report" in close_rendered
    assert "api_key" not in rendered
    assert "token" not in rendered
    assert "source_body" not in rendered
