from __future__ import annotations

from pathlib import Path

from scripts.client_private_local_parser_real_adapter_decision_gate import (
    check_real_adapter_decision_gate,
    render_report,
)


def test_real_adapter_decision_gate_defers_by_default() -> None:
    result = check_real_adapter_decision_gate()

    assert result["ok"], result["errors"]
    assert result["decision"]["decision"] == "defer"
    assert result["decision"]["allowed_to_implement"] is False
    assert result["decision"]["operator_runbook_ok"] is True
    assert result["decision"]["implementation_plan_present"] is True
    blockers = " ".join(result["decision"]["blockers"])
    assert "actual accountant feedback evidence" in blockers
    assert "explicit user authorization" in blockers
    assert "implementation plan" not in blockers
    assert result["next_leaf"] == (
        "real-accountant-session RS2/RS3 evidence capture, then explicit authorization before real adapter coding"
    )


def test_real_adapter_decision_gate_still_detects_missing_plan(tmp_path: Path) -> None:
    result = check_real_adapter_decision_gate(implementation_plan=tmp_path / "missing-plan.md")

    assert result["ok"], result["errors"]
    assert result["decision"]["decision"] == "defer"
    assert result["decision"]["implementation_plan_present"] is False
    blockers = " ".join(result["decision"]["blockers"])
    assert "implementation plan" in blockers
    assert result["next_leaf"] == "local parser real-adapter implementation plan"


def test_real_adapter_decision_gate_can_proceed_when_all_preconditions_are_met(tmp_path: Path) -> None:
    plan_path = tmp_path / "real-adapter-plan.md"
    plan_path.write_text("# Real adapter plan\n", encoding="utf-8")

    result = check_real_adapter_decision_gate(
        explicit_authorization=True,
        implementation_plan=plan_path,
        actual_accountant_evidence_override=True,
    )

    assert result["ok"], result["errors"]
    assert result["decision"]["decision"] == "proceed"
    assert result["decision"]["allowed_to_implement"] is True
    assert result["decision"]["blockers"] == []
    assert result["next_leaf"] == "local parser real-adapter coding"


def test_real_adapter_decision_gate_report_states_no_real_parser_authorization() -> None:
    rendered = render_report(check_real_adapter_decision_gate())

    assert "LPRD1 Local Parser Real-Adapter Decision Gate" in rendered
    assert "Real adapter implementation remains deferred" in rendered
    assert "No real file upload" in rendered
    assert "Still Not Implemented" in rendered


def test_real_adapter_decision_gate_reports_current_session_blockers() -> None:
    result = check_real_adapter_decision_gate()

    assert result["real_accountant_session"]["session_mode"] == "ready_to_schedule"
    assert "reviewer invite has not been sent" in result["real_accountant_session"]["blocked_by"]
