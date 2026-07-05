from __future__ import annotations

import argparse
import json
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
REPORT_PATH = ROOT / "docs" / "reports" / "2026-07-05-oeh1-operator-command-inventory.md"


@dataclass(frozen=True)
class OperatorCommand:
    goal: str
    command: str
    report: str
    safety_note: str


def build_operator_command_inventory() -> dict[str, Any]:
    commands = [
        OperatorCommand(
            goal="quality_rag",
            command="python scripts\\rag_quality_final_gate.py --format text",
            report="docs/reports/2026-07-05-rag-quality-refresh-close-report.md",
            safety_note="read-only eval gate; does not change runtime default",
        ),
        OperatorCommand(
            goal="trust_surface",
            command="python scripts\\product_trust_quality_gate.py --format text",
            report="docs/reports/2026-07-05-product-trust-quality-close-report.md",
            safety_note="public-safe report gate",
        ),
        OperatorCommand(
            goal="controlled_source_lane",
            command="python scripts\\controlled_lane_close_gate.py --format text",
            report="docs/reports/2026-07-05-source-body-ingestion-controlled-lane-close-report.md",
            safety_note="synthetic-only controlled lane; no live body fetch",
        ),
        OperatorCommand(
            goal="workflow_coverage",
            command="python scripts\\workflow_coverage_close_gate.py --format text",
            report="docs/reports/2026-07-05-workflow-coverage-expansion-close-report.md",
            safety_note="uses public-safe workflow evidence",
        ),
        OperatorCommand(
            goal="retriever_promotion",
            command="python scripts\\runtime_retriever_promotion_close_gate.py --format text",
            report="docs/reports/2026-07-05-runtime-retriever-promotion-gate-close-report.md",
            safety_note="close result is defer; command does not promote runtime default",
        ),
        OperatorCommand(
            goal="progress_position",
            command="python scripts\\accounting_intelligence_progress_map.py --format text --write",
            report="docs/reports/2026-07-05-accounting-intelligence-progress-map.md",
            safety_note="writes public progress map only",
        ),
        OperatorCommand(
            goal="weakness_queue",
            command="python scripts\\product_weakness_horizon_candidates.py --format text --write",
            report="docs/reports/2026-07-05-product-weakness-horizon-candidates.md",
            safety_note="writes public horizon queue only",
        ),
        OperatorCommand(
            goal="operator_hardening",
            command="python scripts\\operator_command_inventory.py --format text --write",
            report="docs/reports/2026-07-05-oeh1-operator-command-inventory.md",
            safety_note="command inventory; no protected data inspection",
        ),
    ]
    required_goals = {
        "quality_rag",
        "trust_surface",
        "controlled_source_lane",
        "workflow_coverage",
        "retriever_promotion",
        "progress_position",
        "weakness_queue",
        "operator_hardening",
    }
    goals = {item.goal for item in commands}
    missing_goals = sorted(required_goals - goals)
    checks = {
        "all_required_goals_present": not missing_goals,
        "commands_present": all(item.command for item in commands),
        "reports_present": all(item.report for item in commands),
        "safety_notes_present": all(item.safety_note for item in commands),
        "protected_data_not_required": all(
            "embedding" not in item.safety_note.lower()
            and "dogfood" not in item.safety_note.lower()
            and "private payload" not in item.safety_note.lower()
            for item in commands
        ),
    }
    errors = [name for name, ok in checks.items() if ok is not True]
    return {
        "title": "OEH1 Operator Command Inventory",
        "ok": not errors,
        "horizon": "operator-experience-hardening",
        "completed_milestone": "OEH1",
        "commands": [asdict(item) for item in commands],
        "required_goals": sorted(required_goals),
        "missing_goals": missing_goals,
        "checks": checks,
        "errors": errors,
        "next_gate": "run_doctor_and_environment_checks",
        "report_path": _display_path(REPORT_PATH),
    }


def render_markdown(result: dict[str, Any]) -> str:
    lines = [
        f"# {result['title']}",
        "",
        "> Scope: operator-facing command discovery for the local toolkit.",
        "",
        "## 한 줄 결론",
        "",
        "The local operator now has a goal-based command inventory for quality, trust, source, workflow, retriever, progress, and operator-hardening tasks.",
        "",
        "## Commands",
        "",
        "| Goal | Command | Report | Safety Note |",
        "|---|---|---|---|",
    ]
    for item in result["commands"]:
        lines.append(f"| {item['goal']} | `{item['command']}` | `{item['report']}` | {item['safety_note']} |")
    lines.extend(["", "## Checks", "", "| Check | OK |", "|---|---|"])
    for name, ok in result["checks"].items():
        lines.append(f"| {name} | {ok} |")
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
    result = build_operator_command_inventory()
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(render_markdown(result), encoding="utf-8")
    return result


def _display_path(path: Path) -> str:
    try:
        return path.resolve().relative_to(ROOT).as_posix()
    except ValueError:
        return path.as_posix()


def main() -> int:
    parser = argparse.ArgumentParser(description="Build OEH1 operator command inventory.")
    parser.add_argument("--format", choices=["text", "json", "markdown"], default="text")
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--out", type=Path, default=REPORT_PATH)
    args = parser.parse_args()

    result = write_report(args.out) if args.write else build_operator_command_inventory()
    if args.format == "json":
        print(json.dumps(result, ensure_ascii=False, indent=2))
    elif args.format == "markdown":
        print(render_markdown(result), end="")
    else:
        print(result["title"])
        print(f"- ok: {result['ok']}")
        print(f"- commands: {len(result['commands'])}")
        print(f"- next gate: {result['next_gate']}")
        for error in result["errors"]:
            print(f"- {error}")
    return 0 if result["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
