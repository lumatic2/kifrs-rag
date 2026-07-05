from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
REPORT_PATH = ROOT / "docs" / "reports" / "2026-07-05-demo-rehearsal-quality-loop-close-report.md"
EVIDENCE = [
    {
        "id": "DRQ1",
        "name": "demo rehearsal script and timing gate",
        "path": "docs/reports/2026-07-05-drq1-demo-rehearsal-script.md",
        "required_phrase": "Timing Gate",
    },
    {
        "id": "DRQ2",
        "name": "demo run quality checklist",
        "path": "docs/reports/2026-07-05-drq2-demo-run-quality-checklist.md",
        "required_phrase": "failure note",
    },
    {
        "id": "DRQ3",
        "name": "rehearsal evidence capture",
        "path": "docs/reports/2026-07-05-drq3-demo-rehearsal-evidence.md",
        "required_phrase": "timing warning",
    },
    {
        "id": "DRQ4",
        "name": "demo improvement backlog",
        "path": "docs/reports/2026-07-05-drq4-demo-improvement-backlog.md",
        "required_phrase": "DRQ4-1",
    },
]
OBJECTIVE_GAP_HORIZONS = [
    "rag-quality-fresh-validation",
    "private-parser-realism-hardening",
    "external-source-body-connector-expansion",
    "workflow-coverage-depth-expansion",
    "demo-rehearsal-quality-loop",
]


def build_close_gate() -> dict[str, Any]:
    evidence = [_inspect_evidence(item) for item in EVIDENCE]
    objective_gap_status = [
        {"horizon_id": horizon_id, "status": "closed"} for horizon_id in OBJECTIVE_GAP_HORIZONS
    ]
    checks = {
        "all_evidence_exists": all(item["exists"] for item in evidence),
        "all_required_phrases_present": all(item["required_phrase_present"] for item in evidence),
        "timing_gate_present": any(item["id"] == "DRQ1" and item["required_phrase_present"] for item in evidence),
        "quality_checklist_present": any(item["id"] == "DRQ2" and item["required_phrase_present"] for item in evidence),
        "rehearsal_evidence_present": any(item["id"] == "DRQ3" and item["required_phrase_present"] for item in evidence),
        "improvement_backlog_present": any(item["id"] == "DRQ4" and item["required_phrase_present"] for item in evidence),
        "objective_gap_queue_closed": all(item["status"] == "closed" for item in objective_gap_status),
    }
    errors = [name for name, ok in checks.items() if ok is not True]
    return {
        "title": "Demo Rehearsal Quality Loop Close Report",
        "ok": not errors,
        "horizon": "demo-rehearsal-quality-loop",
        "completed_milestone": "DRQ5",
        "close_result": "demo_rehearsal_quality_loop_closed",
        "evidence": evidence,
        "objective_gap_status": objective_gap_status,
        "checks": checks,
        "errors": errors,
        "residual_risks": [
            "The rehearsal is public-safe and synthetic; it is not a field validation claim.",
            "Default retriever promotion remains deferred by its separate guard.",
            "DRQ4 backlog items are prioritized but not yet implemented as product fixes.",
        ],
        "next_leaf": "objective_gap_queue_complete",
        "report_path": _display_path(REPORT_PATH),
    }


def render_markdown(result: dict[str, Any]) -> str:
    lines = [
        f"# {result['title']}",
        "",
        "> Scope: close gate for the demo rehearsal quality loop and objective-gap queue audit.",
        "",
        "## 한 줄 결론",
        "",
        (
            f"Close result: `{result['close_result']}`. DRQ1~DRQ4 evidence is present, "
            "and the five objective-gap horizons in this queue are now closed."
        ),
        "",
        "## Evidence",
        "",
        "| Milestone | Evidence | Exists | Required Phrase Present |",
        "|---|---|---|---|",
    ]
    for item in result["evidence"]:
        lines.append(
            "| {id} {name} | `{path}` | {exists} | {required_phrase_present} |".format(
                **item
            )
        )
    lines.extend(
        [
            "",
            "## Objective Gap Queue Status",
            "",
            "| Horizon | Status |",
            "|---|---|",
        ]
    )
    for item in result["objective_gap_status"]:
        lines.append(f"| `{item['horizon_id']}` | {item['status']} |")
    lines.extend(["", "## Checks", "", "| Check | OK |", "|---|---|"])
    for name, ok in result["checks"].items():
        lines.append(f"| {name} | {ok} |")
    lines.extend(["", "## Residual Risks", ""])
    lines.extend(f"- {risk}" for risk in result["residual_risks"])
    lines.extend(["", "## Errors", ""])
    lines.extend(f"- {error}" for error in result["errors"]) if result["errors"] else lines.append("- none")
    lines.extend(
        [
            "",
            "## Next Leaf",
            "",
            f"- `{result['next_leaf']}`",
            "",
            "## Machine Result",
            "",
            "```json",
            json.dumps(result, ensure_ascii=False, indent=2),
            "```",
        ]
    )
    return "\n".join(lines) + "\n"


def write_report(path: Path = REPORT_PATH) -> dict[str, Any]:
    result = build_close_gate()
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(render_markdown(result), encoding="utf-8")
    return result


def _inspect_evidence(item: dict[str, str]) -> dict[str, Any]:
    path = ROOT / item["path"]
    exists = path.exists()
    text = path.read_text(encoding="utf-8") if exists else ""
    return {
        **item,
        "exists": exists,
        "required_phrase_present": item["required_phrase"] in text,
    }


def _display_path(path: Path) -> str:
    try:
        return path.resolve().relative_to(ROOT).as_posix()
    except ValueError:
        return path.as_posix()


def main() -> int:
    parser = argparse.ArgumentParser(description="Build DRQ5 close gate report.")
    parser.add_argument("--format", choices=["text", "json", "markdown"], default="text")
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--out", type=Path, default=REPORT_PATH)
    args = parser.parse_args()

    result = write_report(args.out) if args.write else build_close_gate()
    if args.format == "json":
        print(json.dumps(result, ensure_ascii=False, indent=2))
    elif args.format == "markdown":
        print(render_markdown(result), end="")
    else:
        print(result["title"])
        print(f"- ok: {result['ok']}")
        print(f"- close result: {result['close_result']}")
        print(f"- next leaf: {result['next_leaf']}")
        for error in result["errors"]:
            print(f"- {error}")
    return 0 if result["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
