from __future__ import annotations

from kifrs.ingestion.source_record import validate_source_record, validate_source_records
from scripts.non_ifrs_source_record_contract import build_contract_report, render_markdown


def _base(**updates):
    record = {
        "record_id": "kasb-meta-001",
        "record_type": "document_metadata",
        "source_id": "kasb-interpretation-material",
        "source_class": "interpretive_accounting_material",
        "authority_level": "supporting",
        "body_storage_policy": "public_metadata_only",
        "citation_role": "supporting_interpretation",
        "retrieval_lane": "document_metadata",
        "locator": {"type": "url", "url": "https://www.kasb.or.kr/"},
        "provenance": {"produced_by": "unit-test"},
        "public_safe": True,
        "title": "KASB metadata seed",
        "publisher": "KASB",
        "document_type": "interpretive_material",
        "topics": ["interpretation"],
        "chunk_strategy": "metadata_only",
    }
    record.update(updates)
    return record


def test_source_record_accepts_all_planned_record_types() -> None:
    records = [
        _base(),
        _base(
            record_id="law-locator-001",
            record_type="law_locator",
            source_id="commercial-act-capital",
            source_class="law_regulation",
            authority_level="legal_boundary",
            body_storage_policy="no_store_link_only",
            citation_role="legal_boundary",
            retrieval_lane="law_locator",
            law_name="Commercial Act",
            article_locator="capital-transactions",
            official_registry="law.go.kr",
        ),
        _base(
            record_id="structured-fact-001",
            record_type="structured_fact",
            source_id="opendart-structured-financials",
            source_class="filing_data",
            authority_level="fact",
            body_storage_policy="public_synthetic_fixture",
            citation_role="fact_evidence",
            retrieval_lane="structured_fact",
            company_id="SYNTH-DART-001",
            filing_id="synthetic-filing-001",
            period="2025",
            statement_type="financial_position",
            line_item="current_assets",
            value=1000,
            unit="KRW",
            dimensions={},
            quality_flags=["synthetic"],
        ),
        _base(
            record_id="client-private-placeholder-001",
            record_type="client_private_fact",
            source_id="client-private-local",
            source_class="client_private",
            authority_level="client_private",
            body_storage_policy="no_store_handoff",
            citation_role="collection_seed",
            retrieval_lane="local_private_fact",
            locator={"type": "local_private_placeholder", "label": "client-case"},
            case_scope="lease_contract",
            fact_label="payment_schedule_placeholder",
            fact_kind="contract_term",
            private_storage_boundary="local_only",
            deletion_policy="operator_attested_delete",
        ),
    ]

    result = validate_source_records(records)

    assert result["ok"], result["errors"]
    assert result["by_type"]["document_metadata"] == 1
    assert result["by_type"]["law_locator"] == 1
    assert result["by_type"]["structured_fact"] == 1
    assert result["by_type"]["client_private_fact"] == 1


def test_source_record_rejects_forbidden_body_like_fields() -> None:
    result = validate_source_record(_base(body="copied source body"))

    assert not result["ok"]
    assert any("forbidden manifest field" in error for error in result["errors"])


def test_source_record_rejects_wrong_structured_fact_lane() -> None:
    result = validate_source_record(
        _base(
            record_type="structured_fact",
            source_id="opendart-structured-financials",
            source_class="filing_data",
            authority_level="supporting",
            body_storage_policy="public_metadata_only",
            citation_role="supporting_interpretation",
            retrieval_lane="document_metadata",
            company_id="SYNTH-DART-001",
            filing_id="synthetic-filing-001",
            period="2025",
            statement_type="financial_position",
            line_item="current_assets",
            value=1000,
            unit="KRW",
            dimensions={},
            quality_flags=[],
        )
    )

    assert not result["ok"]
    assert any("retrieval_lane must be structured_fact" in error for error in result["errors"])
    assert any("citation_role must be fact_evidence" in error for error in result["errors"])


def test_nis2_contract_report_is_complete() -> None:
    report = build_contract_report()
    rendered = render_markdown(report)

    assert report["ok"], report["errors"]
    assert set(report["record_types"]) == {
        "document_metadata",
        "law_locator",
        "structured_fact",
        "client_private_fact",
    }
    assert "NIS2 Source Record Contract" in rendered
    assert "NIS3_dataization_fixtures_and_validators" in rendered
