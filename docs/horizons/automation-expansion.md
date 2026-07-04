# 자동화 확장 (Automation Expansion) Horizon

> Created: 2026-07-04
> ROADMAP goal id: `automation-expansion`
> Status: active
> Objective: `docs/OBJECTIVE.md`
> 입력: `docs/horizons/practice-map.md` Close 판정 + `docs/practice-map/candidates.md` PM3 추천

## Why now

practice-map horizon이 2026-07-04 조건부 close됐다 — 33 task 지도와 전수 판정, 그리고 다음
자동화 대상 추천(1116 엔진 이식 먼저, 주석 초안 다음)이 나왔다. 지도는 있는데 아직 지도가
고른 업무를 실제로 엔진화한 적이 없다: 커버리지 축은 실증 2/33(6%), 완료율 축은 1109 단일
도메인(6/10)에 머물러 있다. 이 horizon이 PM3의 선정 결과를 처음으로 실행에 옮겨 두 축을
실제로 움직인다 — Objective 단계 분해의 4단계("자동화 확장 → 프로덕트 패키징") 진입이다.

paused `workflow-automation` horizon의 WA2(2번째 도메인 이식)는 AE1과 사실상 동일하므로 이
horizon으로 흡수하고, workflow-automation은 closed 처리한다(2026-07-04 사용자 결정). WA3
(NeedsHumanReview 명시 인터페이스)는 이 horizon의 Next Candidate로 함께 이관한다.

## Goal

PM3가 실무 가치 기준으로 고른 업무 2개를 엔진화한다:
① 1116 리스 결정 엔진 이식으로 **완료율 축을 2-도메인 벡터**(1109 + 1116)로 만들고 — "엔진
패턴이 도메인을 넘어 이식되는가"를 검증한다(구 workflow-automation 닫는 기준 (a)).
② 주석(공시) 초안 생성 엔진으로 **커버리지 축을 실증 4/33**으로 확장한다 — 법인 AI 공백
지대(판단 본질 task)의 첫 신규 개척.

## Milestone candidates (2~5, horizon-run continuation용)

1. **AE1 — 1116 리스 결정 엔진 이식** (first, this planning round)
   WA1 패턴 그대로 복제: 구조화 거래 입력 → 식별 → 분류/면제 → 최초측정 → 후속측정 →
   변경/재평가 → 검토메모, `kifrs/workflows/kifrs1116/` 신설 + RGA1 grounding 레이어 +
   회귀 하네스. fixture 10개 완비(`data/scenarios/1116_lease/scenario_01~10`) → 착수 비용
   최소. 1116은 재평가·변경 트리거가 1109보다 판단적이라 NeedsHumanReview 비중이 클 수
   있음 — 그것도 유효한 측정으로 취급(WA1 6/10 전례). 구 WA2 흡수.
2. **AE2 — B5 주석(공시) 초안 생성 파일럿** (candidate, AE1 뒤 §B0.5 Beat 3로 DoD 확정)
   도메인 1개(1116 리스 주석)로 시작: 공시 요구사항 문단(우리 DB) → 체크리스트 엔진 →
   DART 공개 주석과 대사해 "요구항목 커버리지 %" 측정. 신규 task 개척(커버리지 3→4/33).
   리스크: DART 주석 파싱·요구사항→체크항목 변환 정확도 — 신규 인프라 필요하므로 AE1
   완료 후 별도 계획 라운드에서 범위 확정.
3. **AE3 — NeedsHumanReview 명시 인터페이스** (candidate, signal-triggered — 구 WA3 이관)
   AE1/AE2 회귀에서 사람-개입 케이스가 반복 실패 모드로 확인되면, "needs human judgment"
   출력 형태를 MCP/스킬로 노출할지 설계. 신호 없으면 착수하지 않는다.

## Close criteria

AE1(10개 fixture 회귀 + 완료율 2번째 도메인 측정치 기록) + AE2(주석 도메인 1개 엔진 +
DART 대사 측정치 기록)가 닫히면 horizon 핵심이 닫힌다. AE3는 신호 종속 — 없이도 close 가능.
close 시 커버리지 축 실증 측정을 4/33으로 갱신하고 Objective 임팩트를 기록한다.

## 후속 horizon 후보 (이 horizon이 끝나면)

- **프로덕트 패키징** — 설치 가능한 도구킷 정비 + 데모 자료 + 현업 피드백 (Objective 성공
  모습의 중간 관문). PM2(현업 검증)를 이 시점 재개 검토.
