"""Generate a local markdown demo pack from public synthetic fixtures."""

from __future__ import annotations

import argparse
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from kifrs.workflows.audit_analytics import (
    SYNTHETIC_FS,
    calculate_metrics,
    detect_anomalies,
    link_statement_candidates,
    render_anomaly_note,
)
from kifrs.runtime.answer_boundary import compose_evidence_boundary, render_evidence_boundary
from kifrs.runtime.evidence import load_runtime_evidence
from kifrs.workflows.kifrs1115.fixtures import FIXTURES as FIXTURES_1115
from kifrs.workflows.kifrs1115.review_pack import (
    generate_review_pack as generate_1115_pack,
    render_review_pack_markdown as render_1115_pack,
)
from kifrs.workflows.kifrs1116.fixtures import FIXTURES as FIXTURES_1116
from kifrs.workflows.kifrs1116.review_pack import (
    generate_review_pack as generate_1116_pack,
    render_review_pack_markdown as render_1116_pack,
)
from kifrs.workflows.statement_draft import from_1115_review_pack, from_1116_review_pack


def generate_demo(scenario: str, out_dir: Path) -> list[Path]:
    if scenario != "revenue-financing":
        raise ValueError(f"unsupported demo scenario: {scenario}")

    out_dir.mkdir(parents=True, exist_ok=True)

    evidence_bundle = load_runtime_evidence()
    significant_financing = generate_1115_pack(
        _fixture_1115("scenario_03_significant_financing"),
        evidence_bundle,
    )
    repurchase = generate_1115_pack(
        _fixture_1115("scenario_04_repurchase_call_option"),
        evidence_bundle,
    )
    lease = generate_1116_pack(_fixture_1116("scenario_01_simple_office_lease").txn, evidence_bundle)

    statement_candidates = [
        *from_1115_review_pack(significant_financing),
        *from_1115_review_pack(repurchase),
        *from_1116_review_pack(lease),
    ]
    findings = detect_anomalies(calculate_metrics(SYNTHETIC_FS))
    linked = link_statement_candidates(findings, statement_candidates)

    outputs = {
        "index.md": _index_markdown(),
        "1115-significant-financing-review-pack.md": render_1115_pack(significant_financing),
        "1115-repurchase-review-pack.md": render_1115_pack(repurchase),
        "statement-candidates.md": _statement_candidates_markdown(statement_candidates),
        "evidence-boundary.md": render_evidence_boundary(
            compose_evidence_boundary(evidence_bundle, sorted(set(significant_financing.citations + lease.citations)))
        ),
        "audit-analytics-note.md": render_anomaly_note(SYNTHETIC_FS.entity, findings),
        "audit-facc-links.md": _linked_candidates_markdown(linked),
        "1116-lease-review-pack.md": render_1116_pack(lease),
    }

    written: list[Path] = []
    for filename, content in outputs.items():
        path = out_dir / filename
        path.write_text(content + "\n", encoding="utf-8")
        written.append(path)
    return written


def _fixture_1115(label: str):
    return next(fixture for fixture in FIXTURES_1115 if fixture.label == label)


def _fixture_1116(label: str):
    return next(fixture for fixture in FIXTURES_1116 if fixture.txn.label == label)


def _index_markdown() -> str:
    return "\n".join(
        [
            "# K-IFRS RAG Product Packaging PoC",
            "",
            "Demo scenario: 1115 수익인식 + F/S draft + audit analytics linkage.",
            "",
            "## Files",
            "- `1115-significant-financing-review-pack.md`",
            "- `1115-repurchase-review-pack.md`",
            "- `statement-candidates.md`",
            "- `evidence-boundary.md`",
            "- `audit-analytics-note.md`",
            "- `audit-facc-links.md`",
            "- `1116-lease-review-pack.md`",
            "",
            "## Boundary",
            "- 기준서 원문, DB, embedding, dogfood 자료는 포함하지 않는다.",
            "- 산출물은 decision-prep draft이며 회계사 검토를 대체하지 않는다.",
        ]
    )


def _statement_candidates_markdown(candidates) -> str:
    lines = [
        "# Statement Draft Candidates",
        "",
        "| Statement | Line item | Amount | Source | Status | Evidence |",
        "|---|---|---:|---|---|---|",
    ]
    for item in candidates:
        amount = "" if item.amount is None else f"{item.amount:,.0f}"
        source = f"{item.source_standard}/{item.source_case_id}/{item.source_field}"
        evidence = ", ".join(ref["record_id"] for ref in item.evidence_refs)
        lines.append(
            f"| {item.statement} | {item.line_item} | {amount} | {source} | {item.presentation_status} | {evidence} |"
        )
    return "\n".join(lines)


def _linked_candidates_markdown(linked) -> str:
    lines = [
        "# Audit Finding to F-ACC Candidate Links",
        "",
        "| Finding | Candidate | Amount | Source | Status |",
        "|---|---|---:|---|---|",
    ]
    for item in linked:
        amount = "" if item.amount is None else f"{item.amount:,.0f}"
        source = f"{item.source_standard}/{item.source_case_id}/{item.source_field}"
        lines.append(
            f"| {item.finding_id} | {item.line_item} | {amount} | {source} | {item.presentation_status} |"
        )
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--scenario", default="revenue-financing")
    parser.add_argument("--out", type=Path, default=Path("docs/reports/demo-poc"))
    args = parser.parse_args()

    written = generate_demo(args.scenario, args.out)
    for path in written:
        print(path)


if __name__ == "__main__":
    main()
