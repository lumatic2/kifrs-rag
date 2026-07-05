from __future__ import annotations

import argparse
import json
import sys
import tempfile
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from kifrs.ingestion.manifest import FORBIDDEN_MANIFEST_FIELDS, validate_manifest  # noqa: E402
from scripts.external_source_connector_policy_record import (  # noqa: E402
    check_connector_policy_record,
)


REPORT_PATH = ROOT / "docs" / "reports" / "2026-07-05-esmd1-external-source-connector-metadata-dry-run-gate.md"
DRY_RUN_TIMESTAMP = "2026-07-05T12:00:00+09:00"

DOCUMENT_TYPE_BY_SOURCE_PACK_ITEM = {
    "kasb-implementation-material-index": "interpretive_material_catalog",
    "fss-accounting-inquiry-index": "accounting_inquiry_catalog",
}

TOPICS_BY_SOURCE_PACK_ITEM = {
    "kasb-implementation-material-index": ["interpretation", "education", "implementation"],
    "fss-accounting-inquiry-index": ["accounting_inquiry", "supervision", "practice_context"],
}


def build_metadata_dry_run_manifest() -> dict[str, Any]:
    policy = check_connector_policy_record()
    records = [_metadata_record(item, policy["policy_record"]["connector_id"]) for item in policy["source_pack_item_summaries"]]
    return {
        "version": 1,
        "policy": {
            "public_manifest_safe": True,
            "body_text_committed": False,
            "forbidden_fields_rejected": True,
            "dry_run_only": True,
            "live_fetch_performed": False,
        },
        "records": records,
    }


def check_metadata_dry_run_gate() -> dict[str, Any]:
    policy = check_connector_policy_record()
    manifest = build_metadata_dry_run_manifest()
    errors: list[str] = []

    if policy["ok"] is not True:
        errors.extend(f"policy_record: {error}" for error in policy["errors"])

    if manifest["policy"]["live_fetch_performed"] is not False:
        errors.append("dry-run manifest must not perform live fetch")
    if manifest["policy"]["body_text_committed"] is not False:
        errors.append("dry-run manifest must not commit body text")

    forbidden_paths = _find_forbidden_fields(manifest)
    if forbidden_paths:
        errors.extend(f"dry_run_manifest: {path} forbidden field" for path in forbidden_paths)

    manifest_validation = _validate_manifest_payload(manifest)
    if manifest_validation["ok"] is not True:
        errors.extend(f"manifest_validation: {error}" for error in manifest_validation["errors"])

    records = manifest.get("records", [])
    if len(records) != 2:
        errors.append(f"expected 2 metadata records, got {len(records)}")
    for idx, record in enumerate(records):
        prefix = f"records[{idx}]"
        if record.get("record_type") != "document_metadata":
            errors.append(f"{prefix}: record_type must be document_metadata")
        if record.get("connector_id") != "kasb-fss-interpretive-catalog":
            errors.append(f"{prefix}: connector_id must be kasb-fss-interpretive-catalog")
        if record.get("body_storage_policy") != "public_metadata_only":
            errors.append(f"{prefix}: body_storage_policy must be public_metadata_only")
        if record.get("chunk_strategy") != "metadata_only":
            errors.append(f"{prefix}: chunk_strategy must be metadata_only")
        if record.get("public_manifest_safe") is not True:
            errors.append(f"{prefix}: public_manifest_safe must be true")

    return {
        "ok": not errors,
        "errors": errors,
        "gate_id": "esmd1-external-source-connector-metadata-dry-run-gate",
        "connector_id": "kasb-fss-interpretive-catalog",
        "record_count": len(records),
        "live_fetch_performed": manifest["policy"]["live_fetch_performed"],
        "body_text_committed": manifest["policy"]["body_text_committed"],
        "body_cache_created": False,
        "chunks_created": False,
        "embeddings_created": False,
        "policy_record": {
            "ok": policy["ok"],
            "report_path": policy["report_path"],
            "implementation_decision": policy["policy_record"]["implementation_decision"],
        },
        "manifest_validation": manifest_validation,
        "dry_run_records": records,
        "forbidden_manifest_fields": sorted(FORBIDDEN_MANIFEST_FIELDS),
        "report_path": str(REPORT_PATH.relative_to(ROOT)),
        "next_leaf": "real-accountant-session RS2/RS3 evidence capture, or external source connector metadata close gate",
    }


def render_report(result: dict[str, Any]) -> str:
    lines = [
        "# ESMD1 External Source Connector Metadata Dry-Run Gate",
        "",
        "> Scope: metadata-only dry-run gate for the KASB/FSS interpretive connector.",
        "",
        "## 한 줄 결론",
        "",
        "`kasb-fss-interpretive-catalog` can now produce public-safe document metadata records for the KASB and FSS source seeds without live body retrieval. The gate still forbids body cache, chunk creation, embeddings, indexing, and answer-time use.",
        "",
        "## Gate Result",
        "",
        f"- ok: {result['ok']}",
        f"- connector id: `{result['connector_id']}`",
        f"- dry-run record count: {result['record_count']}",
        f"- live fetch performed: {result['live_fetch_performed']}",
        f"- body text committed: {result['body_text_committed']}",
        f"- body cache created: {result['body_cache_created']}",
        f"- chunks created: {result['chunks_created']}",
        f"- embeddings created: {result['embeddings_created']}",
        f"- manifest validation ok: {result['manifest_validation']['ok']}",
        "",
        "## Dry-Run Records",
        "",
        "| Document | Source | Publisher | Storage | Chunk Strategy | Locator |",
        "|---|---|---|---|---|---|",
    ]
    for record in result["dry_run_records"]:
        locator = record.get("locator", {})
        locator_label = locator.get("url") or locator.get("ref") or locator.get("type")
        lines.append(
            "| "
            f"{record['document_id']} | {record['source_id']} | {record['publisher']} | "
            f"{record['body_storage_policy']} | {record['chunk_strategy']} | {locator_label} |"
        )

    lines.extend([
        "",
        "## Boundary",
        "",
        "- This dry-run creates metadata records only.",
        "- It does not fetch, store, chunk, embed, index, or use source bodies at answer time.",
        "- K-IFRS paragraph DB remains the primary accounting evidence source.",
        "",
        "## Next Leaf",
        "",
        str(result["next_leaf"]),
        "",
        "## Machine Result",
        "",
        "```json",
        json.dumps(result, ensure_ascii=False, indent=2, default=str),
        "```",
    ])
    return "\n".join(lines) + "\n"


def write_report() -> dict[str, Any]:
    result = check_metadata_dry_run_gate()
    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    REPORT_PATH.write_text(render_report(result), encoding="utf-8")
    return result


def _metadata_record(item: dict[str, Any], connector_id: str) -> dict[str, Any]:
    item_id = item["id"]
    locator = item["locator"]
    locator_url = locator.get("url") or locator.get("ref") or locator.get("kind")
    return {
        "record_type": "document_metadata",
        "connector_id": connector_id,
        "connector_version": "0.1.0",
        "source_id": item["source_id"],
        "source_class": "interpretive_accounting_material",
        "namespace": f"external.{item['source_id'].replace('-', '_')}.metadata_dry_run",
        "body_storage_policy": "public_metadata_only",
        "citation_role": "supporting_interpretation",
        "locator": {"type": "url", "url": locator_url},
        "retrieved_at": DRY_RUN_TIMESTAMP,
        "public_manifest_safe": True,
        "provenance": {
            "produced_by": "external_source_connector_metadata_dry_run_gate",
            "source_pack_item_id": item_id,
            "source_note": "Metadata-only dry run; no source body copied or cached.",
        },
        "warnings": [
            "supporting_interpretation_only",
            "metadata_dry_run_only",
            "body_not_committed",
        ],
        "document_id": f"{item_id}-metadata-dry-run",
        "title": f"{item['id']} metadata dry-run record",
        "publisher": item["publisher"],
        "document_type": DOCUMENT_TYPE_BY_SOURCE_PACK_ITEM.get(item_id, "interpretive_material_catalog"),
        "publication_date": None,
        "effective_date": None,
        "related_standards": [],
        "topics": TOPICS_BY_SOURCE_PACK_ITEM.get(item_id, ["interpretation"]),
        "chunk_strategy": "metadata_only",
        "allowed_use": "supporting_interpretation",
    }


def _validate_manifest_payload(manifest: dict[str, Any]) -> dict[str, Any]:
    with tempfile.TemporaryDirectory() as temp_dir:
        manifest_path = Path(temp_dir) / "source_manifest.metadata_dry_run.json"
        manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
        return validate_manifest(manifest_path)


def _find_forbidden_fields(value: Any, path: str = "$") -> list[str]:
    errors: list[str] = []
    if isinstance(value, dict):
        for key, nested in value.items():
            key_path = f"{path}.{key}"
            if str(key).lower() in FORBIDDEN_MANIFEST_FIELDS:
                errors.append(key_path)
            errors.extend(_find_forbidden_fields(nested, key_path))
    elif isinstance(value, list):
        for idx, nested in enumerate(value):
            errors.extend(_find_forbidden_fields(nested, f"{path}[{idx}]"))
    return errors


def main() -> None:
    parser = argparse.ArgumentParser(description="Run KASB/FSS connector metadata-only dry-run gate.")
    parser.add_argument("--format", choices=["text", "json", "markdown"], default="text")
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()

    result = write_report() if args.write else check_metadata_dry_run_gate()
    if args.format == "json":
        print(json.dumps(result, ensure_ascii=False, indent=2, default=str))
    elif args.format == "markdown":
        print(render_report(result), end="")
    else:
        print(f"ok: {result['ok']}")
        print(f"connector_id: {result['connector_id']}")
        print(f"record_count: {result['record_count']}")
        print(f"manifest_validation_ok: {result['manifest_validation']['ok']}")
        print(f"live_fetch_performed: {result['live_fetch_performed']}")
        print(f"body_text_committed: {result['body_text_committed']}")
        print(f"chunks_created: {result['chunks_created']}")
        print(f"embeddings_created: {result['embeddings_created']}")
        print(f"next_leaf: {result['next_leaf']}")
        for error in result["errors"]:
            print(f"- {error}")

    if not result["ok"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
