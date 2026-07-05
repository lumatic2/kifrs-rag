from __future__ import annotations

import argparse
import json
import sys
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from kifrs.authority import load_source_pack, validate_source_pack  # noqa: E402


REPORT_PATH = ROOT / "docs" / "reports" / "2026-07-05-escp1-external-source-connector-policy-record.md"

REQUIRED_REPORTS = {
    "as5_first_connector_recommendation": ROOT
    / "docs"
    / "reports"
    / "2026-07-05-as5-first-connector-recommendation.md",
    "live_external_source_validation": ROOT
    / "docs"
    / "reports"
    / "2026-07-05-lev1-live-external-source-validation.md",
    "external_body_policy_plan": ROOT
    / "docs"
    / "reports"
    / "2026-07-05-espp1-external-source-body-policy-plan.md",
    "external_body_authorization_gate": ROOT
    / "docs"
    / "reports"
    / "2026-07-05-esag1-external-source-body-authorization-gate.md",
    "external_synthetic_parser_chunker_close_gate": ROOT
    / "docs"
    / "reports"
    / "2026-07-05-essc1-external-source-synthetic-parser-chunker-close-gate.md",
}

REQUIRED_SOURCE_PACK_ITEMS = [
    "kasb-implementation-material-index",
    "fss-accounting-inquiry-index",
]

FORBIDDEN_PUBLIC_FIELDS = [
    "api_key",
    "body",
    "content",
    "credential",
    "embedding",
    "excerpt",
    "full_text",
    "pdf_bytes",
    "quote",
    "raw_html",
    "source_body",
    "text",
    "token",
]


@dataclass(frozen=True)
class ConnectorPolicyRecord:
    connector_id: str
    source_pack_item_ids: list[str]
    source_class: str
    lane: str
    citation_role: str
    public_storage_policy: str
    local_storage_policy_after_review: str
    allowed_public_fields: list[str]
    forbidden_public_fields: list[str]
    required_source_checks: list[str]
    required_prerequisite_reports: list[str]
    live_fetch_allowed: bool
    body_cache_allowed: bool
    live_chunking_allowed: bool
    embedding_allowed: bool
    answer_time_use_allowed: bool
    implementation_decision: str
    next_leaf: str

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def build_connector_policy_record() -> ConnectorPolicyRecord:
    return ConnectorPolicyRecord(
        connector_id="kasb-fss-interpretive-catalog",
        source_pack_item_ids=REQUIRED_SOURCE_PACK_ITEMS,
        source_class="interpretive_accounting_material",
        lane="document_rag_metadata_first",
        citation_role="supporting_interpretation_after_kifrs_primary_evidence",
        public_storage_policy="public_metadata_locator_schema_and_author_written_notes_only",
        local_storage_policy_after_review="local_private_body_cache_only_after_source_specific_review_and_explicit_authorization",
        allowed_public_fields=[
            "connector_id",
            "source_pack_item_id",
            "publisher",
            "authority_type",
            "allowed_use",
            "priority",
            "locator",
            "status",
            "keywords",
            "notes",
            "policy_decision",
        ],
        forbidden_public_fields=FORBIDDEN_PUBLIC_FIELDS,
        required_source_checks=[
            "confirm publisher and canonical locator for each source pack item",
            "check source-specific robots, terms, and license constraints before body retrieval",
            "keep K-IFRS paragraph DB as primary accounting evidence",
            "classify KASB/FSS material as supporting interpretation, not standalone treatment authority",
            "verify any cache, chunks, and embeddings target gitignored local/private paths",
            "run forbidden-field regression before committing reports or manifests",
            "record explicit operator authorization before live body fetch, cache, chunk, embed, or index work",
        ],
        required_prerequisite_reports=list(REQUIRED_REPORTS),
        live_fetch_allowed=False,
        body_cache_allowed=False,
        live_chunking_allowed=False,
        embedding_allowed=False,
        answer_time_use_allowed=False,
        implementation_decision="metadata_policy_ready_live_body_ingestion_deferred",
        next_leaf="real-accountant-session RS2/RS3 evidence capture, or external source connector metadata dry-run gate",
    )


def check_connector_policy_record() -> dict[str, Any]:
    record = build_connector_policy_record()
    errors: list[str] = []

    missing_reports = [name for name, path in REQUIRED_REPORTS.items() if not path.exists()]
    if missing_reports:
        errors.append(f"missing prerequisite reports: {missing_reports}")

    source_pack_result = validate_source_pack()
    if not source_pack_result["ok"]:
        errors.extend(f"source_pack: {error}" for error in source_pack_result["errors"])

    pack = load_source_pack()
    pack_items = {item.get("id"): item for item in pack.get("items", [])}
    missing_items = [item_id for item_id in REQUIRED_SOURCE_PACK_ITEMS if item_id not in pack_items]
    if missing_items:
        errors.append(f"missing source pack items: {missing_items}")

    wrong_uses = [
        item_id
        for item_id in REQUIRED_SOURCE_PACK_ITEMS
        if pack_items.get(item_id, {}).get("allowed_use") != "supporting_interpretation"
    ]
    if wrong_uses:
        errors.append(f"connector items must use supporting_interpretation: {wrong_uses}")

    forbidden_overlap = sorted(set(record.allowed_public_fields) & set(record.forbidden_public_fields))
    if forbidden_overlap:
        errors.append(f"allowed_public_fields includes forbidden fields: {forbidden_overlap}")

    if any(
        [
            record.live_fetch_allowed,
            record.body_cache_allowed,
            record.live_chunking_allowed,
            record.embedding_allowed,
            record.answer_time_use_allowed,
        ]
    ):
        errors.append("connector policy record must keep all live body and answer-time use flags false")

    return {
        "ok": not errors,
        "errors": errors,
        "policy_record": record.to_dict(),
        "missing_reports": missing_reports,
        "missing_source_pack_items": missing_items,
        "source_pack_ok": source_pack_result["ok"],
        "source_pack_item_summaries": [
            {
                "id": item_id,
                "source_id": pack_items.get(item_id, {}).get("source_id"),
                "publisher": pack_items.get(item_id, {}).get("publisher"),
                "authority_type": pack_items.get(item_id, {}).get("authority_type"),
                "allowed_use": pack_items.get(item_id, {}).get("allowed_use"),
                "status": pack_items.get(item_id, {}).get("status"),
                "locator": pack_items.get(item_id, {}).get("locator"),
            }
            for item_id in REQUIRED_SOURCE_PACK_ITEMS
            if item_id in pack_items
        ],
        "report_path": str(REPORT_PATH.relative_to(ROOT)),
        "next_leaf": record.next_leaf,
    }


def render_report(result: dict[str, Any]) -> str:
    record = result["policy_record"]
    lines = [
        "# ESCP1 External Source Connector Policy Record",
        "",
        "> Scope: source-specific policy record for the first external interpretive-material connector.",
        "",
        "## 한 줄 결론",
        "",
        "`kasb-fss-interpretive-catalog` is ready as a metadata-only connector policy target. It can support future KASB/FSS metadata dry-runs, but live body fetch, cache, chunk, embedding, indexing, and answer-time use remain disabled.",
        "",
        "## Connector",
        "",
        f"- connector id: `{record['connector_id']}`",
        f"- source class: `{record['source_class']}`",
        f"- lane: `{record['lane']}`",
        f"- citation role: `{record['citation_role']}`",
        f"- decision: `{record['implementation_decision']}`",
        "",
        "## Source Pack Items",
        "",
        "| Item | Source | Publisher | Use | Status | Locator |",
        "|---|---|---|---|---|---|",
    ]
    for item in result["source_pack_item_summaries"]:
        locator = item.get("locator") or {}
        locator_label = locator.get("url") or locator.get("ref") or locator.get("kind")
        lines.append(
            "| "
            f"{item['id']} | {item['source_id']} | {item['publisher']} | "
            f"{item['allowed_use']} | {item['status']} | {locator_label} |"
        )

    lines.extend([
        "",
        "## Public Boundary",
        "",
        f"- public storage policy: `{record['public_storage_policy']}`",
        f"- local storage policy after review: `{record['local_storage_policy_after_review']}`",
        f"- live fetch allowed: {record['live_fetch_allowed']}",
        f"- body cache allowed: {record['body_cache_allowed']}",
        f"- live chunking allowed: {record['live_chunking_allowed']}",
        f"- embedding allowed: {record['embedding_allowed']}",
        f"- answer-time use allowed: {record['answer_time_use_allowed']}",
        "",
        "## Required Source Checks",
        "",
    ])
    lines.extend(f"- {check}" for check in record["required_source_checks"])
    lines.extend([
        "",
        "## Validation",
        "",
        f"- ok: {result['ok']}",
        f"- source pack ok: {result['source_pack_ok']}",
        f"- missing reports: {result['missing_reports']}",
        f"- missing source pack items: {result['missing_source_pack_items']}",
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
    result = check_connector_policy_record()
    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    REPORT_PATH.write_text(render_report(result), encoding="utf-8")
    return result


def main() -> None:
    parser = argparse.ArgumentParser(description="Check external source connector-specific policy record.")
    parser.add_argument("--format", choices=["text", "json", "markdown"], default="text")
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()

    result = write_report() if args.write else check_connector_policy_record()
    if args.format == "json":
        print(json.dumps(result, ensure_ascii=False, indent=2, default=str))
    elif args.format == "markdown":
        print(render_report(result), end="")
    else:
        record = result["policy_record"]
        print(f"ok: {result['ok']}")
        print(f"connector_id: {record['connector_id']}")
        print(f"source_pack_ok: {result['source_pack_ok']}")
        print(f"source_pack_items: {record['source_pack_item_ids']}")
        print(f"live_fetch_allowed: {record['live_fetch_allowed']}")
        print(f"body_cache_allowed: {record['body_cache_allowed']}")
        print(f"live_chunking_allowed: {record['live_chunking_allowed']}")
        print(f"embedding_allowed: {record['embedding_allowed']}")
        print(f"answer_time_use_allowed: {record['answer_time_use_allowed']}")
        print(f"next_leaf: {result['next_leaf']}")
        for error in result["errors"]:
            print(f"- {error}")

    if not result["ok"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
