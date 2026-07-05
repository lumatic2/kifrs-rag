from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from kifrs.runtime.authority_boundary import AUTHORITY_ROLES, build_runtime_authority_boundary  # noqa: E402
from kifrs.workflows.kifrs1109.fixtures import FIXTURES as FIXTURES_1109  # noqa: E402
from kifrs.workflows.kifrs1109.review_pack import (  # noqa: E402
    generate_review_pack as generate_1109_review_pack,
    render_review_pack_markdown as render_1109_markdown,
)
from kifrs.workflows.kifrs1115.fixtures import FIXTURES as FIXTURES_1115  # noqa: E402
from kifrs.workflows.kifrs1115.review_pack import (  # noqa: E402
    generate_review_pack as generate_1115_review_pack,
    render_review_pack_markdown as render_1115_markdown,
)
from kifrs.workflows.kifrs1116.fixtures import FIXTURES as FIXTURES_1116  # noqa: E402
from kifrs.workflows.kifrs1116.review_pack import (  # noqa: E402
    generate_review_pack as generate_1116_review_pack,
    render_review_pack_markdown as render_1116_markdown,
)


REPORT_PATH = ROOT / "docs" / "reports" / "2026-07-05-mah3-review-pack-authority-panel.md"
PANEL_HEADINGS = (
    "### Primary K-IFRS evidence",
    "### Supporting interpretation",
    "### Legal boundary",
    "### Fact evidence",
    "### Client-private fact",
)
FORBIDDEN_MARKERS = ("source_body", "raw_xml", "raw filing payload", "copied protected material")


def build_panel_report() -> dict[str, Any]:
    cases = [
        (
            "1109",
            "scenario_01_corporate_bond_ac",
            ["[1109-4.1.2]"],
            generate_1109_review_pack(FIXTURES_1109[0], authority_boundary=build_runtime_authority_boundary(["[1109-4.1.2]"])),
            render_1109_markdown,
        ),
        (
            "1115",
            FIXTURES_1115[0].label,
            ["[1115-B39~B43]"],
            generate_1115_review_pack(FIXTURES_1115[0], authority_boundary=build_runtime_authority_boundary(["[1115-B39~B43]"])),
            render_1115_markdown,
        ),
        (
            "1116",
            "scenario_01_simple_office_lease",
            ["[1116-53]"],
            generate_1116_review_pack(FIXTURES_1116[0].txn, authority_boundary=build_runtime_authority_boundary(["[1116-53]"])),
            render_1116_markdown,
        ),
    ]
    rows = []
    errors: list[str] = []
    for workflow, case_id, primary_citations, pack, renderer in cases:
        rendered = renderer(pack)
        role_counts = {
            role: len(pack.authority_boundary.get(role, []))
            for role in AUTHORITY_ROLES
        }
        missing_headings = [heading for heading in PANEL_HEADINGS if heading not in rendered]
        forbidden = [marker for marker in FORBIDDEN_MARKERS if marker in rendered]
        if missing_headings:
            errors.append(f"{workflow}: missing panel headings {missing_headings}")
        if forbidden:
            errors.append(f"{workflow}: forbidden markers leaked {forbidden}")
        rows.append(
            {
                "workflow": workflow,
                "case_id": case_id,
                "primary_citations": primary_citations,
                "role_counts": role_counts,
                "has_runtime_authority_boundary": "## Runtime Authority Boundary" in rendered,
                "missing_headings": missing_headings,
                "forbidden_markers": forbidden,
            }
        )
    return {
        "title": "MAH3 Review Pack Authority Panel",
        "ok": not errors,
        "horizon": "multi-authority-runtime-hardening",
        "milestone": "MAH3",
        "workflows": rows,
        "errors": errors,
        "boundary": "external evidence does not replace K-IFRS primary evidence",
        "next_leaf": "MAH4_statement_draft_and_analytics_fact_hook",
        "report_path": _display_path(REPORT_PATH),
    }


def render_markdown(report: dict[str, Any]) -> str:
    lines = [
        f"# {report['title']}",
        "",
        "> Scope: MAH3 review pack authority panel across 1109, 1115, and 1116 workflows.",
        "",
        "## Result",
        "",
        f"- ok: {report['ok']}",
        f"- horizon: `{report['horizon']}`",
        f"- milestone: `{report['milestone']}`",
        f"- next leaf: `{report['next_leaf']}`",
        "",
        "## Boundary Statement",
        "",
        "- External evidence does not replace K-IFRS primary evidence.",
        "- Supporting interpretation, legal boundary, fact evidence, and client-private placeholders render as separate groups.",
        "",
        "## Workflow Coverage",
        "",
        "| Workflow | Case | Runtime panel | Primary | Supporting | Legal | Fact | Client-private |",
        "|---|---|---|---:|---:|---:|---:|---:|",
    ]
    for row in report["workflows"]:
        counts = row["role_counts"]
        lines.append(
            "| "
            f"{row['workflow']} | {row['case_id']} | {row['has_runtime_authority_boundary']} | "
            f"{counts['primary_kifrs_evidence']} | "
            f"{counts['supporting_interpretation']} | "
            f"{counts['legal_boundary']} | "
            f"{counts['fact_evidence']} | "
            f"{counts['client_private_fact']} |"
        )
    lines.extend(
        [
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
    report = build_panel_report()
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(render_markdown(report), encoding="utf-8")
    return report


def _display_path(path: Path) -> str:
    try:
        return path.resolve().relative_to(ROOT).as_posix()
    except ValueError:
        return path.as_posix()


def main() -> int:
    parser = argparse.ArgumentParser(description="Build the MAH3 review pack authority panel report.")
    parser.add_argument("--format", choices=["text", "json", "markdown"], default="text")
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--out", type=Path, default=REPORT_PATH)
    args = parser.parse_args()

    report = write_report(args.out) if args.write else build_panel_report()
    if args.format == "json":
        print(json.dumps(report, ensure_ascii=False, indent=2, default=str))
    elif args.format == "markdown":
        print(render_markdown(report), end="")
    else:
        print(report["title"])
        print(f"- ok: {report['ok']}")
        print(f"- workflows: {', '.join(row['workflow'] for row in report['workflows'])}")
        print(f"- next leaf: {report['next_leaf']}")
    return 0 if report["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
