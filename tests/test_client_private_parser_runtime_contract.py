from __future__ import annotations

from kifrs.runtime.client_private_parser import (
    RuntimeClientPrivateParserContract,
    contract_from_parser_prototype_result,
    render_runtime_client_private_parser_contract,
    validate_runtime_client_private_parser_contract,
)
from scripts.client_private_local_parser_adapter_contract_check import (
    check_local_parser_adapter_contract,
)


def test_runtime_client_private_parser_contract_from_prototype_result() -> None:
    prototype = check_local_parser_adapter_contract()["prototype_result"]
    contract = contract_from_parser_prototype_result(_as_result_object(prototype))

    assert validate_runtime_client_private_parser_contract(contract) == []
    assert contract.local_only is True
    assert contract.raw_file_present is False
    assert contract.parsed_body_present is False
    assert contract.ocr_text_present is False
    assert contract.embedding_present is False
    seed = contract.to_runtime_reference_seed()
    assert seed["structured_fact_keys"] == ["lease_term", "party", "payment_schedule"]
    assert "structured_facts" not in seed


def test_runtime_client_private_parser_contract_rejects_body_like_fields() -> None:
    contract = RuntimeClientPrivateParserContract(
        parser_run_id="bad",
        source_label="contract:bad",
        document_type="contract",
        expected_domain="KIFRS1116",
        structured_facts={"raw_contract": "copied private text"},
        review_questions=["review lease term"],
    )

    errors = validate_runtime_client_private_parser_contract(contract)

    assert any("raw_contract" in error for error in errors)


def test_runtime_client_private_parser_contract_rejects_private_artifacts() -> None:
    contract = RuntimeClientPrivateParserContract(
        parser_run_id="bad",
        source_label="contract:bad",
        document_type="contract",
        expected_domain="KIFRS1116",
        structured_facts={"party": "lessee"},
        review_questions=["review lease term"],
        raw_file_present=True,
        parsed_body_present=True,
        ocr_text_present=True,
        embedding_present=True,
    )

    errors = validate_runtime_client_private_parser_contract(contract)

    assert "raw_file_present must be false" in errors
    assert "parsed_body_present must be false" in errors
    assert "ocr_text_present must be false" in errors
    assert "embedding_present must be false" in errors


def test_runtime_client_private_parser_contract_rendering_is_public_safe() -> None:
    prototype = check_local_parser_adapter_contract()["prototype_result"]
    contract = contract_from_parser_prototype_result(_as_result_object(prototype))
    rendered = render_runtime_client_private_parser_contract(contract)

    assert "Runtime Client-Private Parser Contract" in rendered
    assert "Structured Fact Keys" in rendered
    assert "source_body" not in rendered
    assert "raw_contract" not in rendered
    assert "api_key" not in rendered
    assert "token" not in rendered


def _as_result_object(data: dict[str, object]):
    from kifrs.feedback.case_intake import (
        ClientPrivateDeletionAttestation,
        ClientPrivateParserDryRunFixture,
        RedactedClientPrivateSummary,
        RoutingCandidate,
    )
    from kifrs.feedback.local_parser import LocalPrivateParserPrototypeResult

    return LocalPrivateParserPrototypeResult(
        parser_run_id=str(data["parser_run_id"]),
        fixture=ClientPrivateParserDryRunFixture(**data["fixture"]),
        redacted_summary=RedactedClientPrivateSummary(**data["redacted_summary"]),
        route=RoutingCandidate(**data["route"]),
        deletion_attestation=ClientPrivateDeletionAttestation(**data["deletion_attestation"]),
    )
