# RLP1 Parser Prototype Asset Inventory

> Scope: inventory reusable parser/runtime assets before implementing the local parser prototype path.

## Result

- ok: True
- active horizon: `real-local-parser-prototype`
- completed milestone: `RLP1`
- next milestone: `RLP2`

## Asset Inventory

| Asset | Category | Stage | Path | Reusable For | Gap |
|---|---|---|---|---|---|
| local-parser-module | core_module | prototype_contract | `kifrs/feedback/local_parser.py` | RLP2, RLP3, RLP4, RLP5 | Needs a more realistic local fixture adapter instead of only synthetic dry-run handoff. |
| case-intake-module | core_module | intake_redaction_deletion | `kifrs/feedback/case_intake.py` | RLP2, RLP3, RLP4, RLP5 | Needs product-level leak tests around every parser-facing public artifact. |
| upload-storage-policy | policy | completed_prior_asset | `docs/reports/2026-07-05-cpu1-client-private-upload-storage-policy.md` | RLP3, RLP5 | Policy exists, but RLP still needs a close gate tying policy to the prototype flow. |
| parser-dry-run-fixture | fixture | completed_prior_asset | `docs/reports/2026-07-05-pdf1-private-parser-dry-run-fixture.md` | RLP2, RLP4 | Fixture exists, but RLP2 needs a fixture-like adapter path that emits review questions. |
| deletion-attestation-gate | deletion_gate | completed_prior_asset | `docs/reports/2026-07-05-lda1-local-deletion-attestation-gate.md` | RLP3, RLP5 | Attestation exists, but deletion automation is still simulated/manual. |
| local-parser-close-gate | close_gate | completed_prior_asset | `docs/reports/2026-07-05-cpl1-client-private-local-parser-close-gate.md` | RLP5 | Prior close gate proves readiness, not the new RLP prototype sequence. |
| prototype-spike | prototype | completed_prior_asset | `docs/reports/2026-07-05-lpp1-local-parser-prototype-spike.md` | RLP2 | Prototype spike needs to be wrapped by a reusable local fixture adapter. |
| adapter-contract | adapter_contract | completed_prior_asset | `docs/reports/2026-07-05-lpa1-local-parser-adapter-contract.md` | RLP2, RLP4 | Contract exists, but RLP2 needs adapter output with structured facts plus review questions. |
| adapter-dry-run-gate | adapter_gate | completed_prior_asset | `docs/reports/2026-07-05-lpad1-local-parser-adapter-dry-run-gate.md` | RLP2, RLP5 | Dry-run gate exists, but RLP needs a horizon-specific close gate. |
| adapter-scaffold | adapter_scaffold | completed_prior_asset | `docs/reports/2026-07-05-lpas1-local-parser-adapter-scaffold.md` | RLP2 | Scaffold exists, but a real local parser adapter is still deferred. |
| operator-runbook | operator_runbook | completed_prior_asset | `docs/reports/2026-07-05-lpor1-local-parser-operator-runbook.md` | RLP5 | Runbook exists, but operator UX hardening remains a later horizon. |
| real-adapter-decision-gate | decision_gate | completed_prior_asset | `docs/reports/2026-07-05-lprd1-local-parser-real-adapter-decision-gate.md` | RLP2, RLP5 | Real adapter remains deferred until explicit local-only private-file authorization. |
| real-adapter-implementation-plan | implementation_plan | completed_prior_asset | `docs/reports/2026-07-05-local-parser-real-adapter-implementation-plan.md` | RLP2, RLP5 | Implementation plan exists, but RLP should not introduce real private files. |
| parser-runtime-close-report | runtime_close | completed_prior_asset | `docs/reports/2026-07-05-client-private-parser-runtime-close-report.md` | RLP5 | Runtime close is prior evidence; RLP needs a new prototype close result. |

## RLP2-RLP5 Gaps

- RLP2: Build a local-safe fixture adapter that turns fixture-like input into structured facts and review questions.
- RLP3: Simulate deletion states and block close when retention/deletion attestation is incomplete.
- RLP4: Add product-level leak tests for parser outputs and generated reports.
- RLP5: Tie RLP1 through RLP4 into a close gate with carried trust/runtime evidence.

## Missing Assets

- none

## Boundary

- RLP1 does not implement a parser adapter.
- RLP1 does not introduce real client files, OCR, private embeddings, protected source text, or raw private payload.
- RLP1 only fixes the asset map and next gaps for RLP2 through RLP5.

## Machine Result

```json
{
  "title": "RLP1 Parser Prototype Asset Inventory",
  "ok": true,
  "active_horizon": "real-local-parser-prototype",
  "completed_milestone": "RLP1",
  "next_milestone": "RLP2",
  "assets": [
    {
      "asset_id": "local-parser-module",
      "path": "kifrs/feedback/local_parser.py",
      "category": "core_module",
      "stage": "prototype_contract",
      "reusable_for": [
        "RLP2",
        "RLP3",
        "RLP4",
        "RLP5"
      ],
      "gap_to_next": "Needs a more realistic local fixture adapter instead of only synthetic dry-run handoff.",
      "exists": true
    },
    {
      "asset_id": "case-intake-module",
      "path": "kifrs/feedback/case_intake.py",
      "category": "core_module",
      "stage": "intake_redaction_deletion",
      "reusable_for": [
        "RLP2",
        "RLP3",
        "RLP4",
        "RLP5"
      ],
      "gap_to_next": "Needs product-level leak tests around every parser-facing public artifact.",
      "exists": true
    },
    {
      "asset_id": "upload-storage-policy",
      "path": "docs/reports/2026-07-05-cpu1-client-private-upload-storage-policy.md",
      "category": "policy",
      "stage": "completed_prior_asset",
      "reusable_for": [
        "RLP3",
        "RLP5"
      ],
      "gap_to_next": "Policy exists, but RLP still needs a close gate tying policy to the prototype flow.",
      "exists": true
    },
    {
      "asset_id": "parser-dry-run-fixture",
      "path": "docs/reports/2026-07-05-pdf1-private-parser-dry-run-fixture.md",
      "category": "fixture",
      "stage": "completed_prior_asset",
      "reusable_for": [
        "RLP2",
        "RLP4"
      ],
      "gap_to_next": "Fixture exists, but RLP2 needs a fixture-like adapter path that emits review questions.",
      "exists": true
    },
    {
      "asset_id": "deletion-attestation-gate",
      "path": "docs/reports/2026-07-05-lda1-local-deletion-attestation-gate.md",
      "category": "deletion_gate",
      "stage": "completed_prior_asset",
      "reusable_for": [
        "RLP3",
        "RLP5"
      ],
      "gap_to_next": "Attestation exists, but deletion automation is still simulated/manual.",
      "exists": true
    },
    {
      "asset_id": "local-parser-close-gate",
      "path": "docs/reports/2026-07-05-cpl1-client-private-local-parser-close-gate.md",
      "category": "close_gate",
      "stage": "completed_prior_asset",
      "reusable_for": [
        "RLP5"
      ],
      "gap_to_next": "Prior close gate proves readiness, not the new RLP prototype sequence.",
      "exists": true
    },
    {
      "asset_id": "prototype-spike",
      "path": "docs/reports/2026-07-05-lpp1-local-parser-prototype-spike.md",
      "category": "prototype",
      "stage": "completed_prior_asset",
      "reusable_for": [
        "RLP2"
      ],
      "gap_to_next": "Prototype spike needs to be wrapped by a reusable local fixture adapter.",
      "exists": true
    },
    {
      "asset_id": "adapter-contract",
      "path": "docs/reports/2026-07-05-lpa1-local-parser-adapter-contract.md",
      "category": "adapter_contract",
      "stage": "completed_prior_asset",
      "reusable_for": [
        "RLP2",
        "RLP4"
      ],
      "gap_to_next": "Contract exists, but RLP2 needs adapter output with structured facts plus review questions.",
      "exists": true
    },
    {
      "asset_id": "adapter-dry-run-gate",
      "path": "docs/reports/2026-07-05-lpad1-local-parser-adapter-dry-run-gate.md",
      "category": "adapter_gate",
      "stage": "completed_prior_asset",
      "reusable_for": [
        "RLP2",
        "RLP5"
      ],
      "gap_to_next": "Dry-run gate exists, but RLP needs a horizon-specific close gate.",
      "exists": true
    },
    {
      "asset_id": "adapter-scaffold",
      "path": "docs/reports/2026-07-05-lpas1-local-parser-adapter-scaffold.md",
      "category": "adapter_scaffold",
      "stage": "completed_prior_asset",
      "reusable_for": [
        "RLP2"
      ],
      "gap_to_next": "Scaffold exists, but a real local parser adapter is still deferred.",
      "exists": true
    },
    {
      "asset_id": "operator-runbook",
      "path": "docs/reports/2026-07-05-lpor1-local-parser-operator-runbook.md",
      "category": "operator_runbook",
      "stage": "completed_prior_asset",
      "reusable_for": [
        "RLP5"
      ],
      "gap_to_next": "Runbook exists, but operator UX hardening remains a later horizon.",
      "exists": true
    },
    {
      "asset_id": "real-adapter-decision-gate",
      "path": "docs/reports/2026-07-05-lprd1-local-parser-real-adapter-decision-gate.md",
      "category": "decision_gate",
      "stage": "completed_prior_asset",
      "reusable_for": [
        "RLP2",
        "RLP5"
      ],
      "gap_to_next": "Real adapter remains deferred until explicit local-only private-file authorization.",
      "exists": true
    },
    {
      "asset_id": "real-adapter-implementation-plan",
      "path": "docs/reports/2026-07-05-local-parser-real-adapter-implementation-plan.md",
      "category": "implementation_plan",
      "stage": "completed_prior_asset",
      "reusable_for": [
        "RLP2",
        "RLP5"
      ],
      "gap_to_next": "Implementation plan exists, but RLP should not introduce real private files.",
      "exists": true
    },
    {
      "asset_id": "parser-runtime-close-report",
      "path": "docs/reports/2026-07-05-client-private-parser-runtime-close-report.md",
      "category": "runtime_close",
      "stage": "completed_prior_asset",
      "reusable_for": [
        "RLP5"
      ],
      "gap_to_next": "Runtime close is prior evidence; RLP needs a new prototype close result.",
      "exists": true
    }
  ],
  "missing_assets": [],
  "rlp_gaps": {
    "RLP2": "Build a local-safe fixture adapter that turns fixture-like input into structured facts and review questions.",
    "RLP3": "Simulate deletion states and block close when retention/deletion attestation is incomplete.",
    "RLP4": "Add product-level leak tests for parser outputs and generated reports.",
    "RLP5": "Tie RLP1 through RLP4 into a close gate with carried trust/runtime evidence."
  },
  "report_path": "docs/reports/2026-07-05-rlp1-parser-prototype-asset-inventory.md"
}
```
