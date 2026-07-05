from __future__ import annotations

import json

from scripts.validate_non_ifrs_source_records import DEFAULT_RECORDS_PATH, render_markdown, validate_records


def test_non_ifrs_source_records_cover_all_lanes() -> None:
    result = validate_records()

    assert result["ok"], result["errors"]
    assert result["total"] == 4
    assert result["by_type"]["document_metadata"] == 1
    assert result["by_type"]["law_locator"] == 1
    assert result["by_type"]["structured_fact"] == 1
    assert result["by_type"]["client_private_fact"] == 1
    assert result["next_leaf"] == "NIS4_chunking_and_embedding_policy"


def test_non_ifrs_source_records_reject_body_like_field(tmp_path) -> None:
    payload = json.loads(DEFAULT_RECORDS_PATH.read_text(encoding="utf-8"))
    payload["records"][0]["body"] = "copied source material"
    bad_path = tmp_path / "bad_records.json"
    bad_path.write_text(json.dumps(payload), encoding="utf-8")

    result = validate_records(bad_path)

    assert not result["ok"]
    assert any("forbidden manifest field" in error for error in result["errors"])


def test_nis3_report_is_public_safe_and_actionable() -> None:
    rendered = render_markdown(validate_records())

    assert "NIS3 Dataization Fixtures" in rendered
    assert "document_metadata" in rendered
    assert "law_locator" in rendered
    assert "structured_fact" in rendered
    assert "client_private_fact" in rendered
    assert "NIS4_chunking_and_embedding_policy" in rendered
