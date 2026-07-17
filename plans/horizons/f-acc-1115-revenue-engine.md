# F-ACC 1115 Revenue Engine Horizon

> Created: 2026-07-05
> ROADMAP goal id: `f-acc-1115-revenue-engine`
> Status: active
> Objective: `docs/OBJECTIVE.md`
> Sequence: `docs/horizons/f-acc-technical-expansion.md`

## Why now

1116 리스와 1109 금융상품은 review pack 표면까지 도달했다. 다음 기술 확장은 F-ACC의 복잡 계약 판단
업무와 직접 연결되는 1115 수익인식이다. 1115는 고객 선택권, 유의적 금융요소, 재매입약정처럼 판단
분기가 뚜렷하고, 이미 `data/scenarios/1115_revenue/WORKFLOW.md` seed가 있다.

## Goal

1115 수익 계약을 구조화 입력으로 받아 다음 산출물을 단계적으로 만든다.

- 수익인식 판단 경로
- 수행의무 및 거래가격 배분 판단
- 유의적 금융요소 또는 재매입약정 처리 방향
- 분개/측정 초안
- 검토메모
- F-ACC review pack

## Milestone sequence

1. **R15-1 — schema + seed fixture inventory**
   1115 WORKFLOW seed의 4개 판단유형을 공개 가능한 구조화 fixture로 옮기고, 첫 결정 함수가 판단 경로와
   근거 인용을 반환하게 한다.
2. **R15-2 — five-step decision engine**
   계약 식별, 수행의무, 거래가격, 배분, 수익인식 시점의 핵심 분기를 엔진화한다.
3. **R15-3 — measurement and journal entry draft**
   거래가격 배분, 금융요소 조정, 재매입약정 처리 결과를 분개/측정 초안으로 만든다.
4. **R15-4 — review memo renderer**
   1115 판단 결과를 회계자문팀 검토메모 초안으로 렌더링한다.
5. **R15-5 — review pack integration**
   1115 결과를 기존 F-ACC review pack 표면에 맞춰 묶고 1109/1116과 비교 가능한 상태로 만든다.
6. **R15-6 — fixture regression + completion report**
   seed fixture 전체 완료율과 NeedsHumanReview 경계를 리포트로 남긴다.

## Close criteria

최소 close 기준은 R15-1~R15-6 완료다. 즉 1115도 1109/1116처럼 구조화 입력에서 판단, 분개/측정,
검토메모, review pack, 완료율 리포트까지 이어져야 한다.

## Boundary

`data/` 아래의 1115 workflow와 RAG trace는 비공개 seed다. 공개 코드에는 기준서 원문, 시험 문제 원문,
모범답안 텍스트를 넣지 않는다. fixture에는 엔진 검증에 필요한 구조화 사실과 기대 판단만 둔다.
