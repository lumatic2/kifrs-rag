# Client-Private Intake Readiness

> Date: 2026-07-05
> Gap: `client-private intake is not implemented beyond public-safe/anonymized samples`

## 한 줄 결론

`client_private` 자료를 실제로 업로드·파싱하기 전에, 이 repo가 먼저 가져야 할 것은 upload 기능이 아니라
local-only intake contract다. 현재는 public-safe anonymized case card와 reviewer correction loop까지는
있지만, 실제 계약서/TB/조서를 받는 `client-private-case-intake`는 아직 구현하면 안 된다.

## Existing Assets

| Asset | What it proves | Limit |
|---|---|---|
| `kifrs/feedback/case_intake.py` | anonymized structured facts와 correction은 public-safe로 검증 가능 | 실제 raw private document를 저장하지 않음 |
| `kifrs/feedback/transaction_poc.py` | anonymized KIFRS1116 card를 review pack으로 변환 가능 | 1116 synthetic/sample path 중심 |
| `docs/reports/real-transaction-poc/INDEX.md` | public-safe sample package가 재생성 가능 | 실제 client-private intake 아님 |
| `docs/reports/2026-07-05-accounting-intelligence-gap-audit.md` | technical demo package는 준비됐지만 client-private gap이 남았음을 표시 | 실제 reviewer/session evidence 필요 |

## Required Boundary

Source class:

- `client_private`

Ingestion lane:

- `local_private_case_facts`

Public storage policy:

- `no_store_handoff`

Allowed public artifact:

- anonymized case id
- structured field schema
- redaction checklist result
- allowed output level
- generated review-pack summary with no source text

Forbidden public artifact:

- `raw_contract`
- contract body
- trial balance file
- workpaper payload
- customer identifier
- company name
- private filing body
- copied source body
- parsed private document body
- embeddings or vector dump

Operational rule:

- reviewer checks original documents outside this repo
- do not implement upload in the public toolkit path
- do not parse private source body into committed artifacts

## Intake Readiness Matrix

| Requirement | Status | Why |
|---|---|---|
| Public-safe structured case schema | ready | `CaseIntake` already validates structured facts and forbidden protected fields |
| Public-safe reviewer correction | ready | `ReviewerCorrection` can become eval/backlog candidate |
| Redaction status field | ready | `LocalPrivateCaseIntake.redaction_status` is validated |
| Allowed output level | ready | `LocalPrivateCaseIntake.allowed_output_level` controls reportable output |
| Local private namespace | ready | `source_locator` uses a local-private locator string, not a committed document body |
| Upload/parser UX | not ready | must wait until local-only storage and deletion policy exist |
| Human source verification | required | reviewer must inspect original documents outside this repo |

## Proposed Next Horizon

`client-private-case-intake`

### CP1. Local-Only Intake Contract

Define a local-only case intake record with:

- `case_id`
- `source_locator`
- `document_type`
- `redaction_status`
- `allowed_output_level`
- `structured_facts`
- `reviewer_original_document_check`

Status: complete. Implemented as `LocalPrivateCaseIntake` in `kifrs/feedback/case_intake.py` and checked by
`scripts/client_private_contract_check.py`.

### CP2. Public-Safe Redaction Gate

Reject:

- `raw_contract`
- `customer identifier`
- copied source body
- private filing body
- embedded document payload

Status: complete. Implemented as `redact_local_private_case_for_public` and
`render_redacted_client_private_summary` in `kifrs/feedback/case_intake.py`, checked by
`scripts/client_private_redaction_gate_check.py`.

### CP3. Review-Pack Routing Bridge

Route only sanitized structured facts into existing 1109/1115/1116 review-pack generators.

Status: complete. Implemented as `route_redacted_client_private_summary` in
`kifrs/feedback/case_intake.py`, checked by `scripts/client_private_routing_bridge_check.py`.

### CP4. Local-Only Close Gate

Prove:

- no private source body appears in public reports
- generated review pack is decision-prep only
- reviewer original-document check remains outside repo

## Decision

The next implementation should not jump straight to file upload, OCR, or private document parsing. It should first add
a local-only intake contract and redaction gate. Until then, `client-private-case-intake` remains a planned capability,
not a completed product feature.
