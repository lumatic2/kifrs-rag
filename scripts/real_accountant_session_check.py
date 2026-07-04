from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


REQUIRED_ACTUAL_FIELDS = {
    "actual_feedback_evidence",
    "reviewer_metadata",
    "notes_file",
    "capture_manifest",
    "queue_jsonl",
}
REQUIRED_REVIEWER_FIELDS = {"role", "service_line", "experience_context"}
PROTECTED_MARKERS = {
    "raw_contract",
    "customer_name",
    "client_name",
    "company_name",
    "business_registration_number",
    "resident_registration_number",
    "account_number",
    "source_body",
}


def check_session_manifest(manifest_path: Path, *, root: Path | None = None) -> tuple[bool, list[str], str]:
    root = root or Path.cwd()
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    errors: list[str] = []

    if _contains_protected_marker(manifest):
        errors.append("manifest contains protected marker")

    actual = bool(manifest.get("actual_feedback_evidence"))
    if not actual:
        _check_packet_files(manifest, root, errors)
        return not errors, errors, "ready_to_schedule"

    missing_fields = sorted(field for field in REQUIRED_ACTUAL_FIELDS if field not in manifest)
    if missing_fields:
        errors.append(f"missing actual evidence fields: {', '.join(missing_fields)}")

    reviewer = manifest.get("reviewer_metadata", {})
    missing_reviewer = sorted(field for field in REQUIRED_REVIEWER_FIELDS if not reviewer.get(field))
    if missing_reviewer:
        errors.append(f"missing reviewer metadata: {', '.join(missing_reviewer)}")

    for key in ("notes_file", "capture_manifest", "queue_jsonl"):
        value = manifest.get(key)
        if value and not (root / value).exists():
            errors.append(f"missing {key}: {value}")

    capture_manifest = manifest.get("capture_manifest")
    if capture_manifest and (root / capture_manifest).exists():
        capture = json.loads((root / capture_manifest).read_text(encoding="utf-8"))
        if capture.get("actual_feedback_evidence") is not True:
            errors.append("capture manifest is not actual_feedback_evidence true")

    return not errors, errors, "actual_feedback"


def _check_packet_files(manifest: dict[str, Any], root: Path, errors: list[str]) -> None:
    for field in ("packet_files", "session_files"):
        for item in manifest.get(field, []):
            if not (root / item).exists():
                errors.append(f"missing {field} item: {item}")


def _contains_protected_marker(value: Any) -> bool:
    if isinstance(value, dict):
        return any(str(key) in PROTECTED_MARKERS or _contains_protected_marker(child) for key, child in value.items())
    if isinstance(value, list):
        return any(_contains_protected_marker(item) for item in value)
    if isinstance(value, str):
        return value in PROTECTED_MARKERS
    return False


def main() -> int:
    parser = argparse.ArgumentParser(description="Check real accountant session evidence manifest.")
    parser.add_argument("--manifest", type=Path, required=True)
    args = parser.parse_args()

    ok, errors, mode = check_session_manifest(args.manifest)
    print(f"ok: {ok}")
    print(f"mode: {mode}")
    for error in errors:
        print(f"- {error}")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
