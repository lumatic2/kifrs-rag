"""Canonical non-IFRS source record validation.

This contract sits above the older ingestion manifest validator. It describes
the data unit that later runtime code can consume regardless of whether the
source began as document metadata, a law locator, a structured filing fact, or
a local-private placeholder.
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from kifrs.authority import REGISTRY_PATH, load_authority_sources
from kifrs.ingestion.manifest import (
    ALLOWED_BODY_STORAGE_POLICIES,
    ALLOWED_CITATION_ROLES,
    FORBIDDEN_MANIFEST_FIELDS,
    PUBLIC_SAFE_STORAGE_POLICIES,
    _find_forbidden_fields,
)


ROOT = Path(__file__).resolve().parents[2]

ALLOWED_SOURCE_RECORD_TYPES = {
    "document_metadata",
    "law_locator",
    "structured_fact",
    "client_private_fact",
}
ALLOWED_AUTHORITY_LEVELS = {
    "primary",
    "supporting",
    "legal_boundary",
    "fact",
    "client_private",
}
ALLOWED_RETRIEVAL_LANES = {
    "document_metadata",
    "law_locator",
    "structured_fact",
    "local_private_fact",
}
SOURCE_RECORD_COMMON_REQUIRED_FIELDS = {
    "record_id",
    "record_type",
    "source_id",
    "source_class",
    "authority_level",
    "body_storage_policy",
    "citation_role",
    "retrieval_lane",
    "locator",
    "provenance",
    "public_safe",
}
SOURCE_RECORD_REQUIRED_BY_TYPE = {
    "document_metadata": {
        "title",
        "publisher",
        "document_type",
        "topics",
        "chunk_strategy",
    },
    "law_locator": {
        "law_name",
        "article_locator",
        "official_registry",
        "topics",
        "chunk_strategy",
    },
    "structured_fact": {
        "company_id",
        "filing_id",
        "period",
        "statement_type",
        "line_item",
        "value",
        "unit",
        "dimensions",
        "quality_flags",
    },
    "client_private_fact": {
        "case_scope",
        "fact_label",
        "fact_kind",
        "private_storage_boundary",
        "deletion_policy",
    },
}


def validate_source_record(record: dict[str, Any], *, registry_path: Path = REGISTRY_PATH) -> dict[str, Any]:
    errors: list[str] = []
    registry_source_ids = {source.id for source in load_authority_sources(registry_path)}

    errors.extend(_find_forbidden_fields(record))
    errors.extend(_missing_fields(record, SOURCE_RECORD_COMMON_REQUIRED_FIELDS, "$"))

    record_type = record.get("record_type")
    if record_type not in ALLOWED_SOURCE_RECORD_TYPES:
        errors.append(f"$: invalid record_type {record_type}")
    else:
        errors.extend(_missing_fields(record, SOURCE_RECORD_REQUIRED_BY_TYPE[record_type], "$"))
        errors.extend(_validate_type_contract(record, record_type))

    source_id = record.get("source_id")
    if source_id not in registry_source_ids:
        errors.append(f"$: unknown source_id {source_id}")

    if record.get("authority_level") not in ALLOWED_AUTHORITY_LEVELS:
        errors.append(f"$: invalid authority_level {record.get('authority_level')}")
    if record.get("body_storage_policy") not in ALLOWED_BODY_STORAGE_POLICIES:
        errors.append(f"$: invalid body_storage_policy {record.get('body_storage_policy')}")
    if record.get("citation_role") not in ALLOWED_CITATION_ROLES:
        errors.append(f"$: invalid citation_role {record.get('citation_role')}")
    if record.get("retrieval_lane") not in ALLOWED_RETRIEVAL_LANES:
        errors.append(f"$: invalid retrieval_lane {record.get('retrieval_lane')}")
    if not isinstance(record.get("locator"), dict) or not record.get("locator"):
        errors.append("$: locator must be non-empty object")
    if not isinstance(record.get("provenance"), dict) or not record.get("provenance"):
        errors.append("$: provenance must be non-empty object")
    if (
        record.get("public_safe") is True
        and record.get("body_storage_policy") not in PUBLIC_SAFE_STORAGE_POLICIES
        and not (record_type == "client_private_fact" and record.get("body_storage_policy") == "no_store_handoff")
    ):
        errors.append("$: public_safe record must use public-safe storage policy")

    return {"ok": not errors, "errors": errors, "record_type": record_type, "record_id": record.get("record_id")}


def validate_source_records(records: list[dict[str, Any]], *, registry_path: Path = REGISTRY_PATH) -> dict[str, Any]:
    errors: list[str] = []
    seen: set[str] = set()
    by_type = {record_type: 0 for record_type in sorted(ALLOWED_SOURCE_RECORD_TYPES)}
    for idx, record in enumerate(records):
        result = validate_source_record(record, registry_path=registry_path)
        if not result["ok"]:
            errors.extend(f"records[{idx}]: {error}" for error in result["errors"])
        record_id = str(record.get("record_id", ""))
        if record_id in seen:
            errors.append(f"records[{idx}]: duplicate record_id {record_id}")
        if record_id:
            seen.add(record_id)
        record_type = record.get("record_type")
        if record_type in by_type:
            by_type[str(record_type)] += 1
    return {"ok": not errors, "errors": errors, "total": len(records), "by_type": by_type}


def load_records(path: Path) -> list[dict[str, Any]]:
    raw = json.loads(path.read_text(encoding="utf-8"))
    if isinstance(raw, dict):
        return list(raw.get("records", []))
    if isinstance(raw, list):
        return raw
    raise ValueError(f"unsupported source record payload: {path}")


def _missing_fields(record: dict[str, Any], required: set[str], prefix: str) -> list[str]:
    return [f"{prefix}: missing {field}" for field in sorted(required) if field not in record]


def _validate_type_contract(record: dict[str, Any], record_type: str) -> list[str]:
    errors: list[str] = []
    if record_type == "document_metadata":
        _expect(record, "retrieval_lane", "document_metadata", errors)
        if record.get("citation_role") not in {"supporting_interpretation", "collection_seed"}:
            errors.append("$: document_metadata must use supporting_interpretation or collection_seed")
    elif record_type == "law_locator":
        _expect(record, "retrieval_lane", "law_locator", errors)
        _expect(record, "citation_role", "legal_boundary", errors)
        _expect(record, "body_storage_policy", "no_store_link_only", errors)
    elif record_type == "structured_fact":
        _expect(record, "retrieval_lane", "structured_fact", errors)
        _expect(record, "authority_level", "fact", errors)
        _expect(record, "citation_role", "fact_evidence", errors)
        if not isinstance(record.get("value"), (int, float)) or isinstance(record.get("value"), bool):
            errors.append("$: structured_fact value must be numeric")
        if not isinstance(record.get("dimensions"), dict):
            errors.append("$: structured_fact dimensions must be object")
        if not isinstance(record.get("quality_flags"), list):
            errors.append("$: structured_fact quality_flags must be list")
    elif record_type == "client_private_fact":
        _expect(record, "retrieval_lane", "local_private_fact", errors)
        _expect(record, "authority_level", "client_private", errors)
        _expect(record, "body_storage_policy", "no_store_handoff", errors)
        if record.get("public_safe") is not True:
            errors.append("$: committed client_private_fact placeholders must be public_safe")
    return errors


def _expect(record: dict[str, Any], field: str, expected: str, errors: list[str]) -> None:
    if record.get(field) != expected:
        errors.append(f"$: {field} must be {expected}")


__all__ = [
    "ALLOWED_AUTHORITY_LEVELS",
    "ALLOWED_RETRIEVAL_LANES",
    "ALLOWED_SOURCE_RECORD_TYPES",
    "FORBIDDEN_MANIFEST_FIELDS",
    "validate_source_record",
    "validate_source_records",
    "load_records",
]
