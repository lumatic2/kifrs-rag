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

from scripts.opt_in_retriever_demo_validation import build_demo_validation  # noqa: E402
from scripts.real_accountant_status import summarize_status  # noqa: E402
from scripts.rag_quality_final_gate import TARGET_RETRIEVER  # noqa: E402


REPORT_PATH = ROOT / "docs" / "reports" / "2026-07-05-orpd1-opt-in-retriever-promotion-decision-gate.md"
DEFAULT_SESSION_MANIFEST = ROOT / "docs" / "reports" / "real-accountant-session" / "session_manifest.json"
DEFAULT_OUTREACH_LEDGER = ROOT / "docs" / "reports" / "real-accountant-session" / "outreach-log.sample.jsonl"


@dataclass(frozen=True)
class PromotionDecision:
    decision_id: str
    decision: str
    promote_to_default: bool
    target_retriever: str
    demo_validation_ok: bool
    actual_accountant_evidence: bool
    explicit_authorization: bool
    blockers: list[str]
    next_leaf: str

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def check_promotion_decision_gate(
    *,
    explicit_authorization: bool = False,
    actual_accountant_evidence_override: bool | None = None,
) -> dict[str, Any]:
    demo = build_demo_validation()
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

    blockers: list[str] = []
    if demo["ok"] is not True:
        blockers.append("opt-in retriever demo validation must pass")
    if demo["target_recall20"] < 1.0:
        blockers.append(f"{TARGET_RETRIEVER} recall@20 must remain 1.000")
    if demo["target_buckets"]["absent"] != 0:
        blockers.append(f"{TARGET_RETRIEVER} required-citation absent count must remain 0")
    if demo["target_misses"]:
        blockers.append(f"{TARGET_RETRIEVER} top-20 misses must remain empty")
    if not actual_accountant_evidence:
        blockers.append("actual accountant feedback evidence is required before default retriever promotion")
    if not explicit_authorization:
        blockers.append("explicit user authorization is required before changing the default retriever")

    promote_to_default = not blockers
    decision = "promote" if promote_to_default else "defer"
    next_leaf = (
        "default retriever promotion implementation"
        if promote_to_default
        else "real-accountant-session RS2/RS3 evidence capture, then explicit authorization before default retriever change"
    )
    decision_record = PromotionDecision(
        decision_id="orpd1-opt-in-retriever-promotion-decision-gate",
        decision=decision,
        promote_to_default=promote_to_default,
        target_retriever=TARGET_RETRIEVER,
        demo_validation_ok=bool(demo["ok"]),
        actual_accountant_evidence=bool(actual_accountant_evidence),
        explicit_authorization=explicit_authorization,
        blockers=blockers,
        next_leaf=next_leaf,
    )
    return {
        "ok": bool(demo["ok"]),
        "errors": [] if demo["ok"] else list(demo["errors"]),
        "decision": decision_record.to_dict(),
        "demo_validation": {
            "ok": demo["ok"],
            "target_retriever": demo["target_retriever"],
            "target_recall20": demo["target_recall20"],
            "target_buckets": demo["target_buckets"],
            "target_misses": demo["target_misses"],
            "default_promotion": demo["default_promotion"],
            "report_path": demo["report_path"],
        },
        "real_accountant_session": {
            "session_mode": session["session_mode"],
            "outreach_counts": session["outreach_counts"],
            "close_ready": session["close_ready"],
            "next_action": session["next_action"],
            "blocked_by": session["blocked_by"],
        },
        "report_path": str(REPORT_PATH.relative_to(ROOT)),
        "next_leaf": next_leaf,
    }


def render_report(result: dict[str, Any]) -> str:
    decision = result["decision"]
    demo = result["demo_validation"]
    session = result["real_accountant_session"]
    if decision["promote_to_default"]:
        conclusion = f"`{decision['target_retriever']}` may be promoted to the default retriever because demo validation, actual accountant evidence, and explicit authorization are all present."
    else:
        conclusion = f"`{decision['target_retriever']}` remains opt-in. Retrieval metrics pass, but actual accountant feedback evidence and explicit authorization are still required before changing the default retriever."

    lines = [
        "# ORPD1 Opt-In Retriever Promotion Decision Gate",
        "",
        "> Scope: stop/go gate before changing the default retriever from `hybrid` to the final opt-in repair stack.",
        "",
        "## 한 줄 결론",
        "",
        conclusion,
        "",
        "## Decision",
        "",
        f"- Decision: {decision['decision']}",
        f"- Promote to default: {decision['promote_to_default']}",
        f"- Target retriever: `{decision['target_retriever']}`",
        f"- Demo validation ok: {decision['demo_validation_ok']}",
        f"- Actual accountant evidence: {decision['actual_accountant_evidence']}",
        f"- Explicit authorization: {decision['explicit_authorization']}",
        "",
        "## Blockers",
        "",
    ]
    lines.extend(f"- {blocker}" for blocker in decision["blockers"])
    lines.extend([
        "",
        "## Retrieval Evidence",
        "",
        f"- Demo validation report: `{demo['report_path']}`",
        f"- Target recall@20: {demo['target_recall20']:.3f}",
        f"- Required-citation absent count: {demo['target_buckets']['absent']}",
        f"- Target misses: {len(demo['target_misses'])}",
        f"- Current default promotion state: {demo['default_promotion']}",
        "",
        "## Real Accountant Session Snapshot",
        "",
        f"- Session mode: {session['session_mode']}",
        f"- Outreach counts: {session['outreach_counts']}",
        f"- Close ready: {session['close_ready']}",
        f"- Next action: {session['next_action']}",
        "",
        "## Boundary",
        "",
        "- This gate does not change runtime defaults.",
        "- The current default retriever remains unchanged unless this gate returns `promote` and a separate implementation changes the default.",
        "- Retrieval-only quality is not answer-quality proof and does not replace accountant review.",
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
    result = check_promotion_decision_gate()
    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    REPORT_PATH.write_text(render_report(result), encoding="utf-8")
    return result


def _has_actual_accountant_evidence(session: dict[str, Any]) -> bool:
    return (
        session["session_mode"] == "actual_feedback"
        and session["outreach_counts"].get("completed", 0) > 0
        and bool(session["close_ready"])
    )


def main() -> None:
    parser = argparse.ArgumentParser(description="Run opt-in retriever default-promotion decision gate.")
    parser.add_argument("--format", choices=["text", "json", "markdown"], default="text")
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--authorize-promotion", action="store_true")
    parser.add_argument("--actual-accountant-evidence", action="store_true")
    args = parser.parse_args()

    result = (
        write_report()
        if args.write and not args.authorize_promotion and not args.actual_accountant_evidence
        else check_promotion_decision_gate(
            explicit_authorization=args.authorize_promotion,
            actual_accountant_evidence_override=True if args.actual_accountant_evidence else None,
        )
    )
    if args.format == "json":
        print(json.dumps(result, ensure_ascii=False, indent=2, default=str))
    elif args.format == "markdown":
        print(render_report(result), end="")
    else:
        print(f"ok: {result['ok']}")
        print(f"decision: {result['decision']['decision']}")
        print(f"promote_to_default: {result['decision']['promote_to_default']}")
        print(f"target_retriever: {result['decision']['target_retriever']}")
        print(f"blockers: {result['decision']['blockers']}")
        print(f"next_leaf: {result['next_leaf']}")
        for error in result["errors"]:
            print(f"- {error}")

    if not result["ok"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
