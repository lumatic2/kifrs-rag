"""Shared runtime boundary for primary and non-IFRS authority evidence."""
from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import Any

from kifrs.ingestion.manifest import FORBIDDEN_MANIFEST_FIELDS
from kifrs.ingestion.source_record import (
    load_records,
    validate_source_records,
)


ROOT = Path(__file__).resolve().parents[2]
DEFAULT_SOURCE_RECORDS_PATH = ROOT / "docs" / "ingestion" / "non_ifrs_source_records.example.json"

class AuthorityRole(str, Enum):
    PRIMARY_KIFRS_EVIDENCE = "primary_kifrs_evidence"
    SUPPORTING_INTERPRETATION = "supporting_interpretation"
    LEGAL_BOUNDARY = "legal_boundary"
    FACT_EVIDENCE = "fact_evidence"
    CLIENT_PRIVATE_FACT = "client_private_fact"


AUTHORITY_ROLES = tuple(role.value for role in AuthorityRole)


@dataclass(frozen=True)
class PrimaryKifrsAuthority:
    citation: str
    label: str = "K-IFRS primary evidence"
    authority_role: str = AuthorityRole.PRIMARY_KIFRS_EVIDENCE.value

    def to_reference_dict(self) -> dict[str, object]:
        return {
            "authority_role": self.authority_role,
            "citation": self.citation,
            "label": self.label,
            "source_id": "kifrs-primary",
        }


@dataclass(frozen=True)
class RuntimeAuthorityReference:
    authority_role: str
    record_id: str
    record_type: str
    source_id: str
    source_class: str
    citation_role: str
    authority_level: str
    retrieval_lane: str
    body_storage_policy: str
    locator: dict[str, Any]
    label: str
    public_safe: bool
    safe_facets: dict[str, Any] = field(default_factory=dict)

    def to_reference_dict(self) -> dict[str, object]:
        reference = {
            "authority_role": self.authority_role,
            "record_id": self.record_id,
            "record_type": self.record_type,
            "source_id": self.source_id,
            "source_class": self.source_class,
            "citation_role": self.citation_role,
            "authority_level": self.authority_level,
            "retrieval_lane": self.retrieval_lane,
            "body_storage_policy": self.body_storage_policy,
            "locator": dict(self.locator),
            "label": self.label,
            "public_safe": self.public_safe,
        }
        if self.safe_facets:
            reference["safe_facets"] = dict(self.safe_facets)
        _raise_forbidden_reference_fields(reference)
        return reference


@dataclass(frozen=True)
class RuntimeAuthorityBoundary:
    primary_kifrs_evidence: list[dict[str, object]] = field(default_factory=list)
    supporting_interpretation: list[dict[str, object]] = field(default_factory=list)
    legal_boundary: list[dict[str, object]] = field(default_factory=list)
    fact_evidence: list[dict[str, object]] = field(default_factory=list)
    client_private_fact: list[dict[str, object]] = field(default_factory=list)

    def to_dict(self) -> dict[str, list[dict[str, object]]]:
        return {
            "primary_kifrs_evidence": list(self.primary_kifrs_evidence),
            "supporting_interpretation": list(self.supporting_interpretation),
            "legal_boundary": list(self.legal_boundary),
            "fact_evidence": list(self.fact_evidence),
            "client_private_fact": list(self.client_private_fact),
        }


def build_runtime_authority_boundary(
    primary_citations: list[str] | None = None,
    source_records_path: Path = DEFAULT_SOURCE_RECORDS_PATH,
) -> RuntimeAuthorityBoundary:
    return build_runtime_authority_boundary_from_records(
        records=load_records(source_records_path),
        primary_citations=primary_citations,
    )


def build_runtime_authority_boundary_from_records(
    records: list[dict[str, Any]],
    primary_citations: list[str] | None = None,
) -> RuntimeAuthorityBoundary:
    validation = validate_source_records(records)
    if not validation["ok"]:
        joined = "; ".join(validation["errors"])
        raise ValueError(f"invalid runtime source records: {joined}")

    groups: dict[str, list[dict[str, object]]] = {role: [] for role in AUTHORITY_ROLES}
    for citation in primary_citations or []:
        groups["primary_kifrs_evidence"].append(
            PrimaryKifrsAuthority(citation=citation).to_reference_dict()
        )
    for record in records:
        reference = _source_record_to_reference(record).to_reference_dict()
        groups[str(reference["authority_role"])].append(reference)

    return RuntimeAuthorityBoundary(**groups)


def authority_boundary_references(boundary: RuntimeAuthorityBoundary | None) -> dict[str, list[dict[str, object]]]:
    if boundary is None:
        return {}
    return boundary.to_dict()


def render_runtime_authority_boundary(boundary: RuntimeAuthorityBoundary) -> str:
    return render_runtime_authority_boundary_data(boundary.to_dict())


def render_runtime_authority_boundary_data(data: dict[str, list[dict[str, object]]]) -> str:
    labels = {
        "primary_kifrs_evidence": "Primary K-IFRS evidence",
        "supporting_interpretation": "Supporting interpretation",
        "legal_boundary": "Legal boundary",
        "fact_evidence": "Fact evidence",
        "client_private_fact": "Client-private fact",
    }
    lines = ["## Runtime Authority Boundary"]
    for role in AUTHORITY_ROLES:
        items = data.get(role, [])
        lines.append(f"### {labels[role]}")
        if not items:
            lines.append("- 없음")
            continue
        for item in items:
            if role == "primary_kifrs_evidence":
                lines.append(f"- {item['citation']} ({item['label']})")
            else:
                lines.append(
                    "- "
                    f"{item['label']} "
                    f"[{item['authority_role']}] "
                    f"`{item['source_id']}` / `{item['record_id']}`"
                )
    return "\n".join(lines)


def _source_record_to_reference(record: dict[str, Any]) -> RuntimeAuthorityReference:
    return RuntimeAuthorityReference(
        authority_role=_authority_role(record),
        record_id=str(record["record_id"]),
        record_type=str(record["record_type"]),
        source_id=str(record["source_id"]),
        source_class=str(record["source_class"]),
        citation_role=str(record["citation_role"]),
        authority_level=str(record["authority_level"]),
        retrieval_lane=str(record["retrieval_lane"]),
        body_storage_policy=str(record["body_storage_policy"]),
        locator=dict(record["locator"]),
        label=_reference_label(record),
        public_safe=record.get("public_safe") is True,
        safe_facets=_safe_facets(record),
    )


def _authority_role(record: dict[str, Any]) -> str:
    if record.get("record_type") == "client_private_fact":
        return AuthorityRole.CLIENT_PRIVATE_FACT.value
    citation_role = str(record.get("citation_role"))
    if citation_role in {
        AuthorityRole.SUPPORTING_INTERPRETATION.value,
        AuthorityRole.LEGAL_BOUNDARY.value,
        AuthorityRole.FACT_EVIDENCE.value,
    }:
        return citation_role
    raise ValueError(f"unsupported source record citation role: {citation_role}")


def authority_role_for_source_record(record: dict[str, Any]) -> str:
    """Return the non-primary runtime role for a validated source record."""
    return _authority_role(record)


def is_primary_authority_role(role: str) -> bool:
    return role == AuthorityRole.PRIMARY_KIFRS_EVIDENCE.value


def is_non_primary_authority_role(role: str) -> bool:
    return role in AUTHORITY_ROLES and not is_primary_authority_role(role)


def _reference_label(record: dict[str, Any]) -> str:
    record_type = record.get("record_type")
    if record_type == "document_metadata":
        return str(record.get("title", record["record_id"]))
    if record_type == "law_locator":
        return str(record.get("law_name", record["record_id"]))
    if record_type == "structured_fact":
        return str(record.get("line_item", record["record_id"]))
    if record_type == "client_private_fact":
        return str(record.get("fact_label", record["record_id"]))
    return str(record["record_id"])


def _safe_facets(record: dict[str, Any]) -> dict[str, Any]:
    record_type = record.get("record_type")
    if record_type == "document_metadata":
        return {
            "publisher": record.get("publisher"),
            "document_type": record.get("document_type"),
            "topics": list(record.get("topics", [])),
            "chunk_strategy": record.get("chunk_strategy"),
        }
    if record_type == "law_locator":
        return {
            "article_locator": record.get("article_locator"),
            "official_registry": record.get("official_registry"),
            "topics": list(record.get("topics", [])),
            "chunk_strategy": record.get("chunk_strategy"),
        }
    if record_type == "structured_fact":
        return {
            "company_id": record.get("company_id"),
            "filing_id": record.get("filing_id"),
            "period": record.get("period"),
            "statement_type": record.get("statement_type"),
            "line_item": record.get("line_item"),
            "value": record.get("value"),
            "unit": record.get("unit"),
            "dimensions": dict(record.get("dimensions", {})),
            "quality_flags": list(record.get("quality_flags", [])),
        }
    if record_type == "client_private_fact":
        return {
            "case_scope": record.get("case_scope"),
            "fact_label": record.get("fact_label"),
            "fact_kind": record.get("fact_kind"),
            "private_storage_boundary": record.get("private_storage_boundary"),
            "deletion_policy": record.get("deletion_policy"),
        }
    return {}


def _raise_forbidden_reference_fields(reference: dict[str, Any]) -> None:
    hits = _find_forbidden_reference_fields(reference)
    if hits:
        joined = ", ".join(hits)
        raise ValueError(f"runtime authority reference contains forbidden fields: {joined}")


def _find_forbidden_reference_fields(value: Any, path: str = "$") -> list[str]:
    hits: list[str] = []
    if isinstance(value, dict):
        for key, nested in value.items():
            key_path = f"{path}.{key}"
            if str(key).lower() in FORBIDDEN_MANIFEST_FIELDS or str(key).lower() == "record":
                hits.append(key_path)
            hits.extend(_find_forbidden_reference_fields(nested, key_path))
    elif isinstance(value, list):
        for idx, nested in enumerate(value):
            hits.extend(_find_forbidden_reference_fields(nested, f"{path}[{idx}]"))
    return hits


__all__ = [
    "AUTHORITY_ROLES",
    "AuthorityRole",
    "RuntimeAuthorityBoundary",
    "RuntimeAuthorityReference",
    "PrimaryKifrsAuthority",
    "authority_boundary_references",
    "authority_role_for_source_record",
    "build_runtime_authority_boundary",
    "build_runtime_authority_boundary_from_records",
    "is_non_primary_authority_role",
    "is_primary_authority_role",
    "render_runtime_authority_boundary",
    "render_runtime_authority_boundary_data",
]
