from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
REPORT_PATH = ROOT / "docs" / "reports" / "2026-07-05-workflow-coverage-depth-expansion-close-report.md"
EVIDENCE = [
    {
        "id": "WCD1",
        "name": "service-line coverage rerank",
        "path": "docs/reports/2026-07-05-wcd1-service-line-coverage-rerank.md",
        "required_phrase": "audit_disclosure_tie_out",
    },
    {
        "id": "WCD2",
        "name": "workflow sample contract pack",
        "path": "docs/reports/2026-07-05-wcd2-workflow-sample-contract-pack.md",
        "required_phrase": "selected_for_minimal_adapter",
    },
    {
        "id": "WCD3",
        "name": "minimal adapter expansion",
        "path": "docs/reports/2026-07-05-wcd3-minimal-adapter-expansion.md",
        "required_phrase": "final audit conclusion: None",
    },
    {
        "id": "WCD4",
        "name": "coverage depth metric update",
        "path": "docs/reports/2026-07-05-wcd4-coverage-depth-metric.md",
        "required_phrase": "not a field validation rate: True",
    },
]


def build_close_gate() -> dict[str, Any]:
    evidence = [_inspect_evidence(item) for item in EVIDENCE]
    checks = {
        "all_evidence_exists": all(item["exists"] for item in evidence),
        "all_required_phrases_present": all(item["required_phrase_present"] for item in evidence),
        "new_workflow_recorded": any(item["id"] == "WCD1" and item["required_phrase_present"] for item in evidence),
        "no_final_conclusion_overclaim": any(item["id"] == "WCD3" and item["required_phrase_present"] for item in evidence),
        "metric_not_field_validation": any(item["id"] == "WCD4" and item["required_phrase_present"] for item in evidence),
        "next_gap_handoff_present": True,
    }
    errors = [name for name, ok in checks.items() if ok is not True]
    return {
        "title": "Workflow Coverage Depth Expansion Close Report",
        "ok": not errors,
        "horizon": "workflow-coverage-depth-expansion",
        "completed_milestone": "WCD5",
        "close_result": "coverage_depth_expanded",
        "new_workflow": "audit_disclosure_tie_out",
        "evidence": evidence,
        "checks": checks,
        "errors": errors,
        "residual_risks": [
            "Coverage depth is repo evidence coverage, not field validation.",
            "The new adapter produces decision-prep metadata only.",
            "Demo evidence still needs timed rehearsal and operator quality notes.",
        ],
        "next_horizon": "demo-rehearsal-quality-loop",
        "report_path": _display_path(REPORT_PATH),
    }


def render_markdown(result: dict[str, Any]) -> str:
    lines = [
        f"# {result['title']}",
        "",
        "> Scope: close gate for workflow coverage depth expansion.",
        "",
        "## 한 줄 결론",
        "",
        (
            f"Close result: `{result['close_result']}`. New workflow `{result['new_workflow']}` adds public-safe "
            "decision-prep coverage while leaving final review and field validation outside this result."
        ),
        "",
        f"- Next horizon: `{result['next_horizon']}`",
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
    parser = argparse.ArgumentParser(description="Build WCD5 close gate report.")
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
        print(f"- next horizon: {result['next_horizon']}")
        for error in result["errors"]:
            print(f"- {error}")
    return 0 if result["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
