from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.external_source_connector_live_metadata_report_close_gate import check_live_metadata_report_close_gate  # noqa: E402


REPORT_PATH = ROOT / "docs" / "reports" / "2026-07-05-esdib1-external-source-connector-demo-index-bridge.md"
CONNECTOR_CLOSE_REPORT = "2026-07-05-eslrc1-external-source-connector-live-metadata-report-close-gate.md"

BRIDGE_TARGETS = {
    "demo_index": ROOT / "docs" / "reports" / "demo-poc" / "index.md",
    "demo_manifest": ROOT / "docs" / "reports" / "demo-poc" / "MANIFEST.md",
    "field_feedback_index": ROOT / "docs" / "reports" / "field-feedback" / "INDEX.md",
    "real_session_packet": ROOT / "docs" / "reports" / "real-accountant-session" / "SESSION_PACKET.md",
}


def check_demo_index_bridge() -> dict[str, Any]:
    close_gate = check_live_metadata_report_close_gate()
    errors: list[str] = []
    target_results: list[dict[str, Any]] = []

    if close_gate["ok"] is not True:
        errors.extend(f"live_metadata_report_close_gate: {error}" for error in close_gate["errors"])

    for name, path in BRIDGE_TARGETS.items():
        exists = path.exists()
        text = path.read_text(encoding="utf-8") if exists else ""
        has_connector_report = CONNECTOR_CLOSE_REPORT in text
        has_metadata_boundary = "metadata-only" in text or "metadata" in text.lower()
        target_results.append(
            {
                "name": name,
                "path": str(path.relative_to(ROOT)),
                "exists": exists,
                "has_connector_report": has_connector_report,
                "has_metadata_boundary": has_metadata_boundary,
            }
        )
        if not exists:
            errors.append(f"{name}: missing bridge target {path.relative_to(ROOT)}")
        if not has_connector_report:
            errors.append(f"{name}: missing connector close report link")
        if not has_metadata_boundary:
            errors.append(f"{name}: missing metadata-only boundary wording")

    return {
        "ok": not errors,
        "errors": errors,
        "bridge_id": "esdib1-external-source-connector-demo-index-bridge",
        "connector_id": "kasb-fss-interpretive-catalog",
        "connector_close_report": f"docs/reports/{CONNECTOR_CLOSE_REPORT}",
        "bridged_targets": target_results,
        "body_text_stored": False,
        "body_cache_created": False,
        "chunks_created": False,
        "embeddings_created": False,
        "index_created": False,
        "answer_time_body_use_enabled": False,
        "report_path": str(REPORT_PATH.relative_to(ROOT)),
        "next_leaf": "real-accountant-session RS2/RS3 evidence capture, or external source connector demo-index close gate",
    }


def render_report(result: dict[str, Any]) -> str:
    lines = [
        "# ESDIB1 External Source Connector Demo-Index Bridge",
        "",
        "> Scope: expose the KASB/FSS live-metadata connector evidence from demo and field-feedback entry points.",
        "",
        "## 한 줄 결론",
        "",
        "`kasb-fss-interpretive-catalog` live-metadata evidence is now visible from the demo index, demo manifest, field feedback index, and real accountant session packet. This remains a metadata-only bridge; it does not enable source body ingestion or answer-time external body use.",
        "",
        "## Bridge Result",
        "",
        f"- ok: {result['ok']}",
        f"- connector id: `{result['connector_id']}`",
        f"- connector close report: `{result['connector_close_report']}`",
        f"- body text stored: {result['body_text_stored']}",
        f"- body cache created: {result['body_cache_created']}",
        f"- chunks created: {result['chunks_created']}",
        f"- embeddings created: {result['embeddings_created']}",
        f"- index created: {result['index_created']}",
        "",
        "## Bridged Targets",
        "",
        "| Target | Path | Linked | Boundary |",
        "|---|---|---:|---:|",
    ]
    for target in result["bridged_targets"]:
        lines.append(
            "| "
            f"{target['name']} | `{target['path']}` | "
            f"{target['has_connector_report']} | {target['has_metadata_boundary']} |"
        )

    lines.extend([
        "",
        "## Boundary",
        "",
        "- This bridge only links existing public-safe evidence reports.",
        "- It does not fetch, store, chunk, embed, index, or answer from external source body text.",
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
    result = check_demo_index_bridge()
    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    REPORT_PATH.write_text(render_report(result), encoding="utf-8")
    return result


def main() -> None:
    parser = argparse.ArgumentParser(description="Check KASB/FSS connector evidence bridge in demo entry points.")
    parser.add_argument("--format", choices=["text", "json", "markdown"], default="text")
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()

    result = write_report() if args.write else check_demo_index_bridge()
    if args.format == "json":
        print(json.dumps(result, ensure_ascii=False, indent=2, default=str))
    elif args.format == "markdown":
        print(render_report(result), end="")
    else:
        print(f"ok: {result['ok']}")
        print(f"connector_id: {result['connector_id']}")
        print(f"connector_close_report: {result['connector_close_report']}")
        print(f"body_text_stored: {result['body_text_stored']}")
        print(f"body_cache_created: {result['body_cache_created']}")
        print(f"chunks_created: {result['chunks_created']}")
        print(f"embeddings_created: {result['embeddings_created']}")
        print(f"index_created: {result['index_created']}")
        print(f"next_leaf: {result['next_leaf']}")
        for target in result["bridged_targets"]:
            print(
                f"- {target['name']}: linked={target['has_connector_report']} "
                f"boundary={target['has_metadata_boundary']}"
            )
        for error in result["errors"]:
            print(f"- {error}")

    if not result["ok"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
