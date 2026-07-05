from __future__ import annotations

import argparse
import json
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from kifrs.ingestion.source_record import load_records, validate_source_records  # noqa: E402


REPORT_PATH = ROOT / "docs" / "reports" / "2026-07-05-mah1-runtime-evidence-boundary-audit.md"
SOURCE_RECORDS_PATH = ROOT / "docs" / "ingestion" / "non_ifrs_source_records.example.json"
CHUNKING_POLICY_PATH = ROOT / "docs" / "ingestion" / "non_ifrs_chunking_policy.json"


@dataclass(frozen=True)
class Surface:
    name: str
    path: str
    category: str
    supported_roles: tuple[str, ...]
    note: str


SURFACES = (
    Surface(
        "runtime evidence loader",
        "kifrs/runtime/evidence.py",
        "runtime",
        ("supporting_interpretation", "legal_boundary", "fact_evidence"),
        "Loads the older evidence manifest into safe reference dictionaries.",
    ),
    Surface(
        "external evidence panel",
        "kifrs/runtime/evidence_panel.py",
        "rendering",
        ("supporting_interpretation", "legal_boundary", "fact_evidence"),
        "Renders non-IFRS evidence by role in review-pack style markdown.",
    ),
    Surface(
        "answer boundary",
        "kifrs/runtime/answer_boundary.py",
        "composer",
        (
            "primary_kifrs_evidence",
            "supporting_interpretation",
            "legal_boundary",
            "fact_evidence",
        ),
        "Separates K-IFRS primary citations from external evidence references.",
    ),
    Surface(
        "1116 review pack",
        "kifrs/workflows/kifrs1116/review_pack.py",
        "workflow",
        ("supporting_interpretation", "legal_boundary", "fact_evidence"),
        "Accepts optional external evidence panel data.",
    ),
    Surface(
        "1109 review pack",
        "kifrs/workflows/kifrs1109/review_pack.py",
        "workflow",
        ("supporting_interpretation", "legal_boundary", "fact_evidence"),
        "Accepts optional external evidence panel data.",
    ),
    Surface(
        "1115 review pack",
        "kifrs/workflows/kifrs1115/review_pack.py",
        "workflow",
        ("supporting_interpretation", "legal_boundary", "fact_evidence"),
        "Accepts optional external evidence panel data.",
    ),
    Surface(
        "statement draft schema",
        "kifrs/workflows/statement_draft/schema.py",
        "workflow",
        ("fact_evidence",),
        "Carries evidence references for statement line candidates.",
    ),
)


REQUIRED_ROLES = (
    "primary_kifrs_evidence",
    "supporting_interpretation",
    "legal_boundary",
    "fact_evidence",
    "client_private_fact",
)


def build_boundary_audit() -> dict[str, Any]:
    records = load_records(SOURCE_RECORDS_PATH)
    record_validation = validate_source_records(records)
    chunking_policy = json.loads(CHUNKING_POLICY_PATH.read_text(encoding="utf-8"))
    existing_paths = {_display_path(path) for path in _iter_existing_files()}

    surface_rows = [
        {
            "name": surface.name,
            "path": surface.path,
            "exists": surface.path in existing_paths,
            "category": surface.category,
            "supported_roles": list(surface.supported_roles),
            "note": surface.note,
        }
        for surface in SURFACES
    ]
    runtime_roles = sorted({role for surface in SURFACES for role in surface.supported_roles})
    record_roles = _record_role_map(records)
    gaps = _gap_rows(runtime_roles, record_roles)
    return {
        "title": "MAH1 Runtime Evidence Boundary Audit",
        "ok": record_validation["ok"] and all(row["exists"] for row in surface_rows),
        "horizon": "multi-authority-runtime-hardening",
        "milestone": "MAH1",
        "source_record_validation": record_validation,
        "chunking_policy_lanes": sorted(chunking_policy.get("lanes", {}).keys()),
        "runtime_surfaces": surface_rows,
        "required_roles": list(REQUIRED_ROLES),
        "runtime_supported_roles": runtime_roles,
        "source_record_roles": record_roles,
        "gaps": gaps,
        "next_leaf": "MAH2_runtime_evidence_contract_hardening",
        "report_path": _display_path(REPORT_PATH),
    }


def render_markdown(audit: dict[str, Any]) -> str:
    lines = [
        f"# {audit['title']}",
        "",
        "> Scope: MAH1 audit for multi-authority runtime hardening.",
        "",
        "## Result",
        "",
        f"- ok: {audit['ok']}",
        f"- horizon: `{audit['horizon']}`",
        f"- milestone: `{audit['milestone']}`",
        f"- next leaf: `{audit['next_leaf']}`",
        "",
        "## What Exists Now",
        "",
        "| Surface | Path | Roles | Meaning |",
        "|---|---|---|---|",
    ]
    for row in audit["runtime_surfaces"]:
        roles = ", ".join(row["supported_roles"])
        lines.append(f"| {row['name']} | `{row['path']}` | {roles} | {row['note']} |")
    lines.extend(
        [
            "",
            "## NIS Handoff Compared To Runtime",
            "",
            "| Source record type | Citation role | Authority level | Runtime support |",
            "|---|---|---|---|",
        ]
    )
    for record_type, row in audit["source_record_roles"].items():
        support = "supported" if row["runtime_role_supported"] else "gap"
        lines.append(
            f"| {record_type} | {row['citation_role']} | {row['authority_level']} | {support} |"
        )
    lines.extend(
        [
            "",
            "## Hardening Gaps",
            "",
            "| Milestone | Surface | Gap |",
            "|---|---|---|",
        ]
    )
    for row in audit["gaps"]:
        lines.append(f"| {row['milestone']} | {row['surface']} | {row['gap']} |")
    lines.extend(
        [
            "",
            "## Machine Result",
            "",
            "```json",
            json.dumps(audit, ensure_ascii=False, indent=2, default=str),
            "```",
        ]
    )
    return "\n".join(lines) + "\n"


def write_report(path: Path = REPORT_PATH) -> dict[str, Any]:
    audit = build_boundary_audit()
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(render_markdown(audit), encoding="utf-8")
    return audit


def _record_role_map(records: list[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    runtime_roles = {role for surface in SURFACES for role in surface.supported_roles}
    role_map: dict[str, dict[str, Any]] = {}
    for record in records:
        record_type = str(record["record_type"])
        citation_role = str(record["citation_role"])
        runtime_role = "client_private_fact" if record_type == "client_private_fact" else citation_role
        role_map[record_type] = {
            "citation_role": citation_role,
            "authority_level": record["authority_level"],
            "retrieval_lane": record["retrieval_lane"],
            "runtime_role": runtime_role,
            "runtime_role_supported": runtime_role in runtime_roles,
        }
    return role_map


def _gap_rows(runtime_roles: list[str], record_roles: dict[str, dict[str, Any]]) -> list[dict[str, str]]:
    gaps = [
        {
            "milestone": "MAH2",
            "surface": "runtime authority contract",
            "gap": "NIS source records are validated but not yet converted by a shared authority boundary object.",
        },
        {
            "milestone": "MAH3",
            "surface": "review packs",
            "gap": "Review packs have an external evidence panel, but not a five-group authority panel with client-private placeholder support.",
        },
        {
            "milestone": "MAH4",
            "surface": "statement draft and analytics",
            "gap": "Structured facts need a runtime hook that keeps calculations as fact evidence rather than primary accounting authority.",
        },
        {
            "milestone": "MAH5",
            "surface": "composer gate",
            "gap": "No single gate proves primary/supporting/legal/fact/private evidence render together without protected source bodies.",
        },
    ]
    client_private = record_roles.get("client_private_fact", {})
    if "client_private_fact" not in runtime_roles and not client_private.get("runtime_role_supported"):
        gaps.insert(
            1,
            {
                "milestone": "MAH2",
                "surface": "client-private boundary",
                "gap": "Client-private source records exist only as a public-safe handoff placeholder and are not represented in runtime output yet.",
            },
        )
    return gaps


def _iter_existing_files() -> tuple[Path, ...]:
    return tuple((ROOT / surface.path) for surface in SURFACES if (ROOT / surface.path).exists())


def _display_path(path: Path) -> str:
    try:
        return path.resolve().relative_to(ROOT).as_posix()
    except ValueError:
        return path.as_posix()


def main() -> None:
    parser = argparse.ArgumentParser(description="Audit multi-authority runtime evidence boundaries.")
    parser.add_argument("--format", choices=["text", "json", "markdown"], default="text")
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--out", type=Path, default=REPORT_PATH)
    args = parser.parse_args()

    audit = write_report(args.out) if args.write else build_boundary_audit()
    if args.format == "json":
        print(json.dumps(audit, ensure_ascii=False, indent=2, default=str))
    elif args.format == "markdown":
        print(render_markdown(audit), end="")
    else:
        print(audit["title"])
        print(f"- ok: {audit['ok']}")
        print(f"- runtime supported roles: {', '.join(audit['runtime_supported_roles'])}")
        print(f"- gaps: {len(audit['gaps'])}")
        print(f"- next leaf: {audit['next_leaf']}")


if __name__ == "__main__":
    main()
