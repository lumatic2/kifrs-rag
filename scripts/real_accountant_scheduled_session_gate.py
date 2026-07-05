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

from scripts.real_accountant_close_check import check_close_gate  # noqa: E402
from scripts.real_accountant_outreach_check import check_outreach  # noqa: E402
from scripts.real_accountant_outreach_update import upsert_outreach  # noqa: E402
from scripts.real_accountant_run_sheet import build_run_sheet  # noqa: E402
from scripts.real_accountant_status import summarize_status  # noqa: E402


REPORT_PATH = ROOT / "docs" / "reports" / "real-accountant-session" / "2026-07-05-scheduled-session-gate.md"
DEFAULT_LEDGER = ROOT / "docs" / "reports" / "real-accountant-session" / "outreach-log.sample.jsonl"
DEFAULT_MANIFEST = ROOT / "docs" / "reports" / "real-accountant-session" / "session_manifest.json"
NOTES_PATH = Path("docs/reports/real-accountant-session/actual-feedback-notes.md")


def check_scheduled_session_gate() -> dict[str, Any]:
    errors: list[str] = []
    simulation = _simulate_scheduled_state()
    if simulation["ok"] is not True:
        errors.extend(f"scheduled_simulation: {error}" for error in simulation["errors"])

    run_sheet = build_run_sheet()
    run_sheet_ready = _check_run_sheet(run_sheet)
    if run_sheet_ready["ok"] is not True:
        errors.extend(f"run_sheet: {error}" for error in run_sheet_ready["errors"])

    close_blocked = simulation["close_ready"] is False
    if not close_blocked:
        errors.append("scheduled state must not satisfy close gate without actual feedback evidence")

    return {
        "ok": not errors,
        "errors": errors,
        "gate_id": "rs2-scheduled-session-gate",
        "ledger_path": _display_path(DEFAULT_LEDGER),
        "manifest_path": _display_path(DEFAULT_MANIFEST),
        "scheduled_simulation": simulation,
        "run_sheet_ready": run_sheet_ready,
        "notes_scaffold_command": _notes_scaffold_command(),
        "close_gate_correctly_blocked": close_blocked,
        "boundary": [
            "This gate does not schedule the reviewer.",
            "It only proves that a copied ledger in scheduled state routes the operator to run-day execution.",
            "The real session manifest remains ready_to_schedule until actual public-safe feedback notes, capture manifest, and queue records exist.",
            "Close remains blocked without completed outreach and actual feedback evidence.",
        ],
        "report_path": _display_path(REPORT_PATH),
        "next_leaf": "run the scheduled accountant session, write actual-feedback-notes.md, then capture RS3 evidence",
    }


def render_report(result: dict[str, Any]) -> str:
    simulation = result["scheduled_simulation"]
    run_sheet = result["run_sheet_ready"]
    lines = [
        "# RS2 Scheduled Session Gate",
        "",
        "> Scope: verify the run-day path once a real accountant reviewer is scheduled, without claiming actual feedback evidence.",
        "",
        "## 한 줄 결론",
        "",
        "A copied outreach ledger can move to `scheduled` and the status command then routes the operator to run the session and write actual notes. The close gate still fails, which is correct until actual feedback evidence exists.",
        "",
        "## Scheduled Simulation",
        "",
        f"- ok: {simulation['ok']}",
        f"- counts: {simulation['counts']}",
        f"- next action: {simulation['status_next_action']}",
        f"- session mode: {simulation['session_mode']}",
        f"- close ready: {simulation['close_ready']}",
        f"- close errors: {simulation['close_errors']}",
        "",
        "## Run Sheet Readiness",
        "",
        f"- ok: {run_sheet['ok']}",
        f"- checked commands: {run_sheet['checked_commands']}",
        f"- checked open files: {run_sheet['checked_open_files']}",
        f"- checked after-session items: {run_sheet['checked_after_session']}",
        "",
        "## Notes Scaffold Command",
        "",
        "```powershell",
        str(result["notes_scaffold_command"]),
        "```",
        "",
        "## Boundary",
        "",
    ]
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
    result = check_scheduled_session_gate()
    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    REPORT_PATH.write_text(render_report(result), encoding="utf-8")
    return result


def _simulate_scheduled_state() -> dict[str, Any]:
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
            status="scheduled",
            channel="manual",
            contacted_at="2026-07-05",
            follow_up_by="2026-07-08",
            notes="session scheduled",
        )
        outreach_ok, outreach_errors, counts = check_outreach(temp_ledger)
        status = summarize_status(root=ROOT, manifest=DEFAULT_MANIFEST, outreach_ledger=temp_ledger)
        close_ok, close_errors, close_evidence = check_close_gate(
            root=ROOT,
            manifest_path=DEFAULT_MANIFEST,
            outreach_ledger=temp_ledger,
            run_quality=False,
        )

        errors = list(outreach_errors)
        if counts.get("scheduled", 0) != 1:
            errors.append(f"expected scheduled count 1, got {counts.get('scheduled', 0)}")
        if row.get("invite_sent") is not True:
            errors.append("scheduled row must keep invite_sent true")
        if "Run the scheduled accountant session" not in status["next_action"]:
            errors.append(f"scheduled status should route to run-day execution, got: {status['next_action']}")
        if status["session_mode"] != "ready_to_schedule":
            errors.append(f"scheduled simulation must not change session manifest mode, got {status['session_mode']}")
        if close_ok:
            errors.append("close gate unexpectedly passed without actual feedback evidence")

        return {
            "ok": outreach_ok and not errors,
            "errors": errors,
            "counts": counts,
            "row": row,
            "status_next_action": status["next_action"],
            "session_mode": status["session_mode"],
            "close_ready": close_ok,
            "close_errors": close_errors,
            "close_evidence": close_evidence,
        }


def _check_run_sheet(run_sheet: dict[str, Any]) -> dict[str, Any]:
    errors: list[str] = []
    commands = run_sheet["preflight_commands"]
    open_files = run_sheet["open_files"]
    after_session = run_sheet["after_session"]

    required_commands = [
        "real_accountant_invite_dispatch_gate.py",
        "real_accountant_response_handling_gate.py",
        "real_accountant_scheduled_session_gate.py",
        "demo_poc.py",
    ]
    for command in required_commands:
        if not any(command in item for item in commands):
            errors.append(f"missing preflight command: {command}")

    required_open_files = [
        "docs/reports/field-feedback/2026-07-05-feedback-questionnaire.md",
        "docs/reports/2026-07-05-accounting-intelligence-gap-audit.md",
    ]
    for item in required_open_files:
        if item not in open_files:
            errors.append(f"missing open file: {item}")

    required_after_session = ["real_accountant_notes_check.py", "real_accountant_capture.py", "real_accountant_close_check.py"]
    for item in required_after_session:
        if not any(item in line for line in after_session):
            errors.append(f"missing after-session item: {item}")

    return {
        "ok": not errors,
        "errors": errors,
        "checked_commands": required_commands,
        "checked_open_files": required_open_files,
        "checked_after_session": required_after_session,
    }


def _notes_scaffold_command() -> str:
    return (
        "python scripts\\real_accountant_notes_scaffold.py "
        f"--out {NOTES_PATH.as_posix()} "
        "--date 2026-07-05 "
        '--reviewer-role "CPA reviewer" '
        '--reviewer-service-line "F-ACC" '
        '--reviewer-experience-context "reviewed accounting advisory workpapers" '
        '--session-mode "async review"'
    )


def _display_path(path: Path) -> str:
    try:
        return path.resolve().relative_to(ROOT).as_posix()
    except ValueError:
        return path.as_posix()


def main() -> None:
    parser = argparse.ArgumentParser(description="Check scheduled real accountant session readiness without actual feedback claims.")
    parser.add_argument("--format", choices=["text", "json", "markdown"], default="text")
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()

    result = write_report() if args.write else check_scheduled_session_gate()
    if args.format == "json":
        print(json.dumps(result, ensure_ascii=False, indent=2, default=str))
    elif args.format == "markdown":
        print(render_report(result), end="")
    else:
        print(f"ok: {result['ok']}")
        print(f"scheduled_simulation: {result['scheduled_simulation']}")
        print(f"run_sheet_ready: {result['run_sheet_ready']}")
        print(f"close_gate_correctly_blocked: {result['close_gate_correctly_blocked']}")
        print(f"next_leaf: {result['next_leaf']}")
        for error in result["errors"]:
            print(f"- {error}")

    if not result["ok"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
