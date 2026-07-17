# F-AUD Analytical Procedures Horizon

> Created: 2026-07-05
> ROADMAP goal id: `f-audit-analytical-procedures`
> Status: active
> Objective: `docs/OBJECTIVE.md`
> Sequence: `docs/horizons/f-acc-technical-expansion.md`

## Why now

F-ACC 쪽은 review pack, 주석 skeleton, 재무제표 표시 후보까지 연결됐다. 다음은 회계법인 지도에서 보조
적용처로 남겨둔 F-AUD다. 단, 감사의견·KAM·중요성 판단은 사람 책임으로 두고, 공개 F/S 또는 synthetic
fixture로 검증 가능한 분석적 절차 계산표와 이상징후 메모까지만 다룬다.

## Goal

F/S 숫자를 입력하면 전년 대비, 비율, 추세, threshold 기반 이상징후 후보를 만들고, 관련 회계이슈
review pack 또는 statement draft candidate와 연결되는 감사 분석적 절차 초안을 생성한다.

## Milestone sequence

1. **AP1 — analytical procedure scope and fixture inventory**
   공개 DART F/S를 바로 쓸지, synthetic F/S fixture부터 쓸지 범위를 정하고 필요한 schema를 inventory로 남긴다.
2. **AP2 — ratio/trend schema**
   계정 line과 기간별 금액을 받아 증감률, 구성비, 주요 비율을 계산하는 schema를 만든다.
3. **AP3 — anomaly note renderer**
   threshold를 넘는 변화에 대해 감사인이 검토할 질문과 가능한 회계이슈 연결 memo를 만든다.
4. **AP4 — F-ACC output linkage**
   statement draft candidate 또는 review pack output과 anomaly note를 연결한다.
5. **AP5 — analytical procedure report**
   자동화 가능성과 감사 책임 경계를 completion report로 남긴다.

## Boundary

- 감사의견, KAM, 중요성, 표본설계, 내부통제 결론은 자동화하지 않는다.
- 외부 DART API key가 필요해지면 synthetic fixture로 먼저 진행하고, credential 필요 시 중단한다.
- 이 horizon은 감사팀 보조 산출물 PoC이지 감사조서 전체 자동화가 아니다.
