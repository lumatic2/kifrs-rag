from __future__ import annotations

from scripts.client_private_close_gate import render_close_report, run_client_private_close_gate


def test_client_private_close_gate_passes_without_quality_preflight() -> None:
    result = run_client_private_close_gate()

    assert result["ok"], result["errors"]
    assert result["checks"]["contract"]["ok"] is True
    assert result["checks"]["redaction"]["ok"] is True
    assert result["checks"]["routing"]["ok"] is True
    assert result["checks"]["readiness"]["ok"] is True


def test_client_private_close_report_states_remaining_boundaries() -> None:
    rendered = render_close_report(run_client_private_close_gate())

    assert "CP4 Client-Private Close Report" in rendered
    assert "does not implement upload" in rendered
    assert "private document parsing" in rendered
    assert "Route redacted structured facts" in rendered
