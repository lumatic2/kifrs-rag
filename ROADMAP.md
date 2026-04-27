# kifrs-rag ROADMAP

> K-IFRS 기준서 + AI 도구체인으로 회계사 실무의 상당 부분을 본인이 수행할 수 있는 개인용 시스템. 본인 PC 로컬 비공개 운영.

## 배경

K-IFRS 기준서를 프로그램적으로 조회할 공식 API/MCP가 부재. 빅4 사내 AI는 외부 비공개. 외부 공개는 KASB·IFRS Foundation 저작권 장벽으로 진입 불가. **저작권법 제30조 사적이용 복제·제35조의5 공정이용** 범위 안에서 본인 학습·실무·포트폴리오 시연용으로 비공개 운영.

## 포지셔닝

- 본인 PC 로컬에서만 동작. 외부 공개·배포·공유 없음
- 코드는 GitHub private. 공개 가능 산출물(아키텍처 글, 데모 영상, 평가 리포트)은 옵션 트랙
- `tax-agent` 레포 패턴 재사용 → 신규 개발 비용 최소화
- 외부 공개·협업은 **별도 후속 프로젝트**로 분리

## 야망 (CLAUDE.md 동기화)

회계사가 아닌 본인이 AI 도구체인으로 **회계사 수준의 결과물**(분개·검토 메모·분류 판단·주석 초안)을 낸다.

### 단계 정의

| 단계 | 목표 | 검증 기준 |
|---|---|---|
| **Phase 1** ✅ | 인프라 — 100 기준서 DB + MCP + /accounting 스킬 | dogfood 10건 통과 |
| **Phase 2 (현재)** | 시험 수준 — 회계사 2차 기출을 정확한 조항 인용 + 적용 해설로 푼다 | 2차 기출 5~10문항 본인 채점 정확도 80%+ |
| **Phase 3** | 실무 시나리오 1개 — 금융상품 분류·측정 (1109) | 신규 거래 입력 → 분류 판단 + 분개 + 검토 메모 자동 산출 |
| **Phase 4** | 시나리오 확장 + 누적 | 리스·수익·공정가치 시나리오 + user_note 축적 |

각 단계는 이전 단계 검증 후에만 진행. 단계 건너뛰기 금지.

## 성공기준 4축 (재정의)

| 축 | 기준 |
|---|---|
| **A. 실사용** | 본인이 회계 실무·학습에서 **주 3회 이상 자발 사용** (4주 연속) |
| **B. 시험 수준 정확도** | 회계사 2차 기출 5~10문항 본인 채점 정확도 **80%+** (조항 인용 정확 + 적용 해설 합당) |
| **C. 커버리지** | ✅ 완료 — 100 기준서 / 8,328 paragraphs |
| **D. 포트폴리오** | 보류 — 옵션 트랙. Phase 4 종료 후 재검토 |

---

## Phase 1 — PoC ✅ 완료 (2026-04-14)

인프라 구축. tax-agent 패턴 재사용 + KASB 일괄 다운로더 + 파서 + SQLite + FastMCP.

**최종 결과:**
- 100 기준서 (K-IFRS 63 + 일반기업회계기준 36 + special 1)
- **8,328 paragraphs** (2026-04-24 letter-suffix 616건 복구 포함)
- SQLite DB 29MB (`data/kifrs.db`) + paragraph_fts (trigram + LIKE fallback)
- FastMCP tools: `list_standards`, `get_paragraph`, `list_paragraphs`, `list_sections`, `search_lexical`, `get_context`, `reload_store`
- /accounting 스킬 (Claude Code 등록 완료) + dogfood 10건 의미있는 답 통과
- 0-paragraph 4건 전부 복구 (OCR + GAAP 정규식 추가)
- goldset 8문항 (Q001~Q008, DB 검증 통과)

상세 작업 이력은 git log + 기존 ROADMAP commit 참조.

---

## Phase 2 — 시험 수준 검증 (현재)

**목표**: 회계사 2차 기출을 본인이 /accounting 스킬로 풀어내는 데 정확도 80%+

### Dogfood 라운드 1 ✅ 완료 (2026-04-27)
- [x] 회계사 2차 기출 5문항 수집 (2024년 제59회 재무회계, namucpa 경유 금감원) → `data/dogfood/cpa2/`
- [x] 5문항 dogfood — `/accounting` 스킬로 풀이 + 본인 직관 채점 (학원 답안 잠금 → B 옵션)
- [x] 채점 결과 분석 — 검색 실패 5건 / UX 마찰 (답변 포맷 미스매치) / 인용 정확도 양호 (5/5~6/6)
- 결과 요약: `data/dogfood/cpa2/INDEX.md` Round 1 종합 결과 섹션 참조

### 검색 품질 개선 ✅ 완료 (2026-04-27)
- [x] **🔴 임베딩 인덱스** `kifrs/embed.py` — bge-m3 (1024d, 100 기준서 / 8,328 paragraphs / 31분 53초 인덱싱). SQLite BLOB 저장
- [x] **하이브리드 검색 (RRF)** — `search_hybrid` lexical FTS5 + semantic cosine. MCP tool 2개 추가 (`search_semantic`, `search_hybrid`)
- [x] **5건 검색 실패 키워드 재검증**: ✅ 3건 완벽 (환매약정→재매입약정, 내부창출 브랜드, 재구매) / △ 1건 부분 (선택형 주식기준보상) / ❌ 1건 (공매도 — 본문 부재 추정)
- [x] /accounting SKILL.md 업데이트 — search_hybrid 1순위 / allowed-tools 확장

### 잔여
- [ ] **🟡 [2순위] /accounting 시험 풀이 모드 분기** — 다단 sub-question + 계산 표 + 분개 코드블록 포맷 보강
- [ ] UX: `section_like` 부분 매칭, `get_paragraph_range`

### Dogfood 라운드 2 (hybrid 검색으로 재실행)
- [ ] kifrs MCP 서버 재시작 (Claude Code 재기동 필요)
- [ ] Q01~Q05 hybrid로 재풀이 → 검색 실패 수 감소 측정
- [ ] 본인 채점 — 조항 인용·풀이 정확도 변화
- [ ] 학원 모범답안 입수 후 산식 정밀 검증 (3순위)

### Phase 2 종료 조건
- 회계사 2차 기출 5~10문항 본인 채점 정확도 **80%+**
- 검색 recall 70%+ (임베딩 도입 시)
- 본인이 회계사 시험 공부에 주 3회 자발 사용 (A축 첫 검증)

---

## Phase 3 — 실무 시나리오 1개 (금융상품 분류·측정)

**목표**: 신규 거래 정보 입력 → 1109 분류 워크플로 자동 산출

### 워크플로 단계
- [ ] **거래 정보 입력 양식** — 채권/대여금/지분증권 공통 필드 (계약조건, 사업모형, 의도 등)
- [ ] **SPPI 테스트** — 1109.B4.1.7~ 적용. 통과/실패 + 사유
- [ ] **사업모형 평가** — 보유·매도·기타. 1109.B4.1.1~ 인용
- [ ] **분류 결정** — AC / FVOCI / FVPL
- [ ] **분개 자동 산출** — 최초 인식 + 후속 측정
- [ ] **검토 메모 자동 산출** — 결론 + 조항 인용 + 판단 근거

### Phase 3 종료 조건
- 5~10개 가상 거래 시나리오에 대해 자동 산출물 정확도 80%+ (본인 채점)
- 본인이 학습/실습에 실제 사용

---

## Phase 4 — 시나리오 확장 + 누적

**목표**: A축(주 3회 4주 자발 사용) + Personal AI Accountant 토대

- [ ] 리스(1116) 시나리오 — 신규 임차계약 → 식별 → 측정 → 분개
- [ ] 수익(1115) 시나리오 — 5단계 워크플로
- [ ] 공정가치(1113) 시나리오 — 측정 검토 메모 (KICPA 부담 1위)
- [ ] **user_note 활성화** — 본인 작성 해설 누적 (저작권 안전 창작물)
- [ ] **개정이력** (DB amendment) — 실사용 중 "이전 버전 보고 싶다" 마찰 발생 시 trigger
- [ ] **크로스레퍼런스** (DB cross_reference) — 실사용 중 "관련 조항 자동" 마찰 발생 시 trigger

### Phase 4 종료 조건
- A축 (주 3회 4주) 통과
- 시나리오 3-4개 자동화

---

## 보류 트랙 (옵션)

코드는 보존. 야망 굳어지거나 포트폴리오 욕구 생기면 부활.

- [ ] 평가 하네스 50문항 자동 채점 (`kifrs/eval/` 코드 보존됨)
- [ ] B축 baseline 비교 (kifrs-mcp vs naive PDF) — ANTHROPIC_API_KEY 필요
- [ ] D축 산출물 ① 아키텍처 블로그 글
- [ ] D축 산출물 ② 데모 영상 3-5분
- [ ] D축 산출물 ③ 평가 메트릭 리포트

---

## 작업 원칙

- **기준서 PDF·텍스트·임베딩·DB 덤프 절대 git commit 금지** (`.gitignore` 최상단)
- 회계사 2차 기출 dogfood 자료도 commit 금지 (`data/dogfood/`)
- 코드 레포는 **GitHub private**
- 동료·친구 공유 ❌ — 사적이용 범위 깨짐
- 외부 공개·협업 굳어지면 별도 프로젝트 `kifrs-public`으로 분리

## DB 테이블 채우기 일정

| 테이블 | 현재 | 시점 |
|---|---|---|
| `standard` | ✅ 100개 | Phase 1 완료 |
| `paragraph` | ✅ 8,328행 | Phase 1·2 완료 |
| `paragraph_fts` | ✅ trigram + LIKE | Phase 1 완료 |
| `embedding` (신규) | ❌ 미생성 | **Phase 2** — dogfood 결과 기반 trigger |
| `cross_reference` | 🟡 스키마만 | **Phase 4** — 실사용 마찰 trigger |
| `amendment` | 🟡 스키마만 | **Phase 4** — 실사용 마찰 trigger |
| `user_note` | 🟡 스키마만 | **Phase 4** — 본인 해설 누적 시작 |

---

## 이어서 할 일 (다음 세션 진입점)

**Phase 2 진행 중** — 임베딩 인프라 완료, Round 2 dogfood 진입 단계.

1. [x] CLAUDE.md / ROADMAP.md 야망 격상 (2026-04-27)
2. [x] 회계사 2차 기출 5문항 수집 (2024 제59회 재무회계)
3. [x] 5문항 dogfood Round 1 + 종합 분석 (2026-04-27)
4. [x] **임베딩 인프라 (1순위)** — bge-m3 / 8,328 인덱싱 / hybrid RRF (2026-04-27)
5. [x] /accounting SKILL.md 업데이트 (hybrid 1순위) (2026-04-27)
6. [ ] **kifrs MCP 서버 재기동** (Claude Code 재시작) → 새 도구 활성화
7. [ ] **Round 2 dogfood** — Q01~Q05 hybrid로 재실행, 검색 실패 감소 측정
8. [ ] [2순위] /accounting 시험 풀이 모드 분기 (계산 표·분개 포맷)
9. [ ] [3순위] 학원 모범답안 입수 + 산식 정밀 검증

---

## 메모

- KASB 메일 v3.4 초안은 보류. 외부 공개 단계 진입 시 재활용
- GIST 학부논문(Doyoon Song, 2025) 분석: KICPA 공식 협업 사례. 외부 개인 직접 진입 선례 0건 — 공백 자체가 향후 협업 카드
- **KICPA 조사 K-IFRS 적용 부담 순위**: 공정가치/손상/재평가 27.08% > 금융상품 14.58% > 리스 13.44% > 수익 13.33% > 연결 10.83%
  - Phase 3 첫 시나리오를 **금융상품(1109)** 으로 잡은 근거: ① DB 강점(556 paragraphs) ② 워크플로 결정론적(SPPI→사업모형→분류) ③ 골든셋 Q003·Q008 재활용
  - 1순위 공정가치는 RAG 외에 DCF·옵션모델·시장데이터까지 필요 → Phase 4에서 도전
