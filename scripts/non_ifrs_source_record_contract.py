from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from kifrs.ingestion.source_record import (  # noqa: E402
    ALLOWED_AUTHORITY_LEVELS,
    ALLOWED_RETRIEVAL_LANES,
    ALLOWED_SOURCE_RECORD_TYPES,
)


REPORT_PATH = ROOT / "docs" / "reports" / "2026-07-05-nis2-source-record-contract.md"


def build_contract_report() -> dict[str, Any]:
    record_types = {
        "document_metadata": {
            "purpose": "KASB/FSS/FSC-style supporting document metadata without committed body text.",
            "retrieval_lane": "document_metadata",
            "authority_level": "supporting",
            "storage": "public_metadata_only",
        },
        "law_locator": {
            "purpose": "Law/regulation locator and legal-boundary evidence without article body copy.",
            "retrieval_lane": "law_locator",
            "authority_level": "legal_boundary",
            "storage": "no_store_link_only",
        },
        "structured_fact": {
            "purpose": "OpenDART/XBRL-like facts as normalized structured values.",
            "retrieval_lane": "structured_fact",
            "authority_level": "fact",
            "storage": "public_synthetic_fixture",
        },
        "client_private_fact": {
            "purpose": "Local-only client fact placeholder that never commits private content.",
            "retrieval_lane": "local_private_fact",
            "authority_level": "client_private",
            "storage": "no_store_handoff",
        },
    }
    errors: list[str] = []
    if set(record_types) != set(ALLOWED_SOURCE_RECORD_TYPES):
        errors.append("record type report does not match source_record contract")
    return {
        "ok": not errors,
        "title": "NIS2 Source Record Contract",
        "milestone": "NIS2",
        "record_types": record_types,
        "allowed_authority_levels": sorted(ALLOWED_AUTHORITY_LEVELS),
        "allowed_retrieval_lanes": sorted(ALLOWED_RETRIEVAL_LANES),
        "contract_module": "kifrs/ingestion/source_record.py",
        "test_path": "tests/test_source_record_contract.py",
        "next_leaf": "NIS3_dataization_fixtures_and_validators",
        "errors": errors,
        "report_path": _display_path(REPORT_PATH),
    }


def render_markdown(report: dict[str, Any]) -> str:
    lines = [
        "# NIS2 Source Record Contract",
        "",
        "> Scope: canonical record contract for non-IFRS source dataization.",
        "",
        "## One-Line Conclusion",
        "",
        "Non-IFRS dataization now has one source record contract across document metadata, law locators, structured facts, and client-private placeholders.",
        "",
        "## Record Types",
        "",
        "| Type | Retrieval Lane | Authority Level | Storage | Purpose |",
        "|---|---|---|---|---|",
    ]
    for record_type, item in report["record_types"].items():
        lines.append(
            f"| `{record_type}` | `{item['retrieval_lane']}` | `{item['authority_level']}` | `{item['storage']}` | {item['purpose']} |"
        )
    lines.extend(
        [
            "",
            "## Contract Files",
            "",
            f"- Module: `{report['contract_module']}`",
            f"- Tests: `{report['test_path']}`",
            "",
            "## Next Leaf",
            "",
            report["next_leaf"],
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


def _display_path(path: Path) -> str:
    try:
        return path.resolve().relative_to(ROOT).as_posix()
    except ValueError:
        return path.as_posix()


def main() -> None:
    parser = argparse.ArgumentParser(description="Render NIS2 source record contract report.")
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
        print(f"- record_types: {', '.join(report['record_types'])}")
        print(f"- next_leaf: {report['next_leaf']}")
        print(f"- report_path: {report['report_path']}")
    if not report["ok"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
