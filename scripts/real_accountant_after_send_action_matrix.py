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

from scripts.real_accountant_outreach_check import check_outreach  # noqa: E402
from scripts.real_accountant_outreach_update import upsert_outreach  # noqa: E402
from scripts.real_accountant_response_packet import ALLOWED_RESPONSE, build_response_packet  # noqa: E402
from scripts.real_accountant_status import summarize_status  # noqa: E402


REPORT_PATH = ROOT / "docs" / "reports" / "real-accountant-session" / "2026-07-05-after-send-action-matrix.md"
DEFAULT_LEDGER = ROOT / "docs" / "reports" / "real-accountant-session" / "outreach-log.sample.jsonl"
DEFAULT_MANIFEST = ROOT / "docs" / "reports" / "real-accountant-session" / "session_manifest.json"
RELATIVE_LEDGER = Path("docs/reports/real-accountant-session/outreach-log.sample.jsonl")
EXPECTED_STATUS = {"follow_up": "sent", "schedule": "scheduled", "decline": "declined"}
EXPECTED_NEXT_ACTION_FRAGMENT = {
    "follow_up": "Schedule the reviewer session",
    "schedule": "Run the scheduled accountant session",
    "decline": "invite another reviewer or pause RS2",
}


def build_after_send_action_matrix() -> dict[str, Any]:
    errors: list[str] = []
    rows: list[dict[str, Any]] = []

    for response in sorted(ALLOWED_RESPONSE):
        row = _simulate_response_path(response)
        rows.append(row)
        if row["ok"] is not True:
            errors.extend(f"{response}: {error}" for error in row["errors"])

    return {
        "ok": not errors,
        "errors": errors,
        "gate_id": "rs2-after-send-action-matrix",
        "rows": rows,
        "summary": {
            "total_rows": len(rows),
            "all_paths_public_safe": all(row["packet_public_safe"] for row in rows),
            "all_status_transitions_match": all(row["status_transition_matches"] for row in rows),
            "all_next_actions_match": all(row["next_action_matches"] for row in rows),
        },
        "boundary": [
            "This matrix starts from a copied sent ledger and does not contact the reviewer.",
            "It does not update the real outreach ledger.",
            "Scheduling details that identify a person stay outside the public repo.",
            "Decline is a valid response state, but it does not satisfy actual feedback evidence.",
        ],
        "report_path": _display_path(REPORT_PATH),
        "next_leaf": "after manual invite send, choose follow-up, schedule, or decline response packet and run the matching ledger command",
    }


def render_report(matrix: dict[str, Any]) -> str:
    lines = [
        "# RS2 After-Send Action Matrix",
        "",
        "> Scope: verify the operator choices after the reviewer invite has been manually sent.",
        "",
        "## 한 줄 결론",
        "",
        "After the invite is sent, the operator has three public-safe paths: follow-up keeps the alias at `sent`, schedule moves it to `scheduled`, and decline records `declined` while keeping the horizon open.",
        "",
        "## Summary",
        "",
        f"- ok: {matrix['ok']}",
        f"- total rows: {matrix['summary']['total_rows']}",
        f"- all paths public-safe: {matrix['summary']['all_paths_public_safe']}",
        f"- all status transitions match: {matrix['summary']['all_status_transitions_match']}",
        f"- all next actions match: {matrix['summary']['all_next_actions_match']}",
        "",
        "## Matrix",
        "",
        "| Response | Expected status | Counts | Next action | Command |",
        "|---|---|---|---|---|",
    ]
    for row in matrix["rows"]:
        lines.append(
            "| "
            f"{row['response']} | "
            f"{row['expected_status']} | "
            f"{row['counts']} | "
            f"{row['next_action']} | "
            f"`{row['ledger_update_command']}` |"
        )
    lines.extend(["", "## Boundary", ""])
    lines.extend(f"- {item}" for item in matrix["boundary"])
    lines.extend(
        [
            "",
            "## Next Leaf",
            "",
            str(matrix["next_leaf"]),
            "",
            "## Machine Result",
            "",
            "```json",
            json.dumps(matrix, ensure_ascii=False, indent=2, default=str),
            "```",
        ]
    )
    return "\n".join(lines) + "\n"


def write_report() -> dict[str, Any]:
    matrix = build_after_send_action_matrix()
    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    REPORT_PATH.write_text(render_report(matrix), encoding="utf-8")
    return matrix


def _simulate_response_path(response: str) -> dict[str, Any]:
    expected_status = EXPECTED_STATUS[response]
    with tempfile.TemporaryDirectory() as tmp:
        temp_ledger = Path(tmp) / "outreach-log.sample.jsonl"
        shutil.copyfile(DEFAULT_LEDGER, temp_ledger)
        upsert_outreach(
            temp_ledger,
            reviewer_alias="reviewer-001",
            status="sent",
            channel="manual",
            contacted_at="2026-07-05",
            follow_up_by="2026-07-08",
            notes="invite sent",
        )
        row = upsert_outreach(
            temp_ledger,
            reviewer_alias="reviewer-001",
            status=expected_status,
            channel="manual",
            contacted_at="2026-07-05",
            follow_up_by="2026-07-08",
            notes={"follow_up": "follow-up sent", "schedule": "session scheduled", "decline": "reviewer declined"}[response],
        )
        ok, outreach_errors, counts = check_outreach(temp_ledger)
        status = summarize_status(root=ROOT, manifest=DEFAULT_MANIFEST, outreach_ledger=temp_ledger)
        packet = build_response_packet(response=response, ledger_path=RELATIVE_LEDGER)
        packet_text = json.dumps(packet, ensure_ascii=False)
        protected_markers = ("customer_name", "client_name", "company_name", "business_registration_number", "source_body")
        packet_public_safe = not any(marker in packet_text for marker in protected_markers)
        status_transition_matches = counts.get(expected_status, 0) == 1 and row.get("invite_sent") is True
        next_action_matches = EXPECTED_NEXT_ACTION_FRAGMENT[response] in status["next_action"]

        errors = list(outreach_errors)
        if not packet_public_safe:
            errors.append("response packet contains protected marker")
        if not status_transition_matches:
            errors.append(f"expected {expected_status}=1 with invite_sent true, got counts={counts}, row={row}")
        if not next_action_matches:
            errors.append(f"unexpected next action: {status['next_action']}")

        return {
            "ok": ok and not errors,
            "errors": errors,
            "response": response,
            "expected_status": expected_status,
            "counts": counts,
            "row": row,
            "next_action": status["next_action"],
            "packet_public_safe": packet_public_safe,
            "status_transition_matches": status_transition_matches,
            "next_action_matches": next_action_matches,
            "ledger_update_command": packet["ledger_update_command"],
            "message_preview": str(packet["message"]).splitlines()[0],
        }


def _display_path(path: Path) -> str:
    try:
        return path.resolve().relative_to(ROOT).as_posix()
    except ValueError:
        return path.as_posix()


def main() -> None:
    parser = argparse.ArgumentParser(description="Build after-send response action matrix for the real accountant session.")
    parser.add_argument("--format", choices=["text", "json", "markdown"], default="text")
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()

    matrix = write_report() if args.write else build_after_send_action_matrix()
    if args.format == "json":
        print(json.dumps(matrix, ensure_ascii=False, indent=2, default=str))
    elif args.format == "markdown":
        print(render_report(matrix), end="")
    else:
        print(f"ok: {matrix['ok']}")
        print(f"summary: {matrix['summary']}")
        print(f"next_leaf: {matrix['next_leaf']}")
        for error in matrix["errors"]:
            print(f"- {error}")

    if not matrix["ok"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
