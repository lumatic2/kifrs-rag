# F-ACC 1109 Review Pack Horizon

> Created: 2026-07-05
> ROADMAP goal id: `f-acc-1109-review-pack`
> Status: active
> Objective: `docs/OBJECTIVE.md`
> Upstream: `docs/reports/2026-07-05-rp4-poc-demo-brief.md`

## Why now

사용자는 현업 피드백 없이 기술 확장을 계속하기로 결정했다. 이 경우 다음 증거는 새 인터뷰가 아니라,
1116에서 만든 F-ACC review pack 표면이 다른 기준서 도메인에도 이식되는지 보여주는 것이다.

1109 금융상품 엔진은 이미 10개 fixture 중 6개를 자동화하고, 4개를 NeedsHumanReview로 경계 표시한다.
따라서 새 엔진을 처음부터 만드는 1115보다, 기존 1109 엔진을 review pack으로 감싸는 것이 가장 빠른
기술 확장 증거다.

## Goal

1109 금융상품 분류·측정 엔진의 판단, 최초분개, 검토메모, 사람 검토 필요 항목을 하나의 F-ACC
workpaper pack으로 산출한다.

## Milestone candidates

1. **FR1 — 1109 review pack contract + fixture regression**
   기존 1109 runner/review memo/journal entry output을 structured object와 markdown 산출물로 묶고,
   10개 fixture 전체에서 pack 생성 상태를 검증한다.
2. **FR2 — cross-domain review pack comparison**
   1116과 1109 review pack을 같은 표로 비교해, 공통 필드와 도메인별 차이를 정리한다. 필요하면
   공통 schema 추출 여부를 판단한다.
3. **FR3 — next-domain readiness decision**
   1115 수익 엔진으로 갈지, 1109 잔여 4개 NeedsHumanReview 중 1개를 자동화할지, 주석 대사를 확장할지
   기술적으로 재판정한다.

## Close criteria

FR1이 닫히면 최소 기술 확장 증거는 생긴다: 1116이 아닌 1109에서도 review pack이 생성되어야 한다.
FR2~FR3는 공통화와 다음 도메인 선택을 위한 후속 milestone이다.

## Decision

현업 피드백 없이 계속하는 동안에는 1115 신규 엔진보다 1109 review pack 이식을 우선한다. 이유는
F-ACC 제품 표면의 반복 가능성을 먼저 보여주는 것이 더 직접적인 기술 확장 증거이기 때문이다.
