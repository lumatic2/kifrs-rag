# F-ACC Disclosure Generalization Horizon

> Created: 2026-07-05
> ROADMAP goal id: `f-acc-disclosure-generalization`
> Status: active
> Objective: `docs/OBJECTIVE.md`
> Sequence: `docs/horizons/f-acc-technical-expansion.md`

## Why now

1116, 1109, 1115는 판단·분개·검토메모·review pack 표면을 반복해 증명했다. 다음 F-ACC 병목은
B5 주석 작성이다. 1116에서는 주석 checklist/초안/DART 대사까지 이미 실증했으므로, 이제 이 패턴을
여러 기준서 도메인으로 일반화한다.

## Goal

기준서별 주석 요구사항을 구조화 checklist로 만들고, 사용 가능한 workflow output을 주석 초안과
대사 항목으로 연결한다.

## Milestone sequence

1. **DG1 — disclosure surface inventory**
   기존 1116 주석 산출물, 1109/1115 review pack output, practice-map B5 요구를 비교해 공통 disclosure
   surface를 정의한다.
2. **DG2 — common disclosure checklist schema**
   기준서별 주석 checklist item, source output, human review action을 표현하는 공통 schema를 만든다.
3. **DG3 — 1115 disclosure pilot**
   1115 수익인식 review pack에서 주석 후보 항목을 추출해 disclosure draft skeleton을 만든다.
4. **DG4 — 1109 disclosure pilot**
   1109 금융상품 review pack에서 분류·측정·위험 관련 주석 후보를 skeleton으로 만든다.
5. **DG5 — cross-domain disclosure report**
   1116/1115/1109 주석 surface의 자동화 가능성과 NeedsHumanReview 경계를 리포트로 남긴다.

## Boundary

주석 원문 예시는 공개 코드에 넣지 않는다. 공개 범위는 checklist schema, 후보 항목, renderer, 테스트용
invented fixture다. DART 원문/회사 자료가 필요한 대사는 별도 local-only 자료를 사용한다.
