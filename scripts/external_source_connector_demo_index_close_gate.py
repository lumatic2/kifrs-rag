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

from scripts.external_source_connector_demo_index_bridge import check_demo_index_bridge  # noqa: E402


REPORT_PATH = ROOT / "docs" / "reports" / "2026-07-05-esdibc1-external-source-connector-demo-index-close-gate.md"


def check_demo_index_close_gate(*, run_quality_preflight: bool = False) -> dict[str, Any]:
    bridge = check_demo_index_bridge()
    quality = _run_quality_preflight() if run_quality_preflight else {"ran": False, "ok": None, "public_safe": None, "errors": []}
    errors: list[str] = []

    if bridge["ok"] is not True:
        errors.extend(f"demo_index_bridge: {error}" for error in bridge["errors"])
    if len(bridge["bridged_targets"]) != 4:
        errors.append(f"demo_index_bridge: expected 4 bridge targets, got {len(bridge['bridged_targets'])}")

    for target in bridge["bridged_targets"]:
        prefix = str(target["name"])
        if target.get("exists") is not True:
            errors.append(f"{prefix}: target must exist")
        if target.get("has_connector_report") is not True:
            errors.append(f"{prefix}: connector report link must exist")
        if target.get("has_metadata_boundary") is not True:
            errors.append(f"{prefix}: metadata boundary wording must exist")

    for flag in (
        "body_text_stored",
        "body_cache_created",
        "chunks_created",
        "embeddings_created",
        "index_created",
        "answer_time_body_use_enabled",
    ):
        if bridge.get(flag) is not False:
            errors.append(f"demo_index_bridge: {flag} must be false")

    if run_quality_preflight and quality["ok"] is not True:
        errors.extend(f"quality_preflight: {error}" for error in quality["errors"])
    if run_quality_preflight and quality["public_safe"] is not True:
        errors.append("quality_preflight: public_safe must be true")

    return {
        "ok": not errors,
        "errors": errors,
        "close_gate_id": "esdibc1-external-source-connector-demo-index-close-gate",
        "connector_id": "kasb-fss-interpretive-catalog",
        "closed_scope": [
            "demo index connector evidence bridge",
            "demo manifest connector evidence bridge",
            "field feedback index connector evidence bridge",
            "real accountant session packet connector evidence bridge",
        ],
        "still_not_implemented": [
            "source body fetching/crawling",
            "source body cache",
            "source-specific live chunks",
            "external source embeddings",
            "external source body index namespace",
            "answer-time use of external source body text",
        ],
        "demo_index_bridge": {
            "ok": bridge["ok"],
            "report_path": bridge["report_path"],
            "target_count": len(bridge["bridged_targets"]),
            "body_text_stored": bridge["body_text_stored"],
            "body_cache_created": bridge["body_cache_created"],
            "chunks_created": bridge["chunks_created"],
            "embeddings_created": bridge["embeddings_created"],
            "index_created": bridge["index_created"],
            "answer_time_body_use_enabled": bridge["answer_time_body_use_enabled"],
        },
        "quality_preflight": quality,
        "report_path": str(REPORT_PATH.relative_to(ROOT)),
        "next_leaf": "real-accountant-session RS2/RS3 evidence capture, or external source connector lane summary",
    }


def render_report(result: dict[str, Any]) -> str:
    lines = [
        "# ESDIBC1 External Source Connector Demo-Index Close Gate",
        "",
        "> Scope: close gate for exposing KASB/FSS connector evidence through demo and field-feedback entry points.",
        "",
        "## 한 줄 결론",
        "",
        "`kasb-fss-interpretive-catalog` is closed at the demo-index bridge level. A reviewer can now find the metadata-only connector evidence from the demo index, demo manifest, field feedback index, and real accountant session packet.",
        "",
        "## Close Result",
        "",
        f"- ok: {result['ok']}",
        f"- connector id: `{result['connector_id']}`",
        f"- bridge report: `{result['demo_index_bridge']['report_path']}`",
        f"- bridge target count: {result['demo_index_bridge']['target_count']}",
        f"- body text stored: {result['demo_index_bridge']['body_text_stored']}",
        f"- body cache created: {result['demo_index_bridge']['body_cache_created']}",
        f"- chunks created: {result['demo_index_bridge']['chunks_created']}",
        f"- embeddings created: {result['demo_index_bridge']['embeddings_created']}",
        f"- index created: {result['demo_index_bridge']['index_created']}",
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
    result = check_demo_index_close_gate(run_quality_preflight=run_quality_preflight)
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
    parser = argparse.ArgumentParser(description="Close KASB/FSS connector demo-index bridge lane.")
    parser.add_argument("--format", choices=["text", "json", "markdown"], default="text")
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--run-quality-preflight", action="store_true")
    args = parser.parse_args()

    result = (
        write_report(run_quality_preflight=args.run_quality_preflight)
        if args.write
        else check_demo_index_close_gate(run_quality_preflight=args.run_quality_preflight)
    )
    if args.format == "json":
        print(json.dumps(result, ensure_ascii=False, indent=2, default=str))
    elif args.format == "markdown":
        print(render_report(result), end="")
    else:
        print(f"ok: {result['ok']}")
        print(f"connector_id: {result['connector_id']}")
        print(f"target_count: {result['demo_index_bridge']['target_count']}")
        print(f"body_text_stored: {result['demo_index_bridge']['body_text_stored']}")
        print(f"body_cache_created: {result['demo_index_bridge']['body_cache_created']}")
        print(f"chunks_created: {result['demo_index_bridge']['chunks_created']}")
        print(f"embeddings_created: {result['demo_index_bridge']['embeddings_created']}")
        print(f"index_created: {result['demo_index_bridge']['index_created']}")
        print(f"quality_preflight: {result['quality_preflight']}")
        print(f"next_leaf: {result['next_leaf']}")
        for error in result["errors"]:
            print(f"- {error}")

    if not result["ok"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
