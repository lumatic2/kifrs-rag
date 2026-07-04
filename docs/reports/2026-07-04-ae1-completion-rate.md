# AE1 — 1116 리스 엔진 이식 완료율 리포트

> Generated: 2026-07-04
> Objective 움직이는 축: 시나리오 완료율 (`docs/OBJECTIVE.md`)
> Horizon: `docs/horizons/automation-expansion.md` · Plan: `docs/plans/2026-07-04-ae1-1116-lease-engine.md`

## 완료율: 9/10 (90%)

"완료" = 구조화 거래 입력 → 식별 → 분류/면제 → 최초측정 → 후속측정 분개 → (변경 시)
재측정 headline → 검토메모까지 사람 개입·수정 없이 코드가 산출하고, headline 금액이 시나리오
기대값과 ±2원 이내로 일치. 100% 미달은 실패가 아니다 — 이번 milestone의 목표는 "측정 가능한
상태"이지 100% 통과가 아니다(docs/plans/2026-07-04-ae1-1116-lease-engine.md).

### 측정 방법론 (1109와 비교 시 유의)

- **headline 비교 + ±2원 tolerance**: 시나리오 문서 자체가 손계산 반올림 잔차를 명시한다
  ("반올림 ±1", "잔차 −2", "≈"). fixture의 상각표 셀들은 원 단위로 정확히 foot되지 않는다
  (예: scenario_01 표의 기말잔액은 이자·리스료와 ±1 어긋난다). 따라서 원 단위 완전일치가 아니라
  각 시나리오가 "산출 대상/핵심 답"으로 제시한 headline 금액을 ±2원 tolerance로 비교한다 —
  이는 데이터의 실제 해상도이지 느슨한 기준이 아니다(더 타이트하면 fixture 자체 모순으로 실패).
- **round-half-up**: 회계 관행(사사오입)을 `Decimal(ROUND_HALF_UP)`로 강제. Python 기본
  banker's rounding은 .5 케이스(유효이자 177,297.5·136,162.5 등)에서 fixture와 어긋난다.
- **판단값은 입력**: 리스제공자 금융/운용 분류, 변경 유형, 매수선택권 행사 확실성, 할인율·
  현가계수는 시나리오 제시값을 입력으로 받는다(WA1이 SPPI/사업모형 판단을 evidence로 받은 것과
  동일). 엔진은 판단 자체가 아니라 판단 이후의 결정론적 측정을 자동화한다.

## 자동화됨 (9)

| 시나리오 | 경로 | 대표 headline |
|---|---|---|
| scenario_01_simple_office_lease | 이용자 인식 | 리스부채/사용권자산 3,545,950 · 감가 886,488 |
| scenario_02_restoration_prepaid | 이용자 인식 | 사용권자산 4,107,300 · 복구충당부채 411,350 |
| scenario_03_short_low_value_exemption | 이용자 면제 | 케이스A 연 3,600,000 · 케이스B 연 480,000 |
| scenario_04_lessor_finance_to_operating | 제공자 금융→운용 | 리스순투자 3,238,171 · 변경손익 0 |
| scenario_05_lessor_op_to_finance | 제공자 운용→금융 | 리스채권 2,473,008 · 변경손실 (107,529) |
| scenario_06_lessor_finance_to_finance | 제공자 금융→금융 | 변경손실 (209,071) · 20x2 이자수익 282,350 |
| scenario_07_lessee_term_reassessment | 이용자 재평가 | 재측정 증가 1,605,697 · 재측정 사용권자산 3,421,197 |
| scenario_08_lessee_purchase_option | 이용자 인식 | 리스부채 3,710,490 · 내용연수 6년 감가 618,415 |
| scenario_10_lessee_modification_extend | 이용자 변경 | 20x3말 리스부채 3,312,116 · 사용권자산 3,026,561 |

## 사람 개입 필요 (AE1 core pipeline 밖) (1)

| 시나리오 | 사유 |
|---|---|
| scenario_09_lessee_modification_expand_shrink | 동시 확장+축소 변경 — [1116-46(a)] 축소분 PL 인식과 [1116-45]/[1116-46(b)] 재측정을 2차원으로 분해해야 하고, 단일-차원 변경(연장·재평가)과 달리 별도 결정 로직이 필요. 시나리오 문서 자체가 이 트랙 선택(분리 vs 통합)을 처음엔 오답으로 풀었다가 모범답안 대사로 정정한 판단 케이스 — 엔진이 트랙을 조용히 고르지 않고 사람 확인을 요구하는 것이 정직한 경계. |

## 1109(WA1) 대비 — 패턴 이식성

| | 1109 (WA1) | 1116 (AE1) |
|---|---|---|
| 완료율 | 6/10 | 9/10 |
| 사람 개입 | 4 (IFRIC19·SPPI재설정·재분류·외화) | 1 (동시 확장+축소 변경) |
| 재사용 | — | 9-모듈 구조·grounding·회귀 하네스 통째 복제 |

**엔진 패턴은 도메인을 넘어 이식된다** (구 workflow-automation horizon 닫는 기준 (a) 충족).
1116의 완료율이 1109보다 높은 것은 1116 시나리오 대부분이 결정론적 측정(현가·상각·감가)이고
판단 포인트(분류·변경유형)를 입력으로 받기 때문이다 — 1109는 SPPI/사업모형 외에 별도 기준서
로직(IFRIC19·1021)이 필요한 케이스가 더 많았다. 1116의 유일한 사람-개입 케이스가 "복잡해서"가
아니라 "트랙 선택이 단년 PL을 뒤집는 문서화된 판단"이라는 점은, 완료율 숫자보다 **어디서
자동화가 멈춰야 하는지**를 더 잘 보여준다.

## RGA1 grounding

`kifrs.workflows.kifrs1116.grounding`이 9건 자동화 경로의 모든 하드코딩 인용([1116-x], [1109-x])이
실제 DB 조항을 가리키는지 런타임 검증했고, 전부 통과했다. 인용이 깨지면 `NeedsHumanReview`로
자동 escalate된다(`tests/test_workflow_1116_grounding.py`의 negative 테스트로 검증 — optimistic
path 금지).

## 검증

- `python -m pytest tests/test_workflow_1116_regression.py -q` — 완료율 9/10 고정
- `python -m pytest tests/ -q` — 117 passed (기존 92 + AE1 25 비퇴행)
- `python scripts/quality_preflight.py --format text` — ok: True, public_safe: True

## 다음

- 자동화 9건은 회귀 테스트로 고정 — 향후 리팩토링이 숫자를 바꾸면 테스트가 먼저 실패한다.
- scenario_09(2차원 변경)은 신호가 반복되면 AE3(NeedsHumanReview 명시 인터페이스) 또는 별도
  2차원 변경 모듈 후보. 지금은 단일 케이스라 escalate로 충분.
- 커버리지 축: 실증 판정 2/33 → **3/33** (B3-확장 = 1116 완료율 실측, `docs/practice-map/taxonomy.md`).
