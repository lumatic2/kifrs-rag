from __future__ import annotations

import pytest

from kifrs.ingestion.source_record import load_records
from kifrs.runtime.authority_boundary import (
    AUTHORITY_ROLES,
    DEFAULT_SOURCE_RECORDS_PATH,
    AuthorityRole,
    authority_role_for_source_record,
    build_runtime_authority_boundary,
    build_runtime_authority_boundary_from_records,
    is_non_primary_authority_role,
    is_primary_authority_role,
    render_runtime_authority_boundary,
)


def test_runtime_authority_boundary_groups_all_authority_roles() -> None:
    boundary = build_runtime_authority_boundary(["[1115-B39~B43]"])
    data = boundary.to_dict()

    assert tuple(data) == AUTHORITY_ROLES
    assert data[AuthorityRole.PRIMARY_KIFRS_EVIDENCE.value][0]["citation"] == "[1115-B39~B43]"
    assert len(data[AuthorityRole.SUPPORTING_INTERPRETATION.value]) == 1
    assert len(data[AuthorityRole.LEGAL_BOUNDARY.value]) == 1
    assert len(data[AuthorityRole.FACT_EVIDENCE.value]) == 1
    assert len(data[AuthorityRole.CLIENT_PRIVATE_FACT.value]) == 1


def test_source_records_never_become_primary_authority() -> None:
    records = load_records(DEFAULT_SOURCE_RECORDS_PATH)

    for record in records:
        role = authority_role_for_source_record(record)
        assert is_non_primary_authority_role(role)
        assert not is_primary_authority_role(role)


def test_runtime_authority_boundary_rejects_protected_body_fields() -> None:
    records = load_records(DEFAULT_SOURCE_RECORDS_PATH)
    records[0]["source_body"] = "copied protected material"

    with pytest.raises(ValueError, match="invalid runtime source records"):
        build_runtime_authority_boundary_from_records(records)


def test_runtime_authority_boundary_reference_output_is_public_safe() -> None:
    boundary = build_runtime_authority_boundary(["[1116-53]"])
    rendered = render_runtime_authority_boundary(boundary)
    data = boundary.to_dict()

    assert "Runtime Authority Boundary" in rendered
    assert "Client-private fact" in rendered
    assert "source_body" not in rendered
    assert "raw filing payload" not in rendered
    for items in data.values():
        for item in items:
            assert "record" not in item
            assert "source_body" not in item
            assert "raw_xml" not in item
