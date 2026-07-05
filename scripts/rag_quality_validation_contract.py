from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
REPORT_PATH = ROOT / "docs" / "reports" / "2026-07-05-rqf1-validation-contract.md"


def build_validation_contract() -> dict[str, Any]:
    commands = [
        _command(
            command_id="gap_audit",
            command="python scripts\\accounting_intelligence_gap_audit.py --format text --write",
            evidence="docs/reports/2026-07-05-accounting-intelligence-gap-audit.md",
            purpose="Confirm current Objective gaps and automation snapshot before RAG work.",
        ),
        _command(
            command_id="default_guard",
            command="python scripts\\default_retriever_guard.py --format text",
            evidence="docs/reports/2026-07-05-default-retriever-guard.md",
            purpose="Confirm default retriever cannot change without stronger evidence and authorization.",
        ),
        _command(
            command_id="promotion_close",
            command="python scripts\\runtime_retriever_promotion_close_gate.py --format text",
            evidence="docs/reports/2026-07-05-runtime-retriever-promotion-gate-close-report.md",
            purpose="Carry forward previous promote/defer/rollback evidence.",
        ),
    ]
    metrics = [
        {
            "name": "recall_at_20",
            "minimum": 0.95,
            "reason": "RAG answer quality must retrieve likely source paragraphs before answer composition.",
        },
        {
            "name": "regression_count",
            "maximum": 0,
            "reason": "A stronger retriever cannot regress known cases before default promotion.",
        },
        {
            "name": "latency_budget_seconds",
            "maximum": 2.0,
            "reason": "Interactive accounting use cannot require slow default retrieval.",
        },
        {
            "name": "rollback_available",
            "required": True,
            "reason": "Default retriever changes must be reversible.",
        },
    ]
    boundaries = [
        "Public reports may include commands, metrics, pass/fail status, and report paths.",
        "Public reports may not include K-IFRS source text, parsed DB rows, embeddings, dogfood prompts, private payloads, or secrets.",
        "Local private eval assets may be referenced as missing-local-evidence but not printed.",
        "Default retriever remains unchanged until promotion gate and explicit authorization both pass.",
    ]
    checks = {
        "all_commands_have_evidence": all(item["evidence_exists"] for item in commands),
        "all_commands_are_local_scripts": all(item["command"].startswith("python scripts\\") for item in commands),
        "metrics_defined": len(metrics) >= 4,
        "promotion_blockers_defined": True,
        "public_safety_boundaries_defined": len(boundaries) >= 4,
        "default_change_forbidden_in_rqf1": True,
    }
    errors = [name for name, ok in checks.items() if ok is not True]
    return {
        "title": "RQF1 Validation Corpus And Acceptance Contract",
        "ok": not errors,
        "horizon": "rag-quality-fresh-validation",
        "completed_milestone": "RQF1",
        "contract": {
            "scope": "fresh RAG quality validation before default retriever promotion",
            "dataset_boundary": "public-safe eval metadata and local private eval assets by reference only",
            "promotion_result_space": ["promote", "defer", "rollback", "blocked"],
            "default_change_allowed": False,
        },
        "commands": commands,
        "metrics": metrics,
        "promotion_blockers": [
            "missing fresh baseline snapshot",
            "missing opt-in regression matrix",
            "any known regression",
            "rollback evidence missing",
            "explicit authorization missing",
        ],
        "boundaries": boundaries,
        "checks": checks,
        "errors": errors,
        "next_leaf": "RQF2_current_retriever_baseline_snapshot",
        "report_path": _display_path(REPORT_PATH),
    }


def render_markdown(result: dict[str, Any]) -> str:
    contract = result["contract"]
    lines = [
        f"# {result['title']}",
        "",
        "> Scope: public-safe RAG quality validation contract for the active objective-gap horizon.",
        "",
        "## 한 줄 결론",
        "",
        "RAG quality validation must produce fresh baseline, regression, rollback, and authorization evidence before any default retriever change.",
        "",
        "## Contract",
        "",
        f"- Scope: {contract['scope']}",
        f"- Dataset boundary: {contract['dataset_boundary']}",
        f"- Default change allowed in RQF1: {contract['default_change_allowed']}",
        f"- Result space: {', '.join(contract['promotion_result_space'])}",
        "",
        "## Commands",
        "",
        "| ID | Command | Evidence | Exists | Purpose |",
        "|---|---|---|---|---|",
    ]
    for item in result["commands"]:
        lines.append(
            f"| {item['command_id']} | `{item['command']}` | `{item['evidence']}` | {item['evidence_exists']} | {item['purpose']} |"
        )
    lines.extend(["", "## Metrics", "", "| Metric | Threshold | Reason |", "|---|---|---|"])
    for metric in result["metrics"]:
        threshold = metric.get("minimum", metric.get("maximum", metric.get("required")))
        lines.append(f"| {metric['name']} | {threshold} | {metric['reason']} |")
    lines.extend(["", "## Promotion Blockers", ""])
    lines.extend(f"- {item}" for item in result["promotion_blockers"])
    lines.extend(["", "## Boundaries", ""])
    lines.extend(f"- {item}" for item in result["boundaries"])
    lines.extend(["", "## Checks", "", "| Check | OK |", "|---|---|"])
    for name, ok in result["checks"].items():
        lines.append(f"| {name} | {ok} |")
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
    result = build_validation_contract()
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(render_markdown(result), encoding="utf-8")
    return result


def _command(command_id: str, command: str, evidence: str, purpose: str) -> dict[str, Any]:
    return {
        "command_id": command_id,
        "command": command,
        "evidence": evidence,
        "evidence_exists": (ROOT / evidence).exists(),
        "purpose": purpose,
    }


def _display_path(path: Path) -> str:
    try:
        return path.resolve().relative_to(ROOT).as_posix()
    except ValueError:
        return path.as_posix()


def main() -> int:
    parser = argparse.ArgumentParser(description="Build RQF1 RAG quality validation contract.")
    parser.add_argument("--format", choices=["text", "json", "markdown"], default="text")
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--out", type=Path, default=REPORT_PATH)
    args = parser.parse_args()

    result = write_report(args.out) if args.write else build_validation_contract()
    if args.format == "json":
        print(json.dumps(result, ensure_ascii=False, indent=2))
    elif args.format == "markdown":
        print(render_markdown(result), end="")
    else:
        print(result["title"])
        print(f"- ok: {result['ok']}")
        print(f"- commands: {len(result['commands'])}")
        print(f"- next leaf: {result['next_leaf']}")
        for error in result["errors"]:
            print(f"- {error}")
    return 0 if result["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
