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

from scripts.external_source_connector_metadata_dry_run_gate import check_metadata_dry_run_gate  # noqa: E402
from scripts.external_source_connector_policy_record import check_connector_policy_record  # noqa: E402


REPORT_PATH = ROOT / "docs" / "reports" / "2026-07-05-esmc1-external-source-connector-metadata-close-gate.md"


def check_metadata_close_gate(*, run_quality_preflight: bool = False) -> dict[str, Any]:
    policy = check_connector_policy_record()
    dry_run = check_metadata_dry_run_gate()
    quality = _run_quality_preflight() if run_quality_preflight else {"ran": False, "ok": None, "public_safe": None, "errors": []}
    errors: list[str] = []

    if policy["ok"] is not True:
        errors.extend(f"policy_record: {error}" for error in policy["errors"])
    if dry_run["ok"] is not True:
        errors.extend(f"metadata_dry_run: {error}" for error in dry_run["errors"])

    policy_record = policy["policy_record"]
    if policy_record["implementation_decision"] != "metadata_policy_ready_live_body_ingestion_deferred":
        errors.append("policy_record: unexpected implementation decision")
    for flag in (
        "live_fetch_allowed",
        "body_cache_allowed",
        "live_chunking_allowed",
        "embedding_allowed",
        "answer_time_use_allowed",
    ):
        if policy_record.get(flag) is not False:
            errors.append(f"policy_record: {flag} must be false")

    for flag in (
        "live_fetch_performed",
        "body_text_committed",
        "body_cache_created",
        "chunks_created",
        "embeddings_created",
    ):
        if dry_run.get(flag) is not False:
            errors.append(f"metadata_dry_run: {flag} must be false")

    if dry_run["record_count"] != 2:
        errors.append(f"metadata_dry_run: expected 2 records, got {dry_run['record_count']}")
    if dry_run["manifest_validation"]["ok"] is not True:
        errors.append("metadata_dry_run: manifest validation must pass")

    if run_quality_preflight and quality["ok"] is not True:
        errors.extend(f"quality_preflight: {error}" for error in quality["errors"])
    if run_quality_preflight and quality["public_safe"] is not True:
        errors.append("quality_preflight: public_safe must be true")

    return {
        "ok": not errors,
        "errors": errors,
        "close_gate_id": "esmc1-external-source-connector-metadata-close-gate",
        "connector_id": "kasb-fss-interpretive-catalog",
        "closed_scope": [
            "connector-specific policy record",
            "metadata-only source manifest dry-run",
            "forbidden-field regression for metadata dry-run records",
        ],
        "still_not_implemented": [
            "live external body fetching/crawling",
            "source body cache",
            "source-specific live chunking",
            "external body embeddings",
            "external body index namespace",
            "answer-time use of external source body text",
        ],
        "policy_record": {
            "ok": policy["ok"],
            "report_path": policy["report_path"],
            "implementation_decision": policy_record["implementation_decision"],
            "live_fetch_allowed": policy_record["live_fetch_allowed"],
            "body_cache_allowed": policy_record["body_cache_allowed"],
            "live_chunking_allowed": policy_record["live_chunking_allowed"],
            "embedding_allowed": policy_record["embedding_allowed"],
            "answer_time_use_allowed": policy_record["answer_time_use_allowed"],
        },
        "metadata_dry_run": {
            "ok": dry_run["ok"],
            "report_path": dry_run["report_path"],
            "record_count": dry_run["record_count"],
            "manifest_validation_ok": dry_run["manifest_validation"]["ok"],
            "live_fetch_performed": dry_run["live_fetch_performed"],
            "body_text_committed": dry_run["body_text_committed"],
            "body_cache_created": dry_run["body_cache_created"],
            "chunks_created": dry_run["chunks_created"],
            "embeddings_created": dry_run["embeddings_created"],
        },
        "quality_preflight": quality,
        "report_path": str(REPORT_PATH.relative_to(ROOT)),
        "next_leaf": "real-accountant-session RS2/RS3 evidence capture, or external source connector live-metadata decision gate",
    }


def render_report(result: dict[str, Any]) -> str:
    lines = [
        "# ESMC1 External Source Connector Metadata Close Gate",
        "",
        "> Scope: close gate for KASB/FSS connector metadata-only readiness.",
        "",
        "## 한 줄 결론",
        "",
        "`kasb-fss-interpretive-catalog` is closed at the metadata-only readiness level: source policy and metadata dry-run pass, while live body retrieval, body cache, chunking, embeddings, indexing, and answer-time body use remain unimplemented.",
        "",
        "## Close Result",
        "",
        f"- ok: {result['ok']}",
        f"- connector id: `{result['connector_id']}`",
        f"- policy decision: `{result['policy_record']['implementation_decision']}`",
        f"- dry-run record count: {result['metadata_dry_run']['record_count']}",
        f"- manifest validation ok: {result['metadata_dry_run']['manifest_validation_ok']}",
        f"- live fetch allowed: {result['policy_record']['live_fetch_allowed']}",
        f"- live fetch performed: {result['metadata_dry_run']['live_fetch_performed']}",
        f"- body cache created: {result['metadata_dry_run']['body_cache_created']}",
        f"- chunks created: {result['metadata_dry_run']['chunks_created']}",
        f"- embeddings created: {result['metadata_dry_run']['embeddings_created']}",
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
    result = check_metadata_close_gate(run_quality_preflight=run_quality_preflight)
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
    parser = argparse.ArgumentParser(description="Close KASB/FSS connector metadata-only readiness lane.")
    parser.add_argument("--format", choices=["text", "json", "markdown"], default="text")
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--run-quality-preflight", action="store_true")
    args = parser.parse_args()

    result = (
        write_report(run_quality_preflight=args.run_quality_preflight)
        if args.write
        else check_metadata_close_gate(run_quality_preflight=args.run_quality_preflight)
    )
    if args.format == "json":
        print(json.dumps(result, ensure_ascii=False, indent=2, default=str))
    elif args.format == "markdown":
        print(render_report(result), end="")
    else:
        print(f"ok: {result['ok']}")
        print(f"connector_id: {result['connector_id']}")
        print(f"dry_run_record_count: {result['metadata_dry_run']['record_count']}")
        print(f"manifest_validation_ok: {result['metadata_dry_run']['manifest_validation_ok']}")
        print(f"live_fetch_allowed: {result['policy_record']['live_fetch_allowed']}")
        print(f"live_fetch_performed: {result['metadata_dry_run']['live_fetch_performed']}")
        print(f"body_cache_created: {result['metadata_dry_run']['body_cache_created']}")
        print(f"chunks_created: {result['metadata_dry_run']['chunks_created']}")
        print(f"embeddings_created: {result['metadata_dry_run']['embeddings_created']}")
        print(f"quality_preflight: {result['quality_preflight']}")
        print(f"next_leaf: {result['next_leaf']}")
        for error in result["errors"]:
            print(f"- {error}")

    if not result["ok"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
