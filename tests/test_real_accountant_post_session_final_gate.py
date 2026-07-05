from __future__ import annotations

from scripts.real_accountant_capture_readiness_gate import _synthetic_actual_notes
from scripts.real_accountant_post_session_final_gate import check_post_session_final_gate, render_report


def test_post_session_final_gate_synthetic_mode_runs_full_flow() -> None:
    result = check_post_session_final_gate()

    assert result["ok"], result["errors"]
    assert result["mode"] == "synthetic_readiness"
    flow = result["result"]
    assert flow["notes_safety_ok"] is True
    assert flow["notes_quality_ok"] is True
    assert flow["queue_records"] == 1
    assert flow["manifest_mode"] == "actual_feedback"
    assert flow["close_ready"] is True


def test_post_session_final_gate_accepts_existing_actual_notes_copy(tmp_path) -> None:
    notes = tmp_path / "actual-feedback-notes.md"
    notes.write_text(_synthetic_actual_notes(), encoding="utf-8")

    result = check_post_session_final_gate(notes=notes)

    assert result["ok"], result["errors"]
    assert result["mode"] == "repo_actual_notes"
    assert result["result"]["queue_records"] == 1


def test_post_session_final_gate_report_keeps_boundary_public_safe() -> None:
    report = render_report(check_post_session_final_gate())

    assert "Synthetic mode writes only to a temporary directory" in report
    assert "The real outreach ledger is not marked completed" in report
    assert "source_body" not in report
    assert "api_key" not in report
    assert "token" not in report
