from __future__ import annotations

from pathlib import Path

from scripts.client_private_local_parser_operator_runbook import (
    check_local_parser_operator_runbook,
    check_required_reports,
    operator_runbook_steps,
    render_report,
)


def test_local_parser_operator_runbook_passes_current_chain() -> None:
    result = check_local_parser_operator_runbook()

    assert result["ok"], result["errors"]
    assert result["missing_reports"] == []
    assert all(result["subchecks"].values())
    assert len(result["steps"]) == 6


def test_local_parser_operator_runbook_order_is_explicit() -> None:
    steps = operator_runbook_steps()

    assert [step.step_id for step in steps] == [
        "LPOR1-1",
        "LPOR1-2",
        "LPOR1-3",
        "LPOR1-4",
        "LPOR1-5",
        "LPOR1-6",
    ]
    assert "upload_storage_policy" in steps[0].command
    assert "adapter_scaffold" in steps[4].command
    assert "quality_preflight" in steps[5].command


def test_local_parser_operator_runbook_detects_missing_reports() -> None:
    present, missing = check_required_reports({"missing": Path("does-not-exist-local-parser-report.md")})

    assert present == []
    assert missing == ["missing"]


def test_local_parser_operator_runbook_report_states_stop_conditions() -> None:
    rendered = render_report(check_local_parser_operator_runbook())

    assert "LPOR1 Local Parser Operator Runbook" in rendered
    assert "Run Order" in rendered
    assert "Stop Conditions" in rendered
    assert "structured-facts-only-public-safe" in rendered
    assert "pre-parser operator gate only" in rendered


def test_local_parser_operator_runbook_report_distinguishes_not_implemented() -> None:
    rendered = render_report(check_local_parser_operator_runbook())

    assert "Still Not Implemented" in rendered
    assert "real private document parsing" in rendered
    assert "does not authorize real file upload" in rendered
