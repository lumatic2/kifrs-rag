from __future__ import annotations

from scripts.real_accountant_close_state_matrix import build_close_state_matrix, render_report


def test_close_state_matrix_only_closes_actual_feedback_completed() -> None:
    matrix = build_close_state_matrix()

    assert matrix["ok"], matrix["errors"]
    assert matrix["summary"]["total_rows"] == 8
    assert matrix["summary"]["passing_close_rows"] == 1
    assert matrix["summary"]["blocked_rows"] == 7
    assert matrix["summary"]["only_actual_feedback_completed_closes"] is True

    close_rows = [row for row in matrix["rows"] if row["close_ready"]]
    assert close_rows == [
        {
            **close_rows[0],
            "manifest_mode": "actual_feedback",
            "outreach_state": "completed",
            "expected_close": True,
            "close_ready": True,
        }
    ]


def test_close_state_matrix_report_names_blockers_without_protected_markers() -> None:
    report = render_report(build_close_state_matrix())

    assert "manifest_not_actual_feedback" in report
    assert "no_completed_outreach" in report
    assert "actual_feedback | completed | True | True | none" in report
    assert "source_body" not in report
    assert "api_key" not in report
    assert "token" not in report
