"""Metadata-only external authority registry.

K-IFRS paragraphs remain the primary source of evidence. This registry only
surfaces supporting authority candidates by type and priority without storing
third-party source body.
"""
from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parent.parent
REGISTRY_PATH = ROOT / "docs" / "authority" / "sources.json"
SOURCE_PACK_PATH = ROOT / "docs" / "authority" / "source_pack.json"


@dataclass(frozen=True)
class AuthoritySource:
    id: str
    title: str
    authority_type: str
    priority: int
    scope: str
    keywords: list[str]
    status: str
    note: str

    @classmethod
    def from_dict(cls, raw: dict[str, Any]) -> "AuthoritySource":
        return cls(
            id=raw["id"],
            title=raw["title"],
            authority_type=raw["authority_type"],
            priority=int(raw["priority"]),
            scope=raw.get("scope", ""),
            keywords=list(raw.get("keywords", [])),
            status=raw.get("status", "metadata-only"),
            note=raw.get("note", ""),
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "title": self.title,
            "authority_type": self.authority_type,
            "priority": self.priority,
            "scope": self.scope,
            "keywords": self.keywords,
            "status": self.status,
            "note": self.note,
        }


ALLOWED_AUTHORITY_TYPES = {
    "primary_standard",
    "external_law",
    "external_tax",
    "regulatory_guidance",
    "standard-setter_guidance",
    "exam_convention",
    "personal_note",
}

FORBIDDEN_BODY_FIELDS = {"body", "text", "content", "full_text", "source_body"}
SOURCE_PACK_FORBIDDEN_FIELDS = FORBIDDEN_BODY_FIELDS | {"excerpt", "quote", "embedding"}
ALLOWED_SOURCE_PACK_USES = {
    "primary_evidence",
    "supporting_interpretation",
    "legal_boundary",
    "answer_convention",
    "collection_seed",
}


def load_authority_sources(path: Path = REGISTRY_PATH) -> list[AuthoritySource]:
    if not path.exists():
        return []
    raw = json.loads(path.read_text(encoding="utf-8"))
    return [AuthoritySource.from_dict(item) for item in raw.get("sources", [])]


def validate_authority_registry(path: Path = REGISTRY_PATH) -> dict[str, Any]:
    if not path.exists():
        return {"ok": False, "errors": [f"missing registry: {path}"], "total": 0}
    raw = json.loads(path.read_text(encoding="utf-8"))
    errors: list[str] = []
    ids: set[str] = set()
    sources = raw.get("sources", [])
    for idx, item in enumerate(sources):
        prefix = f"sources[{idx}]"
        for field in ("id", "title", "authority_type", "priority", "scope", "keywords", "status", "note"):
            if field not in item:
                errors.append(f"{prefix}: missing {field}")
        forbidden = sorted(FORBIDDEN_BODY_FIELDS & set(item))
        if forbidden:
            errors.append(f"{prefix}: forbidden body fields {forbidden}")
        source_id = item.get("id")
        if source_id in ids:
            errors.append(f"{prefix}: duplicate id {source_id}")
        if source_id:
            ids.add(source_id)
        if item.get("authority_type") not in ALLOWED_AUTHORITY_TYPES:
            errors.append(f"{prefix}: invalid authority_type {item.get('authority_type')}")
        if not isinstance(item.get("keywords"), list) or not item.get("keywords"):
            errors.append(f"{prefix}: keywords must be non-empty list")
        try:
            int(item.get("priority"))
        except (TypeError, ValueError):
            errors.append(f"{prefix}: priority must be integer-like")
    return {"ok": not errors, "errors": errors, "total": len(sources)}


def load_source_pack(path: Path = SOURCE_PACK_PATH) -> dict[str, Any]:
    if not path.exists():
        return {"version": 0, "policy": {}, "items": []}
    return json.loads(path.read_text(encoding="utf-8"))


def validate_source_pack(
    pack_path: Path = SOURCE_PACK_PATH,
    registry_path: Path = REGISTRY_PATH,
) -> dict[str, Any]:
    registry = validate_authority_registry(registry_path)
    registry_sources = {source.id: source for source in load_authority_sources(registry_path)}
    if not pack_path.exists():
        return {"ok": False, "errors": [f"missing source pack: {pack_path}"], "total": 0}

    raw = load_source_pack(pack_path)
    errors: list[str] = []
    if not registry["ok"]:
        errors.extend(f"registry: {err}" for err in registry["errors"])

    policy = raw.get("policy", {})
    if policy.get("body_text_committed") is not False:
        errors.append("policy.body_text_committed must be false")

    ids: set[str] = set()
    items = raw.get("items", [])
    for idx, item in enumerate(items):
        prefix = f"items[{idx}]"
        for field in (
            "id", "source_id", "title", "publisher", "authority_type",
            "allowed_use", "priority", "locator", "status", "keywords", "notes",
        ):
            if field not in item:
                errors.append(f"{prefix}: missing {field}")

        forbidden = sorted(SOURCE_PACK_FORBIDDEN_FIELDS & set(item))
        if forbidden:
            errors.append(f"{prefix}: forbidden body fields {forbidden}")

        item_id = item.get("id")
        if item_id in ids:
            errors.append(f"{prefix}: duplicate id {item_id}")
        if item_id:
            ids.add(item_id)

        source_id = item.get("source_id")
        source = registry_sources.get(source_id)
        if not source:
            errors.append(f"{prefix}: unknown source_id {source_id}")
        elif item.get("authority_type") != source.authority_type:
            errors.append(
                f"{prefix}: authority_type {item.get('authority_type')} does not match source {source_id}"
            )

        if item.get("allowed_use") not in ALLOWED_SOURCE_PACK_USES:
            errors.append(f"{prefix}: invalid allowed_use {item.get('allowed_use')}")
        if not isinstance(item.get("locator"), dict) or not item.get("locator"):
            errors.append(f"{prefix}: locator must be non-empty object")
        if not isinstance(item.get("keywords"), list) or not item.get("keywords"):
            errors.append(f"{prefix}: keywords must be non-empty list")
        try:
            int(item.get("priority"))
        except (TypeError, ValueError):
            errors.append(f"{prefix}: priority must be integer-like")

        if item.get("allowed_use") == "primary_evidence" and source_id != policy.get("primary_evidence_source_id"):
            errors.append(f"{prefix}: primary_evidence must use policy.primary_evidence_source_id")
        if source_id == policy.get("primary_evidence_source_id") and item.get("allowed_use") != "primary_evidence":
            errors.append(f"{prefix}: primary source must use primary_evidence")

    return {"ok": not errors, "errors": errors, "total": len(items)}


def search_source_pack(query: str, limit: int = 10) -> list[dict[str, Any]]:
    pack = load_source_pack()
    hits: list[tuple[int, dict[str, Any], list[str]]] = []
    for item in pack.get("items", []):
        matched = [kw for kw in item.get("keywords", []) if kw and kw in query]
        if not matched:
            continue
        priority = int(item.get("priority", 100))
        score = len(matched) * 100 - priority
        hits.append((score, item, matched))
    hits.sort(key=lambda row: (-row[0], int(row[1].get("priority", 100)), row[1].get("id", "")))
    return [
        {**item, "matched_keywords": matched, "score": score}
        for score, item, matched in hits[:limit]
    ]


def search_authority(query: str, limit: int = 10) -> list[dict[str, Any]]:
    hits: list[tuple[int, AuthoritySource, list[str]]] = []
    for source in load_authority_sources():
        matched = [kw for kw in source.keywords if kw and kw in query]
        if not matched:
            continue
        score = len(matched) * 100 - source.priority
        hits.append((score, source, matched))
    hits.sort(key=lambda item: (-item[0], item[1].priority, item[1].id))
    return [
        {**source.to_dict(), "matched_keywords": matched, "score": score}
        for score, source, matched in hits[:limit]
    ]
