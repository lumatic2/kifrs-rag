from __future__ import annotations

from scripts.real_accountant_invite_send_receipt import (
    build_receipt_template,
    check_invite_send_receipt,
    render_markdown,
    write_template,
)


def test_invite_send_receipt_template_does_not_claim_sent() -> None:
    result = check_invite_send_receipt()

    assert result["ok"], result["errors"]
    assert result["actual_send_attested"] is False
    assert result["next_action"] == "send_reviewer_invite_then_fill_receipt"
    assert result["receipt"]["reviewer_alias"] == "reviewer-001"
    assert result["receipt"]["manual_send_completed"] is False


def test_require_sent_rejects_unfilled_template() -> None:
    result = check_invite_send_receipt(require_sent=True)

    assert result["ok"] is False
    assert "manual_send_completed must be true" in " ".join(result["errors"])
    assert result["next_action"] == "fix_receipt"


def test_completed_public_safe_receipt_passes_sent_attestation() -> None:
    receipt = build_receipt_template()
    receipt.update(
        {
            "manual_send_completed": True,
            "sent_at": "2026-07-05",
            "operator_attestation": "Sent manually using the packet; no names or source bodies recorded.",
        }
    )

    result = check_invite_send_receipt(receipt, require_sent=True)

    assert result["ok"], result["errors"]
    assert result["actual_send_attested"] is True
    assert result["next_action"] == "update_outreach_ledger_to_sent_and_verify"


def test_receipt_rejects_non_alias_and_private_patterns() -> None:
    receipt = build_receipt_template()
    receipt.update(
        {
            "reviewer_alias": "actual-name",
            "manual_send_completed": True,
            "sent_at": "2026-07-05",
            "operator_attestation": "Sent to person@example.com with source_body attached.",
        }
    )

    result = check_invite_send_receipt(receipt, require_sent=True)

    assert result["ok"] is False
    joined = " ".join(result["errors"])
    assert "public-safe alias" in joined
    assert "source_body" in joined
    assert "@" in joined or "A-Z0-9" in joined


def test_render_markdown_is_public_safe_and_actionable() -> None:
    rendered = render_markdown(check_invite_send_receipt())

    assert "Real Accountant Invite Send Receipt" in rendered
    assert "does not claim the invite was sent" in rendered
    assert "real_accountant_outreach_update.py" in rendered
    assert "real_accountant_outreach_transition_verify.py" in rendered
    assert "api_key" not in rendered
    assert "source_body" not in rendered


def test_write_template_creates_json_template(tmp_path) -> None:
    out = tmp_path / "receipt.template.json"

    template = write_template(out)

    assert out.exists()
    assert template["manual_send_completed"] is False
    assert "real_accountant_outreach_update.py" in out.read_text(encoding="utf-8")
