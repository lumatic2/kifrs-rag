from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from kifrs.runtime.authority_boundary import (  # noqa: E402
    AUTHORITY_ROLES,
    build_runtime_authority_boundary,
    render_runtime_authority_boundary,
)
from scripts.default_retriever_guard import check_default_retriever_guard  # noqa: E402
from scripts.multi_authority_review_pack_panel import build_panel_report  # noqa: E402
from scripts.multi_authority_structured_fact_hook_report import build_structured_fact_hook_result  # noqa: E402
from scripts.non_ifrs_dataization_gate import build_gate as build_non_ifrs_gate  # noqa: E402
from scripts.quality_preflight import run_preflight  # noqa: E402
from scripts.rag_quality_final_gate import build_report as build_rag_quality_report  # noqa: E402
from scripts.validate_non_ifrs_chunking_policy import validate_policy  # noqa: E402
from scripts.validate_non_ifrs_source_records import build_validation as validate_source_records_fixture  # noqa: E402


GATE_REPORT_PATH = ROOT / "docs" / "reports" / "2026-07-05-mah5-runtime-demo-gate.md"
CLOSE_REPORT_PATH = ROOT / "docs" / "reports" / "2026-07-05-multi-authority-runtime-hardening-close-report.md"


def build_gate() -> dict[str, Any]:
    boundary = build_runtime_authority_boundary(
        primary_citations=["[1116-53]", "[1109-4.1.2]", "[1115-B39~B43]"]
    )
    boundary_data = boundary.to_dict()
    role_counts = {role: len(boundary_data[role]) for role in AUTHORITY_ROLES}
    review_pack_panel = build_panel_report()
    structured_fact_hook = build_structured_fact_hook_result()
    source_records = validate_source_records_fixture()
    chunking_policy = validate_policy()
    non_ifrs_gate = build_non_ifrs_gate()
    default_guard = check_default_retriever_guard()
    quality_preflight = run_preflight()
    rag_quality = build_rag_quality_report()
    rendered_demo = render_runtime_authority_boundary(boundary)

    errors: list[str] = []
    for role, count in role_counts.items():
        if count < 1:
            errors.append(f"missing authority role: {role}")
    if not review_pack_panel["ok"]:
        errors.append("review pack authority panel failed")
    if not structured_fact_hook["ok"]:
        errors.append("structured fact hook failed")
    if not source_records["ok"]:
        errors.extend(f"source records: {error}" for error in source_records["errors"])
    if not chunking_policy["ok"]:
        errors.extend(f"chunking policy: {error}" for error in chunking_policy["errors"])
    if not non_ifrs_gate["ok"]:
        errors.extend(f"non-ifrs gate: {error}" for error in non_ifrs_gate["errors"])
    if not default_guard["ok"]:
        errors.extend(f"default retriever guard: {error}" for error in default_guard["errors"])
    if not quality_preflight["ok"]:
        failed = [result["name"] for result in quality_preflight["results"] if result["returncode"] != 0]
        errors.append(f"quality preflight failed: {failed}")
    if not rag_quality["ok"]:
        errors.extend(f"rag quality: {failure}" for failure in rag_quality["failures"])
    if not _public_safe(rendered_demo):
        errors.append("runtime demo is not public safe")

    return {
        "title": "MAH5 Runtime Demo Gate",
        "ok": not errors,
        "horizon": "multi-authority-runtime-hardening",
        "milestone": "MAH5",
        "role_counts": role_counts,
        "review_pack_panel_ok": review_pack_panel["ok"],
        "structured_fact_hook_ok": structured_fact_hook["ok"],
        "source_records_ok": source_records["ok"],
        "chunking_policy_ok": chunking_policy["ok"],
        "non_ifrs_gate_ok": non_ifrs_gate["ok"],
        "default_retriever_guard_ok": default_guard["ok"],
        "quality_preflight_ok": quality_preflight["ok"],
        "rag_quality_ok": rag_quality["ok"],
        "public_safe": _public_safe(rendered_demo),
        "errors": errors,
        "runtime_demo": rendered_demo,
        "carried_regression_commands": [
            "python scripts\\non_ifrs_dataization_gate.py --format text",
            "python scripts\\validate_non_ifrs_source_records.py --format text",
            "python scripts\\validate_non_ifrs_chunking_policy.py --format text",
            "python scripts\\default_retriever_guard.py --format text",
            "python scripts\\quality_preflight.py --format text",
            "python scripts\\rag_quality_final_gate.py --format text",
        ],
        "next_horizon": "client-private-parser-runtime",
        "report_path": _display_path(GATE_REPORT_PATH),
        "close_report_path": _display_path(CLOSE_REPORT_PATH),
    }


def render_markdown(gate: dict[str, Any]) -> str:
    conclusion = (
        "Multi-authority runtime hardening is ready to close."
        if gate["ok"]
        else "Multi-authority runtime hardening is not ready; fix the listed errors."
    )
    lines = [
        f"# {gate['title']}",
        "",
        "> Scope: MAH5 gate for runtime authority boundary demo and carried regressions.",
        "",
        "## One-Line Conclusion",
        "",
        conclusion,
        "",
        "## Gate Status",
        "",
        f"- ok: {gate['ok']}",
        f"- public safe: {gate['public_safe']}",
        f"- review pack panel: {gate['review_pack_panel_ok']}",
        f"- structured fact hook: {gate['structured_fact_hook_ok']}",
        f"- source records: {gate['source_records_ok']}",
        f"- chunking policy: {gate['chunking_policy_ok']}",
        f"- non-IFRS dataization gate: {gate['non_ifrs_gate_ok']}",
        f"- default retriever guard: {gate['default_retriever_guard_ok']}",
        f"- quality preflight: {gate['quality_preflight_ok']}",
        f"- RAG quality final gate: {gate['rag_quality_ok']}",
        "",
        "## Role Counts",
        "",
        "| Role | Count |",
        "|---|---:|",
    ]
    for role, count in gate["role_counts"].items():
        lines.append(f"| {role} | {count} |")
    lines.extend(
        [
            "",
            "## Runtime Demo",
            "",
            gate["runtime_demo"],
            "",
            "## Carried Regression Commands",
            "",
        ]
    )
    lines.extend(f"- `{command}`" for command in gate["carried_regression_commands"])
    lines.extend(["", "## Errors", ""])
    lines.extend(f"- {error}" for error in gate["errors"]) if gate["errors"] else lines.append("- none")
    lines.extend(
        [
            "",
            "## Machine Result",
            "",
            "```json",
            json.dumps({key: value for key, value in gate.items() if key != "runtime_demo"}, ensure_ascii=False, indent=2, default=str),
            "```",
        ]
    )
    return "\n".join(lines) + "\n"


def render_close_markdown(gate: dict[str, Any]) -> str:
    lines = [
        "# Multi-Authority Runtime Hardening Close Report",
        "",
        "## Result",
        "",
        f"- close status: {'closed' if gate['ok'] else 'blocked'}",
        f"- gate report: `{gate['report_path']}`",
        f"- next horizon: `{gate['next_horizon']}`",
        "",
        "## Completed Milestones",
        "",
        "- MAH1 runtime evidence boundary audit",
        "- MAH2 runtime evidence contract hardening",
        "- MAH3 review pack authority panel",
        "- MAH4 statement draft and analytics fact hook",
        "- MAH5 authority composer gate and runtime demo",
        "",
        "## Product Meaning",
        "",
        "Workflow outputs can now show K-IFRS primary evidence, supporting interpretation, legal boundary, structured fact evidence, and client-private placeholders as separate authority groups.",
        "",
        "## Next Horizon",
        "",
        "`client-private-parser-runtime` should add real local parser runtime while preserving the no-public-client-material boundary.",
        "",
    ]
    return "\n".join(lines)


def write_reports() -> dict[str, Any]:
    gate = build_gate()
    GATE_REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    GATE_REPORT_PATH.write_text(render_markdown(gate), encoding="utf-8")
    CLOSE_REPORT_PATH.write_text(render_close_markdown(gate), encoding="utf-8")
    return gate


def _public_safe(rendered: str) -> bool:
    forbidden = ("api_key", "token", "source_body", "full_text", "raw_xml", "xbrl_dump")
    return not any(item in rendered for item in forbidden)


def _display_path(path: Path) -> str:
    try:
        return path.resolve().relative_to(ROOT).as_posix()
    except ValueError:
        return path.as_posix()


def main() -> int:
    parser = argparse.ArgumentParser(description="Run MAH5 multi-authority runtime gate.")
    parser.add_argument("--format", choices=["text", "json", "markdown"], default="text")
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()

    gate = write_reports() if args.write else build_gate()
    if args.format == "json":
        print(json.dumps(gate, ensure_ascii=False, indent=2, default=str))
    elif args.format == "markdown":
        print(render_markdown(gate), end="")
    else:
        print(gate["title"])
        print(f"- ok: {gate['ok']}")
        print(f"- public safe: {gate['public_safe']}")
        print(f"- role counts: {gate['role_counts']}")
        print(f"- next horizon: {gate['next_horizon']}")
    return 0 if gate["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
