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


BODY_POLICY_PATH = ROOT / "docs" / "reports" / "2026-07-05-external-source-body-storage-policy.md"
IMPLEMENTATION_PLAN_PATH = ROOT / "docs" / "reports" / "2026-07-05-external-source-body-ingestion-plan.md"
REPORT_PATH = ROOT / "docs" / "reports" / "2026-07-05-espp1-external-source-body-policy-plan.md"

FORBIDDEN_PUBLIC_FIELDS = {
    "api_key",
    "body",
    "content",
    "credential",
    "embedding",
    "excerpt",
    "full_text",
    "pdf_bytes",
    "quote",
    "raw_xml",
    "source_body",
    "text",
    "token",
    "xbrl_dump",
}


@dataclass(frozen=True)
class ExternalSourceBodyPolicyPlan:
    policy_id: str
    source_classes: list[str]
    body_storage_mode: str
    public_artifact_rule: str
    local_artifact_rule: str
    required_source_checks: list[str]
    required_operator_checks: list[str]
    implementation_steps: list[str]
    proceed_gate_requirements: list[str]
    forbidden_public_fields: list[str]
    body_fetching_allowed_by_this_plan: bool
    chunking_allowed_by_this_plan: bool
    embedding_allowed_by_this_plan: bool
    commit_allowed_by_this_plan: bool

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def default_policy_plan() -> ExternalSourceBodyPolicyPlan:
    return ExternalSourceBodyPolicyPlan(
        policy_id="espp1-external-source-body-policy-plan",
        source_classes=[
            "interpretive_accounting_material",
            "law_regulation",
            "primary_audit_standard",
            "supporting_material",
        ],
        body_storage_mode="local_private_body_only_after_source_review",
        public_artifact_rule="public repo may store metadata, locators, schema, tests, aggregate metrics, and author-written notes only",
        local_artifact_rule="body cache, chunks, and embeddings may exist only in gitignored local/private paths after source-specific review",
        required_source_checks=[
            "record publisher and canonical locator",
            "check robots/terms/license constraints for the exact source",
            "classify authority role before retrieval use",
            "choose source-specific chunk strategy before storing any chunk",
            "document deletion/reindex command before first local cache write",
        ],
        required_operator_checks=[
            "run metadata-only live validation before source-specific review",
            "verify target cache/index paths are gitignored",
            "run forbidden-field scan before committing any report or manifest",
            "keep K-IFRS primary evidence priority above external body text",
            "record explicit user authorization before live body ingestion",
        ],
        implementation_steps=[
            "source-specific policy record",
            "local cache path contract",
            "parser/chunker dry-run with synthetic text",
            "forbidden-field regression tests",
            "explicit authorization gate",
        ],
        proceed_gate_requirements=[
            "source manifest ok",
            "evidence manifest ok",
            "live landing validation report present",
            "external source body storage policy present",
            "external source body ingestion implementation plan present",
            "explicit user authorization present",
        ],
        forbidden_public_fields=sorted(FORBIDDEN_PUBLIC_FIELDS),
        body_fetching_allowed_by_this_plan=False,
        chunking_allowed_by_this_plan=False,
        embedding_allowed_by_this_plan=False,
        commit_allowed_by_this_plan=False,
    )


def validate_policy_plan(plan: ExternalSourceBodyPolicyPlan) -> list[str]:
    errors: list[str] = []
    if not plan.source_classes:
        errors.append("source_classes: must not be empty")
    if plan.body_storage_mode != "local_private_body_only_after_source_review":
        errors.append("body_storage_mode: must require source review and local private storage")
    if "metadata" not in plan.public_artifact_rule or "author-written notes" not in plan.public_artifact_rule:
        errors.append("public_artifact_rule: must limit public output to metadata and author-written notes")
    if "gitignored" not in plan.local_artifact_rule:
        errors.append("local_artifact_rule: must require gitignored local/private paths")
    if not any("robots/terms/license" in check for check in plan.required_source_checks):
        errors.append("required_source_checks: robots/terms/license check is required")
    if not any("explicit user authorization" in check for check in plan.required_operator_checks):
        errors.append("required_operator_checks: explicit authorization check is required")
    for flag in (
        "body_fetching_allowed_by_this_plan",
        "chunking_allowed_by_this_plan",
        "embedding_allowed_by_this_plan",
        "commit_allowed_by_this_plan",
    ):
        if getattr(plan, flag) is not False:
            errors.append(f"{flag}: policy plan must not authorize implementation")
    missing_forbidden = sorted(FORBIDDEN_PUBLIC_FIELDS.difference(plan.forbidden_public_fields))
    if missing_forbidden:
        errors.append(f"forbidden_public_fields: missing {missing_forbidden}")
    return errors


def check_policy_plan() -> dict[str, Any]:
    plan = default_policy_plan()
    errors = validate_policy_plan(plan)
    return {
        "ok": not errors,
        "errors": errors,
        "policy_plan": plan.to_dict(),
        "body_policy_path": str(BODY_POLICY_PATH.relative_to(ROOT)),
        "implementation_plan_path": str(IMPLEMENTATION_PLAN_PATH.relative_to(ROOT)),
        "report_path": str(REPORT_PATH.relative_to(ROOT)),
        "next_leaf": "real-accountant-session RS2/RS3 evidence capture, or external source body-ingestion authorization gate",
    }


def render_body_policy(result: dict[str, Any]) -> str:
    plan = result["policy_plan"]
    lines = [
        "# External Source Body Storage Policy",
        "",
        "> Scope: policy required before any live external source body fetch, cache, chunk, embed, or index work.",
        "",
        "## Decision",
        "",
        "This policy does not authorize body ingestion. It defines the storage boundary that must exist before a separate authorization gate can allow implementation.",
        "",
        "## Covered Source Classes",
        "",
    ]
    lines.extend(f"- `{source_class}`" for source_class in plan["source_classes"])
    lines.extend([
        "",
        "## Storage Boundary",
        "",
        f"- Body storage mode: `{plan['body_storage_mode']}`",
        f"- Public artifact rule: {plan['public_artifact_rule']}",
        f"- Local artifact rule: {plan['local_artifact_rule']}",
        "",
        "## Required Source Checks",
        "",
    ])
    lines.extend(f"- {check}" for check in plan["required_source_checks"])
    lines.extend([
        "",
        "## Required Operator Checks",
        "",
    ])
    lines.extend(f"- {check}" for check in plan["required_operator_checks"])
    lines.extend([
        "",
        "## Public Forbidden Fields",
        "",
    ])
    lines.extend(f"- `{field}`" for field in plan["forbidden_public_fields"])
    lines.extend([
        "",
        "## Authorization Boundary",
        "",
        f"- Body fetching allowed by this policy: {plan['body_fetching_allowed_by_this_plan']}",
        f"- Chunking allowed by this policy: {plan['chunking_allowed_by_this_plan']}",
        f"- Embedding allowed by this policy: {plan['embedding_allowed_by_this_plan']}",
        f"- Commit allowed by this policy: {plan['commit_allowed_by_this_plan']}",
    ])
    return "\n".join(lines) + "\n"


def render_implementation_plan(result: dict[str, Any]) -> str:
    plan = result["policy_plan"]
    lines = [
        "# External Source Body Ingestion Implementation Plan",
        "",
        "> Scope: staged implementation plan that remains blocked until explicit authorization is recorded.",
        "",
        "## One-Line Conclusion",
        "",
        "The next implementation is not body ingestion itself. The next implementation is a source-specific authorization gate that proves policy, plan, source review, and public-safe tests before any live body cache is touched.",
        "",
        "## Implementation Steps",
        "",
    ]
    lines.extend(f"- {step}" for step in plan["implementation_steps"])
    lines.extend([
        "",
        "## Proceed Gate Requirements",
        "",
    ])
    lines.extend(f"- {requirement}" for requirement in plan["proceed_gate_requirements"])
    lines.extend([
        "",
        "## Not Implemented Here",
        "",
        "- live body fetching or crawling",
        "- source body cache",
        "- body chunker",
        "- external body embedding namespace",
        "- answer-time use of external body text",
        "",
        "## Next Leaf",
        "",
        str(result["next_leaf"]),
    ])
    return "\n".join(lines) + "\n"


def render_report(result: dict[str, Any]) -> str:
    lines = [
        "# ESPP1 External Source Body Policy Plan",
        "",
        "> Scope: policy and implementation-plan prerequisite for ESBD1.",
        "",
        "## 한 줄 결론",
        "",
        "External body ingestion still remains blocked, but the missing policy and implementation-plan artifacts now exist. The only remaining implementation blocker should be explicit user authorization plus any source-specific review required by the next gate.",
        "",
        "## Outputs",
        "",
        f"- Body policy: `{result['body_policy_path']}`",
        f"- Implementation plan: `{result['implementation_plan_path']}`",
        "",
        "## Validation",
        "",
        f"- ok: {result['ok']}",
        f"- errors: {result['errors']}",
        "",
        "## Boundary",
        "",
        "- This does not fetch, cache, chunk, embed, or index any external source body.",
        "- This does not authorize live body ingestion.",
        "- This preserves public-safe metadata-only repo boundaries.",
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
    return "\n".join(lines) + "\n"


def write_reports() -> dict[str, Any]:
    result = check_policy_plan()
    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    BODY_POLICY_PATH.write_text(render_body_policy(result), encoding="utf-8")
    IMPLEMENTATION_PLAN_PATH.write_text(render_implementation_plan(result), encoding="utf-8")
    REPORT_PATH.write_text(render_report(result), encoding="utf-8")
    return result


def main() -> None:
    parser = argparse.ArgumentParser(description="Check external source body-ingestion policy and plan prerequisites.")
    parser.add_argument("--format", choices=["text", "json", "markdown"], default="text")
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()

    result = write_reports() if args.write else check_policy_plan()
    if args.format == "json":
        print(json.dumps(result, ensure_ascii=False, indent=2, default=str))
    elif args.format == "markdown":
        print(render_report(result), end="")
    else:
        print(f"ok: {result['ok']}")
        print(f"body_policy_path: {result['body_policy_path']}")
        print(f"implementation_plan_path: {result['implementation_plan_path']}")
        print(f"next_leaf: {result['next_leaf']}")
        for error in result["errors"]:
            print(f"- {error}")

    if not result["ok"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
