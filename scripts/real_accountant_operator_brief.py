from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

try:
    from scripts.real_accountant_invite_packet import build_invite_packet
    from scripts.real_accountant_run_sheet import build_run_sheet
    from scripts.real_accountant_status import summarize_status
except ModuleNotFoundError:
    import sys

    ROOT = Path(__file__).resolve().parents[1]
    if str(ROOT) not in sys.path:
        sys.path.insert(0, str(ROOT))
    try:
        from scripts.real_accountant_invite_packet import build_invite_packet
        from scripts.real_accountant_run_sheet import build_run_sheet
        from scripts.real_accountant_status import summarize_status
    except ModuleNotFoundError:
        from real_accountant_invite_packet import build_invite_packet
        from real_accountant_run_sheet import build_run_sheet
        from real_accountant_status import summarize_status


DEFAULT_MANIFEST = Path("docs/reports/real-accountant-session/session_manifest.json")
DEFAULT_LEDGER = Path("docs/reports/real-accountant-session/outreach-log.sample.jsonl")


def build_operator_brief(
    *,
    root: Path,
    manifest: Path = DEFAULT_MANIFEST,
    outreach_ledger: Path = DEFAULT_LEDGER,
) -> dict[str, Any]:
    status = summarize_status(root=root, manifest=manifest, outreach_ledger=outreach_ledger)
    invite = build_invite_packet(ledger_path=outreach_ledger)
    run_sheet = build_run_sheet()
    return {
        "title": "Real Accountant Session Operator Brief",
        "horizon": status["horizon"],
        "session_mode": status["session_mode"],
        "close_ready": status["close_ready"],
        "next_action": status["next_action"],
        "blocked_by": status["blocked_by"],
        "send_now": {
            "subject": invite["subject"],
            "body": invite["body"],
            "post_send_update_command": invite["post_send_update_command"],
        },
        "commands": {
            "status": "python scripts\\real_accountant_status.py",
            "invite": "python scripts\\real_accountant_invite_packet.py",
            "schedule_response": "python scripts\\real_accountant_response_packet.py --response schedule",
            "run_sheet": "python scripts\\real_accountant_run_sheet.py",
            "preflight": "python scripts\\real_accountant_preflight.py",
            "notes_scaffold": (
                "python scripts\\real_accountant_notes_scaffold.py "
                "--out docs\\reports\\real-accountant-session\\actual-feedback-notes.md "
                "--date 2026-07-05 "
                '--reviewer-role "CPA reviewer" '
                '--reviewer-service-line "F-ACC" '
                '--reviewer-experience-context "reviewed accounting advisory workpapers" '
                '--session-mode "async review"'
            ),
            "notes_check": (
                "python scripts\\real_accountant_notes_check.py "
                "--notes docs\\reports\\real-accountant-session\\actual-feedback-notes.md"
            ),
            "capture": (
                "python scripts\\real_accountant_capture.py "
                "--notes docs\\reports\\real-accountant-session\\actual-feedback-notes.md "
                "--out docs\\reports\\real-accountant-session"
            ),
            "close_gate": (
                "python scripts\\real_accountant_close_check.py "
                "--manifest docs\\reports\\real-accountant-session\\session_manifest.json "
                "--outreach-ledger docs\\reports\\real-accountant-session\\outreach-log.sample.jsonl "
                "--run-quality-preflight"
            ),
        },
        "open_files": run_sheet["open_files"],
        "required_questions": run_sheet["required_questions"],
        "after_session": run_sheet["after_session"],
        "boundary": [
            "Use reviewer aliases only in repo artifacts.",
            "Do not store reviewer real name, customer name, company name, contract text, private filing body, or copied K-IFRS source text.",
            "Do not mark actual_feedback_evidence true until actual notes, capture manifest, queue JSONL, and manifest builder all pass.",
        ],
    }


def render_markdown(brief: dict[str, Any]) -> str:
    lines = [
        f"# {brief['title']}",
        "",
        "## Current State",
        "",
        f"- Horizon: {brief['horizon']}",
        f"- Session mode: {brief['session_mode']}",
        f"- Close ready: {brief['close_ready']}",
        f"- Next action: {brief['next_action']}",
    ]
    if brief["blocked_by"]:
        lines.extend(["", "## Blocked By", ""])
        lines.extend(f"- {item}" for item in brief["blocked_by"])
    lines.extend(
        [
            "",
            "## Send Now",
            "",
            f"Subject: {brief['send_now']['subject']}",
            "",
            brief["send_now"]["body"],
            "",
            "After sending:",
            "",
            f"```powershell\n{brief['send_now']['post_send_update_command']}\n```",
            "",
            "## Command Sequence",
            "",
        ]
    )
    for label, command in brief["commands"].items():
        lines.extend([f"### {label}", "", f"```powershell\n{command}\n```", ""])
    lines.extend(["## Files To Open", ""])
    lines.extend(f"{index}. `{item}`" for index, item in enumerate(brief["open_files"], start=1))
    lines.extend(["", "## Required Questions", ""])
    lines.extend(f"{index}. {item}" for index, item in enumerate(brief["required_questions"], start=1))
    lines.extend(["", "## After Session", ""])
    lines.extend(f"- {item}" for item in brief["after_session"])
    lines.extend(["", "## Boundary", ""])
    lines.extend(f"- {item}" for item in brief["boundary"])
    lines.append("")
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description="Render one operator brief for the real accountant session.")
    parser.add_argument("--root", type=Path, default=Path.cwd())
    parser.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST)
    parser.add_argument("--outreach-ledger", type=Path, default=DEFAULT_LEDGER)
    parser.add_argument("--format", choices=["markdown", "json"], default="markdown")
    args = parser.parse_args()

    brief = build_operator_brief(root=args.root, manifest=args.manifest, outreach_ledger=args.outreach_ledger)
    if args.format == "json":
        print(json.dumps(brief, ensure_ascii=False, indent=2, sort_keys=True))
    else:
        print(render_markdown(brief), end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
