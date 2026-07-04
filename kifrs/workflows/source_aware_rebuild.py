"""Source-aware rebuild metrics for F-ACC review packs.

This layer does not change accounting judgments. It reruns existing public
fixtures with runtime evidence metadata and summarizes how much of each output
is backed by K-IFRS citations, external evidence locators, fact evidence, and
human-review items.
"""
from __future__ import annotations

from collections import Counter, defaultdict
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any

from kifrs.runtime.evidence import EvidenceBundle, load_runtime_evidence
from kifrs.workflows.kifrs1109.fixtures import FIXTURES as FIXTURES_1109
from kifrs.workflows.kifrs1109.review_pack import generate_review_pack as generate_1109_pack
from kifrs.workflows.kifrs1115.fixtures import FIXTURES as FIXTURES_1115
from kifrs.workflows.kifrs1115.review_pack import generate_review_pack as generate_1115_pack
from kifrs.workflows.kifrs1116.fixtures import FIXTURES as FIXTURES_1116
from kifrs.workflows.kifrs1116.review_pack import generate_review_pack as generate_1116_pack


FORBIDDEN_PAYLOAD_KEYS = {"body", "text", "content", "full_text", "source_body"}


@dataclass(frozen=True)
class SourceAwarePackSummary:
    standard: str
    case_id: str
    status: str
    primary_citation_count: int
    external_evidence_count: int
    external_evidence_roles: dict[str, int]
    fact_evidence_count: int
    human_review_count: int
    ready_check_count: int
    needs_human_review_issues: list[str] = field(default_factory=list)

    @property
    def is_automated(self) -> bool:
        return self.status == "automated"

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class SourceAwareRebuildReport:
    summaries: tuple[SourceAwarePackSummary, ...]
    evidence_manifest_path: str
    source_manifest_path: str

    @property
    def total_packs(self) -> int:
        return len(self.summaries)

    @property
    def automated_packs(self) -> int:
        return sum(1 for item in self.summaries if item.is_automated)

    @property
    def human_review_packs(self) -> int:
        return self.total_packs - self.automated_packs

    @property
    def aggregate_external_roles(self) -> dict[str, int]:
        counts: Counter[str] = Counter()
        for summary in self.summaries:
            counts.update(summary.external_evidence_roles)
        return dict(sorted(counts.items()))

    def by_standard(self) -> dict[str, list[SourceAwarePackSummary]]:
        grouped: dict[str, list[SourceAwarePackSummary]] = defaultdict(list)
        for summary in self.summaries:
            grouped[summary.standard].append(summary)
        return dict(sorted(grouped.items()))

    def to_dict(self) -> dict[str, Any]:
        return {
            "total_packs": self.total_packs,
            "automated_packs": self.automated_packs,
            "human_review_packs": self.human_review_packs,
            "aggregate_external_roles": self.aggregate_external_roles,
            "source_manifest_path": self.source_manifest_path,
            "evidence_manifest_path": self.evidence_manifest_path,
            "summaries": [summary.to_dict() for summary in self.summaries],
        }


def summarize_review_pack(pack: Any) -> SourceAwarePackSummary:
    """Convert a 1109/1115/1116 review pack object into common metrics."""
    external_evidence = list(getattr(pack, "external_evidence", []) or [])
    role_counts = Counter(str(item.get("citation_role", "unknown")) for item in external_evidence)
    needs_human_review = list(getattr(pack, "needs_human_review", []) or [])
    checklist = list(getattr(pack, "review_checklist", []) or [])
    issues = [str(getattr(item, "issue", "")) for item in needs_human_review if getattr(item, "issue", "")]

    return SourceAwarePackSummary(
        standard=str(getattr(pack, "standard")),
        case_id=str(getattr(pack, "case_id")),
        status=str(getattr(pack, "status")),
        primary_citation_count=len(list(getattr(pack, "citations", []) or [])),
        external_evidence_count=len(external_evidence),
        external_evidence_roles=dict(sorted(role_counts.items())),
        fact_evidence_count=role_counts.get("fact_evidence", 0),
        human_review_count=len(needs_human_review),
        ready_check_count=sum(1 for item in checklist if getattr(item, "status", "") == "ready"),
        needs_human_review_issues=issues,
    )


def build_default_rebuild_report(evidence_bundle: EvidenceBundle | None = None) -> SourceAwareRebuildReport:
    """Generate source-aware summaries for all public 1109/1115/1116 fixtures."""
    bundle = evidence_bundle or load_runtime_evidence()
    summaries: list[SourceAwarePackSummary] = []

    for fixture in FIXTURES_1109:
        summaries.append(summarize_review_pack(generate_1109_pack(fixture, bundle)))
    for fixture in FIXTURES_1115:
        summaries.append(summarize_review_pack(generate_1115_pack(fixture, bundle)))
    for fixture in FIXTURES_1116:
        summaries.append(summarize_review_pack(generate_1116_pack(fixture.txn, bundle)))

    return SourceAwareRebuildReport(
        summaries=tuple(summaries),
        source_manifest_path=_display_path(bundle.source_manifest_path),
        evidence_manifest_path=_display_path(bundle.evidence_manifest_path),
    )


def render_rebuild_report_markdown(report: SourceAwareRebuildReport) -> str:
    lines = [
        "# Source-Aware Workflow Rebuild Report",
        "",
        "## Summary",
        "",
        f"- Total review packs: {report.total_packs}",
        f"- Automated packs: {report.automated_packs}",
        f"- Needs human review packs: {report.human_review_packs}",
        f"- Source manifest: `{report.source_manifest_path}`",
        f"- Evidence manifest: `{report.evidence_manifest_path}`",
        "",
        "## External Evidence Roles",
        "",
        "| Role | Count |",
        "|---|---:|",
    ]
    for role, count in report.aggregate_external_roles.items():
        lines.append(f"| {role} | {count} |")

    lines.extend([
        "",
        "## By Standard",
        "",
        "| Standard | Packs | Automated | Needs human review | Citations | Fact evidence refs | Human-review items |",
        "|---|---:|---:|---:|---:|---:|---:|",
    ])
    for standard, summaries in report.by_standard().items():
        automated = sum(1 for item in summaries if item.is_automated)
        citations = sum(item.primary_citation_count for item in summaries)
        fact_evidence = sum(item.fact_evidence_count for item in summaries)
        human_items = sum(item.human_review_count for item in summaries)
        lines.append(
            f"| {standard} | {len(summaries)} | {automated} | {len(summaries) - automated} | "
            f"{citations} | {fact_evidence} | {human_items} |"
        )

    lines.extend([
        "",
        "## Pack Detail",
        "",
        "| Standard | Case | Status | Citations | External evidence roles | Fact evidence | Human-review items |",
        "|---|---|---|---:|---|---:|---:|",
    ])
    for summary in report.summaries:
        role_text = ", ".join(f"{role}:{count}" for role, count in summary.external_evidence_roles.items())
        lines.append(
            f"| {summary.standard} | {summary.case_id} | {summary.status} | "
            f"{summary.primary_citation_count} | {role_text} | {summary.fact_evidence_count} | "
            f"{summary.human_review_count} |"
        )

    lines.extend([
        "",
        "## Boundary",
        "",
        "- External evidence remains supporting metadata or synthetic fact evidence.",
        "- K-IFRS citations remain the primary accounting evidence.",
        "- Human-review items are counted, not removed.",
        "- This report does not include source document payloads, private filings, parsed standards, embeddings, or customer data.",
    ])
    return "\n".join(lines) + "\n"


def assert_public_safe_report(data: dict[str, Any]) -> None:
    """Raise if common source-payload field names appear in report data."""
    offenders: list[str] = []

    def visit(value: Any, path: str) -> None:
        if isinstance(value, dict):
            for key, child in value.items():
                if key in FORBIDDEN_PAYLOAD_KEYS:
                    offenders.append(f"{path}.{key}" if path else key)
                visit(child, f"{path}.{key}" if path else key)
        elif isinstance(value, list):
            for index, child in enumerate(value):
                visit(child, f"{path}[{index}]")

    visit(data, "")
    if offenders:
        joined = ", ".join(offenders)
        raise ValueError(f"source payload fields are not public-safe: {joined}")


def _display_path(path: Path) -> str:
    resolved = path.resolve()
    root = Path(__file__).resolve().parents[2]
    try:
        return resolved.relative_to(root).as_posix()
    except ValueError:
        return path.as_posix()
