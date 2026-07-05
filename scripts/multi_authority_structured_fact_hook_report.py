from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from kifrs.runtime.authority_boundary import build_runtime_authority_boundary  # noqa: E402
from kifrs.workflows.audit_analytics import (  # noqa: E402
    SYNTHETIC_FS,
    calculate_metrics,
    detect_anomalies,
    link_statement_candidates,
)
from kifrs.workflows.kifrs1115.fixtures import FIXTURES as FIXTURES_1115  # noqa: E402
from kifrs.workflows.kifrs1115.review_pack import generate_review_pack as pack_1115  # noqa: E402
from kifrs.workflows.statement_draft import from_1115_review_pack  # noqa: E402


REPORT_PATH = ROOT / "docs" / "reports" / "2026-07-05-mah4-structured-fact-runtime-hook.md"


def build_structured_fact_hook_result() -> dict[str, Any]:
    boundary = build_runtime_authority_boundary(primary_citations=["[1115-B39~B43]"])
    pack = pack_1115(FIXTURES_1115[3], authority_boundary=boundary)
    candidates = from_1115_review_pack(pack)
    findings = detect_anomalies(calculate_metrics(SYNTHETIC_FS))
    linked = link_statement_candidates(findings, candidates)
    amount_candidates = [item for item in candidates if item.amount is not None and item.statement != "note"]
    fact_ref_count = sum(len(item.evidence_refs) for item in amount_candidates)
    linked_fact_ref_count = sum(len(item.evidence_refs) for item in linked)
    promoted_primary_refs = [
        ref
        for item in amount_candidates
        for ref in item.evidence_refs
        if ref.get("authority_role") == "primary_kifrs_evidence"
    ]
    return {
        "title": "MAH4 Structured Fact Runtime Hook",
        "ok": fact_ref_count > 0 and linked_fact_ref_count > 0 and not promoted_primary_refs,
        "horizon": "multi-authority-runtime-hardening",
        "milestone": "MAH4",
        "statement_candidates": len(candidates),
        "amount_candidates": len(amount_candidates),
        "fact_ref_count": fact_ref_count,
        "linked_findings": len(linked),
        "linked_fact_ref_count": linked_fact_ref_count,
        "promoted_primary_refs": len(promoted_primary_refs),
        "next_leaf": "MAH5_authority_composer_gate_and_runtime_demo",
        "report_path": _display_path(REPORT_PATH),
    }


def render_markdown(result: dict[str, Any]) -> str:
    lines = [
        f"# {result['title']}",
        "",
        "> Scope: MAH4 proof that structured facts attach to statement draft and analytics as fact evidence only.",
        "",
        "## Result",
        "",
        f"- ok: {result['ok']}",
        f"- horizon: `{result['horizon']}`",
        f"- milestone: `{result['milestone']}`",
        f"- next leaf: `{result['next_leaf']}`",
        "",
        "## Counts",
        "",
        f"- statement candidates: {result['statement_candidates']}",
        f"- amount candidates: {result['amount_candidates']}",
        f"- fact evidence refs on statement amount candidates: {result['fact_ref_count']}",
        f"- linked analytics findings: {result['linked_findings']}",
        f"- fact evidence refs preserved on linked findings: {result['linked_fact_ref_count']}",
        f"- primary evidence refs promoted into fact hook: {result['promoted_primary_refs']}",
        "",
        "## Boundary Meaning",
        "",
        "- Structured facts are calculation support, not accounting authority.",
        "- Statement draft amount lines can hold fact evidence references.",
        "- Analytics links preserve those fact evidence references for reviewer traceability.",
        "",
        "## Machine Result",
        "",
        "```json",
        json.dumps(result, ensure_ascii=False, indent=2, default=str),
        "```",
    ]
    return "\n".join(lines) + "\n"


def write_report(path: Path = REPORT_PATH) -> dict[str, Any]:
    result = build_structured_fact_hook_result()
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(render_markdown(result), encoding="utf-8")
    return result


def _display_path(path: Path) -> str:
    try:
        return path.resolve().relative_to(ROOT).as_posix()
    except ValueError:
        return path.as_posix()


def main() -> None:
    parser = argparse.ArgumentParser(description="Render MAH4 structured fact hook report.")
    parser.add_argument("--format", choices=["text", "json", "markdown"], default="text")
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--out", type=Path, default=REPORT_PATH)
    args = parser.parse_args()

    result = write_report(args.out) if args.write else build_structured_fact_hook_result()
    if args.format == "json":
        print(json.dumps(result, ensure_ascii=False, indent=2, default=str))
    elif args.format == "markdown":
        print(render_markdown(result), end="")
    else:
        print(result["title"])
        print(f"- ok: {result['ok']}")
        print(f"- fact refs: {result['fact_ref_count']}")
        print(f"- linked fact refs: {result['linked_fact_ref_count']}")
        print(f"- next leaf: {result['next_leaf']}")


if __name__ == "__main__":
    main()
