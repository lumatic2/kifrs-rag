from __future__ import annotations

import argparse
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REPORT_PATH = ROOT / "docs" / "reports" / "2026-07-05-client-private-intake-readiness.md"

REQUIRED_EXISTING_ARTIFACTS = {
    "case_intake_contract": ROOT / "kifrs" / "feedback" / "case_intake.py",
    "client_private_contract_check": ROOT / "scripts" / "client_private_contract_check.py",
    "client_private_redaction_gate_check": ROOT / "scripts" / "client_private_redaction_gate_check.py",
    "client_private_routing_bridge_check": ROOT / "scripts" / "client_private_routing_bridge_check.py",
    "client_private_close_gate": ROOT / "scripts" / "client_private_close_gate.py",
    "transaction_poc_bridge": ROOT / "kifrs" / "feedback" / "transaction_poc.py",
    "real_transaction_package": ROOT / "docs" / "reports" / "real-transaction-poc" / "INDEX.md",
    "gap_audit": ROOT / "docs" / "reports" / "2026-07-05-accounting-intelligence-gap-audit.md",
}

REQUIRED_REPORT_TERMS = {
    "client_private",
    "local_private_case_facts",
    "no_store_handoff",
    "redaction_status",
    "allowed_output_level",
    "raw_contract",
    "customer identifier",
    "reviewer checks original documents outside this repo",
    "do not implement upload",
    "do not parse private source body",
    "LocalPrivateCaseIntake",
    "redact_local_private_case_for_public",
    "render_redacted_client_private_summary",
    "route_redacted_client_private_summary",
    "client_private_close_gate.py",
    "Close report",
    "Status: complete",
}

REQUIRED_NEXT_STEPS = {
    "CP1",
    "CP2",
    "CP3",
    "CP4",
}


def check_client_private_intake_readiness(report_path: Path = REPORT_PATH) -> dict[str, object]:
    errors: list[str] = []
    missing_artifacts = [name for name, path in REQUIRED_EXISTING_ARTIFACTS.items() if not path.exists()]
    if missing_artifacts:
        errors.append(f"missing existing artifacts: {missing_artifacts}")

    if not report_path.exists():
        return {
            "ok": False,
            "errors": errors + [f"missing report: {report_path}"],
            "missing_artifacts": missing_artifacts,
            "missing_report_terms": sorted(REQUIRED_REPORT_TERMS),
            "missing_next_steps": sorted(REQUIRED_NEXT_STEPS),
        }

    text = report_path.read_text(encoding="utf-8")
    missing_report_terms = sorted(term for term in REQUIRED_REPORT_TERMS if term not in text)
    if missing_report_terms:
        errors.append(f"missing report terms: {missing_report_terms}")

    missing_next_steps = sorted(step for step in REQUIRED_NEXT_STEPS if step not in text)
    if missing_next_steps:
        errors.append(f"missing next steps: {missing_next_steps}")

    return {
        "ok": not errors,
        "errors": errors,
        "missing_artifacts": missing_artifacts,
        "missing_report_terms": missing_report_terms,
        "missing_next_steps": missing_next_steps,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Check client-private intake planning readiness.")
    parser.add_argument("--format", choices=["text", "json"], default="text")
    args = parser.parse_args()

    result = check_client_private_intake_readiness()
    if args.format == "json":
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(f"ok: {result['ok']}")
        print(f"missing_artifacts: {result['missing_artifacts']}")
        print(f"missing_report_terms: {result['missing_report_terms']}")
        print(f"missing_next_steps: {result['missing_next_steps']}")
        for error in result["errors"]:
            print(f"- {error}")

    if not result["ok"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
