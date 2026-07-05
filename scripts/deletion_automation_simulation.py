from __future__ import annotations

import argparse
import json
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
REPORT_PATH = ROOT / "docs" / "reports" / "2026-07-05-rlp3-deletion-automation-simulation.md"


@dataclass(frozen=True)
class DeletionSimulationState:
    run_id: str
    parser_report: str
    lifecycle_state: str
    deletion_attested: bool
    deletion_before_report_write: bool
    retained_artifacts: list[str] = field(default_factory=list)
    operator_check: str = ""
    real_deletion_automation: bool = False

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class DeletionSimulationGate:
    gate_id: str
    state: DeletionSimulationState
    errors: list[str] = field(default_factory=list)

    @property
    def ok(self) -> bool:
        return not self.errors

    def to_dict(self) -> dict[str, Any]:
        return {
            "gate_id": self.gate_id,
            "state": self.state.to_dict(),
            "errors": list(self.errors),
            "ok": self.ok,
        }


def default_deletion_simulation_state() -> DeletionSimulationState:
    return DeletionSimulationState(
        run_id="rlp3-local-fixture-lease-contract-deletion-sim",
        parser_report="docs/reports/2026-07-05-rlp2-local-fixture-parser-adapter.md",
        lifecycle_state="deleted_and_attested",
        deletion_attested=True,
        deletion_before_report_write=True,
        retained_artifacts=[],
        operator_check="operator verified simulated local fixture source deletion before close",
        real_deletion_automation=False,
    )


def validate_deletion_simulation_state(state: DeletionSimulationState) -> list[str]:
    errors: list[str] = []
    if not state.run_id:
        errors.append("run_id: run_id is required")
    if not state.parser_report:
        errors.append("parser_report: parser_report is required")
    elif not (ROOT / state.parser_report).exists():
        errors.append(f"parser_report: missing parser report {state.parser_report}")
    if state.lifecycle_state != "deleted_and_attested":
        errors.append("lifecycle_state: lifecycle_state must be deleted_and_attested before close")
    if not state.deletion_attested:
        errors.append("deletion_attested: deletion attestation is required before close")
    if not state.deletion_before_report_write:
        errors.append("deletion_before_report_write: deletion must be attested before report write")
    if state.retained_artifacts:
        errors.append(f"retained_artifacts: retained artifacts block close: {state.retained_artifacts}")
    if "delete" not in state.operator_check.lower() and "deletion" not in state.operator_check.lower():
        errors.append("operator_check: operator check must mention deletion")
    if state.real_deletion_automation:
        errors.append("real_deletion_automation: RLP3 must not claim real deletion automation")
    errors.extend(_public_safe_errors(state.to_dict()))
    return errors


def run_deletion_simulation_gate(
    gate_id: str = "rlp3-deletion-automation-simulation",
    state: DeletionSimulationState | None = None,
) -> DeletionSimulationGate:
    effective_state = state or default_deletion_simulation_state()
    errors = []
    if not gate_id:
        errors.append("gate_id: gate_id is required")
    errors.extend(validate_deletion_simulation_state(effective_state))
    return DeletionSimulationGate(gate_id=gate_id, state=effective_state, errors=errors)


def check_deletion_automation_simulation() -> dict[str, Any]:
    gate = run_deletion_simulation_gate()
    return {
        "ok": gate.ok,
        "gate": gate.to_dict(),
        "errors": list(gate.errors),
        "completed_milestone": "RLP3",
        "next_leaf": "RLP4_private_payload_leak_tests",
        "report_path": _display_path(REPORT_PATH),
    }


def render_report(result: dict[str, Any]) -> str:
    gate = result["gate"]
    state = gate["state"]
    lines = [
        "# RLP3 Deletion Automation Simulation",
        "",
        "> Scope: simulated deletion/retention gate for local parser prototype output.",
        "",
        "## 한 줄 결론",
        "",
        "RLP3 adds a close-blocking deletion simulation gate. Parser output may proceed only when the simulated local fixture lifecycle is deleted and attested before report write, with no retained artifacts. This is still not real filesystem deletion automation.",
        "",
        "## Gate Result",
        "",
        f"- ok: {result['ok']}",
        f"- gate: `{gate['gate_id']}`",
        f"- lifecycle state: {state['lifecycle_state']}",
        f"- deletion attested: {state['deletion_attested']}",
        f"- deletion before report write: {state['deletion_before_report_write']}",
        f"- retained artifacts: {len(state['retained_artifacts'])}",
        f"- real deletion automation: {state['real_deletion_automation']}",
        "",
        "## Blocking Rules",
        "",
        "- Close is blocked if lifecycle state is not `deleted_and_attested`.",
        "- Close is blocked if deletion was not attested before report write.",
        "- Close is blocked if retained artifacts remain.",
        "- Close is blocked if the report claims real deletion automation.",
        "",
        "## Boundary",
        "",
        "- RLP3 simulates lifecycle evidence only.",
        "- RLP3 does not delete real files, read private files, run OCR, copy raw text, or create private embeddings.",
        "- Real local deletion automation remains a future local-only implementation decision.",
        "",
        "## Next Leaf",
        "",
        str(result["next_leaf"]),
        "",
        "## Machine Result",
        "",
        "```json",
        json.dumps(result, ensure_ascii=False, indent=2, default=str),
        "```",
    ]
    if result["errors"]:
        lines.extend(["", "## Errors", ""])
        lines.extend(f"- {error}" for error in result["errors"])
    return "\n".join(lines) + "\n"


def write_report(path: Path = REPORT_PATH) -> dict[str, Any]:
    result = check_deletion_automation_simulation()
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(render_report(result), encoding="utf-8")
    return result


def _public_safe_errors(data: Any) -> list[str]:
    forbidden_keys = {
        "api_key",
        "token",
        "source_body",
        "raw_contract",
        "client_name",
        "customer_name",
        "account_number",
        "embedding_vector",
    }
    errors: list[str] = []

    def visit(value: Any, path: str) -> None:
        if isinstance(value, dict):
            for key, child in value.items():
                key_path = f"{path}.{key}" if path else str(key)
                if str(key) in forbidden_keys:
                    errors.append(f"{key_path}: forbidden public field")
                visit(child, key_path)
        elif isinstance(value, list):
            for index, child in enumerate(value):
                visit(child, f"{path}[{index}]")
        elif isinstance(value, str) and value in forbidden_keys:
            errors.append(f"{path}: forbidden public marker")

    visit(data, "")
    return errors


def _display_path(path: Path) -> str:
    try:
        return path.resolve().relative_to(ROOT).as_posix()
    except ValueError:
        return path.as_posix()


def main() -> None:
    parser = argparse.ArgumentParser(description="Run RLP3 deletion automation simulation gate.")
    parser.add_argument("--format", choices=["text", "json", "markdown"], default="text")
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--out", type=Path, default=REPORT_PATH)
    args = parser.parse_args()

    result = write_report(args.out) if args.write else check_deletion_automation_simulation()
    if args.format == "json":
        print(json.dumps(result, ensure_ascii=False, indent=2, default=str))
    elif args.format == "markdown":
        print(render_report(result), end="")
    else:
        gate = result["gate"]
        state = gate["state"]
        print(f"ok: {result['ok']}")
        print(f"lifecycle_state: {state['lifecycle_state']}")
        print(f"deletion_attested: {state['deletion_attested']}")
        print(f"retained_artifacts: {len(state['retained_artifacts'])}")
        print(f"next_leaf: {result['next_leaf']}")
        for error in result["errors"]:
            print(f"- {error}")
    if not result["ok"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
