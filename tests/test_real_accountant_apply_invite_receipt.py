from __future__ import annotations

import json
import shutil

from scripts.real_accountant_apply_invite_receipt import apply_invite_receipt, render_markdown, write_demo_receipt
from scripts.real_accountant_invite_send_receipt import build_receipt_template
from scripts.real_accountant_outreach_check import load_outreach


def _write_receipt(path, *, sent: bool = True) -> None:
    receipt = build_receipt_template()
    receipt.update(
        {
            "manual_send_completed": sent,
            "sent_at": "2026-07-05" if sent else "YYYY-MM-DD",
            "operator_attestation": "Sent manually using the packet; no private identifiers recorded."
            if sent
            else "Not sent yet.",
        }
    )
    path.write_text(json.dumps(receipt, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def test_apply_invite_receipt_updates_copied_ledger_after_valid_receipt(tmp_path) -> None:
    receipt = tmp_path / "receipt.json"
    ledger = tmp_path / "outreach.jsonl"
    _write_receipt(receipt, sent=True)
    shutil.copyfile("docs/reports/real-accountant-session/outreach-log.sample.jsonl", ledger)

    result = apply_invite_receipt(receipt_path=receipt, ledger=ledger)

    assert result["ok"], result["errors"]
    assert result["ledger_updated"] is True
    assert result["actual_send_attested"] is True
    assert result["transition"]["next_action_status"] == "waiting_on_reviewer_reply"
    assert load_outreach(ledger)[0]["status"] == "sent"


def test_apply_invite_receipt_rejects_unfilled_receipt(tmp_path) -> None:
    receipt = tmp_path / "receipt.json"
    ledger = tmp_path / "outreach.jsonl"
    _write_receipt(receipt, sent=False)
    shutil.copyfile("docs/reports/real-accountant-session/outreach-log.sample.jsonl", ledger)

    result = apply_invite_receipt(receipt_path=receipt, ledger=ledger)

    assert result["ok"] is False
    assert result["ledger_updated"] is False
    assert load_outreach(ledger)[0]["status"] == "not_sent"
    assert "manual_send_completed must be true" in " ".join(result["errors"])


def test_apply_invite_receipt_dry_run_does_not_mutate_ledger(tmp_path) -> None:
    receipt = tmp_path / "receipt.json"
    ledger = tmp_path / "outreach.jsonl"
    _write_receipt(receipt, sent=True)
    shutil.copyfile("docs/reports/real-accountant-session/outreach-log.sample.jsonl", ledger)

    result = apply_invite_receipt(receipt_path=receipt, ledger=ledger, dry_run=True)

    assert result["ok"], result["errors"]
    assert result["ledger_updated"] is False
    assert result["actual_send_attested"] is True
    assert load_outreach(ledger)[0]["status"] == "not_sent"


def test_write_demo_receipt_supports_public_safe_cli_smoke(tmp_path) -> None:
    receipt = tmp_path / "demo.json"

    payload = write_demo_receipt(receipt)

    assert receipt.exists()
    assert payload["manual_send_completed"] is True
    assert "Synthetic apply smoke" in payload["operator_attestation"]
    assert "source_body" not in receipt.read_text(encoding="utf-8")


def test_apply_invite_receipt_markdown_states_boundaries(tmp_path) -> None:
    receipt = tmp_path / "receipt.json"
    ledger = tmp_path / "outreach.jsonl"
    _write_receipt(receipt, sent=False)
    shutil.copyfile("docs/reports/real-accountant-session/outreach-log.sample.jsonl", ledger)

    rendered = render_markdown(apply_invite_receipt(receipt_path=receipt, ledger=ledger))

    assert "Real Accountant Invite Receipt Apply" in rendered
    assert "does not send the reviewer invite" in rendered
    assert "Do not run this against the real ledger" in rendered
    assert "api_key" not in rendered
    assert "source_body" not in rendered
