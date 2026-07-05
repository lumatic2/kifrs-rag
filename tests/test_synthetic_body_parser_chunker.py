from __future__ import annotations

import pytest

from scripts.synthetic_body_parser_chunker import (
    SyntheticBodyFixture,
    build_synthetic_body_parser_chunker,
    default_synthetic_fixture,
    parse_and_chunk_synthetic_body,
    render_markdown,
    validate_synthetic_chunks,
    validate_synthetic_fixture,
)


def test_synthetic_body_parser_chunker_builds_public_safe_chunks() -> None:
    result = build_synthetic_body_parser_chunker()

    assert result["ok"], result["errors"]
    assert result["completed_milestone"] == "SBI3"
    assert result["next_leaf"] == "SBI4_controlled_lane_retrieval_gate"
    assert result["chunk_count"] >= 2
    assert all(chunk["citation_role"] == "supporting_interpretation" for chunk in result["chunks"])
    assert all(chunk["authority_level"] == "interpretive" for chunk in result["chunks"])


def test_synthetic_fixture_requires_synthetic_boundary() -> None:
    fixture = SyntheticBodyFixture(
        **{
            **default_synthetic_fixture().to_dict(),
            "synthetic_body": "Revenue guidance without the marker.",
        }
    )

    errors = validate_synthetic_fixture(fixture)

    assert any("synthetic" in error for error in errors)


def test_synthetic_chunker_rejects_wrong_source_id() -> None:
    fixture = SyntheticBodyFixture(
        **{
            **default_synthetic_fixture().to_dict(),
            "source_id": "opendart-structured-financials",
        }
    )

    with pytest.raises(ValueError, match="selected interpretive lane"):
        parse_and_chunk_synthetic_body(fixture)


def test_synthetic_chunks_validate_role_and_length() -> None:
    chunks = parse_and_chunk_synthetic_body(default_synthetic_fixture())

    errors = validate_synthetic_chunks(chunks)

    assert errors == []


def test_synthetic_body_parser_chunker_report_is_public_safe() -> None:
    rendered = render_markdown(build_synthetic_body_parser_chunker())

    assert "SBI3 Synthetic Body Parser And Chunker" in rendered
    assert "synthetic-only parser/chunker" in rendered
    assert "K-IFRS paragraph evidence remains primary" in rendered
    assert "api_key" not in rendered
    assert "token" not in rendered
    assert "source_body" not in rendered
