from __future__ import annotations

from scripts.real_accountant_capture_readiness_gate import check_capture_readiness_gate, render_report


def test_capture_readiness_gate_proves_rs3_path_without_repo_actual_notes() -> None:
    result = check_capture_readiness_gate()

    assert result["ok"], result["errors"]
    simulation = result["simulation"]
    assert simulation["notes_ok"] is True
    assert simulation["capture_manifest_actual"] is True
    assert simulation["queue_records"] == 1
    assert simulation["manifest_mode"] == "actual_feedback"
    assert simulation["close_ready"] is True


def test_capture_readiness_gate_report_keeps_synthetic_boundary_public_safe() -> None:
    report = render_report(check_capture_readiness_gate())

    assert "synthetic public-safe notes" in report
    assert "does not create actual-feedback-notes.md in the repo" in report
    assert "does not mark the real outreach ledger completed" in report
    assert "source_body" not in report
    assert "api_key" not in report
    assert "token" not in report
