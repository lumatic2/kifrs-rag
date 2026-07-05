from __future__ import annotations

from kifrs.feedback import (
    LocalPrivateParserAdapterDryRunCase,
    render_local_private_parser_adapter_dry_run_gate,
    run_local_private_parser_adapter_dry_run_gate,
    validate_local_private_parser_adapter_dry_run_case,
)
from scripts.client_private_local_parser_adapter_contract_check import default_adapter_contract
from scripts.client_private_local_parser_adapter_dry_run_gate import (
    check_local_parser_adapter_dry_run_gate,
    default_dry_run_cases,
    render_report,
)
from scripts.client_private_upload_storage_policy_check import default_policy


def test_local_parser_adapter_dry_run_gate_passes_batch_cases() -> None:
    result = check_local_parser_adapter_dry_run_gate()

    assert result["ok"], result["errors"]
    assert result["gate"]["case_count"] == 2
    assert len(result["gate"]["passed_case_ids"]) == 2
    assert result["gate"]["failed_case_ids"] == []
    routes = [item["route"]["route"] for item in result["gate"]["prototype_results"]]
    assert routes == ["kifrs1116_review_pack", "kifrs1116_review_pack"]


def test_local_parser_adapter_dry_run_case_requires_contract_fields() -> None:
    dry_run_case = LocalPrivateParserAdapterDryRunCase(
        dry_run_id="missing-payment-schedule",
        source_stub="local-private://dry-run/missing-payment-schedule",
        document_type="contract",
        expected_domain="KIFRS1116",
        extracted_fields={
            "party": "lessee",
            "lease_term": "5 years",
        },
    )

    issues = validate_local_private_parser_adapter_dry_run_case(
        dry_run_case,
        default_adapter_contract(),
        default_policy(),
    )

    assert any(issue.path == "extracted_fields" and "payment_schedule" in issue.message for issue in issues)


def test_local_parser_adapter_dry_run_gate_fails_invalid_case() -> None:
    valid_case = default_dry_run_cases()[0]
    invalid_case = LocalPrivateParserAdapterDryRunCase(
        dry_run_id="bad-source-stub",
        source_stub="file://private/client.pdf",
        document_type="contract",
        expected_domain="KIFRS1116",
        extracted_fields=valid_case.extracted_fields,
    )

    gate = run_local_private_parser_adapter_dry_run_gate(
        "test-gate",
        default_adapter_contract(),
        default_policy(),
        [valid_case, invalid_case],
    )

    assert not gate.ok
    assert gate.passed_case_ids == [valid_case.dry_run_id]
    assert gate.failed_case_ids == [invalid_case.dry_run_id]
    assert any("source_stub" in error for error in gate.errors)


def test_render_local_parser_adapter_dry_run_gate_states_boundary() -> None:
    gate = run_local_private_parser_adapter_dry_run_gate(
        "test-gate",
        default_adapter_contract(),
        default_policy(),
        default_dry_run_cases(),
    )
    rendered = render_local_private_parser_adapter_dry_run_gate(gate)

    assert "synthetic dry-run cases only" in rendered
    assert "does not read files" in rendered
    assert "run OCR" in rendered


def test_local_parser_adapter_dry_run_report_distinguishes_not_implemented() -> None:
    rendered = render_report(check_local_parser_adapter_dry_run_gate())

    assert "LPAD1 Local Parser Adapter Dry-Run Gate" in rendered
    assert "Still Not Implemented" in rendered
    assert "real private document parsing" in rendered
    assert "batch dry-run gate" in rendered
