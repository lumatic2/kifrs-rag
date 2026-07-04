from __future__ import annotations

import json

import pytest

from kifrs.runtime.evidence import load_runtime_evidence


def test_runtime_evidence_loader_loads_default_bundle() -> None:
    bundle = load_runtime_evidence()

    assert len(bundle.items) == 3
    assert bundle.get("ev-kasb-interpretation-catalog-seed") is not None
    assert bundle.get("missing") is None


def test_runtime_evidence_loader_groups_by_role() -> None:
    bundle = load_runtime_evidence()

    assert len(bundle.supporting_interpretations) == 1
    assert len(bundle.legal_boundaries) == 1
    assert len(bundle.fact_evidence) == 1
    assert bundle.fact_evidence[0].is_fact_evidence
    assert bundle.legal_boundaries[0].is_legal_boundary


def test_runtime_evidence_reference_dict_excludes_source_record_payload() -> None:
    bundle = load_runtime_evidence()
    reference = bundle.fact_evidence[0].to_reference_dict()

    assert "record" not in reference
    assert reference["citation_role"] == "fact_evidence"
    assert reference["body_storage_policy"] == "public_synthetic_fixture"


def test_runtime_evidence_loader_raises_on_invalid_evidence(tmp_path) -> None:
    bad_evidence = {
        "version": 1,
        "policy": {
            "public_manifest_safe": True,
            "body_text_committed": False,
            "source_manifest": "docs/ingestion/source_manifest.example.json",
        },
        "evidence": [
            {
                "evidence_id": "ev-bad",
                "record_type": "document_metadata",
                "record_id": "missing-record",
                "source_id": "kasb-interpretation-material",
                "citation_role": "supporting_interpretation",
                "body_storage_policy": "public_metadata_only",
                "locator": {"type": "url", "url": "https://www.kasb.or.kr/"},
                "evidence_label": "bad",
                "allowed_output_level": "metadata_locator_only",
            }
        ],
    }
    evidence_path = tmp_path / "bad_evidence.json"
    evidence_path.write_text(json.dumps(bad_evidence), encoding="utf-8")

    with pytest.raises(ValueError, match="unknown source manifest record"):
        load_runtime_evidence(evidence_manifest_path=evidence_path)

