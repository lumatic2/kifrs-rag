"""Runtime evidence loader for accounting workflow outputs.

The ingestion layer validates that manifests are public-safe. This runtime layer
turns validated manifest records into immutable objects that review packs,
statement draft, and answer rendering can consume without knowing the manifest
file shape.
"""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

from kifrs.ingestion.evidence import (
    DEFAULT_EVIDENCE_PATH,
    load_evidence_manifest,
    validate_evidence_manifest,
)
from kifrs.ingestion.manifest import DEFAULT_MANIFEST_PATH, load_manifest


@dataclass(frozen=True)
class RuntimeEvidence:
    evidence_id: str
    record_type: str
    record_id: str
    source_id: str
    citation_role: str
    body_storage_policy: str
    locator: dict[str, Any]
    evidence_label: str
    allowed_output_level: str
    record: dict[str, Any]
    notes: str = ""

    @property
    def is_supporting_interpretation(self) -> bool:
        return self.citation_role == "supporting_interpretation"

    @property
    def is_legal_boundary(self) -> bool:
        return self.citation_role == "legal_boundary"

    @property
    def is_fact_evidence(self) -> bool:
        return self.citation_role == "fact_evidence"

    def to_reference_dict(self) -> dict[str, Any]:
        return {
            "evidence_id": self.evidence_id,
            "record_type": self.record_type,
            "record_id": self.record_id,
            "source_id": self.source_id,
            "citation_role": self.citation_role,
            "body_storage_policy": self.body_storage_policy,
            "locator": self.locator,
            "evidence_label": self.evidence_label,
            "allowed_output_level": self.allowed_output_level,
        }


@dataclass(frozen=True)
class EvidenceBundle:
    source_manifest_path: Path
    evidence_manifest_path: Path
    items: tuple[RuntimeEvidence, ...]

    def by_role(self, role: str) -> tuple[RuntimeEvidence, ...]:
        return tuple(item for item in self.items if item.citation_role == role)

    @property
    def supporting_interpretations(self) -> tuple[RuntimeEvidence, ...]:
        return self.by_role("supporting_interpretation")

    @property
    def legal_boundaries(self) -> tuple[RuntimeEvidence, ...]:
        return self.by_role("legal_boundary")

    @property
    def fact_evidence(self) -> tuple[RuntimeEvidence, ...]:
        return self.by_role("fact_evidence")

    def get(self, evidence_id: str) -> RuntimeEvidence | None:
        for item in self.items:
            if item.evidence_id == evidence_id:
                return item
        return None


def load_runtime_evidence(
    source_manifest_path: Path = DEFAULT_MANIFEST_PATH,
    evidence_manifest_path: Path = DEFAULT_EVIDENCE_PATH,
) -> EvidenceBundle:
    validation = validate_evidence_manifest(evidence_manifest_path, source_manifest_path)
    if not validation["ok"]:
        joined = "; ".join(validation["errors"])
        raise ValueError(f"invalid runtime evidence manifests: {joined}")

    source_index = _source_record_index(load_manifest(source_manifest_path))
    evidence_manifest = load_evidence_manifest(evidence_manifest_path)
    items = tuple(
        _to_runtime_evidence(item, source_index)
        for item in evidence_manifest.get("evidence", [])
    )
    return EvidenceBundle(
        source_manifest_path=source_manifest_path,
        evidence_manifest_path=evidence_manifest_path,
        items=items,
    )


def _to_runtime_evidence(
    item: dict[str, Any],
    source_index: dict[tuple[Any, Any], dict[str, Any]],
) -> RuntimeEvidence:
    record_key = (item["record_type"], item["record_id"])
    return RuntimeEvidence(
        evidence_id=item["evidence_id"],
        record_type=item["record_type"],
        record_id=item["record_id"],
        source_id=item["source_id"],
        citation_role=item["citation_role"],
        body_storage_policy=item["body_storage_policy"],
        locator=dict(item["locator"]),
        evidence_label=item["evidence_label"],
        allowed_output_level=item["allowed_output_level"],
        record=dict(source_index[record_key]),
        notes=item.get("notes", ""),
    )


def _source_record_index(manifest: dict[str, Any]) -> dict[tuple[Any, Any], dict[str, Any]]:
    index: dict[tuple[Any, Any], dict[str, Any]] = {}
    for record in manifest.get("records", []):
        if not isinstance(record, dict):
            continue
        record_type = record.get("record_type")
        record_id = record.get("document_id") if record_type == "document_metadata" else record.get("fact_id")
        if record_type and record_id:
            index[(record_type, record_id)] = record
    return index

