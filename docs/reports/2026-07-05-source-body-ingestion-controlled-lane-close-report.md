# Source Body Ingestion Controlled Lane Close Gate

> Scope: SBI5 close gate for the controlled non-IFRS source-body lane.

## 한 줄 결론

The controlled source-body lane is closed as a synthetic-only interpretive lane: source class, policy, chunks, retrieval role, and product trust evidence are connected.

## Close Status

- status: closed
- selected source class: `interpretive_accounting_material`
- implementation mode: `synthetic_body_only`
- chunk count: 3
- retrieved count: 3
- next horizon: `workflow-coverage-expansion`

## Checks

| Check | OK |
|---|---|
| sbi1_source_selection | True |
| sbi2_policy_record | True |
| sbi3_parser_chunker | True |
| sbi4_retrieval_gate | True |
| product_trust_close | True |
| synthetic_only_boundary | True |
| primary_evidence_preserved | True |
| all_required_reports_present | True |

## Required Reports

| Report | Path | Exists |
|---|---|---|
| sbi1_source_selection | `docs/reports/2026-07-05-sbi1-source-class-selection.md` | True |
| sbi2_policy_record | `docs/reports/2026-07-05-sbi2-source-body-policy-record.md` | True |
| sbi3_parser_chunker | `docs/reports/2026-07-05-sbi3-synthetic-body-parser-chunker.md` | True |
| sbi4_retrieval_gate | `docs/reports/2026-07-05-sbi4-controlled-lane-retrieval-gate.md` | True |
| product_trust_close | `docs/reports/2026-07-05-product-trust-quality-close-report.md` | True |

## Still Not Implemented

- live external body fetch
- external body cache
- external body embeddings
- default retriever change
- primary evidence override

## Carried Regression Commands

- `python -m pytest tests\test_source_class_selection.py tests\test_source_policy_record.py tests\test_synthetic_body_parser_chunker.py tests\test_controlled_lane_retrieval_gate.py tests\test_controlled_lane_close_gate.py -q`
- `python scripts\product_trust_quality_gate.py --format text`

## Errors

- none

## Machine Result

```json
{
  "title": "Source Body Ingestion Controlled Lane Close Gate",
  "ok": true,
  "horizon": "source-body-ingestion-controlled-lane",
  "completed_milestone": "SBI5",
  "close_status": "closed",
  "checks": {
    "sbi1_source_selection": true,
    "sbi2_policy_record": true,
    "sbi3_parser_chunker": true,
    "sbi4_retrieval_gate": true,
    "product_trust_close": true,
    "synthetic_only_boundary": true,
    "primary_evidence_preserved": true,
    "all_required_reports_present": true
  },
  "errors": [],
  "reports": {
    "sbi1_source_selection": {
      "path": "docs/reports/2026-07-05-sbi1-source-class-selection.md",
      "exists": true
    },
    "sbi2_policy_record": {
      "path": "docs/reports/2026-07-05-sbi2-source-body-policy-record.md",
      "exists": true
    },
    "sbi3_parser_chunker": {
      "path": "docs/reports/2026-07-05-sbi3-synthetic-body-parser-chunker.md",
      "exists": true
    },
    "sbi4_retrieval_gate": {
      "path": "docs/reports/2026-07-05-sbi4-controlled-lane-retrieval-gate.md",
      "exists": true
    },
    "product_trust_close": {
      "path": "docs/reports/2026-07-05-product-trust-quality-close-report.md",
      "exists": true
    }
  },
  "missing_reports": [],
  "selected_source_class": "interpretive_accounting_material",
  "implementation_mode": "synthetic_body_only",
  "chunk_count": 3,
  "retrieved_count": 3,
  "still_not_implemented": [
    "live external body fetch",
    "external body cache",
    "external body embeddings",
    "default retriever change",
    "primary evidence override"
  ],
  "carried_regression_commands": [
    "python -m pytest tests\\test_source_class_selection.py tests\\test_source_policy_record.py tests\\test_synthetic_body_parser_chunker.py tests\\test_controlled_lane_retrieval_gate.py tests\\test_controlled_lane_close_gate.py -q",
    "python scripts\\product_trust_quality_gate.py --format text"
  ],
  "next_horizon": "workflow-coverage-expansion",
  "report_path": "docs/reports/2026-07-05-source-body-ingestion-controlled-lane-close-report.md"
}
```
