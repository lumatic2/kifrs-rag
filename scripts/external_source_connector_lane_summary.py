from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.external_source_connector_demo_index_close_gate import check_demo_index_close_gate  # noqa: E402
from scripts.external_source_connector_live_metadata_close_gate import check_live_metadata_close_gate  # noqa: E402
from scripts.external_source_connector_live_metadata_report_close_gate import check_live_metadata_report_close_gate  # noqa: E402
from scripts.external_source_connector_metadata_close_gate import check_metadata_close_gate  # noqa: E402
from scripts.external_source_connector_policy_record import check_connector_policy_record  # noqa: E402


REPORT_PATH = ROOT / "docs" / "reports" / "2026-07-05-esls1-external-source-connector-lane-summary.md"


def build_external_connector_lane_summary() -> dict[str, Any]:
    policy = check_connector_policy_record()
    metadata = check_metadata_close_gate()
    live_metadata = check_live_metadata_close_gate()
    report = check_live_metadata_report_close_gate()
    demo_bridge = check_demo_index_close_gate()

    lane_steps = [
        _step("policy_record", "ESCP1", policy["ok"], policy["report_path"], "connector policy and source-pack item contract"),
        _step("metadata_close_gate", "ESMC1", metadata["ok"], metadata["report_path"], "metadata-only manifest readiness"),
        _step(
            "live_metadata_close_gate",
            "ESLC1",
            live_metadata["ok"],
            live_metadata["report_path"],
            "live metadata scaffold readiness without body storage",
        ),
        _step(
            "live_metadata_report_close_gate",
            "ESLRC1",
            report["ok"],
            report["report_path"],
            "human-readable metadata-only report fixture",
        ),
        _step(
            "demo_index_close_gate",
            "ESDIBC1",
            demo_bridge["ok"],
            demo_bridge["report_path"],
            "demo and field-feedback entry point bridge",
        ),
    ]

    errors: list[str] = []
    for source_name, result in (
        ("policy_record", policy),
        ("metadata_close_gate", metadata),
        ("live_metadata_close_gate", live_metadata),
        ("live_metadata_report_close_gate", report),
        ("demo_index_close_gate", demo_bridge),
    ):
        if result["ok"] is not True:
            errors.extend(f"{source_name}: {error}" for error in result["errors"])

    false_flags = _collect_false_flags(metadata, live_metadata, report, demo_bridge)
    for flag, value in false_flags.items():
        if value is not False:
            errors.append(f"{flag} must be false")

    return {
        "ok": not errors,
        "errors": errors,
        "summary_id": "esls1-external-source-connector-lane-summary",
        "connector_id": "kasb-fss-interpretive-catalog",
        "lane_status": "metadata_and_demo_bridge_closed" if not errors else "needs_attention",
        "lane_steps": lane_steps,
        "closed_capabilities": [
            "connector-specific policy record",
            "metadata-only source manifest dry-run",
            "live metadata probe scaffold",
            "metadata-only human-readable report fixture",
            "demo and field-feedback entry point bridge",
        ],
        "still_not_implemented": [
            "source body fetching/crawling",
            "source body cache",
            "source-specific live chunks",
            "external source embeddings",
            "external source body index namespace",
            "answer-time use of external source body text",
        ],
        "body_text_stored": false_flags["body_text_stored"],
        "body_cache_created": false_flags["body_cache_created"],
        "chunks_created": false_flags["chunks_created"],
        "embeddings_created": false_flags["embeddings_created"],
        "index_created": false_flags["index_created"],
        "answer_time_body_use_enabled": false_flags["answer_time_body_use_enabled"],
        "report_path": str(REPORT_PATH.relative_to(ROOT)),
        "next_leaf": "real-accountant-session RS2/RS3 evidence capture, or external source connector lane close gate",
    }


def render_report(result: dict[str, Any]) -> str:
    lines = [
        "# ESLS1 External Source Connector Lane Summary",
        "",
        "> Scope: summarize the KASB/FSS external connector lane from policy record to demo bridge.",
        "",
        "## 한 줄 결론",
        "",
        "`kasb-fss-interpretive-catalog` is complete through metadata-only policy, metadata dry-run, live metadata scaffold, report fixture, and demo-index bridge. It is not a source-body RAG connector yet.",
        "",
        "## Summary Result",
        "",
        f"- ok: {result['ok']}",
        f"- connector id: `{result['connector_id']}`",
        f"- lane status: `{result['lane_status']}`",
        f"- body text stored: {result['body_text_stored']}",
        f"- body cache created: {result['body_cache_created']}",
        f"- chunks created: {result['chunks_created']}",
        f"- embeddings created: {result['embeddings_created']}",
        f"- index created: {result['index_created']}",
        "",
        "## Lane Steps",
        "",
        "| Step | Evidence | Status | Meaning |",
        "|---|---|---:|---|",
    ]
    for step in result["lane_steps"]:
        lines.append(f"| {step['step_id']} | `{step['report_path']}` | {step['ok']} | {step['meaning']} |")

    lines.extend([
        "",
        "## Closed Capabilities",
        "",
    ])
    lines.extend(f"- {item}" for item in result["closed_capabilities"])
    lines.extend([
        "",
        "## Still Not Implemented",
        "",
    ])
    lines.extend(f"- {item}" for item in result["still_not_implemented"])
    lines.extend([
        "",
        "## Boundary",
        "",
        "- External source evidence remains metadata-only and supporting interpretation only.",
        "- K-IFRS paragraph DB remains the primary accounting evidence source.",
        "- This lane does not fetch, cache, chunk, embed, index, or answer from KASB/FSS source body text.",
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
    result = build_external_connector_lane_summary()
    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    REPORT_PATH.write_text(render_report(result), encoding="utf-8")
    return result


def _step(name: str, step_id: str, ok: bool, report_path: str, meaning: str) -> dict[str, Any]:
    return {
        "name": name,
        "step_id": step_id,
        "ok": ok,
        "report_path": report_path,
        "meaning": meaning,
    }


def _collect_false_flags(*results: dict[str, Any]) -> dict[str, bool]:
    flags = {
        "body_text_stored": False,
        "body_cache_created": False,
        "chunks_created": False,
        "embeddings_created": False,
        "index_created": False,
        "answer_time_body_use_enabled": False,
    }
    for result in results:
        for flag in flags:
            if _contains_true_flag(result, flag):
                flags[flag] = True
    return flags


def _contains_true_flag(value: Any, flag: str) -> bool:
    if isinstance(value, dict):
        return any((key == flag and nested is True) or _contains_true_flag(nested, flag) for key, nested in value.items())
    if isinstance(value, list):
        return any(_contains_true_flag(item, flag) for item in value)
    return False


def main() -> None:
    parser = argparse.ArgumentParser(description="Summarize KASB/FSS external source connector lane.")
    parser.add_argument("--format", choices=["text", "json", "markdown"], default="text")
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()

    result = write_report() if args.write else build_external_connector_lane_summary()
    if args.format == "json":
        print(json.dumps(result, ensure_ascii=False, indent=2, default=str))
    elif args.format == "markdown":
        print(render_report(result), end="")
    else:
        print(f"ok: {result['ok']}")
        print(f"connector_id: {result['connector_id']}")
        print(f"lane_status: {result['lane_status']}")
        print(f"body_text_stored: {result['body_text_stored']}")
        print(f"body_cache_created: {result['body_cache_created']}")
        print(f"chunks_created: {result['chunks_created']}")
        print(f"embeddings_created: {result['embeddings_created']}")
        print(f"index_created: {result['index_created']}")
        print(f"next_leaf: {result['next_leaf']}")
        for step in result["lane_steps"]:
            print(f"- {step['step_id']}: ok={step['ok']} report={step['report_path']}")
        for error in result["errors"]:
            print(f"- {error}")

    if not result["ok"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
