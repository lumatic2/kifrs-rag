from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


DEFAULT_INVITE = Path("docs/reports/real-accountant-session/2026-07-05-session-invite.md")
DEFAULT_LEDGER = Path("docs/reports/real-accountant-session/outreach-log.sample.jsonl")
DEFAULT_ALIAS = "reviewer-001"
DEFAULT_CONTACTED_AT = "2026-07-05"
DEFAULT_FOLLOW_UP_BY = "2026-07-08"
DEFAULT_CHANNEL = "manual"


def build_invite_packet(
    *,
    invite_path: Path = DEFAULT_INVITE,
    ledger_path: Path = DEFAULT_LEDGER,
    reviewer_alias: str = DEFAULT_ALIAS,
    contacted_at: str = DEFAULT_CONTACTED_AT,
    follow_up_by: str = DEFAULT_FOLLOW_UP_BY,
    channel: str = DEFAULT_CHANNEL,
) -> dict[str, Any]:
    if not reviewer_alias.startswith("reviewer-"):
        raise ValueError("reviewer_alias must be a public-safe alias like reviewer-001")
    if not invite_path.exists():
        raise FileNotFoundError(invite_path)

    raw = invite_path.read_text(encoding="utf-8").strip()
    lines = raw.splitlines()
    subject = _subject_from_lines(lines)
    body = "\n".join(line for line in lines[1:] if not line.startswith("# ")).strip()
    update_command = (
        "python scripts\\real_accountant_outreach_update.py "
        f"--ledger {ledger_path.as_posix()} "
        f"--reviewer-alias {reviewer_alias} "
        "--status sent "
        f"--channel {channel} "
        f"--contacted-at {contacted_at} "
        f"--follow-up-by {follow_up_by} "
        '--notes "invite sent"'
    )
    return {
        "reviewer_alias": reviewer_alias,
        "subject": subject,
        "body": body,
        "send_boundary": [
            "Do not ask reviewer to send raw contracts or customer identifiers.",
            "Use only public-safe notes after the session.",
            "Update outreach ledger after sending.",
        ],
        "post_send_update_command": update_command,
    }


def render_text(packet: dict[str, Any]) -> str:
    lines = [
        "Real Accountant Invite Packet",
        "",
        f"Reviewer alias: {packet['reviewer_alias']}",
        f"Subject: {packet['subject']}",
        "",
        "Message:",
        "",
        str(packet["body"]),
        "",
        "Boundary:",
    ]
    lines.extend(f"- {item}" for item in packet["send_boundary"])
    lines.extend(
        [
            "",
            "After sending, run:",
            "",
            str(packet["post_send_update_command"]),
            "",
        ]
    )
    return "\n".join(lines)


def _subject_from_lines(lines: list[str]) -> str:
    for line in lines:
        if line.startswith("# "):
            return line[2:].strip()
    return "회계 AI PoC 30분 피드백 요청"


def main() -> int:
    parser = argparse.ArgumentParser(description="Render the public-safe real accountant invite packet.")
    parser.add_argument("--invite", type=Path, default=DEFAULT_INVITE)
    parser.add_argument("--ledger", type=Path, default=DEFAULT_LEDGER)
    parser.add_argument("--reviewer-alias", default=DEFAULT_ALIAS)
    parser.add_argument("--contacted-at", default=DEFAULT_CONTACTED_AT)
    parser.add_argument("--follow-up-by", default=DEFAULT_FOLLOW_UP_BY)
    parser.add_argument("--channel", default=DEFAULT_CHANNEL)
    parser.add_argument("--format", choices=["text", "json"], default="text")
    args = parser.parse_args()

    packet = build_invite_packet(
        invite_path=args.invite,
        ledger_path=args.ledger,
        reviewer_alias=args.reviewer_alias,
        contacted_at=args.contacted_at,
        follow_up_by=args.follow_up_by,
        channel=args.channel,
    )
    if args.format == "json":
        print(json.dumps(packet, ensure_ascii=False, indent=2, sort_keys=True))
    else:
        print(render_text(packet), end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
