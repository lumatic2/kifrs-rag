from __future__ import annotations

from scripts.client_private_local_parser_real_adapter_implementation_plan import (
    REPORT_PATH,
    check_real_adapter_implementation_plan,
    render_plan,
    render_report,
)


def test_real_adapter_implementation_plan_exists_and_names_preconditions() -> None:
    result = check_real_adapter_implementation_plan()

    assert result["ok"], result["errors"]
    assert result["operator_runbook_ok"] is True
    assert "actual accountant feedback evidence" in result["required_preconditions"]
    assert "explicit user authorization" in result["required_preconditions"]
    assert "local quarantine path preflight" in result["implementation_slices"]
    assert "private embeddings" in result["forbidden_until_separate_gate"]


def test_real_adapter_implementation_plan_text_keeps_public_safe_boundary() -> None:
    markdown = REPORT_PATH.read_text(encoding="utf-8")

    assert "local ephemeral quarantine" in markdown
    assert "structured facts only" in markdown
    assert "no raw private file in public artifacts" in markdown
    assert "no OCR text in public artifacts" in markdown
    assert "delete quarantined files before report write" in markdown
    assert "no private embeddings before a separate namespace gate" in markdown
    assert "quality_preflight" in markdown
    assert "Real adapter coding is still not authorized" in markdown


def test_real_adapter_implementation_plan_renderers_are_public_safe() -> None:
    result = check_real_adapter_implementation_plan()

    plan = render_plan(result)
    report = render_report(result)

    assert "LPIP1 Local Parser Real-Adapter Implementation Plan" in plan
    assert "LPIP1 Local Parser Real-Adapter Implementation Plan Gate" in report
    assert "api_key" not in plan
    assert "token" not in plan
    assert "api_key" not in report
    assert "token" not in report
