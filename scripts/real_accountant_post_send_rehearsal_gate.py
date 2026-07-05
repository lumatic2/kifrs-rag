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

from scripts.real_accountant_invite_send_receipt import (  # noqa: E402
    build_receipt_template,
    check_invite_send_receipt,
)
from scripts.real_accountant_outreach_transition_verify import verify_transition  # noqa: E402
from scripts.real_accountant_outreach_update import upsert_outreach  # noqa: E402


DEFAULT_LEDGER = ROOT / "docs" / "reports" / "real-accountant-session" / "outreach-log.sample.jsonl"
REPORT_PATH = ROOT / "docs" / "reports" / "real-accountant-session" / "2026-07-05-post-send-rehearsal-gate.md"


def build_filled_receipt() -> dict[str, Any]:
    receipt = build_receipt_template()
    receipt.update(
        {
            "manual_send_completed": True,
            "sent_at": "2026-07-05",
            "operator_attestation": "Synthetic rehearsal only; no real reviewer identity or message delivery is recorded.",
        }
    )
    return receipt


def check_post_send_rehearsal(*, ledger: Path = DEFAULT_LEDGER) -> dict[str, Any]:
    receipt = build_filled_receipt()
    receipt_result = check_invite_send_receipt(receipt, require_sent=True)
    errors = list(receipt_result["errors"])
    simulation = _simulate_sent_ledger(ledger, receipt) if receipt_result["ok"] else None
    if simulation and not simulation["ok"]:
        errors.extend(f"simulation: {error}" for error in simulation["errors"])

    return {
        "ok": not errors,
        "errors": errors,
        "title": "Real Accountant Post-Send Rehearsal Gate",
        "receipt_ok": receipt_result["ok"],
        "actual_send_attested": False,
        "source_ledger": _display_path(ledger),
        "receipt": receipt,
        "simulation": simulation,
        "report_path": _display_path(REPORT_PATH),
        "next_action": "after real send, fill receipt, update real ledger to sent, then verify transition",
    }


def render_markdown(result: dict[str, Any]) -> str:
    lines = [
        f"# {result['title']}",
        "",
        "> Scope: rehearse receipt validation plus sent-ledger transition without mutating the real outreach ledger.",
        "",
        "## 한 줄 결론",
        "",
        _one_line_conclusion(result),
        "",
        "## Rehearsal",
        "",
        f"- ok: {result['ok']}",
        f"- receipt ok: {result['receipt_ok']}",
        f"- actual send attested: {result['actual_send_attested']}",
        f"- source ledger: `{result['source_ledger']}`",
    ]
    if result["simulation"]:
        simulation = result["simulation"]
        lines.extend(
            [
                f"- copied ledger transition ok: {simulation['ok']}",
                f"- next-action status after copied ledger update: {simulation['next_action_status']}",
                f"- next-action command after copied ledger update: `{simulation['next_action_command']}`",
            ]
        )
    lines.extend(
        [
            "",
            "## Boundary",
            "",
            "- This gate does not send the invite.",
            "- This gate does not mutate the real outreach ledger.",
            "- This gate does not prove actual reviewer contact.",
        ]
    )
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


def write_report(*, ledger: Path = DEFAULT_LEDGER, out: Path = REPORT_PATH) -> dict[str, Any]:
    result = check_post_send_rehearsal(ledger=ledger)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(render_markdown(result), encoding="utf-8")
    return result


def _simulate_sent_ledger(ledger: Path, receipt: dict[str, Any]) -> dict[str, Any]:
    with tempfile.TemporaryDirectory() as tmp:
        copied_ledger = Path(tmp) / "outreach.jsonl"
        shutil.copyfile(ledger, copied_ledger)
        row = upsert_outreach(
            copied_ledger,
            reviewer_alias=receipt["reviewer_alias"],
            status="sent",
            channel=receipt["channel"],
            contacted_at=receipt["sent_at"],
            follow_up_by="2026-07-08",
            notes="invite sent",
        )
        verification = verify_transition(ledger=copied_ledger, expected_status="sent")
        return {
            "ok": verification["ok"],
            "errors": verification["errors"],
            "row": row,
            "outreach_counts": verification["outreach_counts"],
            "next_action_status": verification["next_action_status"],
            "next_action_command": verification["next_action_command"],
        }


def _one_line_conclusion(result: dict[str, Any]) -> str:
    if result["ok"]:
        return "Receipt validation and sent-ledger transition rehearse successfully on copied files; real send is still operator-owned."
    return "Post-send rehearsal failed; fix the listed errors before using the post-send path."


def _display_path(path: Path) -> str:
    try:
        return path.resolve().relative_to(ROOT).as_posix()
    except ValueError:
        return path.as_posix()


def main() -> None:
    parser = argparse.ArgumentParser(description="Rehearse receipt validation and sent-ledger transition without mutating real files.")
    parser.add_argument("--ledger", type=Path, default=DEFAULT_LEDGER)
    parser.add_argument("--format", choices=["text", "json", "markdown"], default="text")
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--out", type=Path, default=REPORT_PATH)
    args = parser.parse_args()

    result = write_report(ledger=args.ledger, out=args.out) if args.write else check_post_send_rehearsal(ledger=args.ledger)
    if args.format == "json":
        print(json.dumps(result, ensure_ascii=False, indent=2, default=str))
    elif args.format == "markdown":
        print(render_markdown(result), end="")
    else:
        print(f"ok: {result['ok']}")
        print(f"receipt_ok: {result['receipt_ok']}")
        print(f"actual_send_attested: {result['actual_send_attested']}")
        if result["simulation"]:
            print(f"copied_ledger_transition_ok: {result['simulation']['ok']}")
            print(f"next_action_status: {result['simulation']['next_action_status']}")
            print(f"next_action_command: {result['simulation']['next_action_command']}")
        for error in result["errors"]:
            print(f"- {error}")

    if not result["ok"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
