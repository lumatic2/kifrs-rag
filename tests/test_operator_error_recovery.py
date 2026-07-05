from __future__ import annotations

from scripts.operator_error_recovery import build_operator_error_recovery, render_markdown


def test_operator_error_recovery_maps_common_failures() -> None:
    result = build_operator_error_recovery()

    assert result["ok"], result["errors"]
    assert result["horizon"] == "operator-experience-hardening"
    assert result["completed_milestone"] == "OEH4"
    case_ids = {item["case_id"] for item in result["cases"]}
    assert {"pytest_failure", "missing_report", "default_retriever_guard_failure", "protected_data_warning"} <= case_ids
    assert result["checks"]["no_destructive_recovery"] is True
    assert result["checks"]["rerun_commands_present"] is True
    assert result["next_gate"] == "operator_experience_close_gate"


def test_operator_error_recovery_report_is_public_safe() -> None:
    rendered = render_markdown(build_operator_error_recovery())

    assert "OEH4 Error Recovery Playbook" in rendered
    assert "without destructive cleanup" in rendered
    assert "api_key" not in rendered
    assert "token" not in rendered
    assert "source_body" not in rendered
