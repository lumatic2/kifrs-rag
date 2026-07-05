"""Runtime helpers that consume validated ingestion artifacts."""

from .answer_boundary import EvidenceBoundary, PrimaryEvidenceRef, compose_evidence_boundary, render_evidence_boundary
from .authority_boundary import (
    AUTHORITY_ROLES,
    AuthorityRole,
    PrimaryKifrsAuthority,
    RuntimeAuthorityBoundary,
    RuntimeAuthorityReference,
    authority_boundary_references,
    authority_role_for_source_record,
    build_runtime_authority_boundary,
    build_runtime_authority_boundary_from_records,
    is_non_primary_authority_role,
    is_primary_authority_role,
    render_runtime_authority_boundary,
    render_runtime_authority_boundary_data,
)
from .client_private_parser import (
    RuntimeClientPrivateParserContract,
    client_private_contract_to_authority_reference,
    client_private_contracts_to_authority_boundary,
    contract_from_parser_prototype_result,
    render_runtime_client_private_parser_contract,
    validate_runtime_client_private_parser_contract,
)
from .client_private_deletion import (
    RuntimeClientPrivateDeletionGate,
    build_runtime_client_private_deletion_gate,
    render_runtime_client_private_deletion_gate,
)
from .evidence import EvidenceBundle, RuntimeEvidence, load_runtime_evidence
from .evidence_panel import evidence_references, render_external_evidence_panel

__all__ = [
    "AUTHORITY_ROLES",
    "AuthorityRole",
    "EvidenceBundle",
    "EvidenceBoundary",
    "PrimaryEvidenceRef",
    "PrimaryKifrsAuthority",
    "RuntimeAuthorityBoundary",
    "RuntimeAuthorityReference",
    "RuntimeClientPrivateParserContract",
    "RuntimeClientPrivateDeletionGate",
    "RuntimeEvidence",
    "authority_boundary_references",
    "authority_role_for_source_record",
    "build_runtime_authority_boundary",
    "build_runtime_authority_boundary_from_records",
    "build_runtime_client_private_deletion_gate",
    "client_private_contract_to_authority_reference",
    "client_private_contracts_to_authority_boundary",
    "compose_evidence_boundary",
    "contract_from_parser_prototype_result",
    "evidence_references",
    "is_non_primary_authority_role",
    "is_primary_authority_role",
    "load_runtime_evidence",
    "render_evidence_boundary",
    "render_external_evidence_panel",
    "render_runtime_client_private_parser_contract",
    "render_runtime_authority_boundary",
    "render_runtime_authority_boundary_data",
    "render_runtime_client_private_deletion_gate",
    "validate_runtime_client_private_parser_contract",
]
