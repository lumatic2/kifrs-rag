from __future__ import annotations

from kifrs.feedback.case_intake import ClientPrivateDeletionAttestation
from kifrs.runtime.client_private_deletion import (
    build_runtime_client_private_deletion_gate,
    render_runtime_client_private_deletion_gate,
)
from kifrs.runtime.client_private_parser import contract_from_parser_prototype_result
from scripts.client_private_local_parser_adapter_contract_check import check_local_parser_adapter_contract


def _contract_and_attestation():
    prototype = _as_result_object(check_local_parser_adapter_contract()["prototype_result"])
    return contract_from_parser_prototype_result(prototype), prototype.deletion_attestation


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


def test_runtime_client_private_deletion_gate_passes_for_deleted_local_only_state() -> None:
    contract, attestation = _contract_and_attestation()
    gate = build_runtime_client_private_deletion_gate(contract, attestation)

    assert gate.ok is True
    assert gate.deletion_status == "deleted"
    assert gate.deleted_before_report_write is True
    assert gate.raw_file_present is False


def test_runtime_client_private_deletion_gate_blocks_missing_deletion() -> None:
    contract, attestation = _contract_and_attestation()
    bad = ClientPrivateDeletionAttestation(
        **{
            **attestation.to_dict(),
            "deletion_status": "pending",
            "deleted_before_report_write": False,
        }
    )

    gate = build_runtime_client_private_deletion_gate(contract, bad)

    assert gate.ok is False
    assert "deletion_status must be deleted" in gate.errors
    assert "deleted_before_report_write must be true" in gate.errors


def test_runtime_client_private_deletion_gate_blocks_private_artifact_presence() -> None:
    contract, attestation = _contract_and_attestation()
    bad = ClientPrivateDeletionAttestation(
        **{
            **attestation.to_dict(),
            "raw_file_present": True,
            "parsed_body_present": True,
            "ocr_text_present": True,
            "embedding_present": True,
        }
    )

    gate = build_runtime_client_private_deletion_gate(contract, bad)

    assert gate.ok is False
    assert "raw_file_present must be false" in gate.errors
    assert "parsed_body_present must be false" in gate.errors
    assert "ocr_text_present must be false" in gate.errors
    assert "embedding_present must be false" in gate.errors


def test_runtime_client_private_deletion_gate_rendering_is_public_safe() -> None:
    contract, attestation = _contract_and_attestation()
    rendered = render_runtime_client_private_deletion_gate(
        build_runtime_client_private_deletion_gate(contract, attestation)
    )

    assert "Runtime Client-Private Deletion Gate" in rendered
    assert "source_body" not in rendered
    assert "raw_contract" not in rendered
    assert "api_key" not in rendered
    assert "token" not in rendered
