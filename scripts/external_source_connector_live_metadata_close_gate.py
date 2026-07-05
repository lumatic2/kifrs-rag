from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.external_source_connector_live_metadata_decision_gate import (  # noqa: E402
    ALLOWED_LIVE_METADATA_FIELDS,
    FORBIDDEN_LIVE_METADATA_FIELDS,
    check_live_metadata_decision_gate,
)
from scripts.external_source_connector_live_metadata_probe_scaffold import run_live_metadata_probe_scaffold  # noqa: E402


REPORT_PATH = ROOT / "docs" / "reports" / "2026-07-05-eslc1-external-source-connector-live-metadata-close-gate.md"


def check_live_metadata_close_gate(*, run_quality_preflight: bool = False) -> dict[str, Any]:
    decision = check_live_metadata_decision_gate()
    scaffold = run_live_metadata_probe_scaffold(allow_network=False, checked_at="2026-07-05T12:45:00+09:00")
    quality = _run_quality_preflight() if run_quality_preflight else {"ran": False, "ok": None, "public_safe": None, "errors": []}
    errors: list[str] = []

    if decision["ok"] is not True:
        errors.extend(f"decision_gate: {error}" for error in decision["errors"])
    if decision["live_metadata_probe_allowed"] is not True:
        errors.append("decision_gate: live metadata probe must be allowed")
    for flag in (
        "live_body_fetch_allowed",
        "body_cache_allowed",
        "chunking_allowed",
        "embedding_allowed",
        "indexing_allowed",
        "answer_time_body_use_allowed",
    ):
        if decision.get(flag) is not False:
            errors.append(f"decision_gate: {flag} must be false")

    if scaffold["ok"] is not True:
        errors.extend(f"probe_scaffold: {error}" for error in scaffold["errors"])
    if scaffold["record_count"] != 2:
        errors.append(f"probe_scaffold: expected 2 records, got {scaffold['record_count']}")
    for flag in (
        "body_text_stored",
        "body_cache_created",
        "chunks_created",
        "embeddings_created",
        "index_created",
        "answer_time_body_use_enabled",
    ):
        if scaffold.get(flag) is not False:
            errors.append(f"probe_scaffold: {flag} must be false")

    for idx, record in enumerate(scaffold["probe_records"]):
        prefix = f"probe_records[{idx}]"
        if set(record) != set(ALLOWED_LIVE_METADATA_FIELDS):
            errors.append(f"{prefix}: record fields must equal allowed live metadata fields")
        if record.get("body_text_stored") is not False:
            errors.append(f"{prefix}: body_text_stored must be false")

    forbidden_overlap = sorted(set(ALLOWED_LIVE_METADATA_FIELDS) & set(FORBIDDEN_LIVE_METADATA_FIELDS))
    if forbidden_overlap:
        errors.append(f"allowed live metadata fields include forbidden fields: {forbidden_overlap}")

    if run_quality_preflight and quality["ok"] is not True:
        errors.extend(f"quality_preflight: {error}" for error in quality["errors"])
    if run_quality_preflight and quality["public_safe"] is not True:
        errors.append("quality_preflight: public_safe must be true")

    return {
        "ok": not errors,
        "errors": errors,
        "close_gate_id": "eslc1-external-source-connector-live-metadata-close-gate",
        "connector_id": "kasb-fss-interpretive-catalog",
        "closed_scope": [
            "live-metadata decision gate",
            "live-metadata probe scaffold",
            "allowed-field and forbidden-field guards for metadata probe records",
        ],
        "still_not_implemented": [
            "source body fetching/crawling",
            "source body cache",
            "source body chunks",
            "external source embeddings",
            "external source body index namespace",
            "answer-time use of external source body text",
        ],
        "decision_gate": {
            "ok": decision["ok"],
            "report_path": decision["report_path"],
            "decision": decision["decision"],
            "live_metadata_probe_allowed": decision["live_metadata_probe_allowed"],
            "live_body_fetch_allowed": decision["live_body_fetch_allowed"],
            "body_cache_allowed": decision["body_cache_allowed"],
            "chunking_allowed": decision["chunking_allowed"],
            "embedding_allowed": decision["embedding_allowed"],
            "indexing_allowed": decision["indexing_allowed"],
            "answer_time_body_use_allowed": decision["answer_time_body_use_allowed"],
        },
        "probe_scaffold": {
            "ok": scaffold["ok"],
            "report_path": scaffold["report_path"],
            "allow_network": scaffold["allow_network"],
            "record_count": scaffold["record_count"],
            "body_text_stored": scaffold["body_text_stored"],
            "body_cache_created": scaffold["body_cache_created"],
            "chunks_created": scaffold["chunks_created"],
            "embeddings_created": scaffold["embeddings_created"],
            "index_created": scaffold["index_created"],
            "answer_time_body_use_enabled": scaffold["answer_time_body_use_enabled"],
        },
        "quality_preflight": quality,
        "report_path": str(REPORT_PATH.relative_to(ROOT)),
        "next_leaf": "real-accountant-session RS2/RS3 evidence capture, or external source connector live-metadata report fixture",
    }


def render_report(result: dict[str, Any]) -> str:
    lines = [
        "# ESLC1 External Source Connector Live-Metadata Close Gate",
        "",
        "> Scope: close gate for the KASB/FSS live-metadata probe scaffold.",
        "",
        "## 한 줄 결론",
        "",
        "`kasb-fss-interpretive-catalog` is closed at the live-metadata scaffold level. The system may produce locator/status/final URL/content type metadata records, but source body fetching, body cache, chunks, embeddings, indexing, and answer-time body use remain unimplemented.",
        "",
        "## Close Result",
        "",
        f"- ok: {result['ok']}",
        f"- connector id: `{result['connector_id']}`",
        f"- decision: `{result['decision_gate']['decision']}`",
        f"- live metadata probe allowed: {result['decision_gate']['live_metadata_probe_allowed']}",
        f"- scaffold record count: {result['probe_scaffold']['record_count']}",
        f"- scaffold allow network: {result['probe_scaffold']['allow_network']}",
        f"- body text stored: {result['probe_scaffold']['body_text_stored']}",
        f"- body cache created: {result['probe_scaffold']['body_cache_created']}",
        f"- chunks created: {result['probe_scaffold']['chunks_created']}",
        f"- embeddings created: {result['probe_scaffold']['embeddings_created']}",
        f"- index created: {result['probe_scaffold']['index_created']}",
        "",
        "## Closed Scope",
        "",
    ]
    lines.extend(f"- {item}" for item in result["closed_scope"])
    lines.extend([
        "",
        "## Still Not Implemented",
        "",
    ])
    lines.extend(f"- {item}" for item in result["still_not_implemented"])
    lines.extend([
        "",
        "## Quality Preflight",
        "",
        f"- ran: {result['quality_preflight']['ran']}",
        f"- ok: {result['quality_preflight']['ok']}",
        f"- public_safe: {result['quality_preflight']['public_safe']}",
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


def write_report(*, run_quality_preflight: bool = False) -> dict[str, Any]:
    result = check_live_metadata_close_gate(run_quality_preflight=run_quality_preflight)
    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    REPORT_PATH.write_text(render_report(result), encoding="utf-8")
    return result


def _run_quality_preflight() -> dict[str, Any]:
    completed = subprocess.run(
        [sys.executable, "scripts/quality_preflight.py", "--format", "json"],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    if completed.returncode != 0:
        return {
            "ran": True,
            "ok": False,
            "public_safe": None,
            "errors": [completed.stderr.strip() or completed.stdout.strip() or f"exit {completed.returncode}"],
        }
    try:
        payload = json.loads(completed.stdout)
    except json.JSONDecodeError as exc:
        return {"ran": True, "ok": False, "public_safe": None, "errors": [f"invalid quality_preflight json: {exc}"]}
    return {
        "ran": True,
        "ok": payload.get("ok") is True,
        "public_safe": payload.get("public_safe") is True,
        "errors": payload.get("errors", []),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Close KASB/FSS live metadata probe scaffold lane.")
    parser.add_argument("--format", choices=["text", "json", "markdown"], default="text")
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--run-quality-preflight", action="store_true")
    args = parser.parse_args()

    result = (
        write_report(run_quality_preflight=args.run_quality_preflight)
        if args.write
        else check_live_metadata_close_gate(run_quality_preflight=args.run_quality_preflight)
    )
    if args.format == "json":
        print(json.dumps(result, ensure_ascii=False, indent=2, default=str))
    elif args.format == "markdown":
        print(render_report(result), end="")
    else:
        print(f"ok: {result['ok']}")
        print(f"connector_id: {result['connector_id']}")
        print(f"decision: {result['decision_gate']['decision']}")
        print(f"record_count: {result['probe_scaffold']['record_count']}")
        print(f"body_text_stored: {result['probe_scaffold']['body_text_stored']}")
        print(f"body_cache_created: {result['probe_scaffold']['body_cache_created']}")
        print(f"chunks_created: {result['probe_scaffold']['chunks_created']}")
        print(f"embeddings_created: {result['probe_scaffold']['embeddings_created']}")
        print(f"index_created: {result['probe_scaffold']['index_created']}")
        print(f"quality_preflight: {result['quality_preflight']}")
        print(f"next_leaf: {result['next_leaf']}")
        for error in result["errors"]:
            print(f"- {error}")

    if not result["ok"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
