from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.accounting_intelligence_gap_audit import build_gap_audit  # noqa: E402
from scripts.real_accountant_status import summarize_status  # noqa: E402


REPORT_PATH = ROOT / "docs" / "reports" / "real-accountant-session" / "2026-07-05-readiness-index.md"
DEFAULT_MANIFEST = ROOT / "docs" / "reports" / "real-accountant-session" / "session_manifest.json"
DEFAULT_LEDGER = ROOT / "docs" / "reports" / "real-accountant-session" / "outreach-log.sample.jsonl"
READINESS_ITEMS = {
    "RS1 session packet": ROOT / "docs" / "reports" / "real-accountant-session" / "SESSION_PACKET.md",
    "RS2 invite dispatch": ROOT / "docs" / "reports" / "real-accountant-session" / "2026-07-05-invite-dispatch-gate.md",
    "RS2 pre-send final": ROOT / "docs" / "reports" / "real-accountant-session" / "2026-07-05-pre-send-final-gate.md",
    "RS2 after-send actions": ROOT / "docs" / "reports" / "real-accountant-session" / "2026-07-05-after-send-action-matrix.md",
    "RS2 response handling": ROOT / "docs" / "reports" / "real-accountant-session" / "2026-07-05-response-handling-gate.md",
    "RS2 scheduled session": ROOT / "docs" / "reports" / "real-accountant-session" / "2026-07-05-scheduled-session-gate.md",
    "RS3 notes quality": ROOT / "docs" / "reports" / "real-accountant-session" / "2026-07-05-notes-quality-gate.md",
    "RS3 capture readiness": ROOT / "docs" / "reports" / "real-accountant-session" / "2026-07-05-rs3-capture-readiness-gate.md",
    "RS3/RS4 post-session final": ROOT / "docs" / "reports" / "real-accountant-session" / "2026-07-05-post-session-final-gate.md",
    "RS4 close state matrix": ROOT / "docs" / "reports" / "real-accountant-session" / "2026-07-05-close-state-matrix.md",
    "Operator execution brief": ROOT / "docs" / "reports" / "real-accountant-session" / "2026-07-05-operator-execution-brief.md",
}


def build_readiness_index() -> dict[str, Any]:
    status = summarize_status(root=ROOT, manifest=DEFAULT_MANIFEST, outreach_ledger=DEFAULT_LEDGER)
    gap_audit = build_gap_audit()
    self_referential_gap_keys = (
        "real_accountant_readiness_index",
        "real_accountant_external_action_boundary_gate",
    )
    gap_errors = [
        error
        for error in gap_audit.errors
        if not any(key in error for key in self_referential_gap_keys)
    ]
    items = [
        {
            "name": name,
            "path": _display_path(path),
            "present": path.exists(),
        }
        for name, path in READINESS_ITEMS.items()
    ]
    missing = [item for item in items if not item["present"]]
    counts = status["outreach_counts"]
    external_open_items = _external_open_items(status)
    return {
        "ok": not missing and not gap_errors,
        "errors": [f"missing readiness item: {item['name']}" for item in missing] + gap_errors,
        "title": "Real Accountant Session Readiness Index",
        "horizon": status["horizon"],
        "session_mode": status["session_mode"],
        "close_ready": status["close_ready"],
        "next_action": status["next_action"],
        "outreach_counts": counts,
        "ready_items": items,
        "ready_item_count": sum(1 for item in items if item["present"]),
        "total_item_count": len(items),
        "technical_readiness": {
            "all_internal_reports_present": not missing,
            "gap_audit_ok": not gap_errors,
            "public_safe": True,
            "automation_rate": gap_audit.automation_rate,
        },
        "external_open_items": external_open_items,
        "operator_start": "docs/reports/real-accountant-session/2026-07-05-operator-execution-brief.md",
        "report_path": _display_path(REPORT_PATH),
    }


def render_markdown(index: dict[str, Any]) -> str:
    lines = [
        f"# {index['title']}",
        "",
        "> Scope: one-page status for the real-accountant-session horizon.",
        "",
        "## 한 줄 결론",
        "",
        "Internal readiness is complete for the current real-accountant-session runbook, but actual PoC evidence is still external/user-owned: the reviewer invite has not been sent and no actual feedback notes exist.",
        "",
        "## Current State",
        "",
        f"- Horizon: {index['horizon']}",
        f"- Session mode: {index['session_mode']}",
        f"- Close ready: {index['close_ready']}",
        f"- Next action: {index['next_action']}",
        f"- Outreach counts: {index['outreach_counts']}",
        "",
        "## Internal Readiness",
        "",
        f"- Ready items: {index['ready_item_count']} / {index['total_item_count']}",
        f"- Gap audit ok: {index['technical_readiness']['gap_audit_ok']}",
        f"- Automation rate: {index['technical_readiness']['automation_rate']:.2%}",
        "",
        "| Item | Status | Path |",
        "|---|---|---|",
    ]
    for item in index["ready_items"]:
        status = "present" if item["present"] else "missing"
        lines.append(f"| {item['name']} | {status} | `{item['path']}` |")
    lines.extend(["", "## External Open Items", ""])
    lines.extend(f"- {item}" for item in index["external_open_items"])
    lines.extend(
        [
            "",
            "## Operator Start",
            "",
            f"`{index['operator_start']}`",
            "",
            "## Machine Result",
            "",
            "```json",
            json.dumps(index, ensure_ascii=False, indent=2, default=str),
            "```",
        ]
    )
    return "\n".join(lines) + "\n"


def write_report() -> dict[str, Any]:
    index = build_readiness_index()
    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    REPORT_PATH.write_text(render_markdown(index), encoding="utf-8")
    return index


def _external_open_items(status: dict[str, Any]) -> list[str]:
    items: list[str] = []
    counts = status["outreach_counts"]
    if counts.get("sent", 0) == 0 and counts.get("scheduled", 0) == 0 and counts.get("completed", 0) == 0:
        items.append("Send the reviewer invite and update outreach ledger to sent.")
    if counts.get("scheduled", 0) == 0 and counts.get("completed", 0) == 0:
        items.append("Schedule a reviewer session or record decline/follow-up.")
    if counts.get("completed", 0) == 0:
        items.append("Run the reviewer session and update outreach ledger to completed.")
    if status["session_mode"] != "actual_feedback":
        items.append("Write public-safe actual feedback notes, run quality gate, capture queue records, and build actual manifest.")
    if not status["close_ready"]:
        items.append("Run close gate with quality preflight after actual evidence exists.")
    return items


def _display_path(path: Path) -> str:
    try:
        return path.resolve().relative_to(ROOT).as_posix()
    except ValueError:
        return path.as_posix()


def main() -> None:
    parser = argparse.ArgumentParser(description="Build one-page real accountant session readiness index.")
    parser.add_argument("--format", choices=["text", "json", "markdown"], default="text")
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()

    index = write_report() if args.write else build_readiness_index()
    if args.format == "json":
        print(json.dumps(index, ensure_ascii=False, indent=2, default=str))
    elif args.format == "markdown":
        print(render_markdown(index), end="")
    else:
        print(f"ok: {index['ok']}")
        print(f"ready_items: {index['ready_item_count']} / {index['total_item_count']}")
        print(f"next_action: {index['next_action']}")
        print(f"external_open_items: {len(index['external_open_items'])}")
        for error in index["errors"]:
            print(f"- {error}")

    if not index["ok"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
