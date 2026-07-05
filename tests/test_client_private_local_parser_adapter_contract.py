from __future__ import annotations

import pytest

from kifrs.feedback import (
    LocalPrivateParserAdapterContract,
    contract_to_local_private_parser_prototype_input,
    render_local_private_parser_adapter_contract,
    run_local_private_parser_prototype,
    validate_local_private_parser_adapter_contract,
)
from scripts.client_private_local_parser_adapter_contract_check import (
    check_local_parser_adapter_contract,
    default_adapter_contract,
    default_extracted_fields,
    render_report,
)
from scripts.client_private_upload_storage_policy_check import default_policy


def test_local_parser_adapter_contract_routes_handoff_to_review_pack_candidate() -> None:
    result = check_local_parser_adapter_contract()

    assert result["ok"], result["errors"]
    assert result["route"]["route"] == "kifrs1116_review_pack"
    assert result["route"]["status"] == "candidate"
    assert result["prototype_result"]["deletion_attestation"]["deletion_status"] == "deleted"


def test_local_parser_adapter_contract_rejects_real_file_read_claim() -> None:
    contract = LocalPrivateParserAdapterContract(
        **{
            **default_adapter_contract().to_dict(),
            "reads_real_files": True,
        }
    )

    issues = validate_local_private_parser_adapter_contract(contract, default_policy())

    assert any(issue.path == "reads_real_files" for issue in issues)


def test_local_parser_adapter_contract_requires_forbidden_outputs() -> None:
    contract = LocalPrivateParserAdapterContract(
        **{
            **default_adapter_contract().to_dict(),
            "forbidden_outputs": ["raw private file"],
        }
    )

    issues = validate_local_private_parser_adapter_contract(contract, default_policy())

    assert any(issue.path == "forbidden_outputs" and "OCR text" in issue.message for issue in issues)


def test_local_parser_adapter_contract_rejects_protected_field_names() -> None:
    contract = LocalPrivateParserAdapterContract(
        **{
            **default_adapter_contract().to_dict(),
            "required_extracted_fields": ["party", "lease_term", "payment_schedule", "raw_contract"],
        }
    )

    issues = validate_local_private_parser_adapter_contract(contract, default_policy())

    assert any(issue.path == "required_extracted_fields[3]" for issue in issues)


def test_local_parser_adapter_contract_handoff_builds_prototype_input() -> None:
    policy = default_policy()
    contract = default_adapter_contract()
    prototype_input = contract_to_local_private_parser_prototype_input(
        contract,
        policy,
        parser_run_id="test-contract-handoff",
        source_stub="local-private://dry-run/test-contract-handoff",
        document_type="contract",
        expected_domain="KIFRS1116",
        extracted_fields=default_extracted_fields(),
    )
    result = run_local_private_parser_prototype(prototype_input, policy)

    assert prototype_input.parser_mode == "structured_facts_only"
    assert result.route.status == "candidate"


def test_local_parser_adapter_contract_handoff_rejects_missing_required_field() -> None:
    with pytest.raises(ValueError, match="payment_schedule"):
        contract_to_local_private_parser_prototype_input(
            default_adapter_contract(),
            default_policy(),
            parser_run_id="test-contract-handoff",
            source_stub="local-private://dry-run/test-contract-handoff",
            document_type="contract",
            expected_domain="KIFRS1116",
            extracted_fields={"party": "lessee", "lease_term": "5 years"},
        )


def test_render_local_parser_adapter_contract_states_boundary() -> None:
    rendered = render_local_private_parser_adapter_contract(default_adapter_contract(), default_policy())

    assert "does not read files" in rendered
    assert "run OCR" in rendered
    assert "LocalPrivateParserPrototypeInput" in rendered


def test_local_parser_adapter_contract_report_distinguishes_not_implemented() -> None:
    rendered = render_report(check_local_parser_adapter_contract())

    assert "LPA1 Local Parser Adapter Contract" in rendered
    assert "Still Not Implemented" in rendered
    assert "real private document parsing" in rendered
    assert "fixed public-safe contract" in rendered
