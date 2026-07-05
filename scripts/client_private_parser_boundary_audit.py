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

from scripts.client_private_deletion_attestation_check import check_deletion_attestation  # noqa: E402
from scripts.client_private_local_parser_adapter_contract_check import (  # noqa: E402
    check_local_parser_adapter_contract,
)
from scripts.client_private_parser_dry_run_fixture_check import check_parser_dry_run_fixture  # noqa: E402
from scripts.client_private_upload_storage_policy_check import check_upload_storage_policy  # noqa: E402


REPORT_PATH = ROOT / "docs" / "reports" / "2026-07-05-cp1-private-parser-boundary-audit.md"


@dataclass(frozen=True)
class Surface:
    name: str
    path: str
    category: str
    role: str


SURFACES = (
    Surface(
        "client-private case intake schema",
        "kifrs/feedback/case_intake.py",
        "schema",
        "Defines local-private intake, redaction, upload/storage policy, dry-run fixture, deletion attestation, and routing objects.",
    ),
    Surface(
        "local parser prototype and adapter scaffold",
        "kifrs/feedback/local_parser.py",
        "runtime_scaffold",
        "Defines structured-facts-only parser prototype, adapter contract, dry-run gate, and scaffold refusal behavior.",
    ),
    Surface(
        "upload/storage policy check",
        "scripts/client_private_upload_storage_policy_check.py",
        "policy_gate",
        "Checks local ephemeral quarantine, no persistence, and no commit boundary.",
    ),
    Surface(
        "parser dry-run fixture check",
        "scripts/client_private_parser_dry_run_fixture_check.py",
        "fixture_gate",
        "Checks synthetic structured-facts-only parser-shaped fixture.",
    ),
    Surface(
        "deletion attestation check",
        "scripts/client_private_deletion_attestation_check.py",
        "deletion_gate",
        "Checks public-safe deletion evidence contract.",
    ),
    Surface(
        "local parser adapter contract check",
        "scripts/client_private_local_parser_adapter_contract_check.py",
        "adapter_gate",
        "Checks adapter contract and prototype handoff without real file parsing.",
    ),
    Surface(
        "runtime authority boundary",
        "kifrs/runtime/authority_boundary.py",
        "runtime_boundary",
        "Already exposes client_private_fact as a separated authority role.",
    ),
    Surface(
        "client-private source record fixture",
        "docs/ingestion/non_ifrs_source_records.example.json",
        "source_record",
        "Contains public-safe client_private_fact placeholder lane.",
    ),
)


def build_boundary_audit() -> dict[str, Any]:
    checks = {
        "upload_storage_policy": check_upload_storage_policy(),
        "parser_dry_run_fixture": check_parser_dry_run_fixture(),
        "deletion_attestation": check_deletion_attestation(),
        "adapter_contract": check_local_parser_adapter_contract(),
    }
    surface_rows = [
        {
            "name": surface.name,
            "path": surface.path,
            "category": surface.category,
            "role": surface.role,
            "exists": (ROOT / surface.path).exists(),
        }
        for surface in SURFACES
    ]
    errors: list[str] = []
    errors.extend(f"missing surface: {row['path']}" for row in surface_rows if not row["exists"])
    for check_name, result in checks.items():
        if result.get("ok") is not True:
            errors.extend(f"{check_name}: {error}" for error in result.get("errors", []))
    gaps = _gap_rows()
    return {
        "title": "CP1 Private Parser Boundary Audit",
        "ok": not errors,
        "horizon": "client-private-parser-runtime",
        "milestone": "CP1",
        "surfaces": surface_rows,
        "checks": _check_snapshots(checks),
        "gaps": gaps,
        "next_leaf": "CP2_local_parser_runtime_contract",
        "report_path": _display_path(REPORT_PATH),
        "errors": errors,
    }


def render_markdown(audit: dict[str, Any]) -> str:
    lines = [
        f"# {audit['title']}",
        "",
        "> Scope: CP1 audit for local-only private parser/runtime boundary.",
        "",
        "## Result",
        "",
        f"- ok: {audit['ok']}",
        f"- horizon: `{audit['horizon']}`",
        f"- milestone: `{audit['milestone']}`",
        f"- next leaf: `{audit['next_leaf']}`",
        "",
        "## Existing Surfaces",
        "",
        "| Surface | Path | Category | Exists | Role |",
        "|---|---|---|---|---|",
    ]
    for row in audit["surfaces"]:
        lines.append(
            f"| {row['name']} | `{row['path']}` | {row['category']} | {row['exists']} | {row['role']} |"
        )
    lines.extend(
        [
            "",
            "## Check Snapshots",
            "",
            "| Check | OK | Meaning |",
            "|---|---|---|",
        ]
    )
    for name, row in audit["checks"].items():
        lines.append(f"| {name} | {row['ok']} | {row['meaning']} |")
    lines.extend(
        [
            "",
            "## Implementation Gaps",
            "",
            "| Milestone | Gap |",
            "|---|---|",
        ]
    )
    for row in audit["gaps"]:
        lines.append(f"| {row['milestone']} | {row['gap']} |")
    lines.extend(["", "## Errors", ""])
    lines.extend(f"- {error}" for error in audit["errors"]) if audit["errors"] else lines.append("- none")
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


def _check_snapshots(checks: dict[str, dict[str, Any]]) -> dict[str, dict[str, Any]]:
    return {
        "upload_storage_policy": {
            "ok": checks["upload_storage_policy"].get("ok"),
            "meaning": "Storage policy forbids raw/private persistence and commits.",
        },
        "parser_dry_run_fixture": {
            "ok": checks["parser_dry_run_fixture"].get("ok"),
            "meaning": "Synthetic parser-shaped structured facts route to a review-pack candidate.",
        },
        "deletion_attestation": {
            "ok": checks["deletion_attestation"].get("ok"),
            "meaning": "Deletion evidence is public-safe and records no raw file/body/OCR/embedding.",
        },
        "adapter_contract": {
            "ok": checks["adapter_contract"].get("ok"),
            "meaning": "Adapter contract and prototype handoff exist but still do not read real files.",
        },
    }


def _gap_rows() -> list[dict[str, str]]:
    return [
        {
            "milestone": "CP2",
            "gap": "Existing parser prototype and adapter contract are useful, but there is no single runtime parser contract object for this horizon.",
        },
        {
            "milestone": "CP3",
            "gap": "Parser outputs do not yet convert into runtime `client_private_fact` authority references.",
        },
        {
            "milestone": "CP4",
            "gap": "Deletion attestation exists, but runtime close is not yet gated on retention/deletion state.",
        },
        {
            "milestone": "CP5",
            "gap": "No `client_private_parser_runtime_gate.py` closes parser contract, authority adapter, deletion gate, and carried multi-authority/RAG regressions together.",
        },
    ]


def _display_path(path: Path) -> str:
    try:
        return path.resolve().relative_to(ROOT).as_posix()
    except ValueError:
        return path.as_posix()


def main() -> int:
    parser = argparse.ArgumentParser(description="Audit client-private parser runtime boundary.")
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
        print(f"- surfaces: {len(audit['surfaces'])}")
        print(f"- gaps: {len(audit['gaps'])}")
        print(f"- next leaf: {audit['next_leaf']}")
    return 0 if audit["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
