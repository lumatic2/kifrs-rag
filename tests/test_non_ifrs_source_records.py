from __future__ import annotations

import json

from scripts.validate_non_ifrs_source_records import build_validation, render_markdown


def test_non_ifrs_source_records_cover_all_lanes() -> None:
    validation = build_validation()

    assert validation["ok"], validation["errors"]
    assert validation["total"] == 4
    assert validation["by_type"]["document_metadata"] == 1
    assert validation["by_type"]["law_locator"] == 1
    assert validation["by_type"]["structured_fact"] == 1
    assert validation["by_type"]["client_private_fact"] == 1
    assert validation["next_leaf"] == "NIS4_chunking_and_embedding_policy"


def test_non_ifrs_source_records_reject_body_like_fields(tmp_path) -> None:
    bad = {
        "records": [
            {
                "record_id": "bad",
                "record_type": "document_metadata",
                "source_id": "kasb-interpretation-material",
                "source_class": "interpretive_accounting_material",
                "authority_level": "supporting",
                "body_storage_policy": "public_metadata_only",
                "citation_role": "supporting_interpretation",
                "retrieval_lane": "document_metadata",
                "locator": {"type": "url", "url": "https://www.kasb.or.kr/"},
                "provenance": {"produced_by": "test"},
                "public_safe": True,
                "title": "bad",
                "publisher": "KASB",
                "document_type": "interpretive_material",
                "topics": ["bad"],
                "chunk_strategy": "metadata_only",
                "body": "not allowed",
            }
        ]
    }
    path = tmp_path / "bad.json"
    path.write_text(json.dumps(bad, ensure_ascii=False), encoding="utf-8")

    validation = build_validation(path)

    assert not validation["ok"]
    assert any("forbidden manifest field" in error for error in validation["errors"])


def test_non_ifrs_source_record_report_is_actionable() -> None:
    rendered = render_markdown(build_validation())

    assert "NIS3 Dataization Fixtures" in rendered
    assert "document_metadata" in rendered
    assert "law_locator" in rendered
    assert "structured_fact" in rendered
    assert "client_private_fact" in rendered
    assert "NIS4_chunking_and_embedding_policy" in rendered
