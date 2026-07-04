import json
import importlib.util
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "authority_source_taxonomy_check", ROOT / "scripts" / "authority_source_taxonomy_check.py"
)
authority_source_taxonomy_check = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(authority_source_taxonomy_check)


def test_build_report_detects_complete_taxonomy(tmp_path):
    report = tmp_path / "taxonomy.md"
    sources = tmp_path / "sources.json"
    report.write_text(
        "\n".join(f"`{class_id}`" for class_id in authority_source_taxonomy_check.REQUIRED_CLASSES)
        + "\n| `source-a` | `primary_accounting_standard` | metadata-only | note |",
        encoding="utf-8",
    )
    sources.write_text(json.dumps({"sources": [{"id": "source-a"}]}), encoding="utf-8")

    payload = authority_source_taxonomy_check.build_report(report_path=report, sources_path=sources)

    assert payload["ok"] is True
    assert payload["missing_classes"] == []
    assert payload["missing_source_ids"] == []


def test_build_report_detects_missing_registry_mapping(tmp_path):
    report = tmp_path / "taxonomy.md"
    sources = tmp_path / "sources.json"
    report.write_text(
        "\n".join(f"`{class_id}`" for class_id in authority_source_taxonomy_check.REQUIRED_CLASSES),
        encoding="utf-8",
    )
    sources.write_text(json.dumps({"sources": [{"id": "source-a"}]}), encoding="utf-8")

    payload = authority_source_taxonomy_check.build_report(report_path=report, sources_path=sources)

    assert payload["ok"] is False
    assert payload["missing_source_ids"] == ["source-a"]
