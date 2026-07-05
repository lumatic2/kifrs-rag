from __future__ import annotations

import argparse
import json
import sys
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from kifrs.runtime.authority_boundary import build_runtime_authority_boundary  # noqa: E402
from kifrs.workflows.kifrs1116.fixtures import FIXTURES  # noqa: E402
from kifrs.workflows.kifrs1116.review_pack import generate_review_pack  # noqa: E402


REPORT_PATH = ROOT / "docs" / "reports" / "2026-07-05-ptq2-review-pack-confidence-contract.md"
ALLOWED_LABELS = {"ready", "caution", "human_review_required"}


@dataclass(frozen=True)
class ConfidenceSection:
    section: str
    label: str
    reason: str
    evidence: list[str]
    human_boundary: str


def confidence_sections_for_pack(pack: Any) -> list[ConfidenceSection]:
    sections = [
        _section(
            "review_memo",
            "ready" if pack.review_memo else "human_review_required",
            "Review memo draft exists." if pack.review_memo else "Review memo is absent because the workflow stopped.",
            pack.citations,
        ),
        _section(
            "journal_entry",
            "ready" if pack.journal_entry is not None else "human_review_required",
            "Journal entry draft exists." if pack.journal_entry is not None else "Journal entry draft is absent.",
            [],
        ),
        _section(
            "disclosure_draft",
            "caution" if pack.disclosure_draft else "human_review_required",
            (
                "Disclosure draft exists but still requires company-specific completion."
                if pack.disclosure_draft
                else "Disclosure draft is absent for this workflow result."
            ),
            pack.citations,
        ),
        _section(
            "authority_boundary",
            "ready" if _has_authority_boundary(pack) else "caution",
            (
                "Runtime authority groups are attached."
                if _has_authority_boundary(pack)
                else "Runtime authority groups are not attached to this pack."
            ),
            list(pack.authority_boundary.keys()) if getattr(pack, "authority_boundary", None) else [],
        ),
        _section(
            "human_review_items",
            "human_review_required" if pack.needs_human_review else "ready",
            (
                "Human review actions are present and must be resolved before sign-off."
                if pack.needs_human_review
                else "No explicit human review actions were generated."
            ),
            [action.issue for action in pack.needs_human_review],
        ),
    ]
    if pack.status == "needs_human_review":
        return [
            section
            if section.section in {"authority_boundary", "human_review_items"}
            else ConfidenceSection(
                section=section.section,
                label="human_review_required",
                reason=f"Pack status is needs_human_review; {section.reason}",
                evidence=section.evidence,
                human_boundary=section.human_boundary,
            )
            for section in sections
        ]
    return sections


def build_contract() -> dict[str, Any]:
    automated = _pack("scenario_01_simple_office_lease")
    needs_review = _pack("scenario_09_lessee_modification_expand_shrink")
    sample_cases = {
        automated.case_id: [asdict(section) for section in confidence_sections_for_pack(automated)],
        needs_review.case_id: [asdict(section) for section in confidence_sections_for_pack(needs_review)],
    }
    errors = _validate_sample_cases(sample_cases)
    return {
        "title": "PTQ2 Review Pack Confidence Contract",
        "ok": not errors,
        "horizon": "product-trust-and-quality-evidence",
        "milestone": "PTQ2",
        "allowed_labels": sorted(ALLOWED_LABELS),
        "sample_cases": sample_cases,
        "errors": errors,
        "human_boundary": "Confidence labels are decision-support evidence only. Final accounting judgment, review, sign-off, audit opinion, tax/legal conclusion, and client communication remain human responsibilities.",
        "report_path": _display_path(REPORT_PATH),
        "next_leaf": "PTQ3_failure_boundary_matrix",
    }


def render_markdown(contract: dict[str, Any]) -> str:
    lines = [
        f"# {contract['title']}",
        "",
        "> Scope: PTQ2 public-safe confidence labels for review-pack sections.",
        "",
        "## One-Line Result",
        "",
        (
            "Review-pack sections now have ready/caution/human-review-required confidence labels for product trust evidence."
            if contract["ok"]
            else "Review-pack confidence contract failed; fix the listed errors."
        ),
        "",
        "## Human Boundary",
        "",
        contract["human_boundary"],
        "",
        "## Allowed Labels",
        "",
    ]
    lines.extend(f"- `{label}`" for label in contract["allowed_labels"])
    for case_id, sections in contract["sample_cases"].items():
        lines.extend(["", f"## Sample Case: `{case_id}`", "", "| Section | Label | Reason | Evidence |", "|---|---|---|---|"])
        for section in sections:
            evidence = ", ".join(section["evidence"]) if section["evidence"] else "-"
            lines.append(f"| {section['section']} | `{section['label']}` | {section['reason']} | {evidence} |")
    lines.extend(["", "## Errors", ""])
    lines.extend(f"- {error}" for error in contract["errors"]) if contract["errors"] else lines.append("- none")
    lines.extend(
        [
            "",
            "## Machine Result",
            "",
            "```json",
            json.dumps(contract, ensure_ascii=False, indent=2, default=str),
            "```",
        ]
    )
    return "\n".join(lines) + "\n"


def write_report(path: Path = REPORT_PATH) -> dict[str, Any]:
    contract = build_contract()
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(render_markdown(contract), encoding="utf-8")
    return contract


def _section(section: str, label: str, reason: str, evidence: list[str]) -> ConfidenceSection:
    if label not in ALLOWED_LABELS:
        raise ValueError(f"unsupported confidence label: {label}")
    return ConfidenceSection(
        section=section,
        label=label,
        reason=reason,
        evidence=list(evidence),
        human_boundary="Decision-support only; accountant review remains required.",
    )


def _pack(label: str) -> Any:
    fixture = next(item for item in FIXTURES if item.txn.label == label)
    boundary = build_runtime_authority_boundary(primary_citations=["[1116-53]", "[1116-59]"])
    return generate_review_pack(fixture.txn, authority_boundary=boundary)


def _has_authority_boundary(pack: Any) -> bool:
    boundary = getattr(pack, "authority_boundary", {}) or {}
    return all(boundary.get(role) for role in ("primary_kifrs_evidence", "client_private_fact"))


def _validate_sample_cases(sample_cases: dict[str, list[dict[str, Any]]]) -> list[str]:
    errors: list[str] = []
    for case_id, sections in sample_cases.items():
        labels = {section["label"] for section in sections}
        unknown = labels - ALLOWED_LABELS
        if unknown:
            errors.append(f"{case_id}: unknown labels {sorted(unknown)}")
        if not any(section["label"] == "human_review_required" for section in sections):
            errors.append(f"{case_id}: no human-review boundary label")
        if case_id.endswith("expand_shrink") and any(
            section["label"] == "ready"
            for section in sections
            if section["section"] in {"review_memo", "journal_entry", "disclosure_draft"}
        ):
            errors.append(f"{case_id}: stopped workflow sections must not be ready")
    return errors


def _display_path(path: Path) -> str:
    try:
        return path.resolve().relative_to(ROOT).as_posix()
    except ValueError:
        return path.as_posix()


def main() -> int:
    parser = argparse.ArgumentParser(description="Build review-pack confidence labels for product trust evidence.")
    parser.add_argument("--format", choices=["text", "json", "markdown"], default="text")
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--out", type=Path, default=REPORT_PATH)
    args = parser.parse_args()

    contract = write_report(args.out) if args.write else build_contract()
    if args.format == "json":
        print(json.dumps(contract, ensure_ascii=False, indent=2, default=str))
    elif args.format == "markdown":
        print(render_markdown(contract), end="")
    else:
        print(contract["title"])
        print(f"- ok: {contract['ok']}")
        print(f"- labels: {', '.join(contract['allowed_labels'])}")
        print(f"- cases: {', '.join(contract['sample_cases'])}")
        print(f"- next leaf: {contract['next_leaf']}")
    return 0 if contract["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
