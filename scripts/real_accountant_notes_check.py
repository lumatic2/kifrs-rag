from __future__ import annotations

import argparse
import re
from pathlib import Path


REQUIRED_MARKERS = {
    "## Session Metadata",
    "## Scores",
    "## Top Positive",
    "## Top Risk",
    "## Missing Inputs",
    "## Safe Correction Candidates",
    "## Boundary Confirmation",
}
REQUIRED_FILLED_PREFIXES = {
    "- Date:",
    "- Reviewer role:",
    "- Reviewer service-line:",
    "- Reviewer experience context:",
    "- Session mode:",
}
REQUIRED_CHECKBOXES = {
    "- [x] No raw contract copied",
    "- [x] No customer/client/company identifier copied",
    "- [x] No private filing body copied",
    "- [x] No K-IFRS source text copied",
    "- [x] Notes are safe to convert into queue candidates",
}
PROTECTED_MARKERS = {
    "raw_contract",
    "customer_name",
    "client_name",
    "company_name",
    "business_registration_number",
    "resident_registration_number",
    "personal_id",
    "account_number",
    "source_body",
    "raw_filing",
    "contract_body",
}
IDENTIFIER_PATTERNS = {
    "business_registration_number": re.compile(r"\b\d{3}-\d{2}-\d{5}\b"),
    "resident_registration_number": re.compile(r"\b\d{6}-[1-4]\d{6}\b"),
}
PLACEHOLDER_PATTERNS = {
    "Actual feedback evidence: false until completed",
    "- Date:",
    "- Reviewer role:",
    "- Reviewer service-line:",
    "- Reviewer experience context:",
    "- Session mode: screen share / in-person / async review",
    "- Workflow fit (1-5):",
    "- Evidence boundary clarity (1-5):",
    "- Review pack usefulness (1-5):",
    "- Human-review boundary clarity (1-5):",
    "- Real-case PoC willingness (1-5):",
}


def check_actual_notes(path: Path) -> tuple[bool, list[str]]:
    errors: list[str] = []
    if not path.exists():
        return False, [f"missing notes file: {path}"]

    text = path.read_text(encoding="utf-8")
    lower_text = text.lower()

    for marker in sorted(REQUIRED_MARKERS):
        if marker not in text:
            errors.append(f"missing section: {marker}")

    for prefix in sorted(REQUIRED_FILLED_PREFIXES):
        value = _line_value(text, prefix)
        if not value:
            errors.append(f"empty metadata field: {prefix}")

    for checkbox in sorted(REQUIRED_CHECKBOXES):
        if checkbox not in text:
            errors.append(f"boundary checkbox not confirmed: {checkbox}")

    for marker in sorted(PROTECTED_MARKERS):
        if marker in lower_text:
            errors.append(f"protected marker found: {marker}")

    for name, pattern in IDENTIFIER_PATTERNS.items():
        if pattern.search(text):
            errors.append(f"possible protected identifier found: {name}")

    if "Actual feedback evidence: false until completed" in text:
        errors.append("actual feedback evidence marker still false")

    for placeholder in sorted(PLACEHOLDER_PATTERNS):
        if _has_blank_line_value(text, placeholder):
            errors.append(f"unfilled placeholder: {placeholder}")

    if "### Candidate 1" in text and "- Issue:\n" in text:
        errors.append("safe correction candidate appears unfilled")

    return not errors, errors


def _line_value(text: str, prefix: str) -> str:
    for line in text.splitlines():
        if line.startswith(prefix):
            return line[len(prefix) :].strip()
    return ""


def _has_blank_line_value(text: str, prefix: str) -> bool:
    for line in text.splitlines():
        if line == prefix:
            return True
    return False


def main() -> int:
    parser = argparse.ArgumentParser(description="Check public-safe actual accountant feedback notes.")
    parser.add_argument("--notes", type=Path, required=True)
    args = parser.parse_args()

    ok, errors = check_actual_notes(args.notes)
    print(f"ok: {ok}")
    for error in errors:
        print(f"- {error}")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
