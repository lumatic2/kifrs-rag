# WCD2 Workflow Sample Contract Pack

> Scope: public-safe workflow sample contract for coverage-depth expansion.

## 한 줄 결론

`audit_disclosure_tie_out` is now contract-ready for a minimal adapter: inputs, authority needs, output surface, review boundary, and failure states are explicit.

## Workflow

- workflow id: `audit_disclosure_tie_out`
- service line: `F-AUD / F-ACC`
- surface: audit issue support and disclosure requirement tie-out
- status: `selected_for_minimal_adapter`

## Input Facts

| Field | Kind | Required |
|---|---|---|
| `entity_profile_label` | public_safe_label | True |
| `reporting_period` | date_range | True |
| `disclosure_area` | enum | True |
| `standard_scope` | standard_id_or_topic | True |
| `prepared_disclosure_label` | synthetic_or_author_written_label | True |
| `review_pack_refs` | public_report_locator_list | True |

## Authority Needs

| Role | Source | Required |
|---|---|---|
| primary | K-IFRS paragraph retrieval | True |
| supporting | external connector metadata or synthetic interpretive lane | False |
| fact | public-safe fixture facts | True |
| human_review | materiality and final audit conclusion | True |

## Output Surface

- `disclosure_requirement_checklist`
- `prepared_disclosure_tie_out_status`
- `missing_or_ambiguous_evidence_flags`
- `review_note_draft_labels`
- `human_review_required_items`

## Review Boundary

- AI may draft requirement mapping and review notes.
- AI may not conclude audit sufficiency.
- AI may not sign off disclosure completeness.
- Materiality and final conclusion remain human responsibilities.

## Failure States

| State | Action |
|---|---|
| `missing_primary_authority` | `return blocked` |
| `conflicting_fixture_facts` | `return needs_human_review` |
| `unsupported_disclosure_area` | `return unsupported_workflow` |
| `materiality_judgment_required` | `return human_review_required` |

## Checks

| Check | OK |
|---|---|
| workflow_matches_WCD1 | True |
| input_facts_present | True |
| authority_needs_present | True |
| output_surface_present | True |
| review_boundary_explicit | True |
| failure_states_present | True |
| next_milestone_named | True |

## Errors

- none

## Next Leaf

- `WCD3_minimal_adapter_expansion`

## Machine Result

```json
{
  "title": "WCD2 Workflow Sample Contract Pack",
  "ok": true,
  "horizon": "workflow-coverage-depth-expansion",
  "completed_milestone": "WCD2",
  "workflow": {
    "workflow_id": "audit_disclosure_tie_out",
    "service_line": "F-AUD / F-ACC",
    "surface": "audit issue support and disclosure requirement tie-out",
    "status": "selected_for_minimal_adapter"
  },
  "input_facts": [
    {
      "field": "entity_profile_label",
      "kind": "public_safe_label",
      "required": true
    },
    {
      "field": "reporting_period",
      "kind": "date_range",
      "required": true
    },
    {
      "field": "disclosure_area",
      "kind": "enum",
      "required": true
    },
    {
      "field": "standard_scope",
      "kind": "standard_id_or_topic",
      "required": true
    },
    {
      "field": "prepared_disclosure_label",
      "kind": "synthetic_or_author_written_label",
      "required": true
    },
    {
      "field": "review_pack_refs",
      "kind": "public_report_locator_list",
      "required": true
    }
  ],
  "authority_needs": [
    {
      "role": "primary",
      "source": "K-IFRS paragraph retrieval",
      "required": true
    },
    {
      "role": "supporting",
      "source": "external connector metadata or synthetic interpretive lane",
      "required": false
    },
    {
      "role": "fact",
      "source": "public-safe fixture facts",
      "required": true
    },
    {
      "role": "human_review",
      "source": "materiality and final audit conclusion",
      "required": true
    }
  ],
  "output_surface": [
    "disclosure_requirement_checklist",
    "prepared_disclosure_tie_out_status",
    "missing_or_ambiguous_evidence_flags",
    "review_note_draft_labels",
    "human_review_required_items"
  ],
  "review_boundary": [
    "AI may draft requirement mapping and review notes.",
    "AI may not conclude audit sufficiency.",
    "AI may not sign off disclosure completeness.",
    "Materiality and final conclusion remain human responsibilities."
  ],
  "failure_states": [
    {
      "state": "missing_primary_authority",
      "action": "return blocked"
    },
    {
      "state": "conflicting_fixture_facts",
      "action": "return needs_human_review"
    },
    {
      "state": "unsupported_disclosure_area",
      "action": "return unsupported_workflow"
    },
    {
      "state": "materiality_judgment_required",
      "action": "return human_review_required"
    }
  ],
  "checks": {
    "workflow_matches_WCD1": true,
    "input_facts_present": true,
    "authority_needs_present": true,
    "output_surface_present": true,
    "review_boundary_explicit": true,
    "failure_states_present": true,
    "next_milestone_named": true
  },
  "errors": [],
  "next_leaf": "WCD3_minimal_adapter_expansion",
  "report_path": "docs/reports/2026-07-05-wcd2-workflow-sample-contract-pack.md"
}
```
