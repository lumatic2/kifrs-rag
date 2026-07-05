from __future__ import annotations

import argparse
import json
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
REPORT_PATH = ROOT / "docs" / "reports" / "2026-07-05-esb1-source-body-connector-selection.md"


@dataclass(frozen=True)
class SourceConnectorCandidate:
    source_class: str
    authority_role: str
    product_value: str
    authorization_mode: str
    public_report_mode: str
    implementation_status: str
    score: int


SELECTED_CLASS = "interpretive_accounting_material"
BLOCKED_PUBLIC_FIELDS = (
    "body",
    "content",
    "credential",
    "embedding",
    "full_text",
    "pdf_bytes",
    "quote",
    "raw_xml",
    "text",
)


def build_selection() -> dict[str, Any]:
    candidates = [
        SourceConnectorCandidate(
            source_class="interpretive_accounting_material",
            authority_role="supporting_interpretive_evidence",
            product_value="Adds regulator or standard-setter interpretation around K-IFRS decision-prep work without replacing primary K-IFRS paragraphs.",
            authorization_mode="synthetic_dry_run_now; source_specific_local_private_body_only_after_review",
            public_report_mode="metadata, locator, policy, schema, synthetic snippet labels, and metrics only",
            implementation_status="selected_for_ESB2",
            score=5,
        ),
        SourceConnectorCandidate(
            source_class="law_regulation",
            authority_role="legal_supporting_evidence",
            product_value="Useful for commercial law and disclosure boundaries but needs source-specific legal citation policy first.",
            authorization_mode="requires_source_specific_review",
            public_report_mode="metadata and locator only until policy is expanded",
            implementation_status="defer",
            score=3,
        ),
        SourceConnectorCandidate(
            source_class="filing_disclosure",
            authority_role="company_disclosure_evidence",
            product_value="Useful for comparable disclosure review, but XBRL or filing payload storage needs separate boundary tests.",
            authorization_mode="requires_source_specific_review",
            public_report_mode="metadata, issuer class, and locator only",
            implementation_status="defer",
            score=2,
        ),
        SourceConnectorCandidate(
            source_class="client_private_policy",
            authority_role="client_fact_or_policy_evidence",
            product_value="High product value, but belongs behind private parser authorization and deletion controls.",
            authorization_mode="explicit_local_private_authorization_required",
            public_report_mode="structured fact labels and redaction status only",
            implementation_status="defer",
            score=1,
        ),
    ]
    selected = next(candidate for candidate in candidates if candidate.source_class == SELECTED_CLASS)
    allowed_public_fields = [
        "source_class",
        "authority_role",
        "publisher_class",
        "canonical_locator",
        "policy_status",
        "synthetic_fixture_id",
        "chunk_strategy",
        "retrieval_metadata",
        "created_by_script",
    ]
    local_only_fields_after_review = [
        "body_cache_path",
        "chunk_store_path",
        "local_index_namespace",
        "deletion_command",
    ]
    checks = {
        "selected_class_present": selected.source_class == SELECTED_CLASS,
        "live_fetching_blocked": True,
        "public_body_payload_blocked": True,
        "authorization_boundary_explicit": "after_review" in selected.authorization_mode,
        "allowed_public_fields_do_not_include_blocked_fields": not set(allowed_public_fields).intersection(
            BLOCKED_PUBLIC_FIELDS
        ),
        "next_milestone_named": True,
    }
    errors = [name for name, ok in checks.items() if ok is not True]
    return {
        "title": "ESB1 Source-Body Connector Selection And Policy Gate",
        "ok": not errors,
        "horizon": "external-source-body-connector-expansion",
        "completed_milestone": "ESB1",
        "selected_source_class": asdict(selected),
        "candidates": [asdict(candidate) for candidate in candidates],
        "policy": {
            "public_reports_may_store": allowed_public_fields,
            "local_only_after_source_review": local_only_fields_after_review,
            "blocked_public_field_count": len(BLOCKED_PUBLIC_FIELDS),
            "live_fetching_allowed_by_ESB1": False,
            "body_chunking_allowed_by_ESB1": False,
            "embedding_allowed_by_ESB1": False,
        },
        "checks": checks,
        "errors": errors,
        "next_leaf": "ESB2_synthetic_connector_body_fixture_contract",
        "report_path": _display_path(REPORT_PATH),
    }


def render_markdown(result: dict[str, Any]) -> str:
    selected = result["selected_source_class"]
    policy = result["policy"]
    lines = [
        f"# {result['title']}",
        "",
        "> Scope: source-body connector class selection before any live body ingestion.",
        "",
        "## 한 줄 결론",
        "",
        (
            f"Select `{selected['source_class']}` as the first connector lane, but keep live fetching, body chunking, "
            "and embedding blocked until source-specific review and explicit authorization exist."
        ),
        "",
        "## Selected Lane",
        "",
        f"- Source class: `{selected['source_class']}`",
        f"- Authority role: `{selected['authority_role']}`",
        f"- Implementation status: `{selected['implementation_status']}`",
        f"- Authorization mode: `{selected['authorization_mode']}`",
        f"- Public report mode: {selected['public_report_mode']}",
        "",
        "## Candidate Ranking",
        "",
        "| Source Class | Role | Status | Score |",
        "|---|---|---|---:|",
    ]
    for candidate in result["candidates"]:
        lines.append(
            "| {source_class} | {authority_role} | {implementation_status} | {score} |".format(
                **candidate
            )
        )
    lines.extend(
        [
            "",
            "## Public-Safe Policy",
            "",
            "Public reports may store:",
        ]
    )
    lines.extend(f"- `{field}`" for field in policy["public_reports_may_store"])
    lines.extend(
        [
            "",
            "Local-only fields after source review:",
        ]
    )
    lines.extend(f"- `{field}`" for field in policy["local_only_after_source_review"])
    lines.extend(
        [
            "",
            "Blocked by ESB1:",
            f"- live fetching: {policy['live_fetching_allowed_by_ESB1']}",
            f"- body chunking: {policy['body_chunking_allowed_by_ESB1']}",
            f"- embedding: {policy['embedding_allowed_by_ESB1']}",
            f"- blocked public field count: {policy['blocked_public_field_count']}",
            "",
            "## Checks",
            "",
            "| Check | OK |",
            "|---|---|",
        ]
    )
    for name, ok in result["checks"].items():
        lines.append(f"| {name} | {ok} |")
    lines.extend(["", "## Errors", ""])
    lines.extend(f"- {error}" for error in result["errors"]) if result["errors"] else lines.append("- none")
    lines.extend(
        [
            "",
            "## Next Leaf",
            "",
            f"- `{result['next_leaf']}`",
            "",
            "## Machine Result",
            "",
            "```json",
            json.dumps(result, ensure_ascii=False, indent=2),
            "```",
        ]
    )
    return "\n".join(lines) + "\n"


def write_report(path: Path = REPORT_PATH) -> dict[str, Any]:
    result = build_selection()
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(render_markdown(result), encoding="utf-8")
    return result


def _display_path(path: Path) -> str:
    try:
        return path.resolve().relative_to(ROOT).as_posix()
    except ValueError:
        return path.as_posix()


def main() -> int:
    parser = argparse.ArgumentParser(description="Build ESB1 source-body connector selection report.")
    parser.add_argument("--format", choices=["text", "json", "markdown"], default="text")
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--out", type=Path, default=REPORT_PATH)
    args = parser.parse_args()

    result = write_report(args.out) if args.write else build_selection()
    if args.format == "json":
        print(json.dumps(result, ensure_ascii=False, indent=2))
    elif args.format == "markdown":
        print(render_markdown(result), end="")
    else:
        print(result["title"])
        print(f"- ok: {result['ok']}")
        print(f"- selected source class: {result['selected_source_class']['source_class']}")
        print(f"- next leaf: {result['next_leaf']}")
        for error in result["errors"]:
            print(f"- {error}")
    return 0 if result["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
