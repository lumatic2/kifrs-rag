from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.real_accountant_invite_send_receipt import check_invite_send_receipt, load_receipt  # noqa: E402
from scripts.real_accountant_outreach_transition_verify import verify_transition  # noqa: E402
from scripts.real_accountant_outreach_update import upsert_outreach  # noqa: E402


DEFAULT_LEDGER = ROOT / "docs" / "reports" / "real-accountant-session" / "outreach-log.sample.jsonl"
DEFAULT_DEMO_RECEIPT = ROOT / "docs" / "reports" / "real-accountant-session" / "invite-receipt-apply.demo.json"
REPORT_PATH = ROOT / "docs" / "reports" / "real-accountant-session" / "2026-07-05-invite-receipt-apply.md"


def apply_invite_receipt(
    *,
    receipt_path: Path,
    ledger: Path = DEFAULT_LEDGER,
    dry_run: bool = False,
) -> dict[str, Any]:
    receipt = load_receipt(receipt_path)
    receipt_result = check_invite_send_receipt(receipt, require_sent=True)
    errors = list(receipt_result["errors"])
    row: dict[str, Any] | None = None
    verification: dict[str, Any] | None = None

    if receipt_result["ok"] and not dry_run:
        row = upsert_outreach(
            ledger,
            reviewer_alias=receipt["reviewer_alias"],
            status="sent",
            channel=receipt["channel"],
            contacted_at=receipt["sent_at"],
            follow_up_by="2026-07-08",
            notes="invite sent",
        )
        verification = verify_transition(ledger=ledger, expected_status="sent")
        if not verification["ok"]:
            errors.extend(f"transition: {error}" for error in verification["errors"])

    return {
        "ok": not errors,
        "errors": errors,
        "title": "Real Accountant Invite Receipt Apply",
        "dry_run": dry_run,
        "receipt_path": _display_path(receipt_path),
        "ledger": _display_path(ledger),
        "receipt_ok": receipt_result["ok"],
        "actual_send_attested": receipt_result["actual_send_attested"],
        "ledger_updated": row is not None and not dry_run,
        "row": row,
        "transition": verification,
        "report_path": _display_path(REPORT_PATH),
    }


def build_demo_receipt() -> dict[str, Any]:
    return {
        "reviewer_alias": "reviewer-001",
        "manual_send_completed": True,
        "channel": "manual",
        "sent_at": "2026-07-05",
        "invite_packet_path": "docs/reports/real-accountant-session/2026-07-05-reviewer-invite-action-packet.md",
        "ledger_update_command": (
            "python scripts\\real_accountant_outreach_update.py "
            "--ledger docs/reports/real-accountant-session/outreach-log.sample.jsonl "
            "--reviewer-alias reviewer-001 --status sent --channel manual "
            "--contacted-at 2026-07-05 --follow-up-by 2026-07-08 --notes \"invite sent\""
        ),
        "no_raw_identifiers_requested": True,
        "operator_attestation": "Synthetic apply smoke only; no real reviewer contact is attested.",
    }


def write_demo_receipt(path: Path = DEFAULT_DEMO_RECEIPT) -> dict[str, Any]:
    receipt = build_demo_receipt()
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(receipt, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return receipt


def render_markdown(result: dict[str, Any]) -> str:
    lines = [
        f"# {result['title']}",
        "",
        "> Scope: validate a filled invite-send receipt before applying the `sent` outreach ledger update.",
        "",
        "## 한 줄 결론",
        "",
        _one_line_conclusion(result),
        "",
        "## Apply Result",
        "",
        f"- ok: {result['ok']}",
        f"- dry run: {result['dry_run']}",
        f"- receipt: `{result['receipt_path']}`",
        f"- ledger: `{result['ledger']}`",
        f"- receipt ok: {result['receipt_ok']}",
        f"- actual send attested: {result['actual_send_attested']}",
        f"- ledger updated: {result['ledger_updated']}",
    ]
    if result["transition"]:
        lines.extend(
            [
                f"- next-action status: {result['transition']['next_action_status']}",
                f"- next-action command: `{result['transition']['next_action_command']}`",
            ]
        )
    if result["errors"]:
        lines.extend(["", "## Errors", ""])
        lines.extend(f"- {error}" for error in result["errors"])
    lines.extend(
        [
            "",
            "## Boundary",
            "",
            "- This command does not send the reviewer invite.",
            "- It only applies a ledger update when a filled receipt already attests manual send.",
            "- Do not run this against the real ledger until the invite was actually sent.",
            "",
            "## Machine Result",
            "",
            "```json",
            json.dumps(result, ensure_ascii=False, indent=2, default=str),
            "```",
        ]
    )
    return "\n".join(lines) + "\n"


def write_report(result: dict[str, Any], path: Path = REPORT_PATH) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(render_markdown(result), encoding="utf-8")


def _one_line_conclusion(result: dict[str, Any]) -> str:
    if result["ok"] and result["ledger_updated"]:
        return "Filled receipt was validated and the outreach ledger now routes to reviewer-response handling."
    if result["ok"] and result["dry_run"]:
        return "Filled receipt is valid; dry run did not mutate the outreach ledger."
    return "Invite receipt was not applied; fix the listed errors before updating the outreach ledger."


def _display_path(path: Path) -> str:
    try:
        return path.resolve().relative_to(ROOT).as_posix()
    except ValueError:
        return path.as_posix()


def main() -> None:
    parser = argparse.ArgumentParser(description="Validate a filled invite receipt and apply the sent outreach ledger update.")
    parser.add_argument("--receipt", type=Path)
    parser.add_argument("--demo-receipt", action="store_true", help="Write and use a synthetic public-safe demo receipt.")
    parser.add_argument("--ledger", type=Path, default=DEFAULT_LEDGER)
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--format", choices=["text", "json", "markdown"], default="text")
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--out", type=Path, default=REPORT_PATH)
    args = parser.parse_args()

    if args.demo_receipt:
        write_demo_receipt()
        receipt_path = DEFAULT_DEMO_RECEIPT
    elif args.receipt:
        receipt_path = args.receipt
    else:
        parser.error("--receipt is required unless --demo-receipt is used")

    result = apply_invite_receipt(receipt_path=receipt_path, ledger=args.ledger, dry_run=args.dry_run)
    if args.write:
        write_report(result, args.out)

    if args.format == "json":
        print(json.dumps(result, ensure_ascii=False, indent=2, default=str))
    elif args.format == "markdown":
        print(render_markdown(result), end="")
    else:
        print(f"ok: {result['ok']}")
        print(f"dry_run: {result['dry_run']}")
        print(f"receipt_ok: {result['receipt_ok']}")
        print(f"actual_send_attested: {result['actual_send_attested']}")
        print(f"ledger_updated: {result['ledger_updated']}")
        if result["transition"]:
            print(f"next_action_status: {result['transition']['next_action_status']}")
            print(f"next_action_command: {result['transition']['next_action_command']}")
        for error in result["errors"]:
            print(f"- {error}")

    if not result["ok"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
