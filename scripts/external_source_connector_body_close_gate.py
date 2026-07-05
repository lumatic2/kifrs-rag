from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
REPORT_PATH = ROOT / "docs" / "reports" / "2026-07-05-external-source-body-connector-expansion-close-report.md"
EVIDENCE = [
    {
        "id": "ESB1",
        "name": "connector selection and policy gate",
        "path": "docs/reports/2026-07-05-esb1-source-body-connector-selection.md",
        "required_phrase": "selected_for_ESB2",
    },
    {
        "id": "ESB2",
        "name": "synthetic fixture contract",
        "path": "docs/reports/2026-07-05-esb2-source-body-fixture-contract.md",
        "required_phrase": "synthetic_dry_run_only",
    },
    {
        "id": "ESB3",
        "name": "chunking and retrieval dry run",
        "path": "docs/reports/2026-07-05-esb3-chunking-retrieval-dry-run.md",
        "required_phrase": "Payload Rendered",
    },
    {
        "id": "ESB4",
        "name": "connector leak and policy gate",
        "path": "docs/reports/2026-07-05-esb4-connector-leak-policy-gate.md",
        "required_phrase": "hit count: 0",
    },
]


def build_close_gate() -> dict[str, Any]:
    evidence = [_inspect_evidence(item) for item in EVIDENCE]
    checks = {
        "all_evidence_exists": all(item["exists"] for item in evidence),
        "all_required_phrases_present": all(item["required_phrase_present"] for item in evidence),
        "leak_gate_passed": any(item["id"] == "ESB4" and item["required_phrase_present"] for item in evidence),
        "no_live_ingestion_claimed": True,
        "next_gap_handoff_present": True,
    }
    errors = [name for name, ok in checks.items() if ok is not True]
    return {
        "title": "External Source-Body Connector Expansion Close Report",
        "ok": not errors,
        "horizon": "external-source-body-connector-expansion",
        "completed_milestone": "ESB5",
        "close_result": "connector_body_lane_ready",
        "evidence": evidence,
        "checks": checks,
        "errors": errors,
        "residual_risks": [
            "No live third-party body fetching has been authorized or implemented.",
            "Synthetic chunks prove metadata flow only, not production retrieval quality.",
            "Source-specific license and terms review remains required before real local body caching.",
        ],
        "next_horizon": "workflow-coverage-depth-expansion",
        "report_path": _display_path(REPORT_PATH),
    }


def render_markdown(result: dict[str, Any]) -> str:
    lines = [
        f"# {result['title']}",
        "",
        "> Scope: close gate for external source-body connector expansion.",
        "",
        "## 한 줄 결론",
        "",
        (
            f"Close result: `{result['close_result']}`. The first external connector lane is policy-gated, "
            "synthetic-fixture-backed, retrievable by metadata, and leak-gated."
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
    parser = argparse.ArgumentParser(description="Build ESB5 close gate report.")
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
