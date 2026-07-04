"""PK2 tests for the local demo PoC command surface."""

from scripts.demo_poc import generate_demo


def test_generate_demo_writes_expected_markdown_files(tmp_path):
    written = generate_demo("revenue-financing", tmp_path)
    names = {path.name for path in written}

    assert "index.md" in names
    assert "1115-significant-financing-review-pack.md" in names
    assert "1115-repurchase-review-pack.md" in names
    assert "statement-candidates.md" in names
    assert "evidence-boundary.md" in names
    assert "audit-analytics-note.md" in names
    assert "audit-facc-links.md" in names
    assert "1116-lease-review-pack.md" in names

    index = (tmp_path / "index.md").read_text(encoding="utf-8")
    statement = (tmp_path / "statement-candidates.md").read_text(encoding="utf-8")
    evidence = (tmp_path / "evidence-boundary.md").read_text(encoding="utf-8")
    links = (tmp_path / "audit-facc-links.md").read_text(encoding="utf-8")

    assert "기준서 원문, DB, embedding, dogfood 자료는 포함하지 않는다" in index
    assert "금융부채" in statement
    assert "synthetic-dart-2025-annual-001-revenue" in statement
    assert "Primary K-IFRS evidence" in evidence
    assert "Fact evidence" in evidence
    assert "copied source" not in evidence
    assert "ratio:debt_to_equity_rise" in links


def test_generate_demo_rejects_unknown_scenario(tmp_path):
    try:
        generate_demo("unknown", tmp_path)
    except ValueError as exc:
        assert "unsupported demo scenario" in str(exc)
    else:
        raise AssertionError("unknown scenario should fail")
