# PRD — F-ACC review pack

> Created: 2026-07-04
> Horizon: `f-acc-review-pack`
> Source decision: `docs/practice-map/service-line-candidates.md`

## Problem

현재 `kifrs-rag`는 1109/1116 판단 엔진과 1116 주석 초안을 갖고 있지만, 회계법인 회계자문팀이 실제로
받아볼 수 있는 산출물 단위로 묶여 있지는 않다. 그래서 "엔진이 된다"는 증거는 있으나 "이 팀의
이 업무를 줄인다"는 제품 설명이 약하다.

## User

1차 사용자는 회계법인의 Accounting Advisory / Financial Statement support 팀이다. 보조 사용자는
감사팀의 회계이슈 검토 담당자다.

## Product Shape

리스 계약 조건과 지급 스케줄을 입력하면 다음을 한 번에 산출하는 로컬 workpaper pack을 만든다.

- 리스 식별 및 분류 판단 요약
- 최초/후속 측정 계산 요약
- 조정분개 초안
- K-IFRS 1116 검토메모 초안
- 1116 리스 주석 초안
- NeedsHumanReview 항목과 리뷰 checklist

## Non-goals

- 최종 회계 판단, 감사의견, 서명 책임을 대체하지 않는다.
- 기준서 원문·DB·임베딩·dogfood 자료를 공개 산출물에 포함하지 않는다.
- 세무 판단은 `tax-agent`로 분리한다.
- 독립 웹앱/배포 패키징은 이 horizon의 목표가 아니다.

## Success Criteria

- 기존 1116 fixture 10개 중 가능한 케이스에서 review pack markdown/json이 생성된다.
- pack 안에 검토메모, 분개, 주석, 리뷰 checklist가 같은 run id로 연결된다.
- 기존 1116 회귀 테스트와 disclosure 테스트가 깨지지 않는다.
- 산출물이 "회계자문팀 workpaper 초안"으로 설명 가능하다.

## Decision

다음 구현 우선순위는 `1115 수익 엔진`이 아니라 `1116 F-ACC review pack`이다. 이유는 새 도메인을
늘리기보다 이미 검증된 1116 엔진과 주석 초안을 회계법인 산출물 단위로 묶는 것이 PoC 설명력이 더
높기 때문이다.
