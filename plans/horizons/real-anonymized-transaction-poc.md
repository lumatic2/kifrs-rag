# Horizon: Real Anonymized Transaction PoC

> Status: closed
> Created: 2026-07-05
> Sequence: `docs/horizons/accounting-intelligence-expansion.md`
> Previous: `docs/horizons/firm-facing-poc-brief.md`

## Goal

익명화된 F-ACC 거래 카드 1건을 실제 review pack 산출물로 변환하고, 회계사 reviewer correction을
feedback eval/backlog queue로 연결하는 public-safe PoC 흐름을 만든다.

## Why next

`firm-facing-poc-brief`는 회계법인에 보여줄 narrative와 ask를 정리했다. 다음 증거는 설명 자료가
아니라, 익명화 거래 카드가 들어왔을 때 어떤 산출물과 correction queue가 생기는지 보여주는 것이다.

## Milestones

### RA1. Horizon and Plan Setup

Deliverable:

- `docs/horizons/real-anonymized-transaction-poc.md`
- `docs/plans/2026-07-05-real-anonymized-transaction-poc.md`
- `phases/real-anonymized-transaction-poc/*`

Acceptance:

- ROADMAP/OBJECTIVE가 active horizon을 가리킨다.
- RA1~RA4 phase가 정의된다.

Status: completed (2026-07-05)

### RA2. Transaction PoC Adapter

Deliverable:

- `kifrs/feedback/transaction_poc.py`
- `tests/test_real_transaction_poc.py`

Acceptance:

- KIFRS1116 익명화 거래 카드가 `Lease1116` review pack으로 변환된다.
- protected field가 포함된 card는 거부된다.
- reviewer correction이 feedback queue record로 변환된다.

Status: completed (2026-07-05)

### RA3. Public-Safe Sample Package

Deliverable:

- `scripts/real_transaction_poc.py`
- `docs/reports/real-transaction-poc/`

Acceptance:

- 명령 하나로 anonymized input card, review pack, queue JSONL, queue report, index가 생성된다.

Status: completed (2026-07-05)

### RA4. Close Gate

Deliverable:

- `docs/reports/2026-07-05-ra4-real-transaction-poc-close-report.md`

Acceptance:

- focused tests pass.
- generated sample package exists.
- quality preflight remains public-safe.
- ROADMAP/OBJECTIVE가 다음 horizon을 제안한다.

Status: completed (2026-07-05)
