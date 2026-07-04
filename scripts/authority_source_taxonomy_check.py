from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any


DEFAULT_REPORT = Path("docs/reports/2026-07-05-as1-source-taxonomy.md")
DEFAULT_SOURCES = Path("docs/authority/sources.json")
REQUIRED_CLASSES = (
    "primary_accounting_standard",
    "interpretive_accounting_material",
    "primary_audit_standard",
    "law_regulation",
    "filing_data",
    "client_private",
    "supporting_material",
)


def build_report(*, report_path: Path = DEFAULT_REPORT, sources_path: Path = DEFAULT_SOURCES) -> dict[str, Any]:
    text = report_path.read_text(encoding="utf-8")
    source_data = json.loads(sources_path.read_text(encoding="utf-8"))
    source_ids = [source["id"] for source in source_data["sources"]]
    missing_classes = [class_id for class_id in REQUIRED_CLASSES if f"`{class_id}`" not in text]
    mapped_source_ids = sorted(set(re.findall(r"\| `([^`]+)` \| `[^`]+` \|", text)))
    missing_source_ids = [source_id for source_id in source_ids if source_id not in mapped_source_ids]
    return {
        "ok": not missing_classes and not missing_source_ids,
        "required_classes": list(REQUIRED_CLASSES),
        "missing_classes": missing_classes,
        "registry_source_ids": source_ids,
        "mapped_source_ids": mapped_source_ids,
        "missing_source_ids": missing_source_ids,
    }


def render_text(payload: dict[str, Any]) -> str:
    return "\n".join(
        [
            f"ok: {payload['ok']}",
            f"missing_classes: {payload['missing_classes']}",
            f"missing_source_ids: {payload['missing_source_ids']}",
        ]
    )


def main() -> int:
    parser = argparse.ArgumentParser(description="Check AS1 source taxonomy coverage.")
    parser.add_argument("--report", type=Path, default=DEFAULT_REPORT)
    parser.add_argument("--sources", type=Path, default=DEFAULT_SOURCES)
    parser.add_argument("--format", choices=["text", "json"], default="text")
    args = parser.parse_args()

    payload = build_report(report_path=args.report, sources_path=args.sources)
    if args.format == "json":
        print(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True))
    else:
        print(render_text(payload))
    return 0 if payload["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
