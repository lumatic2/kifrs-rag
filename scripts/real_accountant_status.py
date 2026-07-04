from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

try:
    from scripts.real_accountant_close_check import check_close_gate
    from scripts.real_accountant_outreach_check import check_outreach
    from scripts.real_accountant_session_check import check_session_manifest
except ModuleNotFoundError:
    import sys

    ROOT = Path(__file__).resolve().parents[1]
    if str(ROOT) not in sys.path:
        sys.path.insert(0, str(ROOT))
    try:
        from scripts.real_accountant_close_check import check_close_gate
        from scripts.real_accountant_outreach_check import check_outreach
        from scripts.real_accountant_session_check import check_session_manifest
    except ModuleNotFoundError:
        from real_accountant_close_check import check_close_gate
        from real_accountant_outreach_check import check_outreach
        from real_accountant_session_check import check_session_manifest


def summarize_status(*, root: Path, manifest: Path, outreach_ledger: Path) -> dict[str, Any]:
    session_ok, session_errors, session_mode = check_session_manifest(manifest, root=root)
    outreach_ok, outreach_errors, outreach_counts = check_outreach(outreach_ledger)
    close_ok, close_errors, close_evidence = check_close_gate(
        root=root,
        manifest_path=manifest,
        outreach_ledger=outreach_ledger,
        run_quality=False,
    )

    next_action = _next_action(session_mode, outreach_counts, close_ok)
    blocked_by = _blocked_by(session_mode, outreach_counts, close_errors)
    return {
        "horizon": "real-accountant-session",
        "session_ok": session_ok,
        "session_mode": session_mode,
        "session_errors": session_errors,
        "outreach_ok": outreach_ok,
        "outreach_counts": outreach_counts,
        "outreach_errors": outreach_errors,
        "close_ready": close_ok,
        "close_errors": close_errors,
        "close_evidence": close_evidence,
        "next_action": next_action,
        "blocked_by": blocked_by,
    }


def render_text(status: dict[str, Any]) -> str:
    counts = status["outreach_counts"]
    lines = [
        "Real Accountant Session Status",
        "",
        f"- Horizon: {status['horizon']}",
        f"- Session mode: {status['session_mode']}",
        f"- Outreach: not_sent={counts.get('not_sent', 0)}, sent={counts.get('sent', 0)}, scheduled={counts.get('scheduled', 0)}, completed={counts.get('completed', 0)}",
        f"- Close ready: {status['close_ready']}",
        f"- Next action: {status['next_action']}",
    ]
    if status["blocked_by"]:
        lines.extend(["", "Blocked by:"])
        lines.extend(f"- {item}" for item in status["blocked_by"])
    return "\n".join(lines) + "\n"


def _next_action(session_mode: str, outreach_counts: dict[str, int], close_ok: bool) -> str:
    if close_ok:
        return "Write close report and sync ROADMAP/OBJECTIVE."
    if session_mode == "actual_feedback":
        return "Run close gate with quality preflight and fix remaining close errors."
    if outreach_counts.get("completed", 0):
        return "Build actual capture package and actual session manifest."
    if outreach_counts.get("scheduled", 0):
        return "Run the scheduled accountant session and write actual-feedback-notes.md."
    if outreach_counts.get("sent", 0) or outreach_counts.get("responded", 0):
        return "Schedule the reviewer session or update outreach ledger."
    return "Send reviewer invite and update outreach ledger to sent."


def _blocked_by(session_mode: str, outreach_counts: dict[str, int], close_errors: list[str]) -> list[str]:
    blocked: list[str] = []
    if outreach_counts.get("sent", 0) == 0 and outreach_counts.get("scheduled", 0) == 0 and outreach_counts.get("completed", 0) == 0:
        blocked.append("reviewer invite has not been sent")
    if outreach_counts.get("completed", 0) == 0:
        blocked.append("no completed reviewer session in outreach ledger")
    if session_mode != "actual_feedback":
        blocked.append(f"session manifest is {session_mode}, not actual_feedback")
    blocked.extend(error for error in close_errors if error not in blocked)
    return list(dict.fromkeys(blocked))


def main() -> int:
    parser = argparse.ArgumentParser(description="Summarize current real accountant session progress and next action.")
    parser.add_argument("--root", type=Path, default=Path.cwd())
    parser.add_argument(
        "--manifest",
        type=Path,
        default=Path("docs/reports/real-accountant-session/session_manifest.json"),
    )
    parser.add_argument(
        "--outreach-ledger",
        type=Path,
        default=Path("docs/reports/real-accountant-session/outreach-log.sample.jsonl"),
    )
    parser.add_argument("--format", choices=["text", "json"], default="text")
    args = parser.parse_args()

    status = summarize_status(root=args.root, manifest=args.manifest, outreach_ledger=args.outreach_ledger)
    if args.format == "json":
        print(json.dumps(status, ensure_ascii=False, indent=2, sort_keys=True))
    else:
        print(render_text(status), end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
