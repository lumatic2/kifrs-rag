# DG — Disclosure Generalization Plan

> Date: 2026-07-05
> Horizon: `f-acc-disclosure-generalization`

## 산문 요약

F-ACC review pack이 1116/1109/1115로 반복됐으므로, 다음은 B5 주석 작성 자동화 표면을 여러 기준서로
확장한다. 1116 disclosure pilot을 기준점으로 삼고, 1115/1109 산출물에서 disclosure candidate를 뽑아
공통 checklist schema를 만든다.

## Step tree

- [x] DG1 — disclosure surface inventory
  - verify: `docs/reports/2026-07-05-dg1-disclosure-surface-inventory.md`
- [x] DG2 — common disclosure checklist schema
  - verify: schema tests for common disclosure checklist
- [ ] DG3 — 1115 disclosure pilot
  - verify: 1115 review pack에서 disclosure draft skeleton 생성
- [ ] DG4 — 1109 disclosure pilot
  - verify: 1109 review pack에서 disclosure draft skeleton 생성
- [ ] DG5 — cross-domain disclosure report
  - verify: 1116/1115/1109 disclosure surface comparison report

## 결정 로그

- 결정: 주석 일반화는 판단 엔진을 새로 만들기보다, 기존 review pack output을 주석 checklist/source로 재사용한다.
- 결정: 실제 회사 주석 원문이나 DART 원문은 공개 fixture에 넣지 않는다.
