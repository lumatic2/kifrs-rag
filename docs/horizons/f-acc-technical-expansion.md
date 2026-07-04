# F-ACC Technical Expansion Sequence

> Created: 2026-07-05
> Objective: `docs/OBJECTIVE.md`
> Source maps: `docs/practice-map/team-workflows.md`, `docs/practice-map/service-line-candidates.md`
> Purpose: 전체 자동화 후보를 service-line 기준 실행 순서로 고정한다.

## 왜 이 문서가 필요한가

회계법인 service-line 조사 결과 자동화 후보는 3개가 아니라 훨씬 많다. 그런데 `ROADMAP.md`는 현재
horizon 중심 상태판이라, 세션을 다시 열면 큰 순서가 잘 보이지 않는다. 이 문서는 F-ACC를 중심으로
앞으로 구현할 horizon sequence를 고정해, 매번 "다음 뭐 하지"를 새로 판단하지 않게 한다.

## North-star와의 연결

최상위 목표는 "회계사 업무를 AI로 어디까지 자동화할 수 있는가"를 실증하고, 회계법인에 소개 가능한
로컬 도구킷으로 만드는 것이다. F-ACC(Accounting Advisory / F-S support)는 현재 repo의 가장 강한
PoC 표면이다. 이유는 이 팀의 산출물이 검토메모, 분개, 주석 초안, 리뷰 checklist처럼 코드로 생성하고
검증할 수 있는 형태이기 때문이다.

## 구현 순서

| 순서 | Horizon | 주 업무 | 왜 이 순서인가 | 완료 증거 |
|---:|---|---|---|---|
| 1 | `f-acc-review-pack` | 1116 리스 review pack | 이미 1116 엔진과 주석 초안이 있어 제품 표면을 가장 빨리 만들 수 있었다 | RP1~RP4 완료 |
| 2 | `f-acc-1109-review-pack` | 1109 금융상품 review pack | 1116 pack 패턴이 다른 기준서에도 반복되는지 확인 | FR1~FR2 완료 |
| 3 | `f-acc-1115-revenue-engine` | 1115 수익인식 판단 엔진 | F-ACC 복잡 계약 판단 업무와 직접 연결되고, 새 도메인 확장 증거가 가장 크다 | R15 milestones |
| 4 | `f-acc-disclosure-generalization` | 기준서별 주석 checklist/초안/DART 대사 | 1116에서 실증한 B5 주석 작성 자동화를 여러 기준서로 확장 | disclosure coverage report |
| 5 | `f-acc-1109-hardening` | 1109 잔여 NeedsHumanReview hardening | 기존 6/10 자동화율을 높여 신뢰도를 개선 | completion-rate delta |
| 6 | `f-acc-financial-statement-draft` | 재무제표 본문 작성 지원 | F-S support 산출물로 확장하되, 표시/양식 자동화 성격이라 판단 엔진 뒤에 둔다 | F/S draft fixture |
| 7 | `f-audit-analytical-procedures` | 감사 분석적 절차 | F-AUD 보조 적용처. DART 공개 F/S로 검증 가능하지만 K-IFRS 판단 엔진보다는 뒤 | analytical procedure report |
| 8 | `product-packaging-poc` | CLI/demo/sample/README/피드백 질문지 | 기술 표면이 충분히 쌓인 뒤 법인 소개 가능한 도구킷으로 묶는다 | 10분 demo pack |

## 보류/이관

- Tax/C1~C6, D3 비상장 주식평가는 `tax-agent` 경계로 둔다.
- Deal/D2 가치평가, Risk/K-SOX, E2 사업비 정산은 제품 스토리는 있으나 내부자료 또는 별도 도메인
  의존이 커서 현 단계 주 실행 순서에서 제외한다.
- 공통 review pack schema 추출은 세 번째 표면(1115 또는 주석 대사) 이후로 보류한다.

## 현재 실행 포인터

현재 다음 실행은 `f-acc-1115-revenue-engine`이다. 이 horizon은 1115 수익 계약 판단을 구조화 입력,
결정 엔진, 분개/측정 초안, 검토메모, review pack까지 이어 붙인다.
