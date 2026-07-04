from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


ALLOWED_STATUS = {"not_sent", "sent", "responded", "scheduled", "declined", "completed"}
REQUIRED_FIELDS = {"reviewer_alias", "status", "invite_sent", "channel", "contacted_at", "follow_up_by"}
PROTECTED_MARKERS = {
    "customer_name",
    "client_name",
    "company_name",
    "business_registration_number",
    "resident_registration_number",
    "account_number",
    "raw_contract",
    "source_body",
}


def load_outreach(path: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for line_no, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        if not line.strip():
            continue
        row = json.loads(line)
        row["_line_no"] = line_no
        rows.append(row)
    return rows


def check_outreach(path: Path) -> tuple[bool, list[str], dict[str, int]]:
    errors: list[str] = []
    rows = load_outreach(path)
    counts = {status: 0 for status in sorted(ALLOWED_STATUS)}
    seen_aliases: set[str] = set()
    for row in rows:
        line_no = row.get("_line_no", "?")
        missing = sorted(field for field in REQUIRED_FIELDS if field not in row)
        if missing:
            errors.append(f"line {line_no}: missing fields: {', '.join(missing)}")
        status = row.get("status")
        if status not in ALLOWED_STATUS:
            errors.append(f"line {line_no}: unsupported status: {status}")
        else:
            counts[status] += 1
        alias = row.get("reviewer_alias")
        if alias in seen_aliases:
            errors.append(f"line {line_no}: duplicate reviewer_alias: {alias}")
        if alias:
            seen_aliases.add(alias)
        if _contains_protected_marker(row):
            errors.append(f"line {line_no}: protected marker found")
        if status in {"sent", "responded", "scheduled", "completed"} and row.get("invite_sent") is not True:
            errors.append(f"line {line_no}: status {status} requires invite_sent true")
    return not errors, errors, counts


def _contains_protected_marker(value: Any) -> bool:
    if isinstance(value, dict):
        return any(str(key) in PROTECTED_MARKERS or _contains_protected_marker(child) for key, child in value.items())
    if isinstance(value, list):
        return any(_contains_protected_marker(item) for item in value)
    if isinstance(value, str):
        return value in PROTECTED_MARKERS
    return False


def main() -> int:
    parser = argparse.ArgumentParser(description="Check real accountant outreach ledger.")
    parser.add_argument("--ledger", type=Path, required=True)
    args = parser.parse_args()
    ok, errors, counts = check_outreach(args.ledger)
    print(f"ok: {ok}")
    print("counts:")
    for status, count in counts.items():
        print(f"- {status}: {count}")
    for error in errors:
        print(f"- {error}")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
