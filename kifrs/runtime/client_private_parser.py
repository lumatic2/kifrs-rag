"""Runtime contract for local-only client-private parser outputs."""
from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any

from kifrs.feedback.case_intake import FORBIDDEN_KEYS, IDENTIFIER_PATTERNS
from kifrs.runtime.authority_boundary import RuntimeAuthorityBoundary


ALLOWED_RUNTIME_DOCUMENT_TYPES = {
    "contract",
    "trial_balance",
    "accounting_policy",
    "workpaper",
    "management_memo",
    "filing_support",
}
ALLOWED_RUNTIME_DOMAINS = {"KIFRS1109", "KIFRS1115", "KIFRS1116"}
ALLOWED_DELETION_POLICIES = {"manual_before_commit", "automatic_after_review"}


@dataclass(frozen=True)
class RuntimeClientPrivateParserContract:
    parser_run_id: str
    source_label: str
    document_type: str
    expected_domain: str
    structured_facts: dict[str, Any] = field(default_factory=dict)
    review_questions: list[str] = field(default_factory=list)
    deletion_policy: str = "manual_before_commit"
    local_only: bool = True
    raw_file_present: bool = False
    parsed_body_present: bool = False
    ocr_text_present: bool = False
    embedding_present: bool = False

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

    def to_runtime_reference_seed(self) -> dict[str, object]:
        validate_runtime_client_private_parser_contract(self)
        return {
            "parser_run_id": self.parser_run_id,
            "source_label": self.source_label,
            "document_type": self.document_type,
            "expected_domain": self.expected_domain,
            "structured_fact_keys": sorted(str(key) for key in self.structured_facts),
            "review_questions": list(self.review_questions),
            "deletion_policy": self.deletion_policy,
            "local_only": self.local_only,
        }


def validate_runtime_client_private_parser_contract(
    contract: RuntimeClientPrivateParserContract,
) -> list[str]:
    errors: list[str] = []
    if not contract.parser_run_id:
        errors.append("parser_run_id is required")
    if not contract.source_label:
        errors.append("source_label is required")
    if contract.document_type not in ALLOWED_RUNTIME_DOCUMENT_TYPES:
        errors.append(f"unsupported document_type: {contract.document_type}")
    if contract.expected_domain not in ALLOWED_RUNTIME_DOMAINS:
        errors.append(f"unsupported expected_domain: {contract.expected_domain}")
    if not contract.structured_facts:
        errors.append("structured_facts are required")
    if not contract.review_questions:
        errors.append("review_questions are required")
    if contract.deletion_policy not in ALLOWED_DELETION_POLICIES:
        errors.append(f"unsupported deletion_policy: {contract.deletion_policy}")
    if contract.local_only is not True:
        errors.append("local_only must be true")
    if contract.raw_file_present:
        errors.append("raw_file_present must be false")
    if contract.parsed_body_present:
        errors.append("parsed_body_present must be false")
    if contract.ocr_text_present:
        errors.append("ocr_text_present must be false")
    if contract.embedding_present:
        errors.append("embedding_present must be false")
    errors.extend(_public_safe_errors(contract.to_dict()))
    return errors


def contract_from_parser_prototype_result(result: Any) -> RuntimeClientPrivateParserContract:
    fixture = result.fixture
    summary = result.redacted_summary
    return RuntimeClientPrivateParserContract(
        parser_run_id=result.parser_run_id,
        source_label=f"{fixture.document_type}:{fixture.fixture_id}",
        document_type=fixture.document_type,
        expected_domain=result.route.domain,
        structured_facts=dict(summary.structured_facts),
        review_questions=[result.route.reason],
        deletion_policy=result.deletion_attestation.deletion_mode,
        local_only=True,
        raw_file_present=result.deletion_attestation.raw_file_present,
        parsed_body_present=result.deletion_attestation.parsed_body_present,
        ocr_text_present=result.deletion_attestation.ocr_text_present,
        embedding_present=result.deletion_attestation.embedding_present,
    )


def render_runtime_client_private_parser_contract(contract: RuntimeClientPrivateParserContract) -> str:
    errors = validate_runtime_client_private_parser_contract(contract)
    lines = [
        f"# Runtime Client-Private Parser Contract - {contract.parser_run_id}",
        "",
        f"- source label: {contract.source_label}",
        f"- document type: {contract.document_type}",
        f"- expected domain: {contract.expected_domain}",
        f"- deletion policy: {contract.deletion_policy}",
        f"- local only: {contract.local_only}",
        "",
        "## Structured Fact Keys",
        "",
    ]
    lines.extend(f"- {key}" for key in sorted(contract.structured_facts))
    lines.extend(["", "## Review Questions", ""])
    lines.extend(f"- {question}" for question in contract.review_questions)
    lines.extend(
        [
            "",
            "## Boundary",
            "",
            "- Runtime contract carries structured facts, source label, review questions, and deletion policy only.",
            "- It does not carry raw files, parsed private body, OCR text, private embeddings, or client identifiers.",
        ]
    )
    if errors:
        lines.extend(["", "## Validation Errors", ""])
        lines.extend(f"- {error}" for error in errors)
    return "\n".join(lines) + "\n"


def client_private_contract_to_authority_reference(
    contract: RuntimeClientPrivateParserContract,
) -> dict[str, object]:
    errors = validate_runtime_client_private_parser_contract(contract)
    if errors:
        joined = "; ".join(errors)
        raise ValueError(f"invalid client-private parser contract: {joined}")
    reference = {
        "authority_role": "client_private_fact",
        "record_id": contract.parser_run_id,
        "record_type": "client_private_fact",
        "source_id": "client-private-local",
        "source_class": "client_private",
        "citation_role": "collection_seed",
        "authority_level": "client_private",
        "retrieval_lane": "local_private_fact",
        "body_storage_policy": "no_store_handoff",
        "locator": {
            "type": "local_private_runtime_contract",
            "label": contract.source_label,
        },
        "label": contract.source_label,
        "public_safe": True,
        "safe_facets": {
            "document_type": contract.document_type,
            "expected_domain": contract.expected_domain,
            "structured_fact_keys": sorted(str(key) for key in contract.structured_facts),
            "review_question_count": len(contract.review_questions),
            "deletion_policy": contract.deletion_policy,
            "local_only": contract.local_only,
        },
    }
    public_errors = _public_safe_errors(reference)
    if public_errors:
        joined = "; ".join(public_errors)
        raise ValueError(f"client-private authority reference is not public-safe: {joined}")
    return reference


def client_private_contracts_to_authority_boundary(
    contracts: list[RuntimeClientPrivateParserContract],
    primary_citations: list[str] | None = None,
) -> RuntimeAuthorityBoundary:
    primary_refs = [
        {
            "authority_role": "primary_kifrs_evidence",
            "citation": citation,
            "label": "K-IFRS primary evidence",
            "source_id": "kifrs-primary",
        }
        for citation in (primary_citations or [])
    ]
    private_refs = [client_private_contract_to_authority_reference(contract) for contract in contracts]
    return RuntimeAuthorityBoundary(
        primary_kifrs_evidence=primary_refs,
        client_private_fact=private_refs,
    )


def _public_safe_errors(value: Any, path: str = "$") -> list[str]:
    errors: list[str] = []
    if isinstance(value, dict):
        for key, nested in value.items():
            key_path = f"{path}.{key}"
            if str(key) in FORBIDDEN_KEYS:
                errors.append(f"{key_path}: forbidden protected-data field")
            errors.extend(_public_safe_errors(nested, key_path))
    elif isinstance(value, list):
        for index, nested in enumerate(value):
            errors.extend(_public_safe_errors(nested, f"{path}[{index}]"))
    elif isinstance(value, str):
        if value in FORBIDDEN_KEYS:
            errors.append(f"{path}: forbidden protected-data marker")
        for pattern in IDENTIFIER_PATTERNS:
            if pattern.search(value):
                errors.append(f"{path}: possible customer identifier")
    return errors


__all__ = [
    "RuntimeClientPrivateParserContract",
    "client_private_contract_to_authority_reference",
    "client_private_contracts_to_authority_boundary",
    "contract_from_parser_prototype_result",
    "render_runtime_client_private_parser_contract",
    "validate_runtime_client_private_parser_contract",
]
