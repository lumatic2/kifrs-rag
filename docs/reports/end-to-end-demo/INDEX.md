# End-to-End Demo Packet

> Scope: one public-safe navigation surface for the firm-facing local toolkit demo.

## How To Use

Open one index and walk the public-safe end-to-end demo without reading ROADMAP internals.

## Demo Run Order

| Order | Section | Report | Command | Purpose | Recovery |
|---:|---|---|---|---|---|
| 0 | start | `docs/reports/2026-07-05-accounting-intelligence-progress-map.md` | `python scripts\accounting_intelligence_progress_map.py --format text --write` | Orient the operator to the active horizon and next leaf. | rerun the progress map command if the position report is missing |
| 1 | storyboard | `docs/reports/2026-07-05-e2e1-demo-asset-inventory.md` | `python scripts\e2e_demo_asset_inventory.py --format text --write` | Show the ordered public-safe demo story. | rerun E2E1 inventory if any core report is missing |
| 2 | contract | `docs/reports/2026-07-05-e2e2-scenario-contract.md` | `python scripts\e2e_scenario_contract.py --format text --write` | Fix stage inputs, evidence, outputs, review checkpoints, commands, and failure boundaries. | rerun E2E2 contract if stage boundaries are unclear |
| 3 | parser | `docs/reports/2026-07-05-real-local-parser-prototype-close-report.md` | `python scripts\real_local_parser_prototype_close_gate.py --format text` | Explain the local-safe parser boundary. | use E2E1 inventory to identify missing parser evidence |
| 4 | source | `docs/reports/2026-07-05-source-body-ingestion-controlled-lane-close-report.md` | `python scripts\controlled_lane_close_gate.py --format text` | Explain authorized source lane handling. | rerun controlled lane close gate after source policy reports exist |
| 5 | workflow | `docs/reports/2026-07-05-workflow-coverage-expansion-close-report.md` | `python scripts\workflow_coverage_close_gate.py --format text` | Explain the 1037 provisions decision-prep extension. | rerun workflow coverage close gate after adapter evidence exists |
| 6 | retriever | `docs/reports/2026-07-05-runtime-retriever-promotion-gate-close-report.md` | `python scripts\runtime_retriever_promotion_close_gate.py --format text` | Explain why default retriever promotion is deferred. | rerun promotion close gate and keep default unchanged if evidence is weak |
| 7 | operator | `docs/reports/2026-07-05-operator-experience-hardening-close-report.md` | `python scripts\operator_experience_close_gate.py --format text` | Show command discovery, doctor, manifest, and recovery path. | run operator doctor and follow recovery playbook hints |

## Boundaries

- This packet uses public-safe reports only.
- It demonstrates decision-prep and review support, not final accounting judgment.
- It does not claim release readiness.
