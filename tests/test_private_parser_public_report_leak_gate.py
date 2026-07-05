from __future__ import annotations

from scripts.private_parser_public_report_leak_gate import build_public_report_leak_gate, render_markdown


def test_private_parser_public_report_leak_gate_scans_reports_and_uses_synthetic_negative_cases() -> None:
    gate = build_public_report_leak_gate()

    assert gate["ok"] is True
    assert gate["horizon"] == "private-parser-realism-hardening"
    assert gate["completed_milestone"] == "PPR4"
    assert gate["next_leaf"] == "PPR5_horizon_close_and_source_connector_handoff"
    assert gate["hits"] == []
    assert all(case["real_payload"] is False for case in gate["negative_cases"])
    assert gate["blocked_marker_count"] >= 6


def test_private_parser_public_report_leak_gate_markdown_is_public_safe() -> None:
    rendered = render_markdown(build_public_report_leak_gate())

    assert "PPR4 Parser Leak And Public Report Gate" in rendered
    assert "synthetic negative cases" in rendered
    assert "Real Payload" in rendered
    assert "api_key" not in rendered
    assert "token" not in rendered
    assert "kifrs.db" not in rendered
    assert "source_body" not in rendered
