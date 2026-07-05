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

from scripts.real_accountant_invite_packet import build_invite_packet  # noqa: E402
from scripts.real_accountant_outreach_check import check_outreach  # noqa: E402
from scripts.real_accountant_outreach_update import upsert_outreach  # noqa: E402
from scripts.real_accountant_status import summarize_status  # noqa: E402


REPORT_PATH = ROOT / "docs" / "reports" / "real-accountant-session" / "2026-07-05-invite-dispatch-gate.md"
DEFAULT_INVITE = ROOT / "docs" / "reports" / "real-accountant-session" / "2026-07-05-session-invite.md"
DEFAULT_LEDGER = ROOT / "docs" / "reports" / "real-accountant-session" / "outreach-log.sample.jsonl"
RELATIVE_LEDGER = Path("docs/reports/real-accountant-session/outreach-log.sample.jsonl")
DEFAULT_MANIFEST = ROOT / "docs" / "reports" / "real-accountant-session" / "session_manifest.json"


def check_invite_dispatch_gate() -> dict[str, Any]:
    packet = build_invite_packet(invite_path=DEFAULT_INVITE, ledger_path=RELATIVE_LEDGER)
    current_ok, current_errors, current_counts = check_outreach(DEFAULT_LEDGER)
    status = summarize_status(root=ROOT, manifest=DEFAULT_MANIFEST, outreach_ledger=DEFAULT_LEDGER)
    errors: list[str] = []

    if not current_ok:
        errors.extend(f"current_outreach: {error}" for error in current_errors)
    if current_counts.get("not_sent", 0) < 1:
        errors.append("current outreach ledger should contain at least one not_sent reviewer alias before dispatch")
    if current_counts.get("sent", 0) or current_counts.get("scheduled", 0) or current_counts.get("completed", 0):
        errors.append("current sample outreach ledger should not claim sent/scheduled/completed reviewer evidence")
    if packet["reviewer_alias"] != "reviewer-001":
        errors.append("invite packet must use reviewer-001 public-safe alias by default")
    for protected in ("customer_name", "client_name", "company_name", "business_registration_number", "source_body"):
        if protected in json.dumps(packet, ensure_ascii=False):
            errors.append(f"invite packet contains protected marker: {protected}")

    simulation = _simulate_post_send_update()
    if simulation["ok"] is not True:
        errors.extend(f"post_send_simulation: {error}" for error in simulation["errors"])

    return {
        "ok": not errors,
        "errors": errors,
        "gate_id": "rs2-invite-dispatch-gate",
        "invite_path": _display_path(DEFAULT_INVITE),
        "ledger_path": _display_path(DEFAULT_LEDGER),
        "reviewer_alias": packet["reviewer_alias"],
        "subject": packet["subject"],
        "current_outreach_counts": current_counts,
        "current_next_action": status["next_action"],
        "post_send_update_command": packet["post_send_update_command"],
        "post_send_simulation": simulation,
        "boundary": [
            "This gate does not send the invite.",
            "The operator must send the message manually and then run the generated ledger update command.",
            "No raw contracts, customer identifiers, company names, or private source bodies should be requested.",
        ],
        "report_path": _display_path(REPORT_PATH),
        "next_leaf": "operator sends reviewer invite, updates outreach ledger to sent, then schedules RS2 session",
    }


def render_report(result: dict[str, Any]) -> str:
    lines = [
        "# RS2 Invite Dispatch Gate",
        "",
        "> Scope: pre-send gate for the real accountant reviewer invite and post-send ledger update path.",
        "",
        "## 한 줄 결론",
        "",
        "The reviewer invite is ready for manual dispatch. This gate proves the current ledger is still `not_sent`, the invite packet uses a public-safe alias, and the generated post-send command can move a copied ledger to `sent` without protected identifiers.",
        "",
        "## Current State",
        "",
        f"- ok: {result['ok']}",
        f"- invite: `{result['invite_path']}`",
        f"- ledger: `{result['ledger_path']}`",
        f"- reviewer alias: `{result['reviewer_alias']}`",
        f"- subject: {result['subject']}",
        f"- current outreach counts: {result['current_outreach_counts']}",
        f"- current next action: {result['current_next_action']}",
        "",
        "## After Manual Send",
        "",
        "Run this command after the operator actually sends the invite:",
        "",
        "```powershell",
        str(result["post_send_update_command"]),
        "```",
        "",
        "## Post-Send Simulation",
        "",
        f"- ok: {result['post_send_simulation']['ok']}",
        f"- counts after simulation: {result['post_send_simulation']['counts']}",
        f"- simulated row: `{result['post_send_simulation']['row']}`",
        "",
        "## Boundary",
        "",
    ]
    lines.extend(f"- {item}" for item in result["boundary"])
    lines.extend([
        "",
        "## Next Leaf",
        "",
        str(result["next_leaf"]),
        "",
        "## Machine Result",
        "",
        "```json",
        json.dumps(result, ensure_ascii=False, indent=2, default=str),
        "```",
    ])
    return "\n".join(lines) + "\n"


def write_report() -> dict[str, Any]:
    result = check_invite_dispatch_gate()
    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    REPORT_PATH.write_text(render_report(result), encoding="utf-8")
    return result


def _simulate_post_send_update() -> dict[str, Any]:
    with tempfile.TemporaryDirectory() as tmp:
        temp_ledger = Path(tmp) / "outreach-log.sample.jsonl"
        shutil.copyfile(DEFAULT_LEDGER, temp_ledger)
        row = upsert_outreach(
            temp_ledger,
            reviewer_alias="reviewer-001",
            status="sent",
            channel="manual",
            contacted_at="2026-07-05",
            follow_up_by="2026-07-08",
            notes="invite sent",
        )
        ok, errors, counts = check_outreach(temp_ledger)
        if counts.get("sent", 0) != 1:
            errors.append(f"expected sent count 1, got {counts.get('sent', 0)}")
        if row.get("invite_sent") is not True:
            errors.append("simulated row must have invite_sent true")
        return {
            "ok": ok and not errors,
            "errors": errors,
            "counts": counts,
            "row": row,
        }


def _display_path(path: Path) -> str:
    try:
        return path.resolve().relative_to(ROOT).as_posix()
    except ValueError:
        return path.as_posix()


def main() -> None:
    parser = argparse.ArgumentParser(description="Check real accountant invite dispatch readiness.")
    parser.add_argument("--format", choices=["text", "json", "markdown"], default="text")
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()

    result = write_report() if args.write else check_invite_dispatch_gate()
    if args.format == "json":
        print(json.dumps(result, ensure_ascii=False, indent=2, default=str))
    elif args.format == "markdown":
        print(render_report(result), end="")
    else:
        print(f"ok: {result['ok']}")
        print(f"reviewer_alias: {result['reviewer_alias']}")
        print(f"current_counts: {result['current_outreach_counts']}")
        print(f"post_send_simulation: {result['post_send_simulation']}")
        print(f"next_leaf: {result['next_leaf']}")
        for error in result["errors"]:
            print(f"- {error}")

    if not result["ok"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
