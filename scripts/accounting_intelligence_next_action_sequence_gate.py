from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.accounting_intelligence_next_action import build_next_action  # noqa: E402


REPORT_PATH = ROOT / "docs" / "reports" / "2026-07-05-accounting-intelligence-next-action-sequence-gate.md"


def check_next_action_sequence() -> dict[str, Any]:
    action = build_next_action()
    errors: list[str] = []

    if action["recommended_next_decision"] is None:
        simulation = _no_active_sequence()
    else:
        simulation = _manual_sequence_placeholder(action)

    return {
        "ok": not errors,
        "errors": errors,
        "title": "Accounting Intelligence Next Action Sequence Gate",
        "next_action": {
            "decision": action["recommended_next_decision"],
            "status": action["status"],
            "command": action["next_command"],
            "receipt": action["receipt_command"],
            "after": action["after_command"],
            "verify": action["verify_command"],
        },
        "sequence_check": simulation,
        "report_path": _display_path(REPORT_PATH),
    }


def render_markdown(result: dict[str, Any]) -> str:
    action = result["next_action"]
    lines = [
        f"# {result['title']}",
        "",
        "> Scope: verify that the active Accounting Intelligence next-action sequence is internally consistent.",
        "",
        "## 한 줄 결론",
        "",
        _one_line_conclusion(result),
        "",
        "## Sequence",
        "",
        f"- decision: `{action['decision']}`",
        f"- status: {action['status']}",
        f"- command: `{action['command']}`",
        f"- receipt: `{action['receipt']}`",
        f"- after: `{action['after']}`",
        f"- verify: `{action['verify']}`",
        "",
        "## Sequence Check",
        "",
        f"- ok: {result['sequence_check']['ok']}",
        f"- mode: {result['sequence_check']['mode']}",
        f"- detail: {result['sequence_check']['detail']}",
    ]
    if result["errors"]:
        lines.extend(["", "## Errors", ""])
        lines.extend(f"- {error}" for error in result["errors"])
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
    result = check_next_action_sequence()
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(render_markdown(result), encoding="utf-8")
    return result


def _no_active_sequence() -> dict[str, Any]:
    return {
        "ok": True,
        "mode": "no_active_user_action",
        "detail": "No command-after-verify sequence is required because external feedback and authorization gates are parked.",
        "errors": [],
    }


def _manual_sequence_placeholder(action: dict[str, Any]) -> dict[str, Any]:
    return {
        "ok": action["next_command"] != "none",
        "mode": "manual_action_sequence",
        "detail": f"Manual action `{action['recommended_next_decision']}` has command `{action['next_command']}`.",
        "errors": [] if action["next_command"] != "none" else ["manual action has no command"],
    }


def _one_line_conclusion(result: dict[str, Any]) -> str:
    if result["ok"]:
        return "No active user-owned action sequence is required; internal technical work can continue."
    return "The next-action sequence is inconsistent; fix the listed errors before using it."


def _display_path(path: Path) -> str:
    try:
        return path.resolve().relative_to(ROOT).as_posix()
    except ValueError:
        return path.as_posix()


def main() -> None:
    parser = argparse.ArgumentParser(description="Check the Accounting Intelligence next-action command sequence.")
    parser.add_argument("--format", choices=["text", "json", "markdown"], default="text")
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--out", type=Path, default=REPORT_PATH)
    args = parser.parse_args()

    result = write_report(args.out) if args.write else check_next_action_sequence()
    if args.format == "json":
        print(json.dumps(result, ensure_ascii=False, indent=2, default=str))
    elif args.format == "markdown":
        print(render_markdown(result), end="")
    else:
        print(f"ok: {result['ok']}")
        print(f"decision: {result['next_action']['decision']}")
        print(f"command: {result['next_action']['command']}")
        print(f"receipt: {result['next_action']['receipt']}")
        print(f"after: {result['next_action']['after']}")
        print(f"verify: {result['next_action']['verify']}")
        print(f"sequence_check: {result['sequence_check']}")
        for error in result["errors"]:
            print(f"- {error}")

    if not result["ok"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
