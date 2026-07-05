# WCE3 Minimal Review-Pack Adapter

> Scope: minimal adapter output for the WCE2 1037 provisions workflow contract.

## 한 줄 결론

The 1037 provisions workflow now emits a structured review-pack draft from structured local facts, with final recognition and estimate judgment kept in human review.

## Adapter Summary

- workflow id: `1037_provisions`
- input mode: `structured_local_facts`
- recognition assessment: `review_ready`
- measurement summary: `estimate_basis_supplied`
- confidence: `medium`
- journal entry cue: prepare journal entry cue for provision recognition if accountant confirms present obligation, probable outflow, and reliable estimate

## Missing Facts

- none

## Authority Panel

| Role | Purpose |
|---|---|
| primary_kifrs | recognition, measurement, disclosure, and present-value boundary |
| supporting_interpretation | non-primary explanation only; cannot override K-IFRS |
| client_private_fact | facts used by the workflow; not persisted in public output |

## Human Review Checklist

- Confirm the event creates a present legal or constructive obligation.
- Confirm outflow probability; do not let the adapter infer probability from narrative alone.
- Review whether management's estimate is reliable and complete.
- Check whether discounting is material.
- Confirm final recognition, measurement, presentation, and disclosure with the accountant.

## Limitations

- final recognition conclusion
- probability assessment when not supplied
- best estimate, range, and discount rate judgment
- legal interpretation of contract enforceability
- financial statement materiality and presentation conclusion

## Errors

- none

## Machine Result

```json
{
  "title": "WCE3 Minimal Review-Pack Adapter",
  "ok": true,
  "horizon": "workflow-coverage-expansion",
  "completed_milestone": "WCE3",
  "workflow_id": "1037_provisions",
  "input_mode": "structured_local_facts",
  "input_facts": {
    "obligating_event": "board-approved restructuring plan communicated before reporting date",
    "obligation_type": "restructuring",
    "outflow_probability": "probable",
    "estimate_basis": "management provided expected direct exit costs as a bounded amount",
    "discounting_indicator": "not material for this synthetic fixture"
  },
  "output": {
    "structured_summary": {
      "workflow": "Provision recognition and measurement decision-prep memo",
      "recognition_assessment": "review_ready",
      "measurement_summary": "estimate_basis_supplied",
      "journal_entry_cue": "prepare journal entry cue for provision recognition if accountant confirms present obligation, probable outflow, and reliable estimate",
      "missing_facts": [],
      "authority_panel": [
        {
          "role": "primary_kifrs",
          "purpose": "recognition, measurement, disclosure, and present-value boundary"
        },
        {
          "role": "supporting_interpretation",
          "purpose": "non-primary explanation only; cannot override K-IFRS"
        },
        {
          "role": "client_private_fact",
          "purpose": "facts used by the workflow; not persisted in public output"
        }
      ]
    },
    "human_review_checklist": [
      "Confirm the event creates a present legal or constructive obligation.",
      "Confirm outflow probability; do not let the adapter infer probability from narrative alone.",
      "Review whether management's estimate is reliable and complete.",
      "Check whether discounting is material.",
      "Confirm final recognition, measurement, presentation, and disclosure with the accountant."
    ],
    "confidence": "medium",
    "limitations": [
      "final recognition conclusion",
      "probability assessment when not supplied",
      "best estimate, range, and discount rate judgment",
      "legal interpretation of contract enforceability",
      "financial statement materiality and presentation conclusion"
    ]
  },
  "errors": [],
  "report_path": "docs/reports/2026-07-05-wce3-minimal-review-pack-adapter.md"
}
```
