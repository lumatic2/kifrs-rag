from __future__ import annotations

from kifrs.runtime.client_private_parser import (
    client_private_contract_to_authority_reference,
    client_private_contracts_to_authority_boundary,
    contract_from_parser_prototype_result,
)
from kifrs.workflows.kifrs1116.fixtures import FIXTURES
from kifrs.workflows.kifrs1116.review_pack import generate_review_pack, render_review_pack_markdown
from kifrs.workflows.statement_draft import from_1116_review_pack
from scripts.client_private_local_parser_adapter_contract_check import check_local_parser_adapter_contract


def _contract():
    prototype = check_local_parser_adapter_contract()["prototype_result"]
    return contract_from_parser_prototype_result(_as_result_object(prototype))


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


def test_client_private_contract_to_authority_reference_is_private_only() -> None:
    reference = client_private_contract_to_authority_reference(_contract())

    assert reference["authority_role"] == "client_private_fact"
    assert reference["authority_level"] == "client_private"
    assert reference["body_storage_policy"] == "no_store_handoff"
    assert reference["retrieval_lane"] == "local_private_fact"
    assert reference["safe_facets"]["structured_fact_keys"] == ["lease_term", "party", "payment_schedule"]
    assert "structured_facts" not in reference


def test_client_private_authority_boundary_renders_in_review_pack() -> None:
    boundary = client_private_contracts_to_authority_boundary([_contract()], primary_citations=["[1116-53]"])
    pack = generate_review_pack(FIXTURES[0].txn, authority_boundary=boundary)
    rendered = render_review_pack_markdown(pack)

    assert "### Primary K-IFRS evidence" in rendered
    assert "### Client-private fact" in rendered
    assert "client-private-local" in rendered
    assert pack.authority_boundary["client_private_fact"][0]["authority_role"] == "client_private_fact"
    assert pack.authority_boundary["primary_kifrs_evidence"][0]["source_id"] == "kifrs-primary"


def test_client_private_reference_does_not_become_statement_fact_evidence() -> None:
    boundary = client_private_contracts_to_authority_boundary([_contract()], primary_citations=["[1116-53]"])
    pack = generate_review_pack(FIXTURES[0].txn, authority_boundary=boundary)
    candidates = from_1116_review_pack(pack)

    assert candidates
    assert all(
        ref.get("authority_role") != "client_private_fact"
        for candidate in candidates
        for ref in candidate.evidence_refs
    )
    assert all(
        ref.get("authority_role") != "primary_kifrs_evidence"
        for candidate in candidates
        for ref in candidate.evidence_refs
    )


def test_client_private_authority_reference_is_public_safe() -> None:
    rendered = render_review_pack_markdown(
        generate_review_pack(
            FIXTURES[0].txn,
            authority_boundary=client_private_contracts_to_authority_boundary([_contract()]),
        )
    )

    assert "source_body" not in rendered
    assert "raw_contract" not in rendered
    assert "api_key" not in rendered
    assert "token" not in rendered
