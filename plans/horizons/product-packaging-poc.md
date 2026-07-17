# Product Packaging PoC Horizon

> Created: 2026-07-05
> ROADMAP goal id: `product-packaging-poc`
> Status: active
> Objective: `docs/OBJECTIVE.md`
> Sequence: `docs/horizons/f-acc-technical-expansion.md`

## Why now

F-ACC review pack, 1115 engine, disclosure skeleton, F/S draft, F-AUD analytical procedures까지 제품 표면이
쌓였다. 이제 처음으로 회계법인에 소개 가능한 demo pack으로 묶는다.

## Goal

기준서 원문/DB/embedding을 배포하지 않는 로컬 도구킷 전제를 유지하면서, 10분 안에 "거래 입력 →
검토메모/분개/주석/F/S 표시 후보/감사 분석 메모" 흐름을 보여주는 PoC package를 만든다.

## Milestone sequence

1. **PK1 — demo scenario selection**
   1116, 1109, 1115, audit analytics 중 어떤 흐름을 10분 demo에 넣을지 고른다.
2. **PK2 — demo command surface**
   sample input을 받아 주요 output을 생성하는 로컬 command 또는 script를 만든다.
3. **PK3 — sample input/output bundle**
   공개 가능한 invented fixture와 generated output을 묶는다.
4. **PK4 — README/setup guide**
   protected K-IFRS assets는 사용자가 직접 인덱싱한다는 설치/운영 경계를 명시한다.
5. **PK5 — demo brief and feedback questionnaire**
   법인 소개용 10분 demo script와 회계사 피드백 질문지를 만든다.

## Boundary

- 기준서 원문, DB, embedding, dogfood 자료는 package에 포함하지 않는다.
- 외부 배포/릴리즈는 하지 않는다. 이번 horizon은 repo 내부 PoC package다.
- demo는 회계사 검토를 대체하지 않고 decision-prep draft를 보여준다.
