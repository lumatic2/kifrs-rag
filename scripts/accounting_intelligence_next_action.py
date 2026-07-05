from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.accounting_intelligence_decision_queue import (  # noqa: E402
    DEFAULT_EXTERNAL_AUTH_TEMPLATE,
    DEFAULT_OUTREACH_LEDGER,
    DEFAULT_SESSION_MANIFEST,
    build_decision_queue,
)


REPORT_PATH = ROOT / "docs" / "reports" / "2026-07-05-accounting-intelligence-next-action.md"


def build_next_action(
    *,
    external_authorization_record: Path = DEFAULT_EXTERNAL_AUTH_TEMPLATE,
    manifest: Path = DEFAULT_SESSION_MANIFEST,
    outreach_ledger: Path = DEFAULT_OUTREACH_LEDGER,
    refresh_gates: bool = False,
) -> dict[str, Any]:
    queue = build_decision_queue(
        external_authorization_record=external_authorization_record,
        manifest=manifest,
        outreach_ledger=outreach_ledger,
        refresh_gates=refresh_gates,
    )
    return build_next_action_from_queue(queue)


def build_next_action_from_queue(queue: dict[str, Any]) -> dict[str, Any]:
    decision = _recommended_decision(queue)
    return {
        "ok": queue["ok"],
        "errors": queue["errors"],
        "title": "Accounting Intelligence Next Action",
        "mode": queue["mode"],
        "recommended_next_decision": decision["id"] if decision else None,
        "status": decision["status"] if decision else "none",
        "operator_action_required": decision["operator_action_required"] if decision else False,
        "user_decision": decision["user_decision"] if decision else "No user-owned decision is currently required.",
        "current_blocker": decision["current_blocker"] if decision else "none",
        "next_command": decision["next_command"] if decision else "none",
        "evidence": decision["evidence"] if decision else queue["report_path"],
        "open_decision_count": queue["open_decision_count"],
        "operator_action_required_count": queue["operator_action_required_count"],
        "report_path": _display_path(REPORT_PATH),
        "decision_queue_report": queue["report_path"],
    }


def render_markdown(action: dict[str, Any]) -> str:
    lines = [
        f"# {action['title']}",
        "",
        "> Scope: the single next operator-facing action from the Accounting Intelligence decision queue.",
        "",
        "## 한 줄 결론",
        "",
        _one_line_conclusion(action),
        "",
        "## Next Action",
        "",
        f"- decision: `{action['recommended_next_decision']}`",
        f"- status: {action['status']}",
        f"- operator action required: {action['operator_action_required']}",
        f"- decide: {action['user_decision']}",
        f"- blocker: {action['current_blocker']}",
        f"- command: `{action['next_command']}`",
        f"- evidence: `{action['evidence']}`",
        "",
        "## Queue Snapshot",
        "",
        f"- mode: {action['mode']}",
        f"- open decisions: {action['open_decision_count']}",
        f"- operator action required: {action['operator_action_required_count']}",
        f"- decision queue report: `{action['decision_queue_report']}`",
        "",
        "## Machine Result",
        "",
        "```json",
        json.dumps(action, ensure_ascii=False, indent=2, default=str),
        "```",
    ]
    return "\n".join(lines) + "\n"


def write_report(
    *,
    external_authorization_record: Path = DEFAULT_EXTERNAL_AUTH_TEMPLATE,
    manifest: Path = DEFAULT_SESSION_MANIFEST,
    outreach_ledger: Path = DEFAULT_OUTREACH_LEDGER,
    refresh_gates: bool = False,
    path: Path = REPORT_PATH,
) -> dict[str, Any]:
    action = build_next_action(
        external_authorization_record=external_authorization_record,
        manifest=manifest,
        outreach_ledger=outreach_ledger,
        refresh_gates=refresh_gates,
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(render_markdown(action), encoding="utf-8")
    return action


def _recommended_decision(queue: dict[str, Any]) -> dict[str, Any] | None:
    recommended = queue.get("recommended_next_decision")
    for decision in queue["decisions"]:
        if decision["id"] == recommended:
            return decision
    for decision in queue["decisions"]:
        if decision["status"] != "closed" and decision["operator_action_required"]:
            return decision
    return None


def _one_line_conclusion(action: dict[str, Any]) -> str:
    if action["recommended_next_decision"] == "send_reviewer_invite":
        return "Next: send the real accountant reviewer invite; implementation expansion should wait for actual feedback evidence."
    if action["recommended_next_decision"]:
        return f"Next: decide `{action['recommended_next_decision']}`."
    return "No tracked operator action is currently required."


def _display_path(path: Path) -> str:
    try:
        return path.resolve().relative_to(ROOT).as_posix()
    except ValueError:
        return path.as_posix()


def main() -> None:
    parser = argparse.ArgumentParser(description="Render the single next Accounting Intelligence action.")
    parser.add_argument("--format", choices=["text", "json", "markdown"], default="text")
    parser.add_argument("--write", action="store_true", help=f"Write {REPORT_PATH.relative_to(ROOT)}")
    parser.add_argument("--out", type=Path, default=REPORT_PATH)
    parser.add_argument("--external-authorization-record", type=Path, default=DEFAULT_EXTERNAL_AUTH_TEMPLATE)
    parser.add_argument("--manifest", type=Path, default=DEFAULT_SESSION_MANIFEST)
    parser.add_argument("--outreach-ledger", type=Path, default=DEFAULT_OUTREACH_LEDGER)
    parser.add_argument("--refresh-gates", action="store_true")
    args = parser.parse_args()

    action = (
        write_report(
            external_authorization_record=args.external_authorization_record,
            manifest=args.manifest,
            outreach_ledger=args.outreach_ledger,
            refresh_gates=args.refresh_gates,
            path=args.out,
        )
        if args.write
        else build_next_action(
            external_authorization_record=args.external_authorization_record,
            manifest=args.manifest,
            outreach_ledger=args.outreach_ledger,
            refresh_gates=args.refresh_gates,
        )
    )

    if args.format == "json":
        print(json.dumps(action, ensure_ascii=False, indent=2, default=str))
    elif args.format == "markdown":
        print(render_markdown(action), end="")
    else:
        print(action["title"])
        print(f"- decision: {action['recommended_next_decision']}")
        print(f"- status: {action['status']}")
        print(f"- decide: {action['user_decision']}")
        print(f"- blocker: {action['current_blocker']}")
        print(f"- command: {action['next_command']}")
        print(f"- evidence: {action['evidence']}")
        for error in action["errors"]:
            print(f"- {error}")

    if not action["ok"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
