from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
REPORT_PATH = ROOT / "docs" / "reports" / "2026-07-06-demo-rehearsal-improvement-hardening-close-report.md"
EVIDENCE = [
    {
        "id": "DRI1",
        "name": "retriever timing threshold",
        "path": "docs/reports/2026-07-05-drq2-demo-run-quality-checklist.md",
        "required_phrase": "Variance Threshold",
    },
    {
        "id": "DRI2",
        "name": "rehearsal freshness metadata",
        "path": "docs/reports/2026-07-05-drq3-demo-rehearsal-evidence.md",
        "required_phrase": "Freshness Metadata",
    },
    {
        "id": "DRI3",
        "name": "operator summary surface",
        "path": "docs/reports/2026-07-05-accounting-intelligence-progress-map.md",
        "required_phrase": "Operator Summary",
    },
]


def build_close_gate() -> dict[str, Any]:
    evidence = [_inspect_evidence(item) for item in EVIDENCE]
    checks = {
        "all_evidence_exists": all(item["exists"] for item in evidence),
        "all_required_phrases_present": all(item["required_phrase_present"] for item in evidence),
        "timing_threshold_present": any(item["id"] == "DRI1" and item["required_phrase_present"] for item in evidence),
        "freshness_metadata_present": any(item["id"] == "DRI2" and item["required_phrase_present"] for item in evidence),
        "operator_summary_present": any(item["id"] == "DRI3" and item["required_phrase_present"] for item in evidence),
    }
    errors = [name for name, ok in checks.items() if ok is not True]
    return {
        "title": "Demo Rehearsal Improvement Hardening Close Report",
        "ok": not errors,
        "horizon": "demo-rehearsal-improvement-hardening",
        "completed_milestone": "DRI4",
        "close_result": "demo_rehearsal_improvements_hardened",
        "evidence": evidence,
        "checks": checks,
        "errors": errors,
        "implemented_items": ["DRQ4-1", "DRQ4-2", "DRQ4-3"],
        "residual_risks": [
            "The rehearsal remains public-safe and synthetic.",
            "Default retriever promotion remains deferred by the separate guard.",
        ],
        "next_leaf": "demo_rehearsal_improvement_hardening_complete",
        "report_path": _display_path(REPORT_PATH),
    }


def render_markdown(result: dict[str, Any]) -> str:
    lines = [
        f"# {result['title']}",
        "",
        "> Scope: close gate for the three internal DRQ4 rehearsal improvement fixes.",
        "",
        "## 한 줄 결론",
        "",
        (
            f"Close result: `{result['close_result']}`. Implemented internal backlog items: "
            + ", ".join(result["implemented_items"])
            + "."
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
    parser = argparse.ArgumentParser(description="Build DRI4 close gate report.")
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
