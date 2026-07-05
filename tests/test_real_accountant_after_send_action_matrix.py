from __future__ import annotations

from scripts.real_accountant_after_send_action_matrix import build_after_send_action_matrix, render_report


def test_after_send_action_matrix_covers_follow_up_schedule_and_decline() -> None:
    matrix = build_after_send_action_matrix()

    assert matrix["ok"], matrix["errors"]
    assert matrix["summary"]["total_rows"] == 3
    assert matrix["summary"]["all_paths_public_safe"] is True
    assert matrix["summary"]["all_status_transitions_match"] is True
    assert matrix["summary"]["all_next_actions_match"] is True

    by_response = {row["response"]: row for row in matrix["rows"]}
    assert by_response["follow_up"]["expected_status"] == "sent"
    assert by_response["schedule"]["expected_status"] == "scheduled"
    assert by_response["decline"]["expected_status"] == "declined"
    assert "invite another reviewer or pause RS2" in by_response["decline"]["next_action"]


def test_after_send_action_matrix_report_is_public_safe() -> None:
    report = render_report(build_after_send_action_matrix())

    assert "follow-up keeps the alias at `sent`" in report
    assert "schedule moves it to `scheduled`" in report
    assert "decline records `declined`" in report
    assert "source_body" not in report
    assert "api_key" not in report
    assert "token" not in report
