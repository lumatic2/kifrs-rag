# Plan: AE2 — B5 주석(공시) 초안 생성 파일럿 (1116 리스 주석)

> Objective: `docs/OBJECTIVE.md`
> Horizon: `docs/horizons/automation-expansion.md` (`automation-expansion`)
> Milestone: AE2 — B5 주석 초안 생성 파일럿
> Created: 2026-07-04
> 입력: PM3 후보 B5 (`docs/practice-map/candidates.md`), 사용자 확정(2026-07-04): DART 공개 주석 파싱 · 1116 리스 주석 도메인

## Scope boundary

**리스이용자 주석([1116-53~58])**으로 한정한다. AE1 리스 엔진의 산출물(사용권자산 감가상각비·
리스부채 이자비용·단기/소액 리스 비용·리스부채 만기분석·사용권자산 기말 장부금액)을 [1116-53]
10개 요구항목 + [1116-58] 만기분석 체크리스트에 매핑해 **markdown 리스 주석 초안**을 생성하고,
DART 공개 상장사 리스 주석(≥3개)과 대사해 **"요구항목 커버리지 %"**를 측정한다.

파일럿 엔티티 = AE1 이용자 시나리오(S1/S2/S7/S8/S10)를 한 회사의 리스 포트폴리오로 묶어 금액을
집계 → 그 집계로 [1116-53] 주석을 생성한다(단일 리스가 아니라 기간 집계 공시라는 주석의 본질
반영).

Out of scope (이유):
- **리스제공자 주석([1116-89~97])** — AE1이 이용자 케이스를 더 많이 다뤘고 상장사 대부분이
  이용자 주석을 공시. 제공자는 후속 milestone.
- **주석의 회사 특수 서술**(리스 정책 문단, 판단·추정 서술) — 초안까지만(Objective 정합).
  요구항목의 *정량 표*와 *구조*를 채우는 데 집중, 자유서술은 사람.
- **DART 전체 파싱 파이프라인 자동화** — 파일럿은 리스 주석 섹션 확보에 한정(전체 사업보고서
  파싱 아님).

## Step tree (leaf test 적용 — 시그니처 수준, 상세 AC는 §C에서)

- [ ] **Step 1 — 이용자 공시 요구사항 체크리스트 스키마** (`kifrs/workflows/kifrs1116/disclosure.py`)
  [1116-53] 10개 요구항목(⑴감가상각비 ⑵이자비용 ⑶단기리스비용 ⑷소액자산비용 ⑸변동리스료
  ⑹사용권자산 관련 손익 ⑺리스 총 현금유출 ⑻사용권자산 추가 ⑼판매후리스 손익 ⑽유형별 기말
  장부금액) + [1116-58] 만기분석을 구조화 체크리스트로. 각 항목에 근거 조항([1116-x]) 인용.
  (verify: 체크리스트 로드 + 항목 수·조항 인용 단위 테스트, grounding 통과)

- [ ] **Step 2 — AE1 엔진 산출물 → 체크리스트 항목 매핑** (`disclosure.py`)
  AE1 이용자 시나리오 outcome(사용권자산·감가·리스부채·이자·만기·단기저가 비용)을 [1116-53]
  항목에 매핑. 엔진이 산출하는 항목 / 산출 못 하는 항목(변동리스료·판매후리스 등 — 해당 없음
  표시)을 구분. (verify: 포트폴리오 집계 금액이 개별 시나리오 합과 일치하는 단위 테스트)

- [ ] **Step 3 — 주석 초안 생성기** (`disclosure.py`)
  체크리스트 + 매핑된 엔진 산출 → markdown 리스 주석 draft(정량 표 + 만기분석 표 + 근거 인용).
  (verify: 생성 draft가 [1116-53] 요구항목 헤더 + 만기분석 표 포함, 조항 인용 형식)

- [ ] **Step 4 — DART 공개 리스 주석 확보** (`scripts/fetch_dart_lease_notes.py`, gitignored 산출)
  상장사 ≥3개의 리스 주석 섹션을 DART에서 확보. **DART 접근 방식은 결정 로그 참조(API key
  BLOCKED-until-issued 또는 keyless 공시뷰어 HTML).** 확보한 주석 원문은 `data/`(gitignored)에만
  저장 — 커밋 금지. (verify: 3개 회사 리스 주석 섹션 텍스트 확보, 요구항목 태깅)

- [ ] **Step 5 — 대사 로직: 요구항목 커버리지 %** (`disclosure.py`)
  생성 초안이 채운 요구항목 수 / [1116-53]+[58] 총 요구항목 수 = 커버리지 %. DART 실제 주석과
  교차: "실제 상장사도 공시하는 항목인가"로 요구항목의 실무 유효성 확인(빈 요구항목 필터).
  (verify: 커버리지 % 산출 + DART 대사 결과 단위 테스트)

- [ ] **Step 6 (integration) — 회귀 테스트 + grounding + 커버리지 리포트** (`tests/test_1116_disclosure.py`)
  체크리스트·매핑·초안·커버리지를 회귀로 고정, grounding negative 케이스 포함. 커버리지 %
  리포트(`docs/reports/2026-07-04-ae2-disclosure-coverage.md`) 작성 — 커버리지 축 3/33→4/33 갱신.
  (verify: `python -m pytest tests/test_1116_disclosure.py -q` + 리포트 + `pytest tests/` 비퇴행)

## 결정 로그

- **DART 접근 방식 (Step 4)** — 사용자 확정: DART 공개 주석 파싱. 세부는 Step 4 진입 시 결정:
  ① DART Open API(opendart.fss.or.kr, **무료 API key 필요 — BLOCKED-until-issued**) 또는
  ② 공시뷰어 HTML fetch(keyless). Step 1~3은 DART 무관하게 선행하므로 key 발급 전에도 착수
  가능. API key가 필요해지면 그 값은 env로만(커밋·로그 노출 금지), PRD/plan에 필요 사실만 기록.
- **이용자 주석 한정** (제공자 후속) — AE1 이용자 커버리지 + 상장사 공시 빈도 근거. 새 트레이드
  오프 아님(스코프 축소).
- **커버리지 % 정의** — [1116-53](10항목)+[58](만기분석) 요구항목 중 엔진이 자동 산출·채운 항목
  비율. DART 대사는 "실제로 공시되는 항목인가" 교차검증(요구항목 유효성). "실제 주석과 문구
  일치율"이 아니라 "요구항목 충족률" — 자유서술은 범위 밖이므로.
- **파일럿 엔티티 = AE1 시나리오 포트폴리오** — 단일 리스가 아니라 기간 집계 공시가 주석의 본질.
  자작 회사 없이 이미 검증된 AE1 산출물을 재사용해 착수 비용 최소화.
- **보호 데이터 경계** — DART 주석 원문은 공개 자료지만 `data/`(gitignored)에만 저장, 커밋은
  코드·체크리스트·커버리지 리포트(수치)만. 기준서 원문 인용은 최소.
- 이 외 예상되는 사용자 소유 결정: DART API key 발급 여부(Step 4에서 실제 필요 시 요청) 외에는
  없음 — 실행 중 새 리스크·스코프 변경 없는 한 무중단 진행.

## Integration verification (milestone close)

- `python -m pytest tests/test_1116_disclosure.py -q` — 체크리스트·매핑·초안·커버리지 회귀
- `python -m pytest tests/ -q` — 기존 117개 비퇴행
- `python scripts/quality_preflight.py --format text` — ok: True, public_safe: True
- 커버리지 리포트(`docs/reports/2026-07-04-ae2-disclosure-coverage.md`) — 요구항목 커버리지 % +
  DART 대사 결과. 수치가 낮아도 무방(측정 가능 상태가 목표).
- 커버리지 축 갱신: `docs/practice-map/taxonomy.md` B5 실증 판정 반영 (3/33 → 4/33)
- 실패 모드 확인 1건 이상: 엔진이 산출 못 하는 요구항목(변동리스료·판매후리스)을 "미해당/사람
  필요"로 정직하게 표시하는지 negative 테스트 (optimistic-path 금지 — 커버리지 100% 위장 방지)

## 위계 (cascade 백링크)

- Objective: `docs/OBJECTIVE.md` (커버리지 축 신규 개척)
- Horizon: `docs/horizons/automation-expansion.md` — AE2는 2번째 milestone
- 이전 milestone: AE1(`docs/plans/2026-07-04-ae1-1116-lease-engine.md`, 완료 9/10) — 엔진 산출물 재사용
