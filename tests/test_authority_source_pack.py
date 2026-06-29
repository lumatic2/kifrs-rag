import json

from kifrs.authority import (
    SOURCE_PACK_FORBIDDEN_FIELDS,
    load_source_pack,
    search_source_pack,
    validate_source_pack,
)


def test_source_pack_validates_metadata_only_items():
    result = validate_source_pack()
    assert result["ok"], result["errors"]
    assert result["total"] >= 6


def test_source_pack_has_no_body_fields():
    pack = load_source_pack()
    for item in pack["items"]:
        assert not (SOURCE_PACK_FORBIDDEN_FIELDS & set(item))


def test_source_pack_search_finds_fss_document_seed():
    hits = search_source_pack("금융감독원 질의회신 수익")
    assert hits
    assert hits[0]["source_id"] == "fss-accounting-inquiry"
    assert hits[0]["allowed_use"] == "supporting_interpretation"


def test_source_pack_rejects_forbidden_body_field(tmp_path):
    bad_pack = {
        "version": 1,
        "policy": {"primary_evidence_source_id": "kifrs-primary", "body_text_committed": False},
        "items": [
            {
                "id": "bad",
                "source_id": "kifrs-primary",
                "title": "bad",
                "publisher": "bad",
                "authority_type": "primary_standard",
                "allowed_use": "primary_evidence",
                "priority": 10,
                "locator": {"kind": "local_private_db", "ref": "data/kifrs.db"},
                "status": "bad",
                "keywords": ["K-IFRS"],
                "notes": "bad",
                "body": "forbidden",
            }
        ],
    }
    path = tmp_path / "source_pack.json"
    path.write_text(json.dumps(bad_pack, ensure_ascii=False), encoding="utf-8")

    result = validate_source_pack(pack_path=path)
    assert not result["ok"]
    assert any("forbidden body fields" in error for error in result["errors"])
