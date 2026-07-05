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


REPORT_PATH = ROOT / "docs" / "reports" / "2026-07-05-mah2-runtime-evidence-contract.md"
PRIMARY_FIXTURE_CITATIONS = ["[1115-B39~B43]", "[1116-53]"]
FORBIDDEN_MARKERS = ("source_body", "raw_xml", "raw filing payload", "copied protected material")


def build_contract_report() -> dict[str, Any]:
    boundary = build_runtime_authority_boundary(PRIMARY_FIXTURE_CITATIONS)
    data = boundary.to_dict()
    rendered_boundary = render_runtime_authority_boundary(boundary)
    role_counts = {role: len(data[role]) for role in AUTHORITY_ROLES}
    errors: list[str] = []

    if tuple(data) != AUTHORITY_ROLES:
        errors.append("boundary role order does not match AUTHORITY_ROLES")
    if role_counts["primary_kifrs_evidence"] != len(PRIMARY_FIXTURE_CITATIONS):
        errors.append("primary K-IFRS citations were not preserved separately")
    for role in ("supporting_interpretation", "legal_boundary", "fact_evidence", "client_private_fact"):
        if role_counts[role] < 1:
            errors.append(f"missing runtime authority role: {role}")
    errors.extend(_public_safety_errors(data, rendered_boundary))

    return {
        "title": "MAH2 Runtime Evidence Contract",
        "ok": not errors,
        "horizon": "multi-authority-runtime-hardening",
        "milestone": "MAH2",
        "authority_roles": list(AUTHORITY_ROLES),
        "role_counts": role_counts,
        "primary_fixture_citations": list(PRIMARY_FIXTURE_CITATIONS),
        "public_safe": not _public_safety_errors(data, rendered_boundary),
        "errors": errors,
        "next_leaf": "MAH3_review_pack_authority_panel",
        "report_path": _display_path(REPORT_PATH),
    }


def render_markdown(report: dict[str, Any]) -> str:
    lines = [
        f"# {report['title']}",
        "",
        "> Scope: MAH2 contract hardening for separated runtime authority evidence.",
        "",
        "## Result",
        "",
        f"- ok: {report['ok']}",
        f"- horizon: `{report['horizon']}`",
        f"- milestone: `{report['milestone']}`",
        f"- next leaf: `{report['next_leaf']}`",
        "",
        "## Authority Roles",
        "",
        "| Role | Count | Meaning |",
        "|---|---:|---|",
    ]
    meanings = {
        "primary_kifrs_evidence": "K-IFRS paragraph citation; accounting conclusion anchor.",
        "supporting_interpretation": "KASB/FSS-style metadata; interpretation aid only.",
        "legal_boundary": "Law/regulation locator; legal boundary only.",
        "fact_evidence": "DART/OpenDART-style structured fact; calculation input only.",
        "client_private_fact": "Local-only client placeholder; no private material stored.",
    }
    for role in report["authority_roles"]:
        lines.append(f"| `{role}` | {report['role_counts'][role]} | {meanings[role]} |")
    lines.extend(
        [
            "",
            "## Contract Effect",
            "",
            "- Primary K-IFRS evidence is provided only through explicit citations.",
            "- Source records convert into non-primary roles only.",
            "- Client-private records are represented as local-only placeholders.",
            "- Runtime references omit source record bodies and protected payload fields.",
            "",
            "## Machine Result",
            "",
            "```json",
            json.dumps(report, ensure_ascii=False, indent=2, default=str),
            "```",
        ]
    )
    return "\n".join(lines) + "\n"


def write_report(path: Path = REPORT_PATH) -> dict[str, Any]:
    report = build_contract_report()
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(render_markdown(report), encoding="utf-8")
    return report


def _public_safety_errors(data: dict[str, list[dict[str, object]]], rendered_boundary: str) -> list[str]:
    haystacks = [rendered_boundary, json.dumps(data, ensure_ascii=False, sort_keys=True)]
    return [
        f"forbidden marker leaked: {marker}"
        for marker in FORBIDDEN_MARKERS
        if any(marker in haystack for haystack in haystacks)
    ]


def _display_path(path: Path) -> str:
    try:
        return path.resolve().relative_to(ROOT).as_posix()
    except ValueError:
        return path.as_posix()


def main() -> int:
    parser = argparse.ArgumentParser(description="Build the MAH2 runtime authority contract report.")
    parser.add_argument("--format", choices=["text", "json", "markdown"], default="text")
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--out", type=Path, default=REPORT_PATH)
    args = parser.parse_args()

    report = write_report(args.out) if args.write else build_contract_report()
    if args.format == "json":
        print(json.dumps(report, ensure_ascii=False, indent=2, default=str))
    elif args.format == "markdown":
        print(render_markdown(report), end="")
    else:
        print(report["title"])
        print(f"- ok: {report['ok']}")
        print(f"- roles: {', '.join(report['authority_roles'])}")
        print(f"- next leaf: {report['next_leaf']}")
    return 0 if report["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
