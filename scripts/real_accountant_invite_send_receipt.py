from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.real_accountant_invite_packet import build_invite_packet  # noqa: E402


DEFAULT_TEMPLATE = ROOT / "docs" / "reports" / "real-accountant-session" / "invite-send-receipt.template.json"
DEFAULT_REPORT = ROOT / "docs" / "reports" / "real-accountant-session" / "2026-07-05-invite-send-receipt.md"
DEFAULT_INVITE_PACKET = ROOT / "docs" / "reports" / "real-accountant-session" / "2026-07-05-reviewer-invite-action-packet.md"

REQUIRED_BOOL_TRUE_FIELDS = {"no_raw_identifiers_requested"}
PUBLIC_UNSAFE_PATTERNS = [
    re.compile(pattern, re.IGNORECASE)
    for pattern in [
        r"api[_-]?key",
        r"token",
        r"source_body",
        r"customer[_-]?identifier",
        r"사업자번호",
        r"\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b",
    ]
]


def build_receipt_template() -> dict[str, Any]:
    packet = build_invite_packet()
    return {
        "reviewer_alias": packet["reviewer_alias"],
        "manual_send_completed": False,
        "channel": "manual",
        "sent_at": "YYYY-MM-DD",
        "invite_packet_path": DEFAULT_INVITE_PACKET.relative_to(ROOT).as_posix(),
        "ledger_update_command": packet["post_send_update_command"],
        "no_raw_identifiers_requested": True,
        "operator_attestation": "Fill after manual send. Do not include names, emails, customer identifiers, or source bodies.",
    }


def load_receipt(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def check_invite_send_receipt(receipt: dict[str, Any] | None = None, *, require_sent: bool = False) -> dict[str, Any]:
    receipt = build_receipt_template() if receipt is None else receipt
    errors: list[str] = []

    if not str(receipt.get("reviewer_alias", "")).startswith("reviewer-"):
        errors.append("reviewer_alias must be a public-safe alias like reviewer-001")
    if receipt.get("manual_send_completed") is not True and require_sent:
        errors.append("manual_send_completed must be true when --require-sent is used")
    if not receipt.get("channel"):
        errors.append("channel is required")
    sent_at = str(receipt.get("sent_at", ""))
    if require_sent and not re.fullmatch(r"\d{4}-\d{2}-\d{2}", sent_at):
        errors.append("sent_at must use YYYY-MM-DD")
    for field in REQUIRED_BOOL_TRUE_FIELDS:
        if receipt.get(field) is not True:
            errors.append(f"{field} must be true")

    command = str(receipt.get("ledger_update_command", ""))
    if "real_accountant_outreach_update.py" not in command:
        errors.append("ledger_update_command must use real_accountant_outreach_update.py")
    if "--status sent" not in command:
        errors.append("ledger_update_command must set --status sent")
    if f"--reviewer-alias {receipt.get('reviewer_alias')}" not in command:
        errors.append("ledger_update_command reviewer alias must match receipt reviewer_alias")

    if receipt.get("invite_packet_path") != DEFAULT_INVITE_PACKET.relative_to(ROOT).as_posix():
        errors.append("invite_packet_path must point to the reviewer invite action packet")

    unsafe_hits = _public_unsafe_hits(receipt)
    errors.extend(f"public safety: {hit}" for hit in unsafe_hits)

    return {
        "ok": not errors,
        "errors": errors,
        "title": "Real Accountant Invite Send Receipt",
        "actual_send_attested": receipt.get("manual_send_completed") is True and not errors,
        "require_sent": require_sent,
        "receipt": receipt,
        "template_path": _display_path(DEFAULT_TEMPLATE),
        "report_path": _display_path(DEFAULT_REPORT),
        "next_action": _next_action(receipt, errors, require_sent),
    }


def render_markdown(result: dict[str, Any]) -> str:
    receipt = result["receipt"]
    lines = [
        f"# {result['title']}",
        "",
        "> Scope: public-safe manual-send receipt template and validator for RS2 reviewer invite.",
        "",
        "## 한 줄 결론",
        "",
        _one_line_conclusion(result),
        "",
        "## Receipt Fields",
        "",
        f"- reviewer alias: `{receipt.get('reviewer_alias')}`",
        f"- manual send completed: {receipt.get('manual_send_completed')}",
        f"- channel: {receipt.get('channel')}",
        f"- sent at: {receipt.get('sent_at')}",
        f"- no raw identifiers requested: {receipt.get('no_raw_identifiers_requested')}",
        "",
        "## Required After Manual Send",
        "",
        "Run this ledger update only after the invite was actually sent:",
        "",
        "```powershell",
        str(receipt.get("ledger_update_command", "")),
        "```",
        "",
        "Then verify the transition:",
        "",
        "```powershell",
        "python scripts\\real_accountant_outreach_transition_verify.py --expected-status sent --format text",
        "```",
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


def write_template(path: Path = DEFAULT_TEMPLATE) -> dict[str, Any]:
    template = build_receipt_template()
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(template, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return template


def write_report(result: dict[str, Any], path: Path = DEFAULT_REPORT) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(render_markdown(result), encoding="utf-8")


def _public_unsafe_hits(receipt: dict[str, Any]) -> list[str]:
    serialized = json.dumps(receipt, ensure_ascii=False, sort_keys=True)
    hits: list[str] = []
    for pattern in PUBLIC_UNSAFE_PATTERNS:
        if pattern.search(serialized):
            hits.append(f"receipt contains forbidden pattern `{pattern.pattern}`")
    return hits


def _one_line_conclusion(result: dict[str, Any]) -> str:
    if result["actual_send_attested"]:
        return "Manual invite send is attested in a public-safe receipt; update and verify the outreach ledger."
    if result["ok"] and not result["require_sent"]:
        return "Receipt template is ready. It does not claim the invite was sent."
    return "Invite send receipt is not valid for a sent-state claim; fix the listed errors before using it."


def _next_action(receipt: dict[str, Any], errors: list[str], require_sent: bool) -> str:
    if errors:
        return "fix_receipt"
    if receipt.get("manual_send_completed") is True:
        return "update_outreach_ledger_to_sent_and_verify"
    if require_sent:
        return "complete_manual_send_receipt"
    return "send_reviewer_invite_then_fill_receipt"


def _display_path(path: Path) -> str:
    try:
        return path.resolve().relative_to(ROOT).as_posix()
    except ValueError:
        return path.as_posix()


def main() -> None:
    parser = argparse.ArgumentParser(description="Build or validate a public-safe real accountant invite send receipt.")
    parser.add_argument("--receipt", type=Path)
    parser.add_argument("--require-sent", action="store_true")
    parser.add_argument("--write-template", action="store_true")
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--out", type=Path, default=DEFAULT_REPORT)
    parser.add_argument("--format", choices=["text", "json", "markdown"], default="text")
    args = parser.parse_args()

    if args.write_template:
        write_template()

    receipt = load_receipt(args.receipt) if args.receipt else None
    result = check_invite_send_receipt(receipt, require_sent=args.require_sent)
    if args.write:
        write_report(result, args.out)

    if args.format == "json":
        print(json.dumps(result, ensure_ascii=False, indent=2, default=str))
    elif args.format == "markdown":
        print(render_markdown(result), end="")
    else:
        print(f"ok: {result['ok']}")
        print(f"actual_send_attested: {result['actual_send_attested']}")
        print(f"next_action: {result['next_action']}")
        print(f"template: {result['template_path']}")
        print(f"report: {result['report_path']}")
        for error in result["errors"]:
            print(f"- {error}")

    if not result["ok"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
