from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.external_source_connector_metadata_close_gate import check_metadata_close_gate  # noqa: E402
from scripts.live_external_source_validation import validate_live_external_sources  # noqa: E402


REPORT_PATH = ROOT / "docs" / "reports" / "2026-07-05-eslm1-external-source-connector-live-metadata-decision-gate.md"
LEV1_REPORT_PATH = ROOT / "docs" / "reports" / "2026-07-05-lev1-live-external-source-validation.md"

CONNECTOR_ITEM_IDS = {
    "kasb-implementation-material-index",
    "fss-accounting-inquiry-index",
}

ALLOWED_LIVE_METADATA_FIELDS = [
    "item_id",
    "source_id",
    "publisher",
    "allowed_use",
    "url",
    "status_code",
    "final_url",
    "content_type",
    "network_checked",
    "checked_at",
    "body_text_stored",
]

FORBIDDEN_LIVE_METADATA_FIELDS = [
    "api_key",
    "body",
    "content",
    "credential",
    "embedding",
    "excerpt",
    "full_text",
    "html",
    "pdf_bytes",
    "quote",
    "raw_html",
    "source_body",
    "text",
    "token",
]


def check_live_metadata_decision_gate() -> dict[str, Any]:
    close_gate = check_metadata_close_gate()
    live_contract = validate_live_external_sources(allow_network=False)
    errors: list[str] = []

    if close_gate["ok"] is not True:
        errors.extend(f"metadata_close_gate: {error}" for error in close_gate["errors"])
    if live_contract["ok"] is not True:
        errors.extend(f"live_contract: {error}" for error in live_contract["errors"])
    if not LEV1_REPORT_PATH.exists():
        errors.append(f"missing LEV1 report: {LEV1_REPORT_PATH.relative_to(ROOT)}")

    checks = [check for check in live_contract["checks"] if check.get("item_id") in CONNECTOR_ITEM_IDS]
    found_ids = {str(check.get("item_id")) for check in checks}
    missing_items = sorted(CONNECTOR_ITEM_IDS - found_ids)
    if missing_items:
        errors.append(f"missing connector live metadata targets: {missing_items}")
    for check in checks:
        prefix = str(check.get("item_id"))
        if check.get("body_text_stored") is not False:
            errors.append(f"{prefix}: body_text_stored must be false")
        if check.get("allowed_use") != "supporting_interpretation":
            errors.append(f"{prefix}: allowed_use must be supporting_interpretation")

    forbidden_overlap = sorted(set(ALLOWED_LIVE_METADATA_FIELDS) & set(FORBIDDEN_LIVE_METADATA_FIELDS))
    if forbidden_overlap:
        errors.append(f"allowed_live_metadata_fields includes forbidden fields: {forbidden_overlap}")

    live_metadata_probe_allowed = not errors
    return {
        "ok": not errors,
        "errors": errors,
        "decision_gate_id": "eslm1-external-source-connector-live-metadata-decision-gate",
        "connector_id": "kasb-fss-interpretive-catalog",
        "decision": "allow_live_metadata_probe_scaffold" if live_metadata_probe_allowed else "defer",
        "live_metadata_probe_allowed": live_metadata_probe_allowed,
        "live_network_probe_allowed": live_metadata_probe_allowed,
        "live_body_fetch_allowed": False,
        "body_cache_allowed": False,
        "chunking_allowed": False,
        "embedding_allowed": False,
        "indexing_allowed": False,
        "answer_time_body_use_allowed": False,
        "allowed_live_metadata_fields": ALLOWED_LIVE_METADATA_FIELDS,
        "forbidden_live_metadata_fields": FORBIDDEN_LIVE_METADATA_FIELDS,
        "metadata_close_gate": {
            "ok": close_gate["ok"],
            "report_path": close_gate["report_path"],
            "closed_scope": close_gate["closed_scope"],
        },
        "live_contract": {
            "ok": live_contract["ok"],
            "report_path": live_contract["report_path"],
            "network_checked_by_this_gate": live_contract["network_checked"],
            "target_count": live_contract["target_count"],
            "body_text_stored": live_contract["body_text_stored"],
            "connector_targets": checks,
        },
        "required_prior_live_validation_report": str(LEV1_REPORT_PATH.relative_to(ROOT)),
        "report_path": str(REPORT_PATH.relative_to(ROOT)),
        "next_leaf": "real-accountant-session RS2/RS3 evidence capture, or external source connector live-metadata probe scaffold",
    }


def render_report(result: dict[str, Any]) -> str:
    lines = [
        "# ESLM1 External Source Connector Live-Metadata Decision Gate",
        "",
        "> Scope: decide whether the KASB/FSS connector may implement live metadata probes.",
        "",
        "## 한 줄 결론",
        "",
        "`kasb-fss-interpretive-catalog` may proceed to a live-metadata probe scaffold. The decision allows checking public locator metadata only; it still forbids source body fetch, cache, chunking, embeddings, indexing, and answer-time body use.",
        "",
        "## Decision",
        "",
        f"- ok: {result['ok']}",
        f"- connector id: `{result['connector_id']}`",
        f"- decision: `{result['decision']}`",
        f"- live metadata probe allowed: {result['live_metadata_probe_allowed']}",
        f"- live network probe allowed: {result['live_network_probe_allowed']}",
        f"- live body fetch allowed: {result['live_body_fetch_allowed']}",
        f"- body cache allowed: {result['body_cache_allowed']}",
        f"- chunking allowed: {result['chunking_allowed']}",
        f"- embedding allowed: {result['embedding_allowed']}",
        f"- indexing allowed: {result['indexing_allowed']}",
        f"- answer-time body use allowed: {result['answer_time_body_use_allowed']}",
        "",
        "## Connector Targets",
        "",
        "| Item | Source | Publisher | URL | Body Stored |",
        "|---|---|---|---|---|",
    ]
    for check in result["live_contract"]["connector_targets"]:
        lines.append(
            "| "
            f"{check['item_id']} | {check['source_id']} | {check['publisher']} | "
            f"{check['url']} | {check['body_text_stored']} |"
        )

    lines.extend([
        "",
        "## Boundary",
        "",
        "- This decision gate performs no live network request itself.",
        "- It relies on the prior LEV1 metadata-only live validation report.",
        "- The next implementation may check locator/status/final URL/content type metadata only.",
        "- It must not store source body, copied excerpts, raw HTML, chunks, embeddings, or external body indexes.",
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
    result = check_live_metadata_decision_gate()
    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    REPORT_PATH.write_text(render_report(result), encoding="utf-8")
    return result


def main() -> None:
    parser = argparse.ArgumentParser(description="Decide whether KASB/FSS live metadata probe scaffolding is allowed.")
    parser.add_argument("--format", choices=["text", "json", "markdown"], default="text")
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()

    result = write_report() if args.write else check_live_metadata_decision_gate()
    if args.format == "json":
        print(json.dumps(result, ensure_ascii=False, indent=2, default=str))
    elif args.format == "markdown":
        print(render_report(result), end="")
    else:
        print(f"ok: {result['ok']}")
        print(f"connector_id: {result['connector_id']}")
        print(f"decision: {result['decision']}")
        print(f"live_metadata_probe_allowed: {result['live_metadata_probe_allowed']}")
        print(f"live_body_fetch_allowed: {result['live_body_fetch_allowed']}")
        print(f"body_cache_allowed: {result['body_cache_allowed']}")
        print(f"chunking_allowed: {result['chunking_allowed']}")
        print(f"embedding_allowed: {result['embedding_allowed']}")
        print(f"indexing_allowed: {result['indexing_allowed']}")
        print(f"next_leaf: {result['next_leaf']}")
        for error in result["errors"]:
            print(f"- {error}")

    if not result["ok"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
