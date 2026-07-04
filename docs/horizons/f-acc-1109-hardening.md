# F-ACC 1109 Hardening Horizon

> Created: 2026-07-05
> ROADMAP goal id: `f-acc-1109-hardening`
> Status: active
> Objective: `docs/OBJECTIVE.md`
> Sequence: `docs/horizons/f-acc-technical-expansion.md`

## Why now

1116, 1109, 1115 review pack과 disclosure generalization이 끝났다. 남은 품질 병목은 1109 금융상품
review pack의 4개 NeedsHumanReview 케이스다. 1109는 F-ACC pack 중 가장 복잡한 human boundary를
갖고 있으므로, 이 경계를 줄이면 제품 신뢰도가 직접 올라간다.

## Goal

1109 잔여 NeedsHumanReview 케이스를 분석하고, 자동화 가능한 케이스부터 hardening해 완료율을 높인다.

## Milestone sequence

1. **FH1 — 1109 blocker taxonomy**
   IFRIC19, SPPI reset nuance, reclassification, FX dual track의 공통/개별 blocker를 정리한다.
2. **FH2 — SPPI reset nuance hardening**
   재설정 주기/테너 불일치 케이스의 structured input과 decision path를 추가한다.
3. **FH3 — reclassification memo skeleton**
   사업모형 변경 재분류는 자동 결론보다 수동 검토메모 skeleton을 만든다.
4. **FH4 — FX dual-track boundary**
   1109+1021 이중 트랙을 분리해 필요한 입력과 분개/표시 후보를 정리한다.
5. **FH5 — completion-rate delta report**
   1109 automated/NeedsHumanReview 변화와 남은 경계를 리포트로 남긴다.

## Boundary

IFRIC19, 복잡한 재분류, 외화환산은 실제 계약/회사 정책 자료가 많이 필요하다. 억지 자동 결론보다
사람 검토 queue와 skeleton을 강화하는 것도 hardening으로 인정한다.
