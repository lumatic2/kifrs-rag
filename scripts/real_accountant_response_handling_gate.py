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


REPORT_PATH = ROOT / "docs" / "reports" / "real-accountant-session" / "2026-07-05-response-handling-gate.md"
DEFAULT_LEDGER = ROOT / "docs" / "reports" / "real-accountant-session" / "outreach-log.sample.jsonl"
RELATIVE_LEDGER = Path("docs/reports/real-accountant-session/outreach-log.sample.jsonl")
EXPECTED_STATUS = {"follow_up": "sent", "schedule": "scheduled", "decline": "declined"}


def check_response_handling_gate() -> dict[str, Any]:
    current_ok, current_errors, current_counts = check_outreach(DEFAULT_LEDGER)
    errors: list[str] = []
    if not current_ok:
        errors.extend(f"current_outreach: {error}" for error in current_errors)

    packets: dict[str, dict[str, Any]] = {}
    simulations: dict[str, dict[str, Any]] = {}
    for response in sorted(ALLOWED_RESPONSE):
        packet = build_response_packet(response=response, ledger_path=RELATIVE_LEDGER)
        packet_text = json.dumps(packet, ensure_ascii=False)
        for protected in ("customer_name", "client_name", "company_name", "business_registration_number", "source_body"):
            if protected in packet_text:
                errors.append(f"{response} packet contains protected marker: {protected}")
        if f"--status {EXPECTED_STATUS[response]}" not in packet["ledger_update_command"]:
            errors.append(f"{response} packet command does not set {EXPECTED_STATUS[response]}")
        packets[response] = {
            "reviewer_alias": packet["reviewer_alias"],
            "response": packet["response"],
            "ledger_update_command": packet["ledger_update_command"],
            "message_preview": str(packet["message"]).splitlines()[0],
        }

        simulation = _simulate_response_update(response)
        simulations[response] = simulation
        if simulation["ok"] is not True:
            errors.extend(f"{response}_simulation: {error}" for error in simulation["errors"])

    return {
        "ok": not errors,
        "errors": errors,
        "gate_id": "rs2-response-handling-gate",
        "ledger_path": _display_path(DEFAULT_LEDGER),
        "current_outreach_counts": current_counts,
        "response_packets": packets,
        "response_simulations": simulations,
        "boundary": [
            "This gate does not contact the reviewer.",
            "The operator handles the real reply manually, then runs the matching ledger update command.",
            "Scheduling details that identify a person stay outside the public repo.",
            "Declines are valid RS2 outcomes but do not satisfy actual feedback evidence.",
        ],
        "report_path": _display_path(REPORT_PATH),
        "next_leaf": "operator handles reviewer reply, updates outreach ledger, then either schedules RS2 or records decline",
    }


def render_report(result: dict[str, Any]) -> str:
    lines = [
        "# RS2 Response Handling Gate",
        "",
        "> Scope: verify public-safe follow-up, schedule, and decline handling after the reviewer invite is sent.",
        "",
        "## 한 줄 결론",
        "",
        "The RS2 response path is ready: follow-up keeps the alias at `sent`, schedule moves a copied ledger to `scheduled`, and decline moves it to `declined` without protected identifiers. This gate does not contact the reviewer.",
        "",
        "## Current State",
        "",
        f"- ok: {result['ok']}",
        f"- ledger: `{result['ledger_path']}`",
        f"- current outreach counts: {result['current_outreach_counts']}",
        "",
        "## Response Commands",
        "",
    ]
    for response, packet in result["response_packets"].items():
        lines.extend(
            [
                f"### {response}",
                "",
                f"- message preview: {packet['message_preview']}",
                "",
                "```powershell",
                str(packet["ledger_update_command"]),
                "```",
                "",
            ]
        )

    lines.extend(["## Simulations", ""])
    for response, simulation in result["response_simulations"].items():
        lines.extend(
            [
                f"- {response}: ok={simulation['ok']}, expected_status={simulation['expected_status']}, counts={simulation['counts']}",
            ]
        )

    lines.extend([
        "",
        "## Boundary",
        "",
    ])
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
    result = check_response_handling_gate()
    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    REPORT_PATH.write_text(render_report(result), encoding="utf-8")
    return result


def _simulate_response_update(response: str) -> dict[str, Any]:
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
        ok, errors, counts = check_outreach(temp_ledger)
        if counts.get(expected_status, 0) != 1:
            errors.append(f"expected {expected_status} count 1, got {counts.get(expected_status, 0)}")
        if expected_status in {"sent", "scheduled", "declined"} and row.get("invite_sent") is not True:
            errors.append(f"{expected_status} row must keep invite_sent true")
        return {
            "ok": ok and not errors,
            "errors": errors,
            "expected_status": expected_status,
            "counts": counts,
            "row": row,
        }


def _display_path(path: Path) -> str:
    try:
        return path.resolve().relative_to(ROOT).as_posix()
    except ValueError:
        return path.as_posix()


def main() -> None:
    parser = argparse.ArgumentParser(description="Check real accountant outreach response handling readiness.")
    parser.add_argument("--format", choices=["text", "json", "markdown"], default="text")
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()

    result = write_report() if args.write else check_response_handling_gate()
    if args.format == "json":
        print(json.dumps(result, ensure_ascii=False, indent=2, default=str))
    elif args.format == "markdown":
        print(render_report(result), end="")
    else:
        print(f"ok: {result['ok']}")
        print(f"current_counts: {result['current_outreach_counts']}")
        for response, simulation in result["response_simulations"].items():
            print(f"{response}: ok={simulation['ok']} expected_status={simulation['expected_status']} counts={simulation['counts']}")
        print(f"next_leaf: {result['next_leaf']}")
        for error in result["errors"]:
            print(f"- {error}")

    if not result["ok"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
