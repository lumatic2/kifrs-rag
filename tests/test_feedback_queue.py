from __future__ import annotations

import json

import pytest

from kifrs.feedback import CaseIntake, ReviewerCorrection
from kifrs.feedback.queue import (
    load_queue,
    make_queue_record,
    render_queue_report,
    split_queue,
    summarize_queue,
    write_queue,
)


def _case(case_id: str = "anon-case-lease-001") -> CaseIntake:
    return CaseIntake(
        case_id=case_id,
        domain_hint="KIFRS1116",
        anonymized_title="Anonymized lease case",
        fact_pattern_summary="Sanitized lease facts only.",
        structured_facts={
            "party": "lessee",
            "lease_term": "4 years",
            "payment_schedule": "annual arrears",
        },
        requested_outputs=["review_pack", "human_review_questions"],
    )


def _correction(disposition: str = "eval_seed_candidate", severity: str = "medium") -> ReviewerCorrection:
    return ReviewerCorrection(
        case_id="anon-case-lease-001",
        issue="Renewal evidence question is missing",
        severity=severity,
        suggested_fix="Require management renewal assessment evidence.",
        missing_evidence=["management renewal assessment"],
        disposition=disposition,
        affected_outputs=["human_review_questions"],
    )


def test_make_queue_record_from_validated_case_and_correction() -> None:
    record = make_queue_record(_case(), _correction())

    assert record.case_id == "anon-case-lease-001"
    assert record.domain == "KIFRS1116"
    assert record.disposition == "candidate"
    assert record.route == "kifrs1116_review_pack"
    assert "source_body" not in json.dumps(record.to_dict())


def test_make_queue_record_rejects_protected_payload() -> None:
    bad_case = CaseIntake(
        case_id="bad",
        domain_hint="KIFRS1116",
        anonymized_title="Bad",
        fact_pattern_summary="Sanitized",
        structured_facts={
            "party": "lessee",
            "lease_term": "4 years",
            "payment_schedule": "annual",
            "raw_contract": "copied",
        },
    )

    with pytest.raises(ValueError, match="protected-data"):
        make_queue_record(bad_case, _correction())


def test_write_and_load_queue_round_trip(tmp_path) -> None:
    path = tmp_path / "feedback.jsonl"
    records = [
        make_queue_record(_case(), _correction()),
        make_queue_record(
            _case("anon-case-lease-002"),
            ReviewerCorrection(
                case_id="anon-case-lease-002",
                issue="Backlog item",
                severity="high",
                suggested_fix="Add checklist item.",
                disposition="backlog_candidate",
                affected_outputs=["review_pack"],
            ),
        ),
    ]

    write_queue(path, records)
    loaded = load_queue(path)

    assert loaded == records
    assert path.read_text(encoding="utf-8").count("\n") == 2


def test_write_queue_rejects_duplicate_record_id(tmp_path) -> None:
    path = tmp_path / "feedback.jsonl"
    record = make_queue_record(_case(), _correction())

    with pytest.raises(ValueError, match="duplicate"):
        write_queue(path, [record, record])


def test_load_queue_rejects_duplicate_record_id(tmp_path) -> None:
    path = tmp_path / "feedback.jsonl"
    record = make_queue_record(_case(), _correction())
    line = json.dumps(record.to_dict(), ensure_ascii=False)
    path.write_text(f"{line}\n{line}\n", encoding="utf-8")

    with pytest.raises(ValueError, match="duplicate"):
        load_queue(path)


def test_queue_summary_and_split() -> None:
    records = [
        make_queue_record(_case(), _correction()),
        make_queue_record(
            _case("anon-case-lease-002"),
            ReviewerCorrection(
                case_id="anon-case-lease-002",
                issue="No action item",
                severity="low",
                suggested_fix="No change needed.",
                disposition="no_action",
            ),
        ),
    ]

    summary = summarize_queue(records)
    split = split_queue(records)

    assert summary.total == 2
    assert summary.by_domain == {"KIFRS1116": 2}
    assert len(split["eval_seed_candidate"]) == 1
    assert len(split["no_action"]) == 1


def test_queue_report_renders_counts_and_boundary() -> None:
    records = [make_queue_record(_case(), _correction(severity="high"))]
    rendered = render_queue_report(records)

    assert "Eval seed candidates: 1" in rendered
    assert "High/blocker severity records: 1" in rendered
    assert "Raw contracts" in rendered
    assert "source_body" not in rendered
