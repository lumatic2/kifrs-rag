from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from kifrs.ingestion.source_record import load_records, validate_source_records  # noqa: E402


DEFAULT_RECORDS_PATH = ROOT / "docs" / "ingestion" / "non_ifrs_source_records.example.json"
REPORT_PATH = ROOT / "docs" / "reports" / "2026-07-05-nis3-dataization-fixtures.md"


def build_validation(records_path: Path = DEFAULT_RECORDS_PATH) -> dict[str, Any]:
    errors: list[str] = []
    if not records_path.exists():
        return {
            "ok": False,
            "title": "NIS3 Dataization Fixtures",
            "records_path": _display_path(records_path),
            "errors": [f"missing records file: {_display_path(records_path)}"],
            "total": 0,
            "by_type": {},
            "next_leaf": "NIS4_chunking_and_embedding_policy",
            "report_path": _display_path(REPORT_PATH),
        }
    try:
        records = load_records(records_path)
    except Exception as exc:  # pragma: no cover - defensive CLI boundary
        return {
            "ok": False,
            "title": "NIS3 Dataization Fixtures",
            "records_path": _display_path(records_path),
            "errors": [f"failed to load records: {exc}"],
            "total": 0,
            "by_type": {},
            "next_leaf": "NIS4_chunking_and_embedding_policy",
            "report_path": _display_path(REPORT_PATH),
        }
    result = validate_source_records(records)
    errors.extend(result["errors"])
    required_types = {"document_metadata", "law_locator", "structured_fact", "client_private_fact"}
    missing_types = sorted(record_type for record_type in required_types if result["by_type"].get(record_type, 0) == 0)
    errors.extend(f"missing required record type: {record_type}" for record_type in missing_types)
    return {
        "ok": not errors,
        "title": "NIS3 Dataization Fixtures",
        "records_path": _display_path(records_path),
        "total": result["total"],
        "by_type": result["by_type"],
        "required_types": sorted(required_types),
        "next_leaf": "NIS4_chunking_and_embedding_policy",
        "errors": errors,
        "report_path": _display_path(REPORT_PATH),
    }


def render_markdown(validation: dict[str, Any]) -> str:
    conclusion = (
        "The non-IFRS source record fixture covers all planned source lanes and is public-safe."
        if validation["ok"]
        else "The non-IFRS source record fixture is not ready; fix the listed errors."
    )
    lines = [
        "# NIS3 Dataization Fixtures",
        "",
        "> Scope: validate public-safe non-IFRS source record fixtures.",
        "",
        "## One-Line Conclusion",
        "",
        conclusion,
        "",
        "## Fixture",
        "",
        f"- Records path: `{validation['records_path']}`",
        f"- Total records: {validation['total']}",
        "",
        "## Coverage",
        "",
        "| Record Type | Count |",
        "|---|---:|",
    ]
    for record_type in validation["required_types"]:
        lines.append(f"| `{record_type}` | {validation['by_type'].get(record_type, 0)} |")
    lines.extend(["", "## Next Leaf", "", validation["next_leaf"]])
    if validation["errors"]:
        lines.extend(["", "## Errors", ""])
        lines.extend(f"- {error}" for error in validation["errors"])
    lines.extend(
        [
            "",
            "## Machine Result",
            "",
            "```json",
            json.dumps(validation, ensure_ascii=False, indent=2, default=str),
            "```",
        ]
    )
    return "\n".join(lines) + "\n"


def write_report(records_path: Path = DEFAULT_RECORDS_PATH, path: Path = REPORT_PATH) -> dict[str, Any]:
    validation = build_validation(records_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(render_markdown(validation), encoding="utf-8")
    return validation


def _display_path(path: Path) -> str:
    try:
        return path.resolve().relative_to(ROOT).as_posix()
    except ValueError:
        return path.as_posix()


def main() -> None:
    parser = argparse.ArgumentParser(description="Validate public-safe non-IFRS source records.")
    parser.add_argument("records_path", nargs="?", type=Path, default=DEFAULT_RECORDS_PATH)
    parser.add_argument("--format", choices=["text", "json", "markdown"], default="text")
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--out", type=Path, default=REPORT_PATH)
    args = parser.parse_args()

    validation = write_report(args.records_path, args.out) if args.write else build_validation(args.records_path)
    if args.format == "json":
        print(json.dumps(validation, ensure_ascii=False, indent=2, default=str))
    elif args.format == "markdown":
        print(render_markdown(validation), end="")
    else:
        print(validation["title"])
        print(f"- ok: {validation['ok']}")
        print(f"- records_path: {validation['records_path']}")
        print(f"- total: {validation['total']}")
        print(f"- by_type: {validation['by_type']}")
        print(f"- next_leaf: {validation['next_leaf']}")
        print(f"- report_path: {validation['report_path']}")
    if not validation["ok"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
