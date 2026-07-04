from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from kifrs.ingestion.manifest import ALLOWED_BODY_STORAGE_POLICIES  # noqa: E402


REPORT_PATH = ROOT / "docs" / "reports" / "2026-07-05-as4-ingestion-feasibility.md"

REQUIRED_SOURCE_CLASSES = {
    "primary_accounting_standard",
    "interpretive_accounting_material",
    "primary_audit_standard",
    "law_regulation",
    "filing_data",
    "client_private",
    "supporting_material",
}

REQUIRED_LANES = {
    "document_rag",
    "structured_data",
    "local_private_case_facts",
    "metadata_support_only",
}

REQUIRED_CONNECTOR_CANDIDATES = {
    "kasb-fss-interpretive-catalog",
    "opendart-structured-financials",
    "law-regulation-locator",
}


def check_ingestion_feasibility(report_path: Path = REPORT_PATH) -> dict[str, object]:
    if not report_path.exists():
        return _result(
            errors=[f"missing report: {report_path}"],
            missing_source_classes=sorted(REQUIRED_SOURCE_CLASSES),
            missing_lanes=sorted(REQUIRED_LANES),
            missing_connector_candidates=sorted(REQUIRED_CONNECTOR_CANDIDATES),
            missing_storage_labels=sorted(ALLOWED_BODY_STORAGE_POLICIES),
        )

    text = report_path.read_text(encoding="utf-8")
    errors: list[str] = []

    missing_source_classes = sorted(
        source_class for source_class in REQUIRED_SOURCE_CLASSES if f"`{source_class}`" not in text
    )
    if missing_source_classes:
        errors.append(f"missing source classes: {missing_source_classes}")

    missing_lanes = sorted(lane for lane in REQUIRED_LANES if f"`{lane}`" not in text)
    if missing_lanes:
        errors.append(f"missing lanes: {missing_lanes}")

    missing_connector_candidates = sorted(
        candidate for candidate in REQUIRED_CONNECTOR_CANDIDATES if f"`{candidate}`" not in text
    )
    if missing_connector_candidates:
        errors.append(f"missing connector candidates: {missing_connector_candidates}")

    missing_storage_labels = sorted(
        label for label in ALLOWED_BODY_STORAGE_POLICIES if f"`{label}`" not in text
    )
    if missing_storage_labels:
        errors.append(f"missing storage labels: {missing_storage_labels}")

    for required_phrase in (
        "Fetch",
        "Parse",
        "Chunk",
        "Embed",
        "Index",
        "metadata-only document source",
        "structured fact source",
    ):
        if required_phrase not in text:
            errors.append(f"missing required AS4 phrase: {required_phrase}")

    return _result(
        errors=errors,
        missing_source_classes=missing_source_classes,
        missing_lanes=missing_lanes,
        missing_connector_candidates=missing_connector_candidates,
        missing_storage_labels=missing_storage_labels,
    )


def _result(
    *,
    errors: list[str],
    missing_source_classes: list[str],
    missing_lanes: list[str],
    missing_connector_candidates: list[str],
    missing_storage_labels: list[str],
) -> dict[str, object]:
    return {
        "ok": not errors,
        "errors": errors,
        "missing_source_classes": missing_source_classes,
        "missing_lanes": missing_lanes,
        "missing_connector_candidates": missing_connector_candidates,
        "missing_storage_labels": missing_storage_labels,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Check AS4 ingestion feasibility matrix coverage.")
    parser.add_argument("--format", choices=["text", "json"], default="text")
    args = parser.parse_args()

    result = check_ingestion_feasibility()
    if args.format == "json":
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(f"ok: {result['ok']}")
        print(f"missing_source_classes: {result['missing_source_classes']}")
        print(f"missing_lanes: {result['missing_lanes']}")
        print(f"missing_connector_candidates: {result['missing_connector_candidates']}")
        print(f"missing_storage_labels: {result['missing_storage_labels']}")
        for error in result["errors"]:
            print(f"- {error}")

    if not result["ok"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
