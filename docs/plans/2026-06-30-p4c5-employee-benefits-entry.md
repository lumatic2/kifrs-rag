# P4C5 — 1019 확정급여 도메인 승격

> 작성일: 2026-06-30
> ROADMAP goal: `phase4-content`
> Active milestone: `P4C5`

## 1. 목표

q06에 이미 축적된 1019 확정급여·1037 구조조정 판단을 실무 scenario workflow로 승격한다. 목적은 문제풀이 반복이 아니라, 확정급여 사건이 발생했을 때 RAG가 정산손익, 과거근무원가, 순이자, 재측정요소, 자산인식상한, 구조조정충당부채 분기를 안정적으로 찾아오는지 검증하는 것이다.

## 2. 범위 결정

| 영역 | P4C5 포함 여부 | 이유 |
|---|---|---|
| 1019 확정급여 정산 | 포함 | q06 핵심. 정산손익과 정산 전후 순확정급여부채 계산이 검색/판단 모두 중요 |
| 1019 제도개정 | 포함 | 과거근무원가 즉시 PL과 재측정요소 OCI 분리가 핵심 |
| 1019 순이자·자산인식상한 | 포함 | q06 실패 지점. user_note exam_convention과 연결 |
| 1037 구조조정충당부채 | 포함 | q06 물음2. 1019 해고급여와 구조조정 충당부채 해석 분기 검증 |
| 보험수리 모델·외부 actuarial 엔진 | 제외 | P4C5는 주어진 입력으로 기준서 판단을 검증한다 |

## 3. 핵심 citation map

| 판단 | Primary citations |
|---|---|
| 과거근무원가 | `1019-103` |
| 정산손익 | `1019-109`, `1019-110` |
| 자산인식상한 적용 | `1019-101A` |
| 순확정급여부채 순이자 | `1019-123`, `1019-124` |
| 재측정요소 OCI | `1019-127`, `1019-128` |
| 구조조정 직접비용 | `1037-80`, `1037-81` |
| 미래영업손실 제외 | `1037-82` |
| 자산처분이익 제외 | `1037-83` |
| 충당부채 현재가치 unwind | `1037-60`, `1037-61` |

## 4. Seed scenarios

1. `EB-01_defined_benefit_settlement_amendment`: q06 물음1을 확정급여 정산·제도개정·재측정 scenario로 전환.
2. `EB-02_restructuring_termination_benefits`: q06 물음2를 구조조정충당부채와 해고급여 해석 분기 scenario로 전환.

## 5. P4C5 DoD

- [x] 1019/1037 범위 경계 결정
- [x] 핵심 citation map DB/PDF 검증
- [x] 1019 workflow seed 작성
- [x] scenario 2개를 `transaction.md`, `retrieval_trace.md`, `review_memo.md`로 구체화
- [x] 기존 user_note가 P4C5 failure mode를 커버하는지 확인
- [x] answer-time user_note 조회 도구 추가

## 6. 결과

- `data/scenarios/1019_employee_benefits/WORKFLOW.md`: 1019/1037 workflow seed.
- `data/scenarios/1019_employee_benefits/EB-01_defined_benefit_settlement_amendment/`: q06 물음1 승격.
- `data/scenarios/1019_employee_benefits/EB-02_restructuring_termination_benefits/`: q06 물음2 승격.
- `kifrs.store.get_user_notes()`: `exam_convention`/`interpretation_note`를 답변 작성 전 checklist로 조회.
- `kifrs.mcp_server.get_user_notes`: MCP tool 노출.

## 7. Verification

- Citation validation: 14 unique 1019/1037 paragraphs, 0 missing, 0 mismatch.
- Scenario file check: EB-01 and EB-02 both have `transaction.md`, `retrieval_trace.md`, `review_memo.md`.
- user_note idempotency: `existing rows: 13`, `new rows: 0`.
- answer-time note smoke:
  - `중간 정산 순이자 확정급여` -> `1019-123 exam_convention`
  - `자산인식상한 적용 시점` -> `1019-101A exam_convention`
  - `해고급여 vs 구조조정 충당부채` -> `1019-103 interpretation_note`

## 8. 중단선

- 보험수리 평가 엔진, 최소적립요구 상세 모델, 제도별 actuarial API는 시작하지 않는다.
- q06 모범답안과 다른 해석은 무리하게 하나로 합치지 않고, 시험 관습과 기준서 일관성 분기로 기록한다.
