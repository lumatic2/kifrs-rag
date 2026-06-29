from kifrs.authority import load_authority_sources, search_authority, validate_authority_registry


def test_authority_registry_loads_metadata_only_sources():
    sources = load_authority_sources()
    assert sources
    assert all(source.id and source.authority_type for source in sources)


def test_search_authority_finds_commercial_act_candidate():
    hits = search_authority("상법 자본거래 무상증자")
    assert hits
    assert hits[0]["id"] == "commercial-act-capital"
    assert hits[0]["authority_type"] == "external_law"


def test_authority_registry_validates():
    result = validate_authority_registry()
    assert result["ok"]
    assert result["total"] >= 6


def test_search_authority_finds_fss_candidate():
    hits = search_authority("금융감독원 질의회신 수익")
    assert hits
    assert hits[0]["id"] == "fss-accounting-inquiry"
