"""Validation for provenance and citation evidence manifests."""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from kifrs.ingestion.manifest import (
    DEFAULT_MANIFEST_PATH,
    FORBIDDEN_MANIFEST_FIELDS,
    load_manifest,
    validate_manifest,
)


ROOT = Path(__file__).resolve().parents[2]
DEFAULT_EVIDENCE_PATH = ROOT / "docs" / "ingestion" / "evidence_manifest.example.json"

EVIDENCE_REQUIRED_FIELDS = {
    "evidence_id",
    "record_type",
    "record_id",
    "source_id",
    "citation_role",
    "body_storage_policy",
    "locator",
    "evidence_label",
    "allowed_output_level",
}

EXTERNAL_EVIDENCE_ROLES = {
    "supporting_interpretation",
    "legal_boundary",
    "fact_evidence",
}


def load_evidence_manifest(path: Path = DEFAULT_EVIDENCE_PATH) -> dict[str, Any]:
    if not path.exists():
        return {"version": 0, "policy": {}, "evidence": []}
    return json.loads(path.read_text(encoding="utf-8"))


def validate_evidence_manifest(
    evidence_path: Path = DEFAULT_EVIDENCE_PATH,
    source_manifest_path: Path = DEFAULT_MANIFEST_PATH,
) -> dict[str, Any]:
    if not evidence_path.exists():
        return {"ok": False, "errors": [f"missing evidence manifest: {evidence_path}"], "total": 0}

    errors: list[str] = []
    source_result = validate_manifest(source_manifest_path)
    if not source_result["ok"]:
        errors.extend(f"source_manifest: {error}" for error in source_result["errors"])

    raw = load_evidence_manifest(evidence_path)
    errors.extend(_find_forbidden_fields(raw))

    policy = raw.get("policy", {})
    if policy.get("body_text_committed") is not False:
        errors.append("policy.body_text_committed must be false")
    if policy.get("public_manifest_safe") is not True:
        errors.append("policy.public_manifest_safe must be true")

    source_index = _source_record_index(load_manifest(source_manifest_path))
    evidence_items = raw.get("evidence")
    if not isinstance(evidence_items, list) or not evidence_items:
        errors.append("evidence must be a non-empty list")
        return {"ok": False, "errors": errors, "total": 0}

    ids: set[str] = set()
    for idx, item in enumerate(evidence_items):
        prefix = f"evidence[{idx}]"
        if not isinstance(item, dict):
            errors.append(f"{prefix}: must be object")
            continue

        errors.extend(_validate_required_fields(item, EVIDENCE_REQUIRED_FIELDS, prefix))
        evidence_id = item.get("evidence_id")
        if evidence_id in ids:
            errors.append(f"{prefix}: duplicate evidence_id {evidence_id}")
        if evidence_id:
            ids.add(str(evidence_id))

        role = item.get("citation_role")
        if role not in EXTERNAL_EVIDENCE_ROLES:
            errors.append(f"{prefix}: invalid external citation_role {role}")

        record_key = (item.get("record_type"), item.get("record_id"))
        source_record = source_index.get(record_key)
        if not source_record:
            errors.append(f"{prefix}: unknown source manifest record {record_key}")
            continue

        for field in ("source_id", "citation_role", "body_storage_policy"):
            if item.get(field) != source_record.get(field):
                errors.append(
                    f"{prefix}: {field} {item.get(field)} does not match source record {source_record.get(field)}"
                )

        if not isinstance(item.get("locator"), dict) or not item.get("locator"):
            errors.append(f"{prefix}: locator must be non-empty object")

    return {"ok": not errors, "errors": errors, "total": len(evidence_items)}


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


def _validate_required_fields(item: dict[str, Any], required: set[str], prefix: str) -> list[str]:
    return [f"{prefix}: missing {field}" for field in sorted(required) if field not in item]


def _find_forbidden_fields(value: Any, path: str = "$") -> list[str]:
    errors: list[str] = []
    if isinstance(value, dict):
        for key, nested in value.items():
            key_path = f"{path}.{key}"
            if str(key).lower() in FORBIDDEN_MANIFEST_FIELDS:
                errors.append(f"{key_path}: forbidden evidence field")
            errors.extend(_find_forbidden_fields(nested, key_path))
    elif isinstance(value, list):
        for idx, nested in enumerate(value):
            errors.extend(_find_forbidden_fields(nested, f"{path}[{idx}]"))
    return errors

