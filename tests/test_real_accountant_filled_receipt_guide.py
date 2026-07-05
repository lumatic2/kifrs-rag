from __future__ import annotations

from scripts.real_accountant_filled_receipt_guide import build_filled_receipt_guide, render_markdown


def test_filled_receipt_guide_lists_required_edits_and_commands() -> None:
    guide = build_filled_receipt_guide()

    edits = " ".join(guide["required_edits_after_manual_send"])
    assert "manual_send_completed to true" in edits
    assert "YYYY-MM-DD" in edits
    assert "reviewer-001" in edits
    assert "no_raw_identifiers_requested true" in edits
    assert "operator_attestation" in edits
    assert "real_accountant_apply_invite_receipt.py" in guide["apply_command"]
    assert "--receipt docs\\reports\\real-accountant-session\\invite-send-receipt.template.json" in guide["apply_command"]
    assert "real_accountant_outreach_transition_verify.py" in guide["verify_command"]
    assert "--expected-status sent" in guide["verify_command"]


def test_filled_receipt_guide_does_not_claim_actual_send() -> None:
    guide = build_filled_receipt_guide()
    rendered = render_markdown(guide)

    assert "does not send the reviewer invite" in rendered
    assert "does not mark actual send evidence" in rendered
    assert "Do not fill or apply the receipt until the invite was actually sent" in rendered
    assert "This guide does not" in rendered


def test_filled_receipt_guide_is_public_safe() -> None:
    rendered = render_markdown(build_filled_receipt_guide())

    assert "source_body" not in rendered
    assert "api_key" not in rendered
    assert "token" not in rendered
    assert "@" not in rendered
