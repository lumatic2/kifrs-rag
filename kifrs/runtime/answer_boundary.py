"""Answer boundary composition for primary and external evidence."""
from __future__ import annotations

from dataclasses import dataclass, field

from .evidence import EvidenceBundle, RuntimeEvidence


@dataclass(frozen=True)
class PrimaryEvidenceRef:
    citation: str
    label: str = "K-IFRS primary evidence"

    def to_reference_dict(self) -> dict[str, str]:
        return {"citation": self.citation, "label": self.label, "evidence_class": "primary_kifrs_evidence"}


@dataclass(frozen=True)
class EvidenceBoundary:
    primary_kifrs_evidence: list[dict[str, str]] = field(default_factory=list)
    supporting_interpretation: list[dict[str, object]] = field(default_factory=list)
    legal_boundary: list[dict[str, object]] = field(default_factory=list)
    fact_evidence: list[dict[str, object]] = field(default_factory=list)

    def to_dict(self) -> dict[str, list[dict[str, object]]]:
        return {
            "primary_kifrs_evidence": list(self.primary_kifrs_evidence),
            "supporting_interpretation": list(self.supporting_interpretation),
            "legal_boundary": list(self.legal_boundary),
            "fact_evidence": list(self.fact_evidence),
        }


def compose_evidence_boundary(
    bundle: EvidenceBundle,
    primary_citations: list[str] | None = None,
) -> EvidenceBoundary:
    primary_refs = [
        PrimaryEvidenceRef(citation=citation).to_reference_dict()
        for citation in (primary_citations or [])
    ]
    return EvidenceBoundary(
        primary_kifrs_evidence=primary_refs,
        supporting_interpretation=_safe_refs(bundle.supporting_interpretations),
        legal_boundary=_safe_refs(bundle.legal_boundaries),
        fact_evidence=_safe_refs(bundle.fact_evidence),
    )


def render_evidence_boundary(boundary: EvidenceBoundary) -> str:
    sections = [
        ("Primary K-IFRS evidence", boundary.primary_kifrs_evidence),
        ("Supporting interpretation", boundary.supporting_interpretation),
        ("Legal boundary", boundary.legal_boundary),
        ("Fact evidence", boundary.fact_evidence),
    ]
    lines = ["## Evidence Boundary"]
    for title, items in sections:
        lines.append(f"### {title}")
        if not items:
            lines.append("- 없음")
            continue
        for item in items:
            if "citation" in item:
                lines.append(f"- {item['citation']} ({item.get('label')})")
            else:
                lines.append(
                    "- "
                    f"{item.get('evidence_label')} "
                    f"[{item.get('citation_role')}] "
                    f"`{item.get('source_id')}` / `{item.get('record_id')}`"
                )
    return "\n".join(lines)


def _safe_refs(items: tuple[RuntimeEvidence, ...]) -> list[dict[str, object]]:
    return [item.to_reference_dict() for item in items]

