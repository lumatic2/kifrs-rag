from __future__ import annotations

import argparse
import json
import shutil
import sys
import tempfile
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.accounting_intelligence_decision_queue import DEFAULT_OUTREACH_LEDGER  # noqa: E402
from scripts.accounting_intelligence_next_action import build_next_action  # noqa: E402
from scripts.real_accountant_outreach_transition_verify import verify_transition  # noqa: E402
from scripts.real_accountant_outreach_update import upsert_outreach  # noqa: E402


REPORT_PATH = ROOT / "docs" / "reports" / "2026-07-05-accounting-intelligence-next-action-sequence-gate.md"


def check_next_action_sequence() -> dict[str, Any]:
    action = build_next_action()
    errors: list[str] = []

    if action["recommended_next_decision"] != "send_reviewer_invite":
        errors.append(f"expected send_reviewer_invite, got {action['recommended_next_decision']}")
    if "real_accountant_invite_packet.py" not in action["next_command"]:
        errors.append("next command should render the reviewer invite packet")
    if "real_accountant_invite_send_receipt.py" not in action["receipt_command"]:
        errors.append("receipt command should render the invite send receipt template")
    if "--write-template" not in action["receipt_command"]:
        errors.append("receipt command should write the invite send receipt template")
    if "real_accountant_apply_invite_receipt.py" not in action["after_command"]:
        errors.append("after command should validate receipt before updating the outreach ledger")
    if "--receipt" not in action["after_command"]:
        errors.append("after command should require a filled receipt path")
    if "real_accountant_outreach_transition_verify.py" not in action["verify_command"]:
        errors.append("verify command should use the outreach transition verifier")
    if "--expected-status sent" not in action["verify_command"]:
        errors.append("verify command should check expected status sent")

    simulation = _simulate_after_command()
    if simulation["ok"] is not True:
        errors.extend(f"simulation: {error}" for error in simulation["errors"])

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
        "post_send_simulation": simulation,
        "report_path": _display_path(REPORT_PATH),
    }


def render_markdown(result: dict[str, Any]) -> str:
    action = result["next_action"]
    lines = [
        f"# {result['title']}",
        "",
        "> Scope: verify that next-action command -> after -> verify is internally consistent for RS2.",
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
        "## Post-Send Simulation",
        "",
        f"- ok: {result['post_send_simulation']['ok']}",
        f"- next-action status after copied ledger update: {result['post_send_simulation']['next_action_status']}",
        f"- verifier command after copied ledger update: `{result['post_send_simulation']['next_action_command']}`",
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


def _simulate_after_command() -> dict[str, Any]:
    with tempfile.TemporaryDirectory() as tmp:
        copied_ledger = Path(tmp) / "outreach.jsonl"
        shutil.copyfile(DEFAULT_OUTREACH_LEDGER, copied_ledger)
        upsert_outreach(
            copied_ledger,
            reviewer_alias="reviewer-001",
            status="sent",
            channel="manual",
            contacted_at="2026-07-05",
            follow_up_by="2026-07-08",
            notes="invite sent",
        )
        verification = verify_transition(ledger=copied_ledger, expected_status="sent")
        return {
            "ok": verification["ok"],
            "errors": verification["errors"],
            "next_action_status": verification["next_action_status"],
            "next_action_command": verification["next_action_command"],
            "outreach_counts": verification["outreach_counts"],
        }


def _one_line_conclusion(result: dict[str, Any]) -> str:
    if result["ok"]:
        return "The next-action command, post-send ledger update, and sent-state verifier are consistent."
    return "The next-action sequence is inconsistent; fix the listed errors before using it for RS2."


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
        print(f"post_send_simulation: {result['post_send_simulation']}")
        for error in result["errors"]:
            print(f"- {error}")

    if not result["ok"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
