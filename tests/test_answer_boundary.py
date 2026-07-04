from __future__ import annotations

from kifrs.runtime.answer_boundary import compose_evidence_boundary, render_evidence_boundary
from kifrs.runtime.evidence import load_runtime_evidence


def test_answer_boundary_separates_primary_and_external_roles() -> None:
    boundary = compose_evidence_boundary(load_runtime_evidence(), ["[1115-B39~B43]"])
    data = boundary.to_dict()

    assert data["primary_kifrs_evidence"][0]["citation"] == "[1115-B39~B43]"
    assert len(data["supporting_interpretation"]) == 1
    assert len(data["legal_boundary"]) == 1
    assert len(data["fact_evidence"]) == 1


def test_answer_boundary_does_not_promote_external_evidence_to_primary() -> None:
    boundary = compose_evidence_boundary(load_runtime_evidence())
    data = boundary.to_dict()

    assert data["primary_kifrs_evidence"] == []
    assert data["supporting_interpretation"]
    assert data["fact_evidence"]


def test_answer_boundary_rendering_excludes_source_payload_and_quotes() -> None:
    boundary = compose_evidence_boundary(load_runtime_evidence(), ["[1116-53]"])

    rendered = render_evidence_boundary(boundary)

    assert "## Evidence Boundary" in rendered
    assert "Primary K-IFRS evidence" in rendered
    assert "Supporting interpretation" in rendered
    assert "Legal boundary" in rendered
    assert "Fact evidence" in rendered
    assert "record':" not in rendered
    assert "copied source" not in rendered

