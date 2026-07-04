from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from kifrs.ingestion.manifest import (  # noqa: E402
    ALLOWED_BODY_STORAGE_POLICIES,
    PUBLIC_SAFE_STORAGE_POLICIES,
    validate_manifest,
)


REPORT_PATH = ROOT / "docs" / "reports" / "2026-07-05-as3-storage-boundary.md"

REQUIRED_SOURCE_CLASSES = {
    "primary_accounting_standard",
    "interpretive_accounting_material",
    "primary_audit_standard",
    "law_regulation",
    "filing_data",
    "client_private",
    "supporting_material",
}


def check_storage_boundary(report_path: Path = REPORT_PATH) -> dict[str, object]:
    if not report_path.exists():
        return {
            "ok": False,
            "errors": [f"missing report: {report_path}"],
            "missing_source_classes": sorted(REQUIRED_SOURCE_CLASSES),
            "missing_storage_labels": sorted(ALLOWED_BODY_STORAGE_POLICIES),
            "manifest_ok": False,
        }

    text = report_path.read_text(encoding="utf-8")
    errors: list[str] = []

    missing_source_classes = sorted(
        source_class for source_class in REQUIRED_SOURCE_CLASSES if f"`{source_class}`" not in text
    )
    if missing_source_classes:
        errors.append(f"missing source classes: {missing_source_classes}")

    missing_storage_labels = sorted(
        label for label in ALLOWED_BODY_STORAGE_POLICIES if f"`{label}`" not in text
    )
    if missing_storage_labels:
        errors.append(f"missing storage labels: {missing_storage_labels}")

    missing_public_safe_labels = sorted(
        label for label in PUBLIC_SAFE_STORAGE_POLICIES if f"`{label}`" not in text
    )
    if missing_public_safe_labels:
        errors.append(f"missing public-safe labels: {missing_public_safe_labels}")

    for required_phrase in (
        "Public reports must not include",
        "Ingestion Boundary",
        "client_private",
        "source remains `collection_seed`",
    ):
        if required_phrase not in text:
            errors.append(f"missing required AS3 phrase: {required_phrase}")

    manifest_result = validate_manifest()
    if not manifest_result["ok"]:
        errors.extend(f"manifest: {error}" for error in manifest_result["errors"])

    return {
        "ok": not errors,
        "errors": errors,
        "missing_source_classes": missing_source_classes,
        "missing_storage_labels": missing_storage_labels,
        "missing_public_safe_labels": missing_public_safe_labels,
        "manifest_ok": manifest_result["ok"],
        "manifest_total": manifest_result["total"],
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Check AS3 storage boundary policy against ingestion labels.")
    parser.add_argument("--format", choices=["text", "json"], default="text")
    args = parser.parse_args()

    result = check_storage_boundary()
    if args.format == "json":
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(f"ok: {result['ok']}")
        print(f"missing_source_classes: {result['missing_source_classes']}")
        print(f"missing_storage_labels: {result['missing_storage_labels']}")
        print(f"missing_public_safe_labels: {result['missing_public_safe_labels']}")
        print(f"manifest_ok: {result['manifest_ok']}")
        print(f"manifest_total: {result['manifest_total']}")
        for error in result["errors"]:
            print(f"- {error}")

    if not result["ok"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
