from __future__ import annotations

import argparse
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REPORT_PATH = ROOT / "docs" / "reports" / "2026-07-05-as5-first-connector-recommendation.md"

REQUIRED_RECOMMENDED_CONNECTORS = {
    "kasb-fss-interpretive-catalog",
    "opendart-structured-financials",
    "law-regulation-locator",
}

REQUIRED_DEFERRED_CONNECTORS = {
    "audit-standards-namespace",
    "client-private-case-intake",
    "firm-public-guides",
}

REQUIRED_NEXT_MILESTONES = {"MSI1", "MSI2", "MSI3", "MSI4", "MSI5"}


def check_connector_recommendation(report_path: Path = REPORT_PATH) -> dict[str, object]:
    if not report_path.exists():
        return _result(
            errors=[f"missing report: {report_path}"],
            missing_recommended_connectors=sorted(REQUIRED_RECOMMENDED_CONNECTORS),
            missing_deferred_connectors=sorted(REQUIRED_DEFERRED_CONNECTORS),
            missing_next_milestones=sorted(REQUIRED_NEXT_MILESTONES),
        )

    text = report_path.read_text(encoding="utf-8")
    errors: list[str] = []

    missing_recommended_connectors = sorted(
        connector for connector in REQUIRED_RECOMMENDED_CONNECTORS if f"`{connector}`" not in text
    )
    if missing_recommended_connectors:
        errors.append(f"missing recommended connectors: {missing_recommended_connectors}")

    missing_deferred_connectors = sorted(
        connector for connector in REQUIRED_DEFERRED_CONNECTORS if f"`{connector}`" not in text
    )
    if missing_deferred_connectors:
        errors.append(f"missing deferred connectors: {missing_deferred_connectors}")

    missing_next_milestones = sorted(milestone for milestone in REQUIRED_NEXT_MILESTONES if milestone not in text)
    if missing_next_milestones:
        errors.append(f"missing next milestones: {missing_next_milestones}")

    for required_phrase in (
        "`multi-source-ingestion-pipeline`",
        "`supporting_interpretation`",
        "`fact_evidence`",
        "`legal_boundary`",
        "no body ingestion",
        "no external API call",
    ):
        if required_phrase not in text:
            errors.append(f"missing required AS5 phrase: {required_phrase}")

    return _result(
        errors=errors,
        missing_recommended_connectors=missing_recommended_connectors,
        missing_deferred_connectors=missing_deferred_connectors,
        missing_next_milestones=missing_next_milestones,
    )


def _result(
    *,
    errors: list[str],
    missing_recommended_connectors: list[str],
    missing_deferred_connectors: list[str],
    missing_next_milestones: list[str],
) -> dict[str, object]:
    return {
        "ok": not errors,
        "errors": errors,
        "missing_recommended_connectors": missing_recommended_connectors,
        "missing_deferred_connectors": missing_deferred_connectors,
        "missing_next_milestones": missing_next_milestones,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Check AS5 first connector recommendation coverage.")
    parser.add_argument("--format", choices=["text", "json"], default="text")
    args = parser.parse_args()

    result = check_connector_recommendation()
    if args.format == "json":
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(f"ok: {result['ok']}")
        print(f"missing_recommended_connectors: {result['missing_recommended_connectors']}")
        print(f"missing_deferred_connectors: {result['missing_deferred_connectors']}")
        print(f"missing_next_milestones: {result['missing_next_milestones']}")
        for error in result["errors"]:
            print(f"- {error}")

    if not result["ok"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
