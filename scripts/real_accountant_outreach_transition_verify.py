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
from scripts.real_accountant_outreach_check import check_outreach  # noqa: E402
from scripts.real_accountant_status import summarize_status  # noqa: E402


DEFAULT_MANIFEST = ROOT / "docs" / "reports" / "real-accountant-session" / "session_manifest.json"
DEFAULT_LEDGER = ROOT / "docs" / "reports" / "real-accountant-session" / "outreach-log.sample.jsonl"
REPORT_PATH = ROOT / "docs" / "reports" / "real-accountant-session" / "2026-07-05-outreach-transition-verify.md"
EXPECTED_NEXT_ACTION_STATUS = {
    "not_sent": "needs_user_action",
    "sent": "waiting_on_reviewer_reply",
    "responded": "waiting_on_reviewer_reply",
    "scheduled": "session_scheduled",
    "declined": "needs_reviewer_replacement",
    "completed": "needs_notes_capture",
}


def verify_transition(
    *,
    ledger: Path = DEFAULT_LEDGER,
    manifest: Path = DEFAULT_MANIFEST,
    expected_status: str = "not_sent",
) -> dict[str, Any]:
    ok, outreach_errors, counts = check_outreach(ledger)
    status = summarize_status(root=ROOT, manifest=manifest, outreach_ledger=ledger)
    action = build_next_action(manifest=manifest, outreach_ledger=ledger)
    errors = list(outreach_errors)

    if expected_status not in EXPECTED_NEXT_ACTION_STATUS:
        errors.append(f"unsupported expected status: {expected_status}")
    if counts.get(expected_status, 0) < 1:
        errors.append(f"expected at least one {expected_status} outreach row")

    expected_action_status = EXPECTED_NEXT_ACTION_STATUS.get(expected_status)
    if expected_action_status and action["status"] != expected_action_status:
        errors.append(f"expected next-action status {expected_action_status}, got {action['status']}")
    if expected_status == "not_sent" and "real_accountant_invite_packet.py" not in action["next_command"]:
        errors.append("not_sent state should route to real_accountant_invite_packet.py")
    if expected_status in {"sent", "responded"} and "real_accountant_response_packet.py" not in action["next_command"]:
        errors.append("sent/responded state should route to real_accountant_response_packet.py")
    if expected_status == "scheduled" and "real_accountant_run_sheet.py" not in action["next_command"]:
        errors.append("scheduled state should route to real_accountant_run_sheet.py")
    if expected_status == "completed" and "real_accountant_post_session_final_gate.py" not in action["next_command"]:
        errors.append("completed state should route to real_accountant_post_session_final_gate.py")

    return {
        "ok": ok and not errors,
        "errors": errors,
        "title": "Real Accountant Outreach Transition Verify",
        "ledger": _display_path(ledger),
        "manifest": _display_path(manifest),
        "expected_status": expected_status,
        "outreach_counts": counts,
        "session_next_action": status["next_action"],
        "next_action_status": action["status"],
        "next_action_command": action["next_command"],
        "report_path": _display_path(REPORT_PATH),
    }


def render_markdown(result: dict[str, Any]) -> str:
    lines = [
        f"# {result['title']}",
        "",
        "> Scope: verify that a manually updated outreach ledger routes RS2 to the correct next action.",
        "",
        "## 한 줄 결론",
        "",
        _one_line_conclusion(result),
        "",
        "## Transition",
        "",
        f"- ok: {result['ok']}",
        f"- ledger: `{result['ledger']}`",
        f"- expected status: {result['expected_status']}",
        f"- outreach counts: {result['outreach_counts']}",
        f"- session next action: {result['session_next_action']}",
        f"- next-action status: {result['next_action_status']}",
        f"- next-action command: `{result['next_action_command']}`",
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


def write_report(
    *,
    ledger: Path = DEFAULT_LEDGER,
    manifest: Path = DEFAULT_MANIFEST,
    expected_status: str = "not_sent",
    out: Path = REPORT_PATH,
) -> dict[str, Any]:
    result = verify_transition(ledger=ledger, manifest=manifest, expected_status=expected_status)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(render_markdown(result), encoding="utf-8")
    return result


def _one_line_conclusion(result: dict[str, Any]) -> str:
    if result["ok"]:
        return f"Ledger has the expected `{result['expected_status']}` state and next-action routing is correct."
    return f"Ledger is not ready for `{result['expected_status']}` routing; fix the listed errors before continuing RS2."


def _display_path(path: Path) -> str:
    try:
        return path.resolve().relative_to(ROOT).as_posix()
    except ValueError:
        return path.as_posix()


def main() -> None:
    parser = argparse.ArgumentParser(description="Verify real accountant outreach state transition routing.")
    parser.add_argument("--ledger", type=Path, default=DEFAULT_LEDGER)
    parser.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST)
    parser.add_argument("--expected-status", choices=sorted(EXPECTED_NEXT_ACTION_STATUS), default="not_sent")
    parser.add_argument("--format", choices=["text", "json", "markdown"], default="text")
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--out", type=Path, default=REPORT_PATH)
    args = parser.parse_args()

    result = (
        write_report(
            ledger=args.ledger,
            manifest=args.manifest,
            expected_status=args.expected_status,
            out=args.out,
        )
        if args.write
        else verify_transition(ledger=args.ledger, manifest=args.manifest, expected_status=args.expected_status)
    )
    if args.format == "json":
        print(json.dumps(result, ensure_ascii=False, indent=2, default=str))
    elif args.format == "markdown":
        print(render_markdown(result), end="")
    else:
        print(f"ok: {result['ok']}")
        print(f"ledger: {result['ledger']}")
        print(f"expected_status: {result['expected_status']}")
        print(f"outreach_counts: {result['outreach_counts']}")
        print(f"next_action_status: {result['next_action_status']}")
        print(f"next_action_command: {result['next_action_command']}")
        for error in result["errors"]:
            print(f"- {error}")

    if not result["ok"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
