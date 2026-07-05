from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.client_private_local_parser_real_adapter_decision_gate import (  # noqa: E402
    check_real_adapter_decision_gate,
)
from scripts.external_source_body_ingestion_authorization_gate import (  # noqa: E402
    check_authorization_gate,
    load_authorization_record,
)
from scripts.real_accountant_status import summarize_status  # noqa: E402


REPORT_PATH = ROOT / "docs" / "reports" / "2026-07-05-accounting-intelligence-decision-queue.md"
DEFAULT_RETRIEVER_PROMOTION_REPORT = (
    ROOT / "docs" / "reports" / "2026-07-05-orpd1-opt-in-retriever-promotion-decision-gate.md"
)
DEFAULT_SESSION_MANIFEST = ROOT / "docs" / "reports" / "real-accountant-session" / "session_manifest.json"
DEFAULT_OUTREACH_LEDGER = ROOT / "docs" / "reports" / "real-accountant-session" / "outreach-log.sample.jsonl"
DEFAULT_EXTERNAL_AUTH_TEMPLATE = ROOT / "docs" / "reports" / "external-source-body-authorization-record.template.json"


def build_decision_queue(
    *,
    external_authorization_record: Path = DEFAULT_EXTERNAL_AUTH_TEMPLATE,
    refresh_gates: bool = False,
) -> dict[str, Any]:
    session = summarize_status(
        root=ROOT,
        manifest=DEFAULT_SESSION_MANIFEST,
        outreach_ledger=DEFAULT_OUTREACH_LEDGER,
    )
    external_authorization = _check_external_authorization(external_authorization_record)
    local_parser = check_real_adapter_decision_gate()
    retriever_promotion = _check_retriever_promotion(refresh_gates=refresh_gates)

    decisions = [
        _reviewer_invite_decision(session),
        _external_body_authorization_decision(external_authorization, external_authorization_record),
        _local_parser_real_adapter_decision(local_parser),
        _retriever_promotion_decision(retriever_promotion),
    ]
    open_decisions = [decision for decision in decisions if decision["status"] != "closed"]
    ready_to_act = [decision for decision in open_decisions if decision["operator_action_required"]]
    return {
        "ok": all(decision["gate_ok"] for decision in decisions),
        "errors": [error for decision in decisions for error in decision["errors"]],
        "title": "Accounting Intelligence Decision Queue",
        "mode": "refresh_gates" if refresh_gates else "cached_reports",
        "decision_count": len(decisions),
        "open_decision_count": len(open_decisions),
        "operator_action_required_count": len(ready_to_act),
        "recommended_next_decision": ready_to_act[0]["id"] if ready_to_act else None,
        "decisions": decisions,
        "report_path": _display_path(REPORT_PATH),
    }


def render_markdown(queue: dict[str, Any]) -> str:
    lines = [
        f"# {queue['title']}",
        "",
        "> Scope: user-owned decisions that unblock the Accounting Intelligence Expansion objective.",
        "",
        "## 한 줄 결론",
        "",
        _one_line_conclusion(queue),
        "",
        "## Summary",
        "",
        f"- ok: {queue['ok']}",
        f"- mode: {queue['mode']}",
        f"- decisions: {queue['decision_count']}",
        f"- open decisions: {queue['open_decision_count']}",
        f"- operator action required: {queue['operator_action_required_count']}",
        f"- recommended next decision: {queue['recommended_next_decision']}",
        "",
        "## Decision Queue",
        "",
        "| Priority | Decision | Status | What User Decides | Unblocks |",
        "|---:|---|---|---|---|",
    ]
    for decision in queue["decisions"]:
        lines.append(
            "| {priority} | `{id}` | {status} | {question} | {unblocks} |".format(
                priority=decision["priority"],
                id=decision["id"],
                status=decision["status"],
                question=decision["user_decision"],
                unblocks=decision["unblocks"],
            )
        )
    lines.extend(["", "## Details", ""])
    for decision in queue["decisions"]:
        lines.extend(
            [
                f"### {decision['priority']}. {decision['title']}",
                "",
                f"- status: {decision['status']}",
                f"- gate ok: {decision['gate_ok']}",
                f"- operator action required: {decision['operator_action_required']}",
                f"- user decision: {decision['user_decision']}",
                f"- unblocks: {decision['unblocks']}",
                f"- current blocker: {decision['current_blocker']}",
                f"- next command: {decision['next_command']}",
                f"- evidence: `{decision['evidence']}`",
                "",
            ]
        )
    lines.extend(
        [
            "## Machine Result",
            "",
            "```json",
            json.dumps(queue, ensure_ascii=False, indent=2, default=str),
            "```",
        ]
    )
    return "\n".join(lines) + "\n"


def write_report() -> dict[str, Any]:
    queue = build_decision_queue()
    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    REPORT_PATH.write_text(render_markdown(queue), encoding="utf-8")
    return queue


def _check_external_authorization(record_path: Path) -> dict[str, Any]:
    try:
        authorization = load_authorization_record(record_path)
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        return {
            "ok": False,
            "errors": [str(exc)],
            "decision": "defer",
            "allowed_to_implement": False,
            "authorization_present": record_path.exists(),
            "authorization_valid": False,
            "blockers": [str(exc)],
            "report_path": _display_path(record_path),
        }
    return check_authorization_gate(
        authorization=authorization,
        authorization_record_path=record_path,
    )


def _check_retriever_promotion(*, refresh_gates: bool) -> dict[str, Any]:
    if refresh_gates:
        from scripts.opt_in_retriever_promotion_decision_gate import (  # noqa: PLC0415
            check_promotion_decision_gate,
        )

        return check_promotion_decision_gate()
    try:
        result = _load_machine_result(DEFAULT_RETRIEVER_PROMOTION_REPORT)
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        return {
            "ok": False,
            "errors": [str(exc)],
            "decision": {
                "blockers": [str(exc)],
                "promote_to_default": False,
            },
            "report_path": _display_path(DEFAULT_RETRIEVER_PROMOTION_REPORT),
        }
    result["report_path"] = result.get("report_path") or _display_path(DEFAULT_RETRIEVER_PROMOTION_REPORT)
    return result


def _reviewer_invite_decision(session: dict[str, Any]) -> dict[str, Any]:
    counts = session["outreach_counts"]
    not_sent = counts.get("not_sent", 0)
    completed = counts.get("completed", 0)
    closed = session["close_ready"] is True and completed > 0
    action_required = not closed and not_sent > 0 and counts.get("sent", 0) == 0
    return {
        "id": "send_reviewer_invite",
        "title": "Send real accountant reviewer invite",
        "priority": 1,
        "status": "closed" if closed else "needs_user_action",
        "gate_ok": True,
        "errors": [],
        "operator_action_required": action_required,
        "user_decision": "Which reviewer should receive the invite, and should the invite be sent now?",
        "unblocks": "RS2 actual accountant session, RS3 actual notes capture, RS4 close gate",
        "current_blocker": session["blocked_by"][0] if session["blocked_by"] else "none",
        "next_command": "python scripts\\real_accountant_invite_packet.py",
        "evidence": "docs/reports/real-accountant-session/2026-07-05-operator-execution-brief.md",
    }


def _external_body_authorization_decision(result: dict[str, Any], record_path: Path) -> dict[str, Any]:
    blockers = result.get("blockers", [])
    allowed = result.get("allowed_to_implement") is True
    return {
        "id": "approve_external_body_authorization_record",
        "title": "Approve source-specific external body authorization record",
        "priority": 2,
        "status": "closed" if allowed else "needs_user_action",
        "gate_ok": bool(result.get("ok")),
        "errors": list(result.get("errors", [])),
        "operator_action_required": not allowed,
        "user_decision": "Whether to fill a source-specific authorization record for live local-private body ingestion.",
        "unblocks": "external source body connector implementation",
        "current_blocker": blockers[0] if blockers else "none",
        "next_command": f"Fill `{_display_path(record_path)}`, then run the external body authorization gate with that record.",
        "evidence": _display_path(record_path),
    }


def _local_parser_real_adapter_decision(result: dict[str, Any]) -> dict[str, Any]:
    decision = result["decision"]
    blockers = decision["blockers"]
    allowed = decision["allowed_to_implement"] is True
    return {
        "id": "approve_local_private_parser_adapter",
        "title": "Approve real local-private parser adapter",
        "priority": 3,
        "status": "closed" if allowed else "waiting_on_accountant_evidence",
        "gate_ok": bool(result["ok"]),
        "errors": list(result["errors"]),
        "operator_action_required": False,
        "user_decision": "Whether to authorize real private-file parser work after actual accountant evidence exists.",
        "unblocks": "real local file upload/OCR/parser/deletion automation",
        "current_blocker": blockers[0] if blockers else "none",
        "next_command": "python scripts\\client_private_local_parser_real_adapter_decision_gate.py --format text",
        "evidence": result["report_path"],
    }


def _retriever_promotion_decision(result: dict[str, Any]) -> dict[str, Any]:
    decision = result["decision"]
    blockers = decision["blockers"]
    allowed = decision["promote_to_default"] is True
    return {
        "id": "approve_default_retriever_promotion",
        "title": "Approve opt-in retriever default promotion",
        "priority": 4,
        "status": "closed" if allowed else "waiting_on_accountant_evidence",
        "gate_ok": bool(result["ok"]),
        "errors": list(result["errors"]),
        "operator_action_required": False,
        "user_decision": "Whether to promote the opt-in repair retriever to default after actual accountant evidence exists.",
        "unblocks": "default retriever change from hybrid to ifrs1109_classification_hybrid stack",
        "current_blocker": blockers[0] if blockers else "none",
        "next_command": "python scripts\\opt_in_retriever_promotion_decision_gate.py --format text",
        "evidence": result["report_path"],
    }


def _load_machine_result(path: Path) -> dict[str, Any]:
    text = path.read_text(encoding="utf-8")
    marker = "## Machine Result"
    marker_index = text.find(marker)
    if marker_index < 0:
        raise ValueError(f"missing Machine Result section: {_display_path(path)}")
    json_start = text.find("```json", marker_index)
    if json_start < 0:
        raise ValueError(f"missing Machine Result json fence: {_display_path(path)}")
    json_start = text.find("\n", json_start)
    json_end = text.find("```", json_start)
    if json_start < 0 or json_end < 0:
        raise ValueError(f"malformed Machine Result json fence: {_display_path(path)}")
    payload = json.loads(text[json_start:json_end].strip())
    if not isinstance(payload, dict):
        raise ValueError(f"Machine Result must be a JSON object: {_display_path(path)}")
    return payload


def _one_line_conclusion(queue: dict[str, Any]) -> str:
    if queue["recommended_next_decision"] == "send_reviewer_invite":
        return "The next useful user-owned decision is sending the real accountant reviewer invite; other implementation approvals should wait for actual feedback evidence."
    if queue["recommended_next_decision"]:
        return f"The next useful user-owned decision is `{queue['recommended_next_decision']}`."
    return "No user-owned decision is currently required by the tracked gates."


def _display_path(path: Path) -> str:
    try:
        return path.resolve().relative_to(ROOT).as_posix()
    except ValueError:
        return path.as_posix()


def main() -> None:
    parser = argparse.ArgumentParser(description="Render the Accounting Intelligence user-owned decision queue.")
    parser.add_argument("--format", choices=["text", "json", "markdown"], default="text")
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--external-authorization-record", type=Path, default=DEFAULT_EXTERNAL_AUTH_TEMPLATE)
    parser.add_argument("--refresh-gates", action="store_true")
    args = parser.parse_args()

    queue = (
        write_report()
        if args.write and args.external_authorization_record == DEFAULT_EXTERNAL_AUTH_TEMPLATE and not args.refresh_gates
        else build_decision_queue(
            external_authorization_record=args.external_authorization_record,
            refresh_gates=args.refresh_gates,
        )
    )
    if args.format == "json":
        print(json.dumps(queue, ensure_ascii=False, indent=2, default=str))
    elif args.format == "markdown":
        print(render_markdown(queue), end="")
    else:
        print(f"ok: {queue['ok']}")
        print(f"mode: {queue['mode']}")
        print(f"open_decisions: {queue['open_decision_count']}")
        print(f"operator_action_required: {queue['operator_action_required_count']}")
        print(f"recommended_next_decision: {queue['recommended_next_decision']}")
        for decision in queue["decisions"]:
            print(f"- {decision['priority']}. {decision['id']}: {decision['status']} ({decision['current_blocker']})")
        for error in queue["errors"]:
            print(f"- {error}")

    if not queue["ok"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
