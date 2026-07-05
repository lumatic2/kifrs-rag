from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.retriever_failure_rollback_policy import build_retriever_failure_rollback_policy  # noqa: E402


REPORT_PATH = ROOT / "docs" / "reports" / "2026-07-05-rpg4-operator-promotion-command.md"


def build_retriever_promotion_command() -> dict[str, Any]:
    rollback = build_retriever_failure_rollback_policy()
    policy = rollback["policy"]
    command_output = {
        "command": "retriever-promotion status --dry-run",
        "mutates_runtime": False,
        "decision": "defer",
        "target_retriever": policy["target_retriever"],
        "current_default": policy["current_default"],
        "safe_fallback": policy["safe_fallback"],
        "required_before_promote": [
            "latency/cost measurement",
            "close-gate promote decision",
            "operator-reviewed rollback path",
            "explicit runtime implementation review",
        ],
        "operator_actions": [
            "keep current default hybrid",
            "run regression/latency gate after latency evidence exists",
            "use rollback policy if any promotion experiment fails",
            "do not expose target retriever in MCP modes before close gate",
        ],
    }
    checks = {
        "rollback_policy_ok": rollback["ok"],
        "dry_run_only": command_output["mutates_runtime"] is False,
        "decision_visible": command_output["decision"] in {"promote", "defer", "block"},
        "required_evidence_visible": bool(command_output["required_before_promote"]),
        "rollback_path_visible": command_output["safe_fallback"] == "hybrid",
        "target_retriever_visible": command_output["target_retriever"] == "ifrs1109_classification_hybrid",
    }
    errors = [name for name, ok in checks.items() if ok is not True]
    return {
        "title": "RPG4 Operator Promotion Command",
        "ok": not errors,
        "horizon": "runtime-retriever-promotion-gate",
        "completed_milestone": "RPG4",
        "command_output": command_output,
        "checks": checks,
        "errors": errors,
        "next_gate": "promotion_gate_close_report",
        "report_path": _display_path(REPORT_PATH),
    }


def render_markdown(result: dict[str, Any]) -> str:
    output = result["command_output"]
    lines = [
        f"# {result['title']}",
        "",
        "> Scope: dry-run operator surface for retriever promotion status.",
        "",
        "## 한 줄 결론",
        "",
        "The operator command reports `defer`, shows required evidence, and does not mutate runtime defaults.",
        "",
        "## Command Output",
        "",
        f"- command: `{output['command']}`",
        f"- mutates runtime: {output['mutates_runtime']}",
        f"- decision: `{output['decision']}`",
        f"- target retriever: `{output['target_retriever']}`",
        f"- current default: `{output['current_default']}`",
        f"- safe fallback: `{output['safe_fallback']}`",
        f"- next gate: `{result['next_gate']}`",
        "",
        "## Required Before Promote",
        "",
    ]
    lines.extend(f"- {item}" for item in output["required_before_promote"])
    lines.extend(["", "## Operator Actions", ""])
    lines.extend(f"- {item}" for item in output["operator_actions"])
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
            json.dumps(result, ensure_ascii=False, indent=2, default=str),
            "```",
        ]
    )
    return "\n".join(lines) + "\n"


def write_report(path: Path = REPORT_PATH) -> dict[str, Any]:
    result = build_retriever_promotion_command()
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(render_markdown(result), encoding="utf-8")
    return result


def _display_path(path: Path) -> str:
    try:
        return path.resolve().relative_to(ROOT).as_posix()
    except ValueError:
        return path.as_posix()


def main() -> int:
    parser = argparse.ArgumentParser(description="Build RPG4 dry-run retriever promotion command output.")
    parser.add_argument("--format", choices=["text", "json", "markdown"], default="text")
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--out", type=Path, default=REPORT_PATH)
    args = parser.parse_args()

    result = write_report(args.out) if args.write else build_retriever_promotion_command()
    if args.format == "json":
        print(json.dumps(result, ensure_ascii=False, indent=2, default=str))
    elif args.format == "markdown":
        print(render_markdown(result), end="")
    else:
        print(result["title"])
        print(f"- ok: {result['ok']}")
        print(f"- decision: {result['command_output']['decision']}")
        print(f"- mutates runtime: {result['command_output']['mutates_runtime']}")
        for error in result["errors"]:
            print(f"- {error}")
    return 0 if result["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
