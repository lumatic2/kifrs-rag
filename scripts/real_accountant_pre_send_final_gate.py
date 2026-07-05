from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.real_accountant_capture_readiness_gate import check_capture_readiness_gate  # noqa: E402
from scripts.real_accountant_invite_dispatch_gate import check_invite_dispatch_gate  # noqa: E402
from scripts.real_accountant_operator_execution_brief import build_execution_brief  # noqa: E402
from scripts.real_accountant_response_handling_gate import check_response_handling_gate  # noqa: E402
from scripts.real_accountant_scheduled_session_gate import check_scheduled_session_gate  # noqa: E402
from scripts.real_accountant_status import summarize_status  # noqa: E402


REPORT_PATH = ROOT / "docs" / "reports" / "real-accountant-session" / "2026-07-05-pre-send-final-gate.md"
DEFAULT_MANIFEST = ROOT / "docs" / "reports" / "real-accountant-session" / "session_manifest.json"
DEFAULT_LEDGER = ROOT / "docs" / "reports" / "real-accountant-session" / "outreach-log.sample.jsonl"


def check_pre_send_final_gate() -> dict[str, Any]:
    errors: list[str] = []
    status = summarize_status(root=ROOT, manifest=DEFAULT_MANIFEST, outreach_ledger=DEFAULT_LEDGER)
    invite = check_invite_dispatch_gate()
    response = check_response_handling_gate()
    scheduled = check_scheduled_session_gate()
    capture = check_capture_readiness_gate()
    execution = build_execution_brief(root=ROOT)

    readiness = {
        "invite_dispatch": invite["ok"],
        "response_handling": response["ok"],
        "scheduled_session": scheduled["ok"],
        "capture_readiness": capture["ok"],
    }
    for name, ok in readiness.items():
        if ok is not True:
            errors.append(f"{name} gate failed")

    counts = status["outreach_counts"]
    if counts.get("not_sent", 0) < 1:
        errors.append("pre-send state requires at least one not_sent reviewer alias")
    if counts.get("sent", 0) or counts.get("scheduled", 0) or counts.get("completed", 0):
        errors.append("pre-send state must not already claim sent/scheduled/completed evidence")
    if status["session_mode"] != "ready_to_schedule":
        errors.append(f"session mode must remain ready_to_schedule before send, got {status['session_mode']}")
    if status["close_ready"] is not False:
        errors.append("close gate must not be ready before actual accountant evidence")

    run_order = execution["run_order"]
    if len(run_order) != 6:
        errors.append(f"execution brief should contain 6 run-order phases, got {len(run_order)}")
    joined_commands = "\n".join(command for step in run_order for command in step["commands"])
    for required in (
        "real_accountant_invite_packet.py",
        "real_accountant_outreach_update.py",
        "real_accountant_response_packet.py",
        "real_accountant_run_sheet.py",
        "real_accountant_capture.py",
        "real_accountant_close_check.py",
    ):
        if required not in joined_commands:
            errors.append(f"execution brief missing command: {required}")

    return {
        "ok": not errors,
        "errors": errors,
        "gate_id": "rs2-pre-send-final-gate",
        "status": {
            "session_mode": status["session_mode"],
            "close_ready": status["close_ready"],
            "next_action": status["next_action"],
            "outreach_counts": status["outreach_counts"],
        },
        "readiness_gates": readiness,
        "execution_run_order_phases": [step["phase"] for step in run_order],
        "post_send_update_command": invite["post_send_update_command"],
        "boundary": [
            "This final gate does not send the reviewer invite.",
            "It confirms the repo is still in pre-send state and ready for manual operator action.",
            "Actual reviewer identity, sending, scheduling, and feedback notes stay user/operator-owned.",
            "The horizon remains open until actual notes, capture manifest, queue JSONL, completed outreach, and close gate pass.",
        ],
        "report_path": _display_path(REPORT_PATH),
        "next_leaf": "operator sends the reviewer invite and runs the generated post-send ledger update command",
    }


def render_report(result: dict[str, Any]) -> str:
    lines = [
        "# RS2 Pre-Send Final Gate",
        "",
        "> Scope: final repository-side smoke before the operator manually sends the real accountant reviewer invite.",
        "",
        "## 한 줄 결론",
        "",
        "The repository-side pre-send path is ready: invite dispatch, response handling, scheduled-session, capture-readiness, and execution-brief checks all pass while the real ledger still does not claim sent or actual feedback evidence.",
        "",
        "## Current State",
        "",
        f"- ok: {result['ok']}",
        f"- session mode: {result['status']['session_mode']}",
        f"- close ready: {result['status']['close_ready']}",
        f"- next action: {result['status']['next_action']}",
        f"- outreach counts: {result['status']['outreach_counts']}",
        "",
        "## Readiness Gates",
        "",
    ]
    lines.extend(f"- {name}: {ok}" for name, ok in result["readiness_gates"].items())
    lines.extend(["", "## Execution Run Order", ""])
    lines.extend(f"- {phase}" for phase in result["execution_run_order_phases"])
    lines.extend(
        [
            "",
            "## After Manual Send",
            "",
            "```powershell",
            str(result["post_send_update_command"]),
            "```",
            "",
            "## Boundary",
            "",
        ]
    )
    lines.extend(f"- {item}" for item in result["boundary"])
    lines.extend(
        [
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
        ]
    )
    return "\n".join(lines) + "\n"


def write_report() -> dict[str, Any]:
    result = check_pre_send_final_gate()
    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    REPORT_PATH.write_text(render_report(result), encoding="utf-8")
    return result


def _display_path(path: Path) -> str:
    try:
        return path.resolve().relative_to(ROOT).as_posix()
    except ValueError:
        return path.as_posix()


def main() -> None:
    parser = argparse.ArgumentParser(description="Run final pre-send smoke for the real accountant session.")
    parser.add_argument("--format", choices=["text", "json", "markdown"], default="text")
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()

    result = write_report() if args.write else check_pre_send_final_gate()
    if args.format == "json":
        print(json.dumps(result, ensure_ascii=False, indent=2, default=str))
    elif args.format == "markdown":
        print(render_report(result), end="")
    else:
        print(f"ok: {result['ok']}")
        print(f"status: {result['status']}")
        print(f"readiness_gates: {result['readiness_gates']}")
        print(f"next_leaf: {result['next_leaf']}")
        for error in result["errors"]:
            print(f"- {error}")

    if not result["ok"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
