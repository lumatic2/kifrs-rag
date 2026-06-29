# P4C4 — 1113 공정가치 도메인 진입 설계

> 작성일: 2026-06-30
> ROADMAP goal: `phase4-content`
> Active milestone: `P4C4`

## 1. 목표

1113 공정가치 도메인은 KICPA 적용 부담이 높지만, 바로 DCF·옵션모델·시장데이터 수집으로 들어가면 범위가 커진다. P4C4의 첫 목표는 "공정가치가 무엇이고, 어떤 시장/투입변수/가치평가기법/서열체계로 판단하는가"를 RAG eval workflow로 고정하는 것이다.

## 2. 범위 결정

| 영역 | P4C4 포함 여부 | 이유 |
|---|---|---|
| 1113 본문 판단 | 포함 | 정의, 시장참여자, 유출가격, 최고 최선의 사용, 가치평가기법, 서열체계가 RAG로 검증 가능 |
| 숫자 모델 | 제한 포함 | 예제 입력이 주어진 단순 현재가치·서열체계 분류까지만 |
| 외부 시장데이터 | 제외 | 실시간 데이터/API 의존이 생기면 회계 판단보다 데이터 파이프라인 문제가 커짐 |
| 옵션모델 | 제외 | 별도 수학/파생상품 모델링 horizon 필요 |
| 1036 손상·1016 재평가 연결 | 후속 | 1113 core workflow가 안정된 뒤 cross-standard로 확장 |

## 3. 핵심 citation map

| 판단 | Primary citations |
|---|---|
| 공정가치 정의 | `1113-9`, `1113-24` |
| 시장 기반 측정 | `1113-2`, `1113-11` |
| 비금융자산 최고 최선의 사용 | `1113-27` |
| 가치평가기법 | `1113-61`, `1113-62`, `1113-67` |
| 공정가치 서열체계 | `1113-72`, `1113-76`, `1113-81`, `1113-86` |
| 공시 | `1113-91`, `1113-93` |

## 4. First workflow seed

산출물: `data/scenarios/1113_fair_value/WORKFLOW.md`

첫 seed는 특정 외부 가격을 가져오지 않고 다음 세 가지 가상 케이스로 구성한다.

1. 상장주식: 활성시장 동일자산 공시가격 → 수준 1 — 완료
2. 회사채: 동일자산 활성시장 가격은 없지만 관측 가능한 수익률 곡선·신용스프레드 사용 → 수준 2 — 완료
3. 비상장 지분 또는 현금창출자산: 관측 불가능한 장기 성장률/할인율/현금흐름 가정 사용 → 수준 3 — 완료

## 5. P4C4 DoD

- [x] 1113 범위 경계 결정
- [x] 핵심 citation map 작성
- [x] 1113 workflow seed 작성
- [x] 첫 scenario 1개를 `transaction.md`, `retrieval_trace.md`, `review_memo.md`로 구체화
- [x] user_note 후보 또는 parser metadata issue가 있으면 기록

## 6. 결과

- `data/scenarios/1113_fair_value/FV-01_level1_listed_equity/`: 활성시장 상장주식, 수준 1.
- `data/scenarios/1113_fair_value/FV-02_level2_corporate_bond/`: 관측 가능한 수익률·스프레드 기반 회사채, 수준 2.
- `data/scenarios/1113_fair_value/FV-03_level3_private_equity/`: 내부 DCF 가정 기반 비상장 지분, 수준 3.
- `data/scenarios/1113_fair_value/user_note_candidates.md`: 종가/수익률곡선/DCF 등 검색어를 1113 서열체계 문단으로 연결하는 후보.
- `scripts/seed_user_notes.py`: 위 후보 3건을 SQLite `user_note` seed로 승격.

## 7. 중단선

- 외부 시장데이터 조회 자동화는 P4C4에 포함하지 않는다.
- 옵션가격결정모형, Monte Carlo, DCF 엔진 구현은 별도 horizon 없이는 시작하지 않는다.
- 1113은 "어떤 값을 써야 하는가"보다 "어떤 관점과 투입변수 수준으로 측정해야 하는가"를 먼저 검증한다.
