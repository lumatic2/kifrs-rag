# WCE2 First Workflow Candidate Contract

> Scope: WCE2 contract for the workflow selected by WCE1.

## 한 줄 결론

`1037_provisions` is now a bounded decision-prep workflow contract: it can draft recognition/measurement review material, but final conclusion and estimate judgment stay with the accountant.

## Contract

- workflow id: `1037_provisions`
- service line: F-ACC / F-AUD
- standard scope: KIFRS1037
- workflow name: Provision recognition and measurement decision-prep memo
- purpose: Prepare a bounded accountant-review draft for provision recognition, measurement, journal-entry cues, and missing-facts review questions.

## Inputs

| Name | Required | Source | Description |
|---|---|---|---|
| obligating_event | True | structured local facts | Past event or condition that may create a present obligation. |
| obligation_type | True | structured local facts | Legal, constructive, onerous contract, restructuring, restoration, or other provision category. |
| outflow_probability | True | structured local facts | Management-assessed likelihood bucket; the AI does not invent probability. |
| estimate_basis | False | structured local facts | Management estimate, range, expected value, present-value assumption, or missing estimate marker. |
| discounting_indicator | False | structured local facts | Whether time value of money is material and requires present-value review. |

## Outputs

- recognition_assessment
- measurement_summary
- journal_entry_cue
- missing_facts
- human_review_checklist
- authority_panel

## Evidence Roles

| Role | Allowed Sources | Purpose |
|---|---|---|
| primary_kifrs | KIFRS1037 | recognition, measurement, disclosure, and present-value boundary |
| supporting_interpretation | controlled interpretive lane | non-primary explanation only; cannot override K-IFRS |
| client_private_fact | structured local facts only | facts used by the workflow; not persisted in public output |

## Human Review Boundary

- final recognition conclusion
- probability assessment when not supplied
- best estimate, range, and discount rate judgment
- legal interpretation of contract enforceability
- financial statement materiality and presentation conclusion

## Not Implemented

- contract OCR
- legal enforceability opinion
- automatic best-estimate calculation from raw evidence
- default retriever promotion
- live external source fetch

## Errors

- none

## Machine Result

```json
{
  "title": "WCE2 First Workflow Candidate Contract",
  "ok": true,
  "horizon": "workflow-coverage-expansion",
  "completed_milestone": "WCE2",
  "selected_candidate": "1037_provisions",
  "contract": {
    "workflow_id": "1037_provisions",
    "service_line": "F-ACC / F-AUD",
    "standard_scope": [
      "KIFRS1037"
    ],
    "workflow_name": "Provision recognition and measurement decision-prep memo",
    "purpose": "Prepare a bounded accountant-review draft for provision recognition, measurement, journal-entry cues, and missing-facts review questions.",
    "inputs": [
      {
        "name": "obligating_event",
        "required": true,
        "source": "structured local facts",
        "description": "Past event or condition that may create a present obligation."
      },
      {
        "name": "obligation_type",
        "required": true,
        "source": "structured local facts",
        "description": "Legal, constructive, onerous contract, restructuring, restoration, or other provision category."
      },
      {
        "name": "outflow_probability",
        "required": true,
        "source": "structured local facts",
        "description": "Management-assessed likelihood bucket; the AI does not invent probability."
      },
      {
        "name": "estimate_basis",
        "required": false,
        "source": "structured local facts",
        "description": "Management estimate, range, expected value, present-value assumption, or missing estimate marker."
      },
      {
        "name": "discounting_indicator",
        "required": false,
        "source": "structured local facts",
        "description": "Whether time value of money is material and requires present-value review."
      }
    ],
    "outputs": [
      "recognition_assessment",
      "measurement_summary",
      "journal_entry_cue",
      "missing_facts",
      "human_review_checklist",
      "authority_panel"
    ],
    "evidence_roles": [
      {
        "role": "primary_kifrs",
        "allowed_sources": [
          "KIFRS1037"
        ],
        "purpose": "recognition, measurement, disclosure, and present-value boundary"
      },
      {
        "role": "supporting_interpretation",
        "allowed_sources": [
          "controlled interpretive lane"
        ],
        "purpose": "non-primary explanation only; cannot override K-IFRS"
      },
      {
        "role": "client_private_fact",
        "allowed_sources": [
          "structured local facts only"
        ],
        "purpose": "facts used by the workflow; not persisted in public output"
      }
    ],
    "human_review_boundary": [
      "final recognition conclusion",
      "probability assessment when not supplied",
      "best estimate, range, and discount rate judgment",
      "legal interpretation of contract enforceability",
      "financial statement materiality and presentation conclusion"
    ],
    "not_implemented": [
      "contract OCR",
      "legal enforceability opinion",
      "automatic best-estimate calculation from raw evidence",
      "default retriever promotion",
      "live external source fetch"
    ],
    "wce1_evidence": "docs/reports/2026-07-05-wce1-coverage-gap-ranking.md",
    "next_adapter": "minimal_workflow_review_pack_adapter"
  },
  "errors": [],
  "report_path": "docs/reports/2026-07-05-wce2-first-workflow-contract.md"
}
```
