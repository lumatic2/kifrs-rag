# WCD1 Service-Line Coverage Rerank

> Scope: rerank firm-service workflow gaps for the next coverage-depth sample.

## 한 줄 결론

Recommended next workflow: `audit_disclosure_tie_out` across `F-AUD / F-ACC`. It broadens coverage from accounting advisory into audit support while reusing existing disclosure, review-pack, retrieval, and connector evidence.

## Ranking Criteria

- `automation_value`
- `evidence_availability`
- `implementation_cost`
- `public_safety`

## Ranked Gaps

| Rank | Workflow | Service Line | Surface | Score | Recommended |
|---:|---|---|---|---:|---|
| 1 | `audit_disclosure_tie_out` | F-AUD / F-ACC | audit issue support and disclosure requirement tie-out | 13 | True |
| 2 | `fs_statement_line_mapping` | F-ACC | financial statement line-item mapping and display candidate review | 11 | False |
| 3 | `audit_analytical_variance_memo` | F-AUD | analytical procedure variance explanation memo | 9 | False |
| 4 | `acquisition_accounting_issue_memo` | F-DEAL / F-ACC | acquisition accounting issue memo | 5 | False |
| 5 | `k_sox_control_checklist` | F-RISK | internal-control checklist and gap memo | 4 | False |

## Checks

| Check | OK |
|---|---|
| service_lines_present | True |
| top_candidate_marked | True |
| top_candidate_public_safe | True |
| top_candidate_uses_existing_evidence | True |
| no_external_dependency_required | True |
| next_milestone_named | True |

## Errors

- none

## Next Leaf

- `WCD2_workflow_sample_contract_pack`

## Machine Result

```json
{
  "title": "WCD1 Service-Line Coverage Rerank",
  "ok": true,
  "horizon": "workflow-coverage-depth-expansion",
  "completed_milestone": "WCD1",
  "ranking_criteria": [
    "automation_value",
    "evidence_availability",
    "implementation_cost",
    "public_safety"
  ],
  "ranked_gaps": [
    {
      "workflow_id": "audit_disclosure_tie_out",
      "service_line": "F-AUD / F-ACC",
      "workflow_surface": "audit issue support and disclosure requirement tie-out",
      "current_evidence": "1116 disclosure draft, review-pack evidence, K-IFRS retrieval, source-body connector lane",
      "automation_value": 5,
      "evidence_availability": 5,
      "implementation_cost": 2,
      "public_safety": 5,
      "recommended_next": true,
      "score": 13
    },
    {
      "workflow_id": "fs_statement_line_mapping",
      "service_line": "F-ACC",
      "workflow_surface": "financial statement line-item mapping and display candidate review",
      "current_evidence": "financial statement draft and review-pack reports",
      "automation_value": 4,
      "evidence_availability": 4,
      "implementation_cost": 2,
      "public_safety": 5,
      "recommended_next": false,
      "score": 11
    },
    {
      "workflow_id": "audit_analytical_variance_memo",
      "service_line": "F-AUD",
      "workflow_surface": "analytical procedure variance explanation memo",
      "current_evidence": "audit analytical procedures horizon and public-safe fixture metrics",
      "automation_value": 4,
      "evidence_availability": 4,
      "implementation_cost": 3,
      "public_safety": 4,
      "recommended_next": false,
      "score": 9
    },
    {
      "workflow_id": "acquisition_accounting_issue_memo",
      "service_line": "F-DEAL / F-ACC",
      "workflow_surface": "acquisition accounting issue memo",
      "current_evidence": "service map only; limited acquisition-accounting workflow evidence",
      "automation_value": 4,
      "evidence_availability": 2,
      "implementation_cost": 4,
      "public_safety": 3,
      "recommended_next": false,
      "score": 5
    },
    {
      "workflow_id": "k_sox_control_checklist",
      "service_line": "F-RISK",
      "workflow_surface": "internal-control checklist and gap memo",
      "current_evidence": "service map only; internal process materials usually required",
      "automation_value": 3,
      "evidence_availability": 2,
      "implementation_cost": 4,
      "public_safety": 3,
      "recommended_next": false,
      "score": 4
    }
  ],
  "recommended_workflow": {
    "workflow_id": "audit_disclosure_tie_out",
    "service_line": "F-AUD / F-ACC",
    "workflow_surface": "audit issue support and disclosure requirement tie-out",
    "reason": "It broadens coverage from accounting advisory into audit support while reusing existing disclosure, review-pack, retrieval, and connector evidence."
  },
  "checks": {
    "service_lines_present": true,
    "top_candidate_marked": true,
    "top_candidate_public_safe": true,
    "top_candidate_uses_existing_evidence": true,
    "no_external_dependency_required": true,
    "next_milestone_named": true
  },
  "errors": [],
  "next_leaf": "WCD2_workflow_sample_contract_pack",
  "report_path": "docs/reports/2026-07-05-wcd1-service-line-coverage-rerank.md"
}
```
