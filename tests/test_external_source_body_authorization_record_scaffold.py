from __future__ import annotations

from scripts.external_source_body_authorization_record_scaffold import (
    build_authorization_template,
    build_scaffold_result,
    render_report,
    write_scaffold,
)
from scripts.external_source_body_ingestion_authorization_gate import load_authorization_record


def test_scaffold_writes_non_authorizing_template(tmp_path) -> None:
    template_path = tmp_path / "authorization.template.json"
    report_path = tmp_path / "scaffold.md"

    result = write_scaffold(template_path=template_path, report_path=report_path)

    assert result["ok"], result["errors"]
    assert result["template_exists"] is True
    assert result["template_gate_decision"] == "defer"
    assert result["template_allowed_to_implement"] is False
    assert "authorized_by is required" in " ".join(result["template_blockers"])
    template = build_authorization_template()
    assert template["authorized_by"] == ""
    assert template["authorization_scope"] == "synthetic_dry_run_only"
    assert template["live_fetch_allowed"] is False
    assert template["chunking_allowed"] is False
    assert template["embedding_allowed"] is False


def test_scaffold_result_before_write_is_safe_and_pending(tmp_path) -> None:
    template_path = tmp_path / "missing.template.json"

    result = build_scaffold_result(template_path=template_path)

    assert result["ok"], result["errors"]
    assert result["template_exists"] is False
    assert result["template_gate_decision"] is None
    assert result["template_allowed_to_implement"] is None


def test_scaffold_report_keeps_authorization_boundary(tmp_path) -> None:
    template_path = tmp_path / "authorization.template.json"
    report_path = tmp_path / "scaffold.md"
    result = write_scaffold(template_path=template_path, report_path=report_path)

    report = render_report(result)

    assert "intentionally not an approval" in report
    assert "Live fetch, chunking, embedding, indexing, and public body commits remain disabled." in report
    assert "source-specific" in report
    assert "api_key" not in report
    assert "token" not in report


def test_authorization_loader_rejects_string_booleans(tmp_path) -> None:
    record = tmp_path / "bad-bool.json"
    record.write_text(
        """{
  "authorized_by": "user-explicit-approval",
  "authorization_scope": "source_specific_local_private_body",
  "risk_acknowledgement": "true",
  "source_review_required": true,
  "public_repo_body_commit_allowed": false,
  "live_fetch_allowed": true,
  "chunking_allowed": true,
  "embedding_allowed": true
}""",
        encoding="utf-8",
    )

    try:
        load_authorization_record(record)
    except ValueError as exc:
        assert "risk_acknowledgement must be a JSON boolean" in str(exc)
    else:
        raise AssertionError("string boolean authorization fields should be rejected")
