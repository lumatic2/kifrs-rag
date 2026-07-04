"""Rendering helpers for external evidence panels."""
from __future__ import annotations

import json
from typing import Any

from .evidence import EvidenceBundle


ROLE_LABELS = {
    "supporting_interpretation": "해석 보조 근거",
    "legal_boundary": "법적 경계 근거",
    "fact_evidence": "수치 사실 근거",
}


def evidence_references(bundle: EvidenceBundle | None) -> list[dict[str, Any]]:
    if bundle is None:
        return []
    return [item.to_reference_dict() for item in bundle.items]


def render_external_evidence_panel(external_evidence: list[dict[str, Any]]) -> list[str]:
    lines = ["## 외부 근거"]
    if not external_evidence:
        lines.append("- 없음")
        return lines

    for role in ("supporting_interpretation", "legal_boundary", "fact_evidence"):
        items = [item for item in external_evidence if item.get("citation_role") == role]
        if not items:
            continue
        lines.append(f"### {ROLE_LABELS[role]}")
        for item in items:
            locator = json.dumps(item.get("locator", {}), ensure_ascii=False, sort_keys=True)
            lines.append(
                "- "
                f"{item.get('evidence_label')} "
                f"(`{item.get('source_id')}` / `{item.get('record_id')}`): {locator}"
            )
    return lines
