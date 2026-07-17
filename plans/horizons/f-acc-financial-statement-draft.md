# F-ACC Financial Statement Draft Horizon

> Created: 2026-07-05
> ROADMAP goal id: `f-acc-financial-statement-draft`
> Status: active
> Objective: `docs/OBJECTIVE.md`
> Sequence: `docs/horizons/f-acc-technical-expansion.md`

## Why now

F-ACC pack은 1116/1109/1115에서 판단, 분개, 검토메모, 주석 checklist까지 반복됐다. 다음 회계자문/F-S
support 산출물은 재무제표 본문/표시 draft다. 기준서 판단 엔진 결과를 F/S 표시와 본문 초안으로 연결한다.

## Goal

기존 review pack output을 이용해 재무제표 본문/표시 draft skeleton을 만든다.

## Milestone sequence

1. **FS1 — statement draft surface inventory**
   1109/1115/1116 pack output에서 재무상태표, 손익계산서, 주석 연결에 쓸 수 있는 field를 정리한다.
2. **FS2 — statement line schema**
   재무제표 line item, source pack, amount, presentation question을 표현하는 schema를 만든다.
3. **FS3 — 1109 statement draft pilot**
   1109 분류/분개 결과를 금융자산·손익/OCI 표시 skeleton으로 연결한다.
4. **FS4 — 1115 statement draft pilot**
   수익/계약부채/금융요소 표시 skeleton을 만든다.
5. **FS5 — F/S draft report**
   F/S draft surface의 자동화 가능성과 남은 사람 검토 경계를 리포트로 남긴다.

## Boundary

재무제표 전체 작성은 회사 TB, mapping table, 계정과목 정책이 필요하다. 이번 horizon은 전체 F/S 완성이 아니라
기준서 판단 엔진 output을 표시 skeleton으로 연결하는 PoC다.
