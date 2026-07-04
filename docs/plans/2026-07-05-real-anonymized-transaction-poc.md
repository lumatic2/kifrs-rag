# Plan: Real Anonymized Transaction PoC

> Objective: `docs/OBJECTIVE.md`
> Horizon: `docs/horizons/real-anonymized-transaction-poc.md`
> Status source: `phases/real-anonymized-transaction-poc/index.json`

## 요약

이번 run은 실제 고객자료를 저장하지 않고, 익명화된 구조화 거래 카드 1건이 F-ACC review pack과
feedback queue로 이어지는지를 증명한다. 첫 대상은 KIFRS1116 리스 거래다.

## Step Tree

- [x] RA1 — horizon/phase/plan setup. (verify: `Test-Path docs\horizons\real-anonymized-transaction-poc.md`)
- [x] RA2 — transaction PoC adapter. (verify: `python -m pytest tests\test_real_transaction_poc.py -q`)
- [x] RA3 — public-safe sample package command. (verify: `python scripts\real_transaction_poc.py --out docs\reports\real-transaction-poc`)
- [x] RA4 — close gate and status sync. (verify: focused tests + `python scripts\quality_preflight.py --format text`)

## 결정 로그

- 결정: 첫 익명화 거래 PoC는 KIFRS1116 리스 카드로 한다.
- 이유: 기존 1116 review pack이 검토메모, 분개, 주석 초안, human-review checklist를 모두 갖고 있다.
- 결정: 실제 원문 계약이나 고객 식별자는 받지 않는다. 구조화 facts와 reviewer correction만 저장한다.
- 예상 사용자 소유 결정: 없음. 실제 회계사에게 어떤 거래를 받을지는 별도 사용자 액션이지만, 이번 run은 public-safe sample로 검증한다.

## 중단점

- protected field가 산출물에 필요해지는 경우 즉시 중단한다.
- 기존 quality preflight가 public-safe가 아니게 되면 close하지 않는다.
