from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.default_retriever_guard import check_default_retriever_guard  # noqa: E402
from scripts.rag_reliability_retrieval_citation_diagnostics import build_diagnostics  # noqa: E402


REPORT_PATH = ROOT / "docs" / "reports" / "2026-07-05-rr4-repair-policy-candidate.md"

METHODOLOGY_NODES = [
    "rag-evaluation-metrics",
    "rag-retrieval-strategy",
    "rag-retrieval-rank-debugging-playbook",
    "rag-reranking-strategy",
]


def build_policy_candidate() -> dict[str, Any]:
    diagnostics = build_diagnostics()
    guard = check_default_retriever_guard()
    target = diagnostics["retrievers"][1]
    accepted = [
        {
            "id": "keep_default_hybrid",
            "decision": "accept",
            "policy": "Keep MCP runtime default at `hybrid`.",
            "why": "Default remains stable while RR evidence is retrieval/citation-focused rather than full answer-quality proof.",
            "evidence": "default retriever guard",
        },
        {
            "id": "keep_target_opt_in_eval_path",
            "decision": "accept",
            "policy": f"Keep `{target}` available as an opt-in eval/demo retriever.",
            "why": "RR3 shows target recall@20 is 1.000 with zero required-citation top-20 misses.",
            "evidence": "RR3 retrieval/citation diagnostics",
        },
        {
            "id": "use_bucket_diagnostics_for_rr5",
            "decision": "accept",
            "policy": "Use RR2 buckets and RR3 rank transitions as the promotion evidence shape.",
            "why": "Bucket-level evidence exposes disclosure, workflow, judgment, and exam-convention behavior without protected question text.",
            "evidence": "RR2 eval matrix + RR3 diagnostics",
        },
    ]
    deferred = [
        {
            "id": "default_promotion",
            "decision": "defer",
            "policy": f"Do not promote `{target}` to default in this milestone.",
            "blocker": "Requires RR5 promotion gate and explicit authorization.",
        },
        {
            "id": "mcp_mode_exposure",
            "decision": "defer",
            "policy": f"Do not expose `{target}` as an MCP search mode yet.",
            "blocker": "Would change user-facing runtime behavior before answer-quality regression policy is finalized.",
        },
        {
            "id": "heavy_reranker_default",
            "decision": "defer",
            "policy": "Do not make reranked or heavy reranker paths default.",
            "blocker": "RR3's current issue is coverage/promotion policy, not a measured need for heavier latency/cost.",
        },
        {
            "id": "new_external_source_ingestion",
            "decision": "defer",
            "policy": "Do not add non-IFRS source ingestion inside this RAG reliability horizon.",
            "blocker": "That belongs to the next horizon after RR5 handoff.",
        },
    ]
    verification = [
        "python scripts\\default_retriever_guard.py --format text",
        "python scripts\\rag_reliability_retrieval_citation_diagnostics.py --format text",
        "python scripts\\quality_preflight.py --format text",
    ]
    errors: list[str] = []
    if guard["ok"] is not True:
        errors.extend(f"default_guard: {error}" for error in guard["errors"])
    if diagnostics["ok"] is not True:
        errors.extend(f"diagnostics: {error}" for error in diagnostics["errors"])
    if guard["target_retriever_exposed_in_mcp"]:
        errors.append("target retriever is exposed in MCP modes before policy approval")
    if guard["promote_to_default"]:
        errors.append("promotion gate says promote before RR5 handoff")
    return {
        "ok": not errors,
        "title": "RR4 Repair Policy Candidate",
        "milestone": "RR4",
        "methodology_nodes": METHODOLOGY_NODES,
        "accepted_policies": accepted,
        "deferred_policies": deferred,
        "verification_commands": verification,
        "guard_snapshot": {
            "default_mode": guard["default_mode"],
            "target_retriever": guard["target_retriever"],
            "target_retriever_exposed_in_mcp": guard["target_retriever_exposed_in_mcp"],
            "promotion_decision": guard["promotion_decision"],
            "promote_to_default": guard["promote_to_default"],
        },
        "rr3_snapshot": {
            "target_misses": len(diagnostics["target_misses"]),
            "recovered_item_ids": diagnostics["recovered_item_ids"],
            "failure_taxonomy": diagnostics["failure_taxonomy"],
        },
        "next_leaf": "RR5 promotion gate and next-horizon handoff",
        "errors": errors,
        "report_path": _display_path(REPORT_PATH),
    }


def render_markdown(policy: dict[str, Any]) -> str:
    lines = [
        "# RR4 Repair Policy Candidate",
        "",
        "> Scope: decide which RAG repair behavior can be used now, and which runtime changes stay deferred.",
        "",
        "## 한 줄 결론",
        "",
        _one_line_conclusion(policy),
        "",
        "## Methodology Source",
        "",
    ]
    lines.extend(f"- `{node}`" for node in policy["methodology_nodes"])
    lines.extend(
        [
            "",
            "## Accepted Policies",
            "",
            "| ID | Policy | Why | Evidence |",
            "|---|---|---|---|",
        ]
    )
    for item in policy["accepted_policies"]:
        lines.append(f"| {item['id']} | {item['policy']} | {item['why']} | {item['evidence']} |")
    lines.extend(
        [
            "",
            "## Deferred Policies",
            "",
            "| ID | Policy | Blocker |",
            "|---|---|---|",
        ]
    )
    for item in policy["deferred_policies"]:
        lines.append(f"| {item['id']} | {item['policy']} | {item['blocker']} |")
    lines.extend(
        [
            "",
            "## Guard Snapshot",
            "",
            f"- Default mode: `{policy['guard_snapshot']['default_mode']}`",
            f"- Target retriever: `{policy['guard_snapshot']['target_retriever']}`",
            f"- Target exposed in MCP: {policy['guard_snapshot']['target_retriever_exposed_in_mcp']}",
            f"- Promotion decision: {policy['guard_snapshot']['promotion_decision']}",
            f"- Promote to default: {policy['guard_snapshot']['promote_to_default']}",
            "",
            "## RR3 Snapshot",
            "",
            f"- Target misses: {policy['rr3_snapshot']['target_misses']}",
            f"- Recovered item ids: {', '.join(policy['rr3_snapshot']['recovered_item_ids'])}",
            f"- Failure taxonomy: {policy['rr3_snapshot']['failure_taxonomy']}",
            "",
            "## Verification Commands",
            "",
        ]
    )
    lines.extend(f"- `{command}`" for command in policy["verification_commands"])
    lines.extend(["", "## Next Leaf", "", policy["next_leaf"]])
    if policy["errors"]:
        lines.extend(["", "## Errors", ""])
        lines.extend(f"- {error}" for error in policy["errors"])
    lines.extend(
        [
            "",
            "## Machine Result",
            "",
            "```json",
            json.dumps(policy, ensure_ascii=False, indent=2, default=str),
            "```",
        ]
    )
    return "\n".join(lines) + "\n"


def write_report(path: Path = REPORT_PATH) -> dict[str, Any]:
    policy = build_policy_candidate()
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(render_markdown(policy), encoding="utf-8")
    return policy


def _one_line_conclusion(policy: dict[str, Any]) -> str:
    if policy["ok"]:
        return "Use the repair retriever as an opt-in eval/demo path, keep runtime default unchanged, and carry promotion to RR5."
    return "Repair policy candidate failed a guard; fix errors before RR5."


def _display_path(path: Path) -> str:
    try:
        return path.resolve().relative_to(ROOT).as_posix()
    except ValueError:
        return path.as_posix()


def main() -> None:
    parser = argparse.ArgumentParser(description="Render RR4 RAG repair policy candidate.")
    parser.add_argument("--format", choices=["text", "json", "markdown"], default="text")
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--out", type=Path, default=REPORT_PATH)
    args = parser.parse_args()

    policy = write_report(args.out) if args.write else build_policy_candidate()
    if args.format == "json":
        print(json.dumps(policy, ensure_ascii=False, indent=2, default=str))
    elif args.format == "markdown":
        print(render_markdown(policy), end="")
    else:
        print(policy["title"])
        print(f"- ok: {policy['ok']}")
        print(f"- accepted: {len(policy['accepted_policies'])}")
        print(f"- deferred: {len(policy['deferred_policies'])}")
        print(f"- next_leaf: {policy['next_leaf']}")
        print(f"- report_path: {policy['report_path']}")
    if not policy["ok"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
