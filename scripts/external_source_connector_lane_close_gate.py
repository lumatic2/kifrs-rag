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

from scripts.external_source_connector_lane_summary import build_external_connector_lane_summary  # noqa: E402


REPORT_PATH = ROOT / "docs" / "reports" / "2026-07-05-eslsc1-external-source-connector-lane-close-gate.md"
REQUIRED_STEP_IDS = ["ESCP1", "ESMC1", "ESLC1", "ESLRC1", "ESDIBC1"]


def check_external_connector_lane_close_gate(*, run_quality_preflight: bool = False) -> dict[str, Any]:
    summary = build_external_connector_lane_summary()
    quality = _run_quality_preflight() if run_quality_preflight else {"ran": False, "ok": None, "public_safe": None, "errors": []}
    errors: list[str] = []

    if summary["ok"] is not True:
        errors.extend(f"lane_summary: {error}" for error in summary["errors"])
    if summary["lane_status"] != "metadata_and_demo_bridge_closed":
        errors.append(f"lane_summary: unexpected lane status {summary['lane_status']}")

    step_ids = [step["step_id"] for step in summary["lane_steps"]]
    if step_ids != REQUIRED_STEP_IDS:
        errors.append(f"lane_summary: expected steps {REQUIRED_STEP_IDS}, got {step_ids}")
    for step in summary["lane_steps"]:
        if step.get("ok") is not True:
            errors.append(f"lane_summary: {step.get('step_id')} must be ok")
        if not step.get("report_path"):
            errors.append(f"lane_summary: {step.get('step_id')} report_path is required")

    for flag in (
        "body_text_stored",
        "body_cache_created",
        "chunks_created",
        "embeddings_created",
        "index_created",
        "answer_time_body_use_enabled",
    ):
        if summary.get(flag) is not False:
            errors.append(f"lane_summary: {flag} must be false")

    if run_quality_preflight and quality["ok"] is not True:
        errors.extend(f"quality_preflight: {error}" for error in quality["errors"])
    if run_quality_preflight and quality["public_safe"] is not True:
        errors.append("quality_preflight: public_safe must be true")

    return {
        "ok": not errors,
        "errors": errors,
        "close_gate_id": "eslsc1-external-source-connector-lane-close-gate",
        "connector_id": "kasb-fss-interpretive-catalog",
        "closed_scope": [
            "connector policy record",
            "metadata-only dry-run and close gate",
            "live metadata scaffold and close gate",
            "metadata-only report fixture and close gate",
            "demo-index bridge and close gate",
            "lane summary",
        ],
        "still_not_implemented": summary["still_not_implemented"],
        "lane_summary": {
            "ok": summary["ok"],
            "report_path": summary["report_path"],
            "lane_status": summary["lane_status"],
            "step_ids": step_ids,
            "body_text_stored": summary["body_text_stored"],
            "body_cache_created": summary["body_cache_created"],
            "chunks_created": summary["chunks_created"],
            "embeddings_created": summary["embeddings_created"],
            "index_created": summary["index_created"],
            "answer_time_body_use_enabled": summary["answer_time_body_use_enabled"],
        },
        "quality_preflight": quality,
        "report_path": str(REPORT_PATH.relative_to(ROOT)),
        "next_leaf": "real-accountant-session RS2/RS3 evidence capture, or external source connector post-close demo packet note",
    }


def render_report(result: dict[str, Any]) -> str:
    lines = [
        "# ESLSC1 External Source Connector Lane Close Gate",
        "",
        "> Scope: final close gate for the KASB/FSS external connector metadata-only lane.",
        "",
        "## 한 줄 결론",
        "",
        "`kasb-fss-interpretive-catalog` is closed as a metadata-only external connector lane. It is visible in the demo/reviewer path, but external source body RAG remains intentionally unimplemented.",
        "",
        "## Close Result",
        "",
        f"- ok: {result['ok']}",
        f"- connector id: `{result['connector_id']}`",
        f"- lane summary: `{result['lane_summary']['report_path']}`",
        f"- lane status: `{result['lane_summary']['lane_status']}`",
        f"- steps: {', '.join(result['lane_summary']['step_ids'])}",
        f"- body text stored: {result['lane_summary']['body_text_stored']}",
        f"- body cache created: {result['lane_summary']['body_cache_created']}",
        f"- chunks created: {result['lane_summary']['chunks_created']}",
        f"- embeddings created: {result['lane_summary']['embeddings_created']}",
        f"- index created: {result['lane_summary']['index_created']}",
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
    result = check_external_connector_lane_close_gate(run_quality_preflight=run_quality_preflight)
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
    parser = argparse.ArgumentParser(description="Close KASB/FSS external source connector metadata-only lane.")
    parser.add_argument("--format", choices=["text", "json", "markdown"], default="text")
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--run-quality-preflight", action="store_true")
    args = parser.parse_args()

    result = (
        write_report(run_quality_preflight=args.run_quality_preflight)
        if args.write
        else check_external_connector_lane_close_gate(run_quality_preflight=args.run_quality_preflight)
    )
    if args.format == "json":
        print(json.dumps(result, ensure_ascii=False, indent=2, default=str))
    elif args.format == "markdown":
        print(render_report(result), end="")
    else:
        print(f"ok: {result['ok']}")
        print(f"connector_id: {result['connector_id']}")
        print(f"lane_status: {result['lane_summary']['lane_status']}")
        print(f"steps: {result['lane_summary']['step_ids']}")
        print(f"body_text_stored: {result['lane_summary']['body_text_stored']}")
        print(f"body_cache_created: {result['lane_summary']['body_cache_created']}")
        print(f"chunks_created: {result['lane_summary']['chunks_created']}")
        print(f"embeddings_created: {result['lane_summary']['embeddings_created']}")
        print(f"index_created: {result['lane_summary']['index_created']}")
        print(f"quality_preflight: {result['quality_preflight']}")
        print(f"next_leaf: {result['next_leaf']}")
        for error in result["errors"]:
            print(f"- {error}")

    if not result["ok"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
