from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.real_accountant_operator_brief import DEFAULT_LEDGER, DEFAULT_MANIFEST, build_operator_brief  # noqa: E402


REPORT_PATH = ROOT / "docs" / "reports" / "real-accountant-session" / "2026-07-05-operator-execution-brief.md"


def build_execution_brief(
    *,
    root: Path,
    manifest: Path = DEFAULT_MANIFEST,
    outreach_ledger: Path = DEFAULT_LEDGER,
) -> dict[str, Any]:
    operator = build_operator_brief(root=root, manifest=manifest, outreach_ledger=outreach_ledger)
    commands = operator["commands"]
    readiness_gates = {
        "invite_dispatch": "python scripts\\real_accountant_invite_dispatch_gate.py --format text --write",
        "response_handling": "python scripts\\real_accountant_response_handling_gate.py --format text --write",
        "scheduled_session": "python scripts\\real_accountant_scheduled_session_gate.py --format text --write",
        "capture_readiness": "python scripts\\real_accountant_capture_readiness_gate.py --format text --write",
    }
    return {
        "title": "Real Accountant Session Execution Brief",
        "horizon": operator["horizon"],
        "session_mode": operator["session_mode"],
        "close_ready": operator["close_ready"],
        "next_action": operator["next_action"],
        "blocked_by": operator["blocked_by"],
        "proof_snapshot": operator["proof_snapshot"],
        "send_now_subject": operator["send_now"]["subject"],
        "post_send_update_command": operator["send_now"]["post_send_update_command"],
        "readiness_gates": readiness_gates,
        "run_order": [
            {
                "phase": "1. Before sending",
                "operator_action": "Render the invite, check dispatch readiness, then send the message manually.",
                "commands": [commands["status"], commands["invite"], readiness_gates["invite_dispatch"]],
            },
            {
                "phase": "2. After sending",
                "operator_action": "Update the alias-only outreach ledger to sent.",
                "commands": [operator["send_now"]["post_send_update_command"]],
            },
            {
                "phase": "3. After reviewer reply",
                "operator_action": "Render the matching reply packet and update the ledger to follow-up, scheduled, or declined.",
                "commands": [commands["schedule_response"], readiness_gates["response_handling"]],
            },
            {
                "phase": "4. Session day",
                "operator_action": "Run the scheduled-session gate, open the run sheet, and conduct the 30-minute review.",
                "commands": [readiness_gates["scheduled_session"], commands["run_sheet"], commands["preflight"]],
            },
            {
                "phase": "5. After session",
                "operator_action": "Create public-safe notes, check them, capture queue records, and build the actual manifest.",
                "commands": [
                    readiness_gates["capture_readiness"],
                    commands["notes_scaffold"],
                    commands["notes_check"],
                    commands["capture"],
                    _manifest_build_command(),
                ],
            },
            {
                "phase": "6. Close",
                "operator_action": "Only close the horizon after completed outreach, actual notes, capture manifest, queue JSONL, and close gate pass.",
                "commands": [commands["close_gate"]],
            },
        ],
        "decisions": [
            "No repo-side product decision remains for this brief.",
            "The reviewer identity, real sending, scheduling, and actual feedback content are user/operator-owned.",
        ],
        "boundary": operator["boundary"],
        "report_path": _display_path(REPORT_PATH),
    }


def render_markdown(brief: dict[str, Any]) -> str:
    lines = [
        f"# {brief['title']}",
        "",
        "> Scope: one execution surface for RS2 invite, RS2 scheduling, RS3 notes capture, and RS4 close gate.",
        "",
        "## Current Position",
        "",
        f"- Horizon: {brief['horizon']}",
        f"- Session mode: {brief['session_mode']}",
        f"- Close ready: {brief['close_ready']}",
        f"- Next action: {brief['next_action']}",
        f"- Send subject: {brief['send_now_subject']}",
        "",
        "## Blocked By",
        "",
    ]
    lines.extend(f"- {item}" for item in brief["blocked_by"])
    snapshot = brief["proof_snapshot"]
    lines.extend(
        [
            "",
            "## Product Proof Snapshot",
            "",
            f"- Claim: {snapshot['objective_ready_claim']}",
            f"- Automation rate: {snapshot['automation_rate']:.2%}",
            f"- Review packs: {snapshot['automated_packs']} automated / {snapshot['total_review_packs']} total",
            f"- Needs human review: {snapshot['human_review_packs']}",
            "",
            "## Run Order",
            "",
        ]
    )
    for step in brief["run_order"]:
        lines.extend([f"### {step['phase']}", "", step["operator_action"], ""])
        for command in step["commands"]:
            lines.extend(["```powershell", str(command), "```", ""])
    lines.extend(["## Decisions", ""])
    lines.extend(f"- {item}" for item in brief["decisions"])
    lines.extend(["", "## Boundary", ""])
    lines.extend(f"- {item}" for item in brief["boundary"])
    lines.extend(["", "## Machine Result", "", "```json", json.dumps(brief, ensure_ascii=False, indent=2), "```"])
    return "\n".join(lines) + "\n"


def write_report() -> dict[str, Any]:
    brief = build_execution_brief(root=ROOT)
    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    REPORT_PATH.write_text(render_markdown(brief), encoding="utf-8")
    return brief


def _manifest_build_command() -> str:
    return (
        "python scripts\\real_accountant_manifest_build.py "
        "--out docs\\reports\\real-accountant-session\\session_manifest.json "
        "--notes docs\\reports\\real-accountant-session\\actual-feedback-notes.md "
        "--capture-manifest docs\\reports\\real-accountant-session\\capture-manifest.json "
        "--queue-jsonl docs\\reports\\real-accountant-session\\feedback-queue.jsonl "
        '--reviewer-role "CPA reviewer" '
        '--reviewer-service-line "F-ACC" '
        '--reviewer-experience-context "reviewed accounting advisory workpapers"'
    )


def _display_path(path: Path) -> str:
    try:
        return path.resolve().relative_to(ROOT).as_posix()
    except ValueError:
        return path.as_posix()


def main() -> int:
    parser = argparse.ArgumentParser(description="Render a concise execution brief for the real accountant session.")
    parser.add_argument("--root", type=Path, default=ROOT)
    parser.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST)
    parser.add_argument("--outreach-ledger", type=Path, default=DEFAULT_LEDGER)
    parser.add_argument("--format", choices=["markdown", "json", "text"], default="text")
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()

    brief = write_report() if args.write else build_execution_brief(
        root=args.root,
        manifest=args.manifest,
        outreach_ledger=args.outreach_ledger,
    )
    if args.format == "json":
        print(json.dumps(brief, ensure_ascii=False, indent=2, sort_keys=True))
    elif args.format == "markdown":
        print(render_markdown(brief), end="")
    else:
        print("ok: True")
        print(f"session_mode: {brief['session_mode']}")
        print(f"next_action: {brief['next_action']}")
        print(f"run_order_steps: {len(brief['run_order'])}")
        print(f"report_path: {brief['report_path']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
