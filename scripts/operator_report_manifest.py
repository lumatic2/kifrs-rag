from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
REPORT_PATH = ROOT / "docs" / "reports" / "2026-07-05-oeh3-report-manifest.md"


def build_operator_report_manifest() -> dict[str, Any]:
    entries = [
        _entry(1, "position", "Where am I?", "docs/reports/2026-07-05-accounting-intelligence-progress-map.md"),
        _entry(2, "queue", "What product weakness horizon is active?", "docs/reports/2026-07-05-product-weakness-horizon-candidates.md"),
        _entry(3, "commands", "What can I run?", "docs/reports/2026-07-05-oeh1-operator-command-inventory.md"),
        _entry(4, "doctor", "Is the local operator surface healthy?", "docs/reports/2026-07-05-oeh2-run-doctor.md"),
        _entry(5, "retriever", "Why is retriever promotion deferred?", "docs/reports/2026-07-05-runtime-retriever-promotion-gate-close-report.md"),
        _entry(6, "workflow", "What new accounting workflow was added?", "docs/reports/2026-07-05-workflow-coverage-expansion-close-report.md"),
        _entry(7, "source", "What non-IFRS source lane exists?", "docs/reports/2026-07-05-source-body-ingestion-controlled-lane-close-report.md"),
    ]
    checks = {
        "entries_ordered": [item["order"] for item in entries] == sorted(item["order"] for item in entries),
        "all_entries_have_goal": all(item["goal"] for item in entries),
        "all_entries_have_path": all(item["path"] for item in entries),
        "missing_hints_present": all(item["hint"] for item in entries),
        "protected_paths_absent": all("data/" not in item["path"] and "embedding" not in item["path"].lower() for item in entries),
    }
    errors = [name for name, ok in checks.items() if ok is not True]
    return {
        "title": "OEH3 Report Manifest",
        "ok": not errors,
        "horizon": "operator-experience-hardening",
        "completed_milestone": "OEH3",
        "entries": entries,
        "checks": checks,
        "errors": errors,
        "next_gate": "error_recovery_playbook",
        "report_path": _display_path(REPORT_PATH),
    }


def render_markdown(result: dict[str, Any]) -> str:
    lines = [
        f"# {result['title']}",
        "",
        "> Scope: ordered public report navigation surface for local operators.",
        "",
        "## 한 줄 결론",
        "",
        "The operator can now start from progress, then queue, commands, doctor, and the latest close reports without reading ROADMAP internals.",
        "",
        "## Manifest",
        "",
        "| Order | Goal | Question | Report | Exists | Hint |",
        "|---:|---|---|---|---|---|",
    ]
    for item in result["entries"]:
        lines.append(
            f"| {item['order']} | {item['goal']} | {item['question']} | `{item['path']}` | {item['exists']} | `{item['hint']}` |"
        )
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
    result = build_operator_report_manifest()
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(render_markdown(result), encoding="utf-8")
    return result


def _entry(order: int, goal: str, question: str, path: str) -> dict[str, Any]:
    return {
        "order": order,
        "goal": goal,
        "question": question,
        "path": path,
        "exists": (ROOT / path).exists(),
        "hint": "rerun producing command from OEH1 inventory if missing",
    }


def _display_path(path: Path) -> str:
    try:
        return path.resolve().relative_to(ROOT).as_posix()
    except ValueError:
        return path.as_posix()


def main() -> int:
    parser = argparse.ArgumentParser(description="Build OEH3 report manifest.")
    parser.add_argument("--format", choices=["text", "json", "markdown"], default="text")
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--out", type=Path, default=REPORT_PATH)
    args = parser.parse_args()

    result = write_report(args.out) if args.write else build_operator_report_manifest()
    if args.format == "json":
        print(json.dumps(result, ensure_ascii=False, indent=2))
    elif args.format == "markdown":
        print(render_markdown(result), end="")
    else:
        print(result["title"])
        print(f"- ok: {result['ok']}")
        print(f"- entries: {len(result['entries'])}")
        print(f"- next gate: {result['next_gate']}")
        for error in result["errors"]:
            print(f"- {error}")
    return 0 if result["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
