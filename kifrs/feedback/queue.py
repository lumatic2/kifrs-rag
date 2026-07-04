"""JSONL queue for public-safe feedback eval/backlog candidates."""
from __future__ import annotations

from collections import Counter
from dataclasses import asdict, dataclass
import json
from pathlib import Path
from typing import Any, Iterable

from .case_intake import (
    CaseIntake,
    ReviewerCorrection,
    ValidationIssue,
    case_to_eval_seed_candidate,
    route_case,
    validate_case_intake,
    validate_reviewer_correction,
)


QUEUE_VERSION = 1
ALLOWED_QUEUE_STATUS = {"candidate", "backlog_candidate", "no_action"}


@dataclass(frozen=True)
class FeedbackQueueRecord:
    record_id: str
    case_id: str
    domain: str
    route: str
    disposition: str
    severity: str
    issue: str
    expected_improvement: str
    missing_evidence: list[str]
    affected_outputs: list[str]
    source: str = "public-safe-sample"
    version: int = QUEUE_VERSION

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class FeedbackQueueSummary:
    total: int
    by_disposition: dict[str, int]
    by_domain: dict[str, int]
    high_severity: tuple[FeedbackQueueRecord, ...]


def make_queue_record(
    case: CaseIntake,
    correction: ReviewerCorrection,
    *,
    source: str = "public-safe-sample",
) -> FeedbackQueueRecord:
    case_issues = validate_case_intake(case)
    correction_issues = validate_reviewer_correction(correction)
    if case_issues or correction_issues:
        raise ValueError(_format_issues(case_issues, correction_issues))

    seed = case_to_eval_seed_candidate(case, correction)
    route = route_case(case)
    disposition = seed["status"]
    if disposition not in ALLOWED_QUEUE_STATUS:
        raise ValueError(f"unsupported queue disposition: {disposition}")

    return FeedbackQueueRecord(
        record_id=f"{case.case_id}:{correction.disposition}:{_slug(correction.issue)}",
        case_id=case.case_id,
        domain=seed["domain"],
        route=route.route,
        disposition=disposition,
        severity=correction.severity,
        issue=correction.issue,
        expected_improvement=correction.suggested_fix,
        missing_evidence=list(correction.missing_evidence),
        affected_outputs=list(correction.affected_outputs),
        source=source,
    )


def write_queue(path: Path, records: Iterable[FeedbackQueueRecord]) -> None:
    items = list(records)
    duplicate = _duplicate_record_id(items)
    if duplicate:
        raise ValueError(f"duplicate feedback queue record_id: {duplicate}")

    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        "\n".join(json.dumps(item.to_dict(), ensure_ascii=False, sort_keys=True) for item in items) + "\n",
        encoding="utf-8",
    )


def load_queue(path: Path) -> list[FeedbackQueueRecord]:
    records: list[FeedbackQueueRecord] = []
    seen: set[str] = set()
    if not path.exists():
        return []
    for line_no, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        if not line.strip():
            continue
        raw = json.loads(line)
        record = FeedbackQueueRecord(**raw)
        if record.record_id in seen:
            raise ValueError(f"duplicate feedback queue record_id at line {line_no}: {record.record_id}")
        seen.add(record.record_id)
        records.append(record)
    return records


def summarize_queue(records: Iterable[FeedbackQueueRecord]) -> FeedbackQueueSummary:
    items = tuple(records)
    by_disposition = Counter(item.disposition for item in items)
    by_domain = Counter(item.domain for item in items)
    high_severity = tuple(item for item in items if item.severity in {"high", "blocker"})
    return FeedbackQueueSummary(
        total=len(items),
        by_disposition=dict(sorted(by_disposition.items())),
        by_domain=dict(sorted(by_domain.items())),
        high_severity=high_severity,
    )


def split_queue(records: Iterable[FeedbackQueueRecord]) -> dict[str, list[FeedbackQueueRecord]]:
    buckets = {"eval_seed_candidate": [], "backlog_candidate": [], "no_action": []}
    for record in records:
        key = "eval_seed_candidate" if record.disposition == "candidate" else record.disposition
        buckets[key].append(record)
    return buckets


def render_queue_report(records: Iterable[FeedbackQueueRecord], *, title: str = "Feedback Queue Report") -> str:
    items = tuple(records)
    summary = summarize_queue(items)
    split = split_queue(items)
    lines = [
        f"# {title}",
        "",
        "> Public-safe feedback queue. This is not a raw client workpaper store.",
        "",
        "## Summary",
        "",
        f"- Total records: {summary.total}",
        f"- Eval seed candidates: {len(split['eval_seed_candidate'])}",
        f"- Backlog candidates: {len(split['backlog_candidate'])}",
        f"- No-action records: {len(split['no_action'])}",
        f"- High/blocker severity records: {len(summary.high_severity)}",
        "",
        "## By Domain",
        "",
        "| Domain | Count |",
        "|---|---:|",
    ]
    for domain, count in summary.by_domain.items():
        lines.append(f"| {domain} | {count} |")

    lines.extend([
        "",
        "## Queue Detail",
        "",
        "| Record | Case | Domain | Disposition | Severity | Route | Issue |",
        "|---|---|---|---|---|---|---|",
    ])
    for record in items:
        lines.append(
            f"| {record.record_id} | {record.case_id} | {record.domain} | {record.disposition} | "
            f"{record.severity} | {record.route} | {record.issue} |"
        )

    if summary.high_severity:
        lines.extend(["", "## High Severity", ""])
        lines.extend(f"- {record.record_id}: {record.issue}" for record in summary.high_severity)

    lines.extend([
        "",
        "## Boundary",
        "",
        "- Queue records store validated correction candidates only.",
        "- Raw contracts, customer identifiers, copied source bodies, private filings, parsed standards, embeddings, and workpaper payloads are not stored here.",
    ])
    return "\n".join(lines) + "\n"


def _duplicate_record_id(records: Iterable[FeedbackQueueRecord]) -> str | None:
    seen: set[str] = set()
    for record in records:
        if record.record_id in seen:
            return record.record_id
        seen.add(record.record_id)
    return None


def _format_issues(
    case_issues: list[ValidationIssue],
    correction_issues: list[ValidationIssue],
) -> str:
    return "; ".join(
        [f"case.{issue.path}: {issue.message}" for issue in case_issues]
        + [f"correction.{issue.path}: {issue.message}" for issue in correction_issues]
    )


def _slug(value: str) -> str:
    chars = [char.lower() if char.isalnum() else "-" for char in value]
    slug = "".join(chars).strip("-")
    while "--" in slug:
        slug = slug.replace("--", "-")
    return slug[:48] or "correction"
