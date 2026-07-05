from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
TEMPLATE_PATH = ROOT / "docs" / "reports" / "real-accountant-session" / "invite-send-receipt.template.json"
REPORT_PATH = ROOT / "docs" / "reports" / "real-accountant-session" / "2026-07-05-filled-receipt-guide.md"
APPLY_COMMAND = (
    "python scripts\\real_accountant_apply_invite_receipt.py "
    "--receipt docs\\reports\\real-accountant-session\\invite-send-receipt.template.json "
    "--ledger docs/reports/real-accountant-session/outreach-log.sample.jsonl --format text"
)
VERIFY_COMMAND = (
    "python scripts\\real_accountant_outreach_transition_verify.py "
    "--expected-status sent --format text"
)


def build_filled_receipt_guide() -> dict[str, Any]:
    return {
        "title": "Real Accountant Filled Receipt Guide",
        "template_path": _display_path(TEMPLATE_PATH),
        "report_path": _display_path(REPORT_PATH),
        "required_edits_after_manual_send": [
            "Set manual_send_completed to true only after the invite was actually sent.",
            "Set sent_at to the actual YYYY-MM-DD send date.",
            "Keep reviewer_alias public-safe, for example reviewer-001.",
            "Keep no_raw_identifiers_requested true.",
            "Keep operator_attestation free of names, emails, customer identifiers, source bodies, credentials, and secrets.",
        ],
        "apply_command": APPLY_COMMAND,
        "verify_command": VERIFY_COMMAND,
        "boundaries": [
            "This guide does not send the reviewer invite.",
            "This guide does not mark actual send evidence.",
            "Do not fill or apply the receipt until the invite was actually sent.",
            "Use the receipt-apply command instead of directly editing the outreach ledger.",
        ],
        "next_action": "send_reviewer_invite_then_fill_receipt_apply_and_verify",
    }


def render_markdown(guide: dict[str, Any]) -> str:
    lines = [
        f"# {guide['title']}",
        "",
        "> Scope: operator guide for filling the RS2 invite-send receipt after a real manual send.",
        "",
        "## One-Line Result",
        "",
        "After the reviewer invite is actually sent, fill the receipt template with public-safe facts, apply it through the receipt validator, then verify the outreach ledger routes to sent-state handling.",
        "",
        "## Template",
        "",
        f"- `{guide['template_path']}`",
        "",
        "## Required Edits After Manual Send",
        "",
    ]
    lines.extend(f"- {item}" for item in guide["required_edits_after_manual_send"])
    lines.extend(
        [
            "",
            "## Apply",
            "",
            "Run only after the receipt is filled from an actual manual send:",
            "",
            "```powershell",
            guide["apply_command"],
            "```",
            "",
            "## Verify",
            "",
            "Confirm the ledger now routes to the post-invite reviewer response path:",
            "",
            "```powershell",
            guide["verify_command"],
            "```",
            "",
            "## Boundaries",
            "",
        ]
    )
    lines.extend(f"- {item}" for item in guide["boundaries"])
    lines.extend(
        [
            "",
            "## Machine Result",
            "",
            "```json",
            json.dumps(guide, ensure_ascii=False, indent=2),
            "```",
        ]
    )
    return "\n".join(lines) + "\n"


def write_report(path: Path = REPORT_PATH) -> dict[str, Any]:
    guide = build_filled_receipt_guide()
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(render_markdown(guide), encoding="utf-8")
    return guide


def _display_path(path: Path) -> str:
    try:
        return path.resolve().relative_to(ROOT).as_posix()
    except ValueError:
        return path.as_posix()


def main() -> None:
    parser = argparse.ArgumentParser(description="Render the public-safe guide for filling the real accountant invite receipt.")
    parser.add_argument("--format", choices=["text", "json", "markdown"], default="text")
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--out", type=Path, default=REPORT_PATH)
    args = parser.parse_args()

    guide = write_report(args.out) if args.write else build_filled_receipt_guide()

    if args.format == "json":
        print(json.dumps(guide, ensure_ascii=False, indent=2))
    elif args.format == "markdown":
        print(render_markdown(guide), end="")
    else:
        print(f"template: {guide['template_path']}")
        print(f"apply: {guide['apply_command']}")
        print(f"verify: {guide['verify_command']}")
        print(f"next_action: {guide['next_action']}")


if __name__ == "__main__":
    main()
