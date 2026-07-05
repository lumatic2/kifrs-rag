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


def validate_records(path: Path = DEFAULT_RECORDS_PATH) -> dict[str, Any]:
    records = load_records(path)
    result = validate_source_records(records)
    return {
        "ok": result["ok"],
        "title": "NIS3 Dataization Fixtures",
        "milestone": "NIS3",
        "records_path": _display_path(path),
        "total": result["total"],
        "by_type": result["by_type"],
        "errors": result["errors"],
        "next_leaf": "NIS4_chunking_and_embedding_policy",
        "report_path": _display_path(REPORT_PATH),
    }


def render_markdown(result: dict[str, Any]) -> str:
    lines = [
        "# NIS3 Dataization Fixtures",
        "",
        "> Scope: public-safe non-IFRS source record fixture and validator.",
        "",
        "## One-Line Conclusion",
        "",
        "The four source lanes now have a single public-safe fixture validated by the NIS2 source record contract.",
        "",
        "## Fixture",
        "",
        f"- Records path: `{result['records_path']}`",
        f"- Total records: {result['total']}",
        "",
        "## Record Type Coverage",
        "",
        "| Record Type | Count |",
        "|---|---:|",
    ]
    for record_type, count in result["by_type"].items():
        lines.append(f"| `{record_type}` | {count} |")
    if result["errors"]:
        lines.extend(["", "## Errors", ""])
        lines.extend(f"- {error}" for error in result["errors"])
    lines.extend(
        [
            "",
            "## Next Leaf",
            "",
            result["next_leaf"],
            "",
            "## Machine Result",
            "",
            "```json",
            json.dumps(result, ensure_ascii=False, indent=2, default=str),
            "```",
        ]
    )
    return "\n".join(lines) + "\n"


def write_report(path: Path = REPORT_PATH, records_path: Path = DEFAULT_RECORDS_PATH) -> dict[str, Any]:
    result = validate_records(records_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(render_markdown(result), encoding="utf-8")
    return result


def _display_path(path: Path) -> str:
    try:
        return path.resolve().relative_to(ROOT).as_posix()
    except ValueError:
        return path.as_posix()


def main() -> None:
    parser = argparse.ArgumentParser(description="Validate non-IFRS source record fixtures.")
    parser.add_argument("records_path", nargs="?", type=Path, default=DEFAULT_RECORDS_PATH)
    parser.add_argument("--format", choices=["text", "json", "markdown"], default="text")
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--out", type=Path, default=REPORT_PATH)
    args = parser.parse_args()

    result = write_report(args.out, args.records_path) if args.write else validate_records(args.records_path)
    if args.format == "json":
        print(json.dumps(result, ensure_ascii=False, indent=2, default=str))
    elif args.format == "markdown":
        print(render_markdown(result), end="")
    else:
        print(result["title"])
        print(f"- ok: {result['ok']}")
        print(f"- records_path: {result['records_path']}")
        print(f"- total: {result['total']}")
        print(f"- by_type: {result['by_type']}")
        print(f"- next_leaf: {result['next_leaf']}")
        print(f"- report_path: {result['report_path']}")
        for error in result["errors"]:
            print(f"- {error}")
    if not result["ok"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
