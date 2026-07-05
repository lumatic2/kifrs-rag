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

from kifrs.ingestion.evidence import validate_evidence_manifest  # noqa: E402
from kifrs.ingestion.manifest import validate_manifest  # noqa: E402
from scripts.live_external_source_validation import validate_live_external_sources  # noqa: E402


REPORT_PATH = ROOT / "docs" / "reports" / "2026-07-05-esbd1-external-source-body-ingestion-decision-gate.md"
DEFAULT_BODY_POLICY = ROOT / "docs" / "reports" / "2026-07-05-external-source-body-storage-policy.md"
DEFAULT_IMPLEMENTATION_PLAN = ROOT / "docs" / "reports" / "2026-07-05-external-source-body-ingestion-plan.md"
LEV1_REPORT = ROOT / "docs" / "reports" / "2026-07-05-lev1-live-external-source-validation.md"


@dataclass(frozen=True)
class BodyIngestionDecision:
    decision_id: str
    decision: str
    allowed_to_implement: bool
    source_manifest_ok: bool
    evidence_manifest_ok: bool
    live_landing_validation_ok: bool
    live_landing_report_present: bool
    body_policy_present: bool
    implementation_plan_present: bool
    explicit_authorization: bool
    blockers: list[str]
    next_leaf: str

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def check_body_ingestion_decision_gate(
    *,
    explicit_authorization: bool = False,
    body_policy: Path = DEFAULT_BODY_POLICY,
    implementation_plan: Path = DEFAULT_IMPLEMENTATION_PLAN,
) -> dict[str, Any]:
    source_result = validate_manifest()
    evidence_result = validate_evidence_manifest()
    live_result = validate_live_external_sources(allow_network=False)

    body_policy_present = body_policy.exists()
    implementation_plan_present = implementation_plan.exists()
    live_landing_report_present = LEV1_REPORT.exists()

    blockers: list[str] = []
    if not source_result["ok"]:
        blockers.append("source manifest must pass before body ingestion")
    if not evidence_result["ok"]:
        blockers.append("evidence manifest must pass before body ingestion")
    if not live_result["ok"] or not live_landing_report_present:
        blockers.append("live external landing validation report is required before body ingestion")
    if not body_policy_present:
        blockers.append("copyright/robots/storage policy for external source bodies is required")
    if not implementation_plan_present:
        blockers.append("body-ingestion implementation plan is required before coding")
    if not explicit_authorization:
        blockers.append("explicit user authorization is required before live body ingestion/chunking/embedding")

    allowed_to_implement = not blockers
    decision = "proceed" if allowed_to_implement else "defer"
    if allowed_to_implement:
        next_leaf = "external source body ingestion implementation"
    elif body_policy_present and implementation_plan_present:
        next_leaf = "real-accountant-session RS2/RS3 evidence capture, or external source body-ingestion authorization gate"
    else:
        next_leaf = "real-accountant-session RS2/RS3 evidence capture, or external source body-ingestion policy plan"
    decision_record = BodyIngestionDecision(
        decision_id="esbd1-external-source-body-ingestion-decision-gate",
        decision=decision,
        allowed_to_implement=allowed_to_implement,
        source_manifest_ok=bool(source_result["ok"]),
        evidence_manifest_ok=bool(evidence_result["ok"]),
        live_landing_validation_ok=bool(live_result["ok"]),
        live_landing_report_present=live_landing_report_present,
        body_policy_present=body_policy_present,
        implementation_plan_present=implementation_plan_present,
        explicit_authorization=explicit_authorization,
        blockers=blockers,
        next_leaf=next_leaf,
    )

    return {
        "ok": bool(source_result["ok"] and evidence_result["ok"] and live_result["ok"] and live_landing_report_present),
        "errors": _prefixed_errors("source_manifest", source_result["errors"])
        + _prefixed_errors("evidence_manifest", evidence_result["errors"])
        + _prefixed_errors("live_external_source_validation", live_result["errors"])
        + ([] if live_landing_report_present else [f"missing live validation report: {_display_path(LEV1_REPORT)}"]),
        "decision": decision_record.to_dict(),
        "source_manifest": {
            "ok": source_result["ok"],
            "total": source_result.get("total", 0),
        },
        "evidence_manifest": {
            "ok": evidence_result["ok"],
            "total": evidence_result.get("total", 0),
        },
        "live_external_source_validation": {
            "ok": live_result["ok"],
            "target_count": live_result["target_count"],
            "network_checked": live_result["network_checked"],
            "body_text_stored": live_result["body_text_stored"],
            "report_present": live_landing_report_present,
        },
        "body_policy": str(_display_path(body_policy)),
        "implementation_plan": str(_display_path(implementation_plan)),
        "report_path": str(REPORT_PATH.relative_to(ROOT)),
        "next_leaf": next_leaf,
    }


def render_report(result: dict[str, Any]) -> str:
    decision = result["decision"]
    live = result["live_external_source_validation"]
    conclusion = (
        "External source body ingestion can proceed only after explicit user authorization is recorded; all prerequisite policy and plan artifacts are present."
        if decision["body_policy_present"] and decision["implementation_plan_present"]
        else "External source body ingestion remains deferred. Landing-surface validation and public-safe manifests exist, but copyright/robots/storage policy, an implementation plan, and explicit user authorization are required before any body fetch/store/chunk/embed work starts."
    )
    lines = [
        "# ESBD1 External Source Body-Ingestion Decision Gate",
        "",
        "> Scope: decision gate before any live external source body ingestion, chunking, embedding, crawling, or stored text pipeline.",
        "",
        "## 한 줄 결론",
        "",
        conclusion,
        "",
        "## Decision",
        "",
        f"- Decision: {decision['decision']}",
        f"- Allowed to implement: {decision['allowed_to_implement']}",
        f"- Source manifest ok: {decision['source_manifest_ok']}",
        f"- Evidence manifest ok: {decision['evidence_manifest_ok']}",
        f"- Live landing validation ok: {decision['live_landing_validation_ok']}",
        f"- Live landing report present: {decision['live_landing_report_present']}",
        f"- Body policy present: {decision['body_policy_present']}",
        f"- Implementation plan present: {decision['implementation_plan_present']}",
        f"- Explicit authorization: {decision['explicit_authorization']}",
        "",
        "## Preconditions Snapshot",
        "",
        f"- Source manifest records: {result['source_manifest']['total']}",
        f"- Evidence manifest records: {result['evidence_manifest']['total']}",
        f"- Live external targets: {live['target_count']}",
        f"- Network checked in this gate: {live['network_checked']}",
        f"- Body text stored by live validation: {live['body_text_stored']}",
        "",
        "## Blockers",
        "",
    ]
    lines.extend(f"- {blocker}" for blocker in decision["blockers"])
    lines.extend([
        "",
        "## What This Enables",
        "",
        "- The project now has a machine-readable stop/go gate before external body ingestion work.",
        "- Future body ingestion can start only when source/evidence manifests, landing validation, policy, plan, and authorization are all present.",
        "- Until then, external sources remain metadata/evidence surfaces only.",
        "",
        "## Still Not Implemented",
        "",
        "- live body fetching or crawling",
        "- source body storage",
        "- source-specific chunking",
        "- external body embeddings",
        "- external body index namespace",
        "- answer-time promotion of external body text",
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
    result = check_body_ingestion_decision_gate()
    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    REPORT_PATH.write_text(render_report(result), encoding="utf-8")
    return result


def _prefixed_errors(prefix: str, errors: list[str]) -> list[str]:
    return [f"{prefix}: {error}" for error in errors]


def _display_path(path: Path) -> str:
    try:
        return path.resolve().relative_to(ROOT).as_posix()
    except ValueError:
        return path.as_posix()


def main() -> None:
    parser = argparse.ArgumentParser(description="Run external source body-ingestion decision gate.")
    parser.add_argument("--format", choices=["text", "json", "markdown"], default="text")
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--authorize-body-ingestion", action="store_true")
    parser.add_argument("--body-policy", type=Path, default=DEFAULT_BODY_POLICY)
    parser.add_argument("--implementation-plan", type=Path, default=DEFAULT_IMPLEMENTATION_PLAN)
    args = parser.parse_args()

    result = (
        write_report()
        if args.write
        and not args.authorize_body_ingestion
        and args.body_policy == DEFAULT_BODY_POLICY
        and args.implementation_plan == DEFAULT_IMPLEMENTATION_PLAN
        else check_body_ingestion_decision_gate(
            explicit_authorization=args.authorize_body_ingestion,
            body_policy=args.body_policy,
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
