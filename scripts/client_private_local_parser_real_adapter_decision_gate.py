from __future__ import annotations

import argparse
import json
import sys
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.client_private_local_parser_operator_runbook import (  # noqa: E402
    check_local_parser_operator_runbook,
)
from scripts.real_accountant_status import summarize_status  # noqa: E402


REPORT_PATH = ROOT / "docs" / "reports" / "2026-07-05-lprd1-local-parser-real-adapter-decision-gate.md"
DEFAULT_IMPLEMENTATION_PLAN = ROOT / "docs" / "reports" / "2026-07-05-local-parser-real-adapter-implementation-plan.md"
DEFAULT_SESSION_MANIFEST = ROOT / "docs" / "reports" / "real-accountant-session" / "session_manifest.json"
DEFAULT_OUTREACH_LEDGER = ROOT / "docs" / "reports" / "real-accountant-session" / "outreach-log.sample.jsonl"


@dataclass(frozen=True)
class RealAdapterDecision:
    decision_id: str
    decision: str
    allowed_to_implement: bool
    operator_runbook_ok: bool
    actual_accountant_evidence: bool
    explicit_authorization: bool
    implementation_plan_present: bool
    blockers: list[str]
    next_leaf: str

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def check_real_adapter_decision_gate(
    *,
    explicit_authorization: bool = False,
    implementation_plan: Path = DEFAULT_IMPLEMENTATION_PLAN,
    actual_accountant_evidence_override: bool | None = None,
) -> dict[str, Any]:
    operator = check_local_parser_operator_runbook()
    session = summarize_status(
        root=ROOT,
        manifest=DEFAULT_SESSION_MANIFEST,
        outreach_ledger=DEFAULT_OUTREACH_LEDGER,
    )
    actual_accountant_evidence = (
        actual_accountant_evidence_override
        if actual_accountant_evidence_override is not None
        else _has_actual_accountant_evidence(session)
    )
    implementation_plan_present = implementation_plan.exists()

    blockers: list[str] = []
    if not operator["ok"]:
        blockers.append("local parser operator runbook is not passing")
    if not actual_accountant_evidence:
        blockers.append("actual accountant feedback evidence is required before real private-file parser work")
    if not explicit_authorization:
        blockers.append("explicit user authorization is required before real adapter implementation")
    if not implementation_plan_present:
        blockers.append("real adapter implementation plan is required before coding")

    allowed_to_implement = not blockers
    decision = "proceed" if allowed_to_implement else "defer"
    if allowed_to_implement:
        next_leaf = "local parser real-adapter coding"
    elif not implementation_plan_present:
        next_leaf = "local parser real-adapter implementation plan"
    else:
        next_leaf = "real-accountant-session RS2/RS3 evidence capture, then explicit authorization before real adapter coding"
    decision_record = RealAdapterDecision(
        decision_id="lprd1-local-parser-real-adapter-decision-gate",
        decision=decision,
        allowed_to_implement=allowed_to_implement,
        operator_runbook_ok=bool(operator["ok"]),
        actual_accountant_evidence=bool(actual_accountant_evidence),
        explicit_authorization=explicit_authorization,
        implementation_plan_present=implementation_plan_present,
        blockers=blockers,
        next_leaf=next_leaf,
    )
    return {
        "ok": bool(operator["ok"]),
        "errors": [] if operator["ok"] else list(operator["errors"]),
        "decision": decision_record.to_dict(),
        "operator_runbook": {
            "ok": operator["ok"],
            "report_path": operator["report_path"],
            "subchecks": operator["subchecks"],
        },
        "real_accountant_session": {
            "session_mode": session["session_mode"],
            "outreach_counts": session["outreach_counts"],
            "close_ready": session["close_ready"],
            "next_action": session["next_action"],
            "blocked_by": session["blocked_by"],
        },
        "implementation_plan": str(_display_path(implementation_plan)),
        "report_path": str(REPORT_PATH.relative_to(ROOT)),
        "next_leaf": decision_record.next_leaf,
    }


def render_report(result: dict[str, Any]) -> str:
    decision = result["decision"]
    session = result["real_accountant_session"]
    if decision["allowed_to_implement"]:
        conclusion = "Real adapter implementation is authorized by this gate because the runbook, actual accountant evidence, explicit authorization, and implementation plan are all present."
    elif decision["implementation_plan_present"]:
        conclusion = "Real adapter implementation remains deferred. The operator runbook and implementation plan are present, but actual accountant feedback evidence and explicit user authorization are still required. No real file upload, OCR, source-body parsing, deletion automation, or private embedding work is authorized by this gate."
    else:
        conclusion = "Real adapter implementation remains deferred. The operator runbook passes, but actual accountant feedback evidence, explicit user authorization, and a real-adapter implementation plan are not present. No real file upload, OCR, source-body parsing, deletion automation, or private embedding work is authorized by this gate."
    lines = [
        "# LPRD1 Local Parser Real-Adapter Decision Gate",
        "",
        "> Scope: decision gate before any real local-only private-file parser adapter implementation.",
        "",
        "## 한 줄 결론",
        "",
        conclusion,
        "",
        "## Decision",
        "",
        f"- Decision: {decision['decision']}",
        f"- Allowed to implement: {decision['allowed_to_implement']}",
        f"- Operator runbook ok: {decision['operator_runbook_ok']}",
        f"- Actual accountant evidence: {decision['actual_accountant_evidence']}",
        f"- Explicit authorization: {decision['explicit_authorization']}",
        f"- Implementation plan present: {decision['implementation_plan_present']}",
        "",
        "## Blockers",
        "",
    ]
    lines.extend(f"- {blocker}" for blocker in decision["blockers"])
    lines.extend([
        "",
        "## Real Accountant Session Snapshot",
        "",
        f"- Session mode: {session['session_mode']}",
        f"- Outreach counts: {session['outreach_counts']}",
        f"- Close ready: {session['close_ready']}",
        f"- Next action: {session['next_action']}",
        "",
        "## What This Enables",
        "",
        "- The project now has a machine-readable stop/go gate before real private-file parser work.",
        "- Future implementation can start only after actual feedback evidence, explicit authorization, and a plan exist.",
        "- Until then, parser work remains limited to policy, contract, dry-run, scaffold, and operator-runbook artifacts.",
        "",
        "## Still Not Implemented",
        "",
        "- real file upload UI",
        "- OCR",
        "- real private document parsing",
        "- real file deletion automation",
        "- private embedding/index namespace",
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
    result = check_real_adapter_decision_gate()
    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    REPORT_PATH.write_text(render_report(result), encoding="utf-8")
    return result


def _has_actual_accountant_evidence(session: dict[str, Any]) -> bool:
    return (
        session["session_mode"] == "actual_feedback"
        and session["outreach_counts"].get("completed", 0) > 0
        and bool(session["close_ready"])
    )


def _display_path(path: Path) -> str:
    try:
        return path.resolve().relative_to(ROOT).as_posix()
    except ValueError:
        return path.as_posix()


def main() -> None:
    parser = argparse.ArgumentParser(description="Run local parser real-adapter decision gate.")
    parser.add_argument("--format", choices=["text", "json", "markdown"], default="text")
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--authorize-real-adapter", action="store_true")
    parser.add_argument("--implementation-plan", type=Path, default=DEFAULT_IMPLEMENTATION_PLAN)
    args = parser.parse_args()

    result = (
        write_report()
        if args.write and not args.authorize_real_adapter and args.implementation_plan == DEFAULT_IMPLEMENTATION_PLAN
        else check_real_adapter_decision_gate(
            explicit_authorization=args.authorize_real_adapter,
            implementation_plan=args.implementation_plan,
        )
    )
    if args.format == "json":
        print(json.dumps(result, ensure_ascii=False, indent=2, default=str))
    elif args.format == "markdown":
        print(render_report(result), end="")
    else:
        print(f"ok: {result['ok']}")
        print(f"decision: {result['decision']['decision']}")
        print(f"allowed_to_implement: {result['decision']['allowed_to_implement']}")
        print(f"blockers: {result['decision']['blockers']}")
        print(f"next_leaf: {result['next_leaf']}")
        for error in result["errors"]:
            print(f"- {error}")

    if not result["ok"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
