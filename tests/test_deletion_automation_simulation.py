from __future__ import annotations

from scripts.deletion_automation_simulation import (
    DeletionSimulationState,
    check_deletion_automation_simulation,
    default_deletion_simulation_state,
    render_report,
    run_deletion_simulation_gate,
    validate_deletion_simulation_state,
)


def test_deletion_simulation_gate_passes_default_state() -> None:
    result = check_deletion_automation_simulation()

    assert result["ok"], result["errors"]
    assert result["completed_milestone"] == "RLP3"
    assert result["next_leaf"] == "RLP4_private_payload_leak_tests"
    assert result["gate"]["state"]["lifecycle_state"] == "deleted_and_attested"
    assert result["gate"]["state"]["deletion_attested"] is True


def test_deletion_simulation_blocks_missing_attestation() -> None:
    state = DeletionSimulationState(
        **{
            **default_deletion_simulation_state().to_dict(),
            "deletion_attested": False,
        }
    )

    gate = run_deletion_simulation_gate(state=state)

    assert not gate.ok
    assert any("deletion_attested" in error for error in gate.errors)


def test_deletion_simulation_blocks_retained_artifacts() -> None:
    state = DeletionSimulationState(
        **{
            **default_deletion_simulation_state().to_dict(),
            "retained_artifacts": ["tmp/client_private/example.pdf"],
        }
    )

    errors = validate_deletion_simulation_state(state)

    assert any("retained_artifacts" in error for error in errors)


def test_deletion_simulation_does_not_claim_real_automation() -> None:
    state = DeletionSimulationState(
        **{
            **default_deletion_simulation_state().to_dict(),
            "real_deletion_automation": True,
        }
    )

    gate = run_deletion_simulation_gate(state=state)

    assert not gate.ok
    assert any("real_deletion_automation" in error for error in gate.errors)


def test_deletion_simulation_report_is_public_safe() -> None:
    rendered = render_report(check_deletion_automation_simulation())

    assert "RLP3 Deletion Automation Simulation" in rendered
    assert "not real filesystem deletion automation" in rendered
    assert "Blocking Rules" in rendered
    assert "api_key" not in rendered
    assert "token" not in rendered
    assert "source_body" not in rendered
