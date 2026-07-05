from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.real_accountant_readiness_index import build_readiness_index  # noqa: E402


REPORT_PATH = (
    ROOT
    / "docs"
    / "reports"
    / "real-accountant-session"
    / "2026-07-05-external-action-boundary-gate.md"
)


def check_external_action_boundary_gate() -> dict[str, Any]:
    readiness = build_readiness_index()
    errors: list[str] = []

    if readiness["ok"] is not True:
        errors.append("readiness index must pass before external action boundary can be asserted")
    if readiness["ready_item_count"] != readiness["total_item_count"]:
        errors.append(
            f"internal readiness must be complete, got {readiness['ready_item_count']} / {readiness['total_item_count']}"
        )
    if readiness["technical_readiness"]["gap_audit_ok"] is not True:
        errors.append("gap audit must be ok before external action boundary can be asserted")
    if readiness["session_mode"] != "ready_to_schedule":
        errors.append(f"session mode must remain ready_to_schedule, got {readiness['session_mode']}")
    if readiness["close_ready"] is not False:
        errors.append("close gate must remain false before actual feedback evidence")
    if readiness["next_action"] != "Send reviewer invite and update outreach ledger to sent.":
        errors.append(f"next action must be reviewer invite send, got {readiness['next_action']}")

    counts = readiness["outreach_counts"]
    expected_counts = {
        "not_sent": 1,
        "sent": 0,
        "responded": 0,
        "scheduled": 0,
        "declined": 0,
        "completed": 0,
    }
    for name, expected in expected_counts.items():
        actual = counts.get(name, 0)
        if actual != expected:
            errors.append(f"outreach count {name} must be {expected}, got {actual}")

    required_open_item_fragments = (
        "Send the reviewer invite",
        "Schedule a reviewer session",
        "Run the reviewer session",
        "Write public-safe actual feedback notes",
        "Run close gate",
    )
    joined_open_items = "\n".join(readiness["external_open_items"])
    for fragment in required_open_item_fragments:
        if fragment not in joined_open_items:
            errors.append(f"external open items missing: {fragment}")

    protected_markers = ("source_body", "api_key", "token", "customer_name", "contract_body")
    rendered_inputs = json.dumps(readiness, ensure_ascii=False, default=str)
    for marker in protected_markers:
        if marker in rendered_inputs:
            errors.append(f"protected marker leaked into boundary evidence: {marker}")

    return {
        "ok": not errors,
        "errors": errors,
        "gate_id": "rs2-external-action-boundary-gate",
        "boundary_type": "external_action_required",
        "horizon": readiness["horizon"],
        "internal_readiness_complete": readiness["ready_item_count"] == readiness["total_item_count"],
        "ready_item_count": readiness["ready_item_count"],
        "total_item_count": readiness["total_item_count"],
        "session_mode": readiness["session_mode"],
        "close_ready": readiness["close_ready"],
        "next_action": readiness["next_action"],
        "outreach_counts": counts,
        "external_open_items": readiness["external_open_items"],
        "operator_start": readiness["operator_start"],
        "repo_side_recommendation": (
            "Do not add another readiness gate as the next repo-side step; the next real action is manual "
            "reviewer invite send, followed by the generated post-send ledger update command."
        ),
        "completion_boundary": [
            "Do not close the real-accountant-session horizon yet.",
            "Do not mark actual_feedback_evidence true before actual public-safe notes exist.",
            "Do not replace a completed reviewer session with synthetic readiness evidence.",
            "After manual invite send, run real_accountant_outreach_update.py to move the alias ledger to sent.",
        ],
        "report_path": _display_path(REPORT_PATH),
    }


def render_report(result: dict[str, Any]) -> str:
    lines = [
        "# RS2 External Action Boundary Gate",
        "",
        "> Scope: freeze the current real-accountant-session state as internally ready but externally waiting.",
        "",
        "## One-Line Result",
        "",
        (
            "Internal readiness is complete, but this is not another readiness gate to keep expanding. "
            "The next action is manual reviewer invite send."
        ),
        "",
        "## Current Boundary",
        "",
        f"- ok: {result['ok']}",
        f"- boundary type: {result['boundary_type']}",
        f"- horizon: {result['horizon']}",
        f"- internal readiness: {result['ready_item_count']} / {result['total_item_count']}",
        f"- session mode: {result['session_mode']}",
        f"- close ready: {result['close_ready']}",
        f"- next action: {result['next_action']}",
        f"- outreach counts: {result['outreach_counts']}",
        "",
        "## External Open Items",
        "",
    ]
    lines.extend(f"- {item}" for item in result["external_open_items"])
    lines.extend(
        [
            "",
            "## Repo-Side Recommendation",
            "",
            result["repo_side_recommendation"],
            "",
            "## Completion Boundary",
            "",
        ]
    )
    lines.extend(f"- {item}" for item in result["completion_boundary"])
    lines.extend(
        [
            "",
            "## Operator Start",
            "",
            f"`{result['operator_start']}`",
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
    result = check_external_action_boundary_gate()
    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    REPORT_PATH.write_text(render_report(result), encoding="utf-8")
    return result


def _display_path(path: Path) -> str:
    try:
        return path.resolve().relative_to(ROOT).as_posix()
    except ValueError:
        return path.as_posix()


def main() -> None:
    parser = argparse.ArgumentParser(description="Assert the real accountant session external action boundary.")
    parser.add_argument("--format", choices=["text", "json", "markdown"], default="text")
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()

    result = write_report() if args.write else check_external_action_boundary_gate()
    if args.format == "json":
        print(json.dumps(result, ensure_ascii=False, indent=2, default=str))
    elif args.format == "markdown":
        print(render_report(result), end="")
    else:
        print(f"ok: {result['ok']}")
        print(f"boundary_type: {result['boundary_type']}")
        print(f"internal_readiness: {result['ready_item_count']} / {result['total_item_count']}")
        print(f"next_action: {result['next_action']}")
        print(f"recommendation: {result['repo_side_recommendation']}")
        for error in result["errors"]:
            print(f"- {error}")

    if not result["ok"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
