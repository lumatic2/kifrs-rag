# F-ACC Review Pack Horizon

> Created: 2026-07-04
> ROADMAP goal id: `f-acc-review-pack`
> Status: active
> Objective: `docs/OBJECTIVE.md`
> Upstream decision: `docs/practice-map/service-line-candidates.md`

## Why now

`firm-service-map`은 다음 구현 후보를 F-ACC(Accounting Advisory / F-S support)로 좁혔다. 지금 부족한
것은 설치 패키징이 아니라, 회계자문팀이 실제로 받을 수 있는 산출물 단위의 제품성이다.

1116 리스 엔진은 이미 10개 fixture 중 9개를 완료했고, 1116 주석 초안도 11개 요구항목 중 8개를
자동화했다. 이제 이 조각들을 "리스 계약 검토 workpaper pack"으로 묶어야 법인 PoC에서 설명 가능한
제품 표면이 된다.

## Goal

리스 계약 조건을 입력하면 회계자문팀용 검토메모, 계산/분개, 주석 초안, 리뷰 checklist,
NeedsHumanReview 항목을 하나의 review pack으로 산출한다.

## Milestone candidates

1. **RP1 — 1116 review pack contract + renderer**
   기존 1116 runner, review memo, disclosure output을 하나의 structured object와 markdown 산출물로
   묶는다. 새 판단 로직은 만들지 않고 composition layer로 시작한다.
2. **RP2 — fixture regression + sample pack**
   기존 1116 fixture에서 review pack을 생성하고, 대표 sample markdown/json을 `docs/reports/`에 남긴다.
3. **RP3 — NeedsHumanReview checklist hardening**
   자동화가 멈춰야 하는 조건을 review checklist로 명시하고, 회계사가 리뷰할 쟁점을 누락 없이 보이게 한다.
4. **RP4 — PoC demo brief**
   회계법인 Accounting Advisory 팀에 설명 가능한 1~2페이지 데모 브리프를 만든다.

## Close criteria

RP1~RP2가 닫히면 핵심 기능은 닫힌다: review pack contract와 fixture 기반 sample이 있어야 한다.
RP3~RP4는 제품 설명력과 현업 피드백 준비를 높이는 후속 milestone이다.

## Objective impact

이 horizon은 Objective의 "결정준비 초안까지 자동"을 회계법인 산출물 단위로 끌어올린다. 성공하면
지표는 단순 완료율이 아니라 "F-ACC workpaper pack 생성 가능 여부"로 확장된다.
