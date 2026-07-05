# WCD3 Minimal Adapter Expansion

> Scope: minimal public-safe adapter for the selected workflow coverage-depth sample.

## 한 줄 결론

`audit_disclosure_tie_out` now produces requirement mapping, tie-out status, review flags, and draft-note labels without making a final audit conclusion.

## Sample Input

| Field | Value |
|---|---|
| `workflow_id` | audit_disclosure_tie_out |
| `entity_profile_label` | public_fixture_manufacturing_group |
| `reporting_period` | 2026-Q2 |
| `disclosure_area` | lease_disclosure |
| `standard_scope` | KIFRS1116_disclosure_requirements |
| `prepared_disclosure_label` | author_written_lease_disclosure_draft_label |
| `review_pack_refs` | ['docs/reports/2026-07-05-wcd2-workflow-sample-contract-pack.md', 'docs/reports/2026-07-05-esb3-chunking-retrieval-dry-run.md'] |

## Disclosure Requirement Checklist

| Requirement | Status | Evidence Ref |
|---|---|---|
| `lease_maturity_analysis_label` | `mapped` | docs/reports/2026-07-05-wcd2-workflow-sample-contract-pack.md |
| `lease_expense_split_label` | `needs_evidence` | None |
| `significant_judgement_label` | `human_review_required` | docs/reports/2026-07-05-esb3-chunking-retrieval-dry-run.md |

## Adapter Output

- tie-out status: `partial`
- missing or ambiguous flags: ['lease_expense_split_label', 'significant_judgement_label']
- review note draft labels: ['lease_disclosure_mapping_note_label', 'lease_judgement_review_note_label']
- human review required items: ['materiality_threshold', 'final_disclosure_completeness', 'audit_sufficiency']
- final audit conclusion: None

## Checks

| Check | OK |
|---|---|
| workflow_matches_contract | True |
| checklist_present | True |
| tie_out_status_present | True |
| review_flags_present | True |
| no_final_audit_conclusion | True |
| next_milestone_named | True |

## Errors

- none

## Next Leaf

- `WCD4_coverage_depth_metric_update`

## Machine Result

```json
{
  "title": "WCD3 Minimal Adapter Expansion",
  "ok": true,
  "horizon": "workflow-coverage-depth-expansion",
  "completed_milestone": "WCD3",
  "sample_input": {
    "workflow_id": "audit_disclosure_tie_out",
    "entity_profile_label": "public_fixture_manufacturing_group",
    "reporting_period": "2026-Q2",
    "disclosure_area": "lease_disclosure",
    "standard_scope": "KIFRS1116_disclosure_requirements",
    "prepared_disclosure_label": "author_written_lease_disclosure_draft_label",
    "review_pack_refs": [
      "docs/reports/2026-07-05-wcd2-workflow-sample-contract-pack.md",
      "docs/reports/2026-07-05-esb3-chunking-retrieval-dry-run.md"
    ]
  },
  "adapter_output": {
    "workflow_id": "audit_disclosure_tie_out",
    "disclosure_requirement_checklist": [
      {
        "requirement_id": "lease_maturity_analysis_label",
        "status": "mapped",
        "evidence_ref": "docs/reports/2026-07-05-wcd2-workflow-sample-contract-pack.md"
      },
      {
        "requirement_id": "lease_expense_split_label",
        "status": "needs_evidence",
        "evidence_ref": null
      },
      {
        "requirement_id": "significant_judgement_label",
        "status": "human_review_required",
        "evidence_ref": "docs/reports/2026-07-05-esb3-chunking-retrieval-dry-run.md"
      }
    ],
    "prepared_disclosure_tie_out_status": "partial",
    "missing_or_ambiguous_evidence_flags": [
      "lease_expense_split_label",
      "significant_judgement_label"
    ],
    "review_note_draft_labels": [
      "lease_disclosure_mapping_note_label",
      "lease_judgement_review_note_label"
    ],
    "human_review_required_items": [
      "materiality_threshold",
      "final_disclosure_completeness",
      "audit_sufficiency"
    ],
    "final_audit_conclusion": null
  },
  "checks": {
    "workflow_matches_contract": true,
    "checklist_present": true,
    "tie_out_status_present": true,
    "review_flags_present": true,
    "no_final_audit_conclusion": true,
    "next_milestone_named": true
  },
  "errors": [],
  "next_leaf": "WCD4_coverage_depth_metric_update",
  "report_path": "docs/reports/2026-07-05-wcd3-minimal-adapter-expansion.md"
}
```
