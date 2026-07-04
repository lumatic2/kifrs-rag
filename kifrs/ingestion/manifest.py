"""Validation for public-safe ingestion manifests.

The ingestion manifest is intentionally metadata-first. It can describe external
document locators and synthetic/structured facts, but it must not commit source
body, copied excerpts, raw filings, embeddings, or credentials.
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from kifrs.authority import REGISTRY_PATH, load_authority_sources


ROOT = Path(__file__).resolve().parents[2]
DEFAULT_MANIFEST_PATH = ROOT / "docs" / "ingestion" / "source_manifest.example.json"

ALLOWED_RECORD_TYPES = {"document_metadata", "structured_fact"}
ALLOWED_BODY_STORAGE_POLICIES = {
    "public_metadata_only",
    "local_private_body",
    "local_private_structured_data",
    "public_synthetic_fixture",
    "no_store_link_only",
    "no_store_handoff",
}
PUBLIC_SAFE_STORAGE_POLICIES = {
    "public_metadata_only",
    "public_synthetic_fixture",
    "no_store_link_only",
}
ALLOWED_CITATION_ROLES = {
    "supporting_interpretation",
    "legal_boundary",
    "collection_seed",
    "fact_evidence",
}
FORBIDDEN_MANIFEST_FIELDS = {
    "api_key",
    "body",
    "content",
    "credential",
    "embedding",
    "excerpt",
    "full_text",
    "pdf_bytes",
    "quote",
    "raw_xml",
    "source_body",
    "text",
    "token",
    "xbrl_dump",
}

COMMON_REQUIRED_FIELDS = {
    "record_type",
    "connector_id",
    "connector_version",
    "source_id",
    "source_class",
    "namespace",
    "body_storage_policy",
    "citation_role",
    "locator",
    "retrieved_at",
    "public_manifest_safe",
    "provenance",
}

DOCUMENT_METADATA_REQUIRED_FIELDS = {
    "document_id",
    "title",
    "publisher",
    "document_type",
    "publication_date",
    "effective_date",
    "related_standards",
    "topics",
    "chunk_strategy",
    "allowed_use",
}

STRUCTURED_FACT_REQUIRED_FIELDS = {
    "fact_id",
    "company_id",
    "filing_id",
    "period",
    "statement_type",
    "line_item",
    "value",
    "unit",
    "dimensions",
    "filing_locator",
    "quality_flags",
}


def load_manifest(path: Path = DEFAULT_MANIFEST_PATH) -> dict[str, Any]:
    if not path.exists():
        return {"version": 0, "policy": {}, "records": []}
    return json.loads(path.read_text(encoding="utf-8"))


def validate_manifest(
    manifest_path: Path = DEFAULT_MANIFEST_PATH,
    registry_path: Path = REGISTRY_PATH,
) -> dict[str, Any]:
    if not manifest_path.exists():
        return {"ok": False, "errors": [f"missing manifest: {manifest_path}"], "total": 0}

    raw = load_manifest(manifest_path)
    errors: list[str] = []
    registry_source_ids = {source.id for source in load_authority_sources(registry_path)}

    errors.extend(_find_forbidden_fields(raw))

    policy = raw.get("policy", {})
    if policy.get("body_text_committed") is not False:
        errors.append("policy.body_text_committed must be false")
    if policy.get("forbidden_fields_rejected") is not True:
        errors.append("policy.forbidden_fields_rejected must be true")
    public_manifest_safe = policy.get("public_manifest_safe") is True

    records = raw.get("records")
    if not isinstance(records, list) or not records:
        errors.append("records must be a non-empty list")
        return {"ok": False, "errors": errors, "total": 0}

    seen_record_ids: set[str] = set()
    for idx, record in enumerate(records):
        prefix = f"records[{idx}]"
        if not isinstance(record, dict):
            errors.append(f"{prefix}: must be object")
            continue

        errors.extend(_validate_common_record(record, prefix, registry_source_ids, public_manifest_safe))

        record_type = record.get("record_type")
        if record_type == "document_metadata":
            errors.extend(_validate_required_fields(record, DOCUMENT_METADATA_REQUIRED_FIELDS, prefix))
            record_id = record.get("document_id")
        elif record_type == "structured_fact":
            errors.extend(_validate_required_fields(record, STRUCTURED_FACT_REQUIRED_FIELDS, prefix))
            record_id = record.get("fact_id")
        else:
            errors.append(f"{prefix}: invalid record_type {record_type}")
            record_id = None

        if record_id in seen_record_ids:
            errors.append(f"{prefix}: duplicate record id {record_id}")
        if record_id:
            seen_record_ids.add(str(record_id))

    return {"ok": not errors, "errors": errors, "total": len(records)}


def _validate_common_record(
    record: dict[str, Any],
    prefix: str,
    registry_source_ids: set[str],
    public_manifest_safe: bool,
) -> list[str]:
    errors = _validate_required_fields(record, COMMON_REQUIRED_FIELDS, prefix)

    source_id = record.get("source_id")
    if source_id not in registry_source_ids:
        errors.append(f"{prefix}: unknown source_id {source_id}")

    body_storage_policy = record.get("body_storage_policy")
    if body_storage_policy not in ALLOWED_BODY_STORAGE_POLICIES:
        errors.append(f"{prefix}: invalid body_storage_policy {body_storage_policy}")
    if public_manifest_safe and body_storage_policy not in PUBLIC_SAFE_STORAGE_POLICIES:
        errors.append(f"{prefix}: body_storage_policy {body_storage_policy} is not public-manifest safe")

    citation_role = record.get("citation_role")
    if citation_role not in ALLOWED_CITATION_ROLES:
        errors.append(f"{prefix}: invalid citation_role {citation_role}")

    if not isinstance(record.get("locator"), dict) or not record.get("locator"):
        errors.append(f"{prefix}: locator must be non-empty object")
    if not isinstance(record.get("provenance"), dict) or not record.get("provenance"):
        errors.append(f"{prefix}: provenance must be non-empty object")
    if public_manifest_safe and record.get("public_manifest_safe") is not True:
        errors.append(f"{prefix}: public_manifest_safe must be true")

    return errors


def _validate_required_fields(record: dict[str, Any], required: set[str], prefix: str) -> list[str]:
    return [f"{prefix}: missing {field}" for field in sorted(required) if field not in record]


def _find_forbidden_fields(value: Any, path: str = "$") -> list[str]:
    errors: list[str] = []
    if isinstance(value, dict):
        for key, nested in value.items():
            key_path = f"{path}.{key}"
            if str(key).lower() in FORBIDDEN_MANIFEST_FIELDS:
                errors.append(f"{key_path}: forbidden manifest field")
            errors.extend(_find_forbidden_fields(nested, key_path))
    elif isinstance(value, list):
        for idx, nested in enumerate(value):
            errors.extend(_find_forbidden_fields(nested, f"{path}[{idx}]"))
    return errors

