from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any


DEFAULT_PACKET = Path("docs/reports/real-accountant-session/SESSION_PACKET.md")
DEFAULT_RUNBOOK = Path("docs/reports/field-feedback-runbook/2026-07-05-30min-session-runbook.md")
DEFAULT_CHECKLIST = Path("docs/reports/field-feedback-runbook/2026-07-05-operator-checklist.md")


def build_run_sheet(
    *,
    packet_path: Path = DEFAULT_PACKET,
    runbook_path: Path = DEFAULT_RUNBOOK,
    checklist_path: Path = DEFAULT_CHECKLIST,
) -> dict[str, Any]:
    packet = packet_path.read_text(encoding="utf-8")
    runbook = runbook_path.read_text(encoding="utf-8")
    checklist = checklist_path.read_text(encoding="utf-8")
    return {
        "title": "Real Accountant 30-Minute Run Sheet",
        "status_command": "python scripts\\real_accountant_status.py",
        "invite_packet_command": "python scripts\\real_accountant_invite_packet.py",
        "preflight_check_command": "python scripts\\real_accountant_preflight.py",
        "open_files": _numbered_items_after(packet, "## Files to Open During Session"),
        "preflight_commands": _checklist_commands(checklist),
        "opening_script": _checklist_items_after(checklist, "## Opening Script"),
        "required_questions": _numbered_items_after(runbook, "## Required Questions"),
        "after_session": [
            "Optionally create the notes scaffold with python scripts\\real_accountant_notes_scaffold.py --out docs\\reports\\real-accountant-session\\actual-feedback-notes.md.",
            "Write docs/reports/real-accountant-session/actual-feedback-notes.md from public-safe notes only.",
            "Run python scripts\\real_accountant_notes_check.py --notes docs\\reports\\real-accountant-session\\actual-feedback-notes.md.",
            "Run python scripts\\real_accountant_capture.py --notes docs\\reports\\real-accountant-session\\actual-feedback-notes.md --out docs\\reports\\real-accountant-session.",
            "Update outreach ledger to scheduled/completed through real_accountant_outreach_update.py.",
            "Do not close the horizon until real_accountant_close_check.py passes.",
        ],
        "boundary": [
            "Do not request or store raw contracts, customer identifiers, private filing bodies, copied K-IFRS source text, parsed DB, embeddings, or workpaper payloads.",
            "Treat this as product validation, not adoption approval or final accounting judgment.",
        ],
    }


def render_text(sheet: dict[str, Any]) -> str:
    lines = [
        str(sheet["title"]),
        "",
        "Before Invite:",
        f"- {sheet['status_command']}",
        f"- {sheet['invite_packet_command']}",
        f"- {sheet['preflight_check_command']}",
        "",
        "Preflight Commands:",
    ]
    lines.extend(f"- {item}" for item in sheet["preflight_commands"])
    lines.extend(["", "Open Files:"])
    lines.extend(f"{index}. {item}" for index, item in enumerate(sheet["open_files"], start=1))
    lines.extend(["", "Opening Script:"])
    lines.extend(f"- {item}" for item in sheet["opening_script"])
    lines.extend(["", "Required Questions:"])
    lines.extend(f"{index}. {item}" for index, item in enumerate(sheet["required_questions"], start=1))
    lines.extend(["", "After Session:"])
    lines.extend(f"- {item}" for item in sheet["after_session"])
    lines.extend(["", "Boundary:"])
    lines.extend(f"- {item}" for item in sheet["boundary"])
    lines.append("")
    return "\n".join(lines)


def _section_lines(text: str, heading: str) -> list[str]:
    lines = text.splitlines()
    try:
        start = lines.index(heading) + 1
    except ValueError:
        return []
    section: list[str] = []
    for line in lines[start:]:
        if line.startswith("## ") and section:
            break
        section.append(line)
    return section


def _numbered_items_after(text: str, heading: str) -> list[str]:
    items: list[str] = []
    for line in _section_lines(text, heading):
        match = re.match(r"\d+\.\s+(.+)", line.strip())
        if match:
            items.append(match.group(1).strip("`"))
    return items


def _checklist_commands(text: str) -> list[str]:
    commands: list[str] = []
    for line in _section_lines(text, "## Preflight"):
        match = re.match(r"- \[ \] `(.+)`", line.strip())
        if match:
            commands.append(match.group(1))
    return commands


def _checklist_items_after(text: str, heading: str) -> list[str]:
    items: list[str] = []
    for line in _section_lines(text, heading):
        match = re.match(r"- \[ \] \"(.+)\"", line.strip())
        if match:
            items.append(match.group(1))
    return items


def main() -> int:
    parser = argparse.ArgumentParser(description="Render a public-safe operator run sheet for the real accountant session.")
    parser.add_argument("--packet", type=Path, default=DEFAULT_PACKET)
    parser.add_argument("--runbook", type=Path, default=DEFAULT_RUNBOOK)
    parser.add_argument("--checklist", type=Path, default=DEFAULT_CHECKLIST)
    parser.add_argument("--format", choices=["text", "json"], default="text")
    args = parser.parse_args()

    sheet = build_run_sheet(packet_path=args.packet, runbook_path=args.runbook, checklist_path=args.checklist)
    if args.format == "json":
        print(json.dumps(sheet, ensure_ascii=False, indent=2, sort_keys=True))
    else:
        print(render_text(sheet), end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
