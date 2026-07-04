# F-ACC Technical Expansion Roadmap Plan

> Date: 2026-07-05
> Objective: `docs/OBJECTIVE.md`
> Sequence doc: `docs/horizons/f-acc-technical-expansion.md`

## 산문 요약

회계법인 service-line 조사에서 나온 자동화 후보를 단기 후보 3개로 축소하지 않고, 실제 구현할 horizon
sequence로 다시 정리한다. 이 계획은 F-ACC 중심 기술 확장을 review pack → 1115 → 주석 일반화 →
1109 hardening → 재무제표 본문 → 감사 분석적 절차 → 패키징 순서로 진행하도록 고정했다.

## Step tree

- [x] Step A — 전체 후보를 service-line 기준 horizon sequence로 문서화
  - verify: `docs/horizons/f-acc-technical-expansion.md` 존재
- [x] Step B — 첫 실행 horizon을 1115 수익인식 엔진으로 작성
  - verify: `docs/horizons/f-acc-1115-revenue-engine.md` 존재
- [x] Step C — ROADMAP current horizon을 1115로 전환
  - verify: `ROADMAP.md` closed horizon `f-acc-1115-revenue-engine`
- [x] Step D — R15-1~R15-6 1115 revenue engine 구현
  - verify: `docs/reports/2026-07-05-r15-1115-revenue-engine-completion.md`
- [x] Step E — disclosure generalization 구현
  - verify: `docs/reports/2026-07-05-dg5-cross-domain-disclosure-report.md`
- [x] Step F — 1109 hardening 구현
  - verify: `docs/reports/2026-07-05-fh5-1109-hardening-delta.md`
- [ ] Step G — 남은 sequence를 horizon/step/검증 단위로 hardening
  - verify: `docs/plans/2026-07-05-f-acc-remaining-sequence-hardening.md`
- [ ] Step H — F/S draft FS1부터 실행
  - verify: `docs/reports/2026-07-05-fs1-statement-draft-surface-inventory.md`

## 결정 로그

- 결정: 후보를 버리지 않는다. 단, 구현 순서는 F-ACC 산출물 설명력과 로컬 검증성을 기준으로 정한다.
- 결정: 1115 수익인식 엔진, disclosure generalization, 1109 hardening은 완료했다.
- 결정: 현재 실행은 `f-acc-financial-statement-draft`이다.
- 결정: common review-pack schema 추출은 1115 또는 주석 대사 표면 이후로 보류한다.
- 결정: tax/valuation/K-SOX는 지도에는 남기되 현재 kifrs-rag 실행 순서에서는 후순위 또는 sibling repo로 둔다.
