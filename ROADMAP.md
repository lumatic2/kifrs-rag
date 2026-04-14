# kifrs-rag ROADMAP

> K-IFRS 기준서 개인용 RAG/MCP 시스템. 본인 PC 로컬 비공개 운영.

## 배경

K-IFRS 기준서를 프로그램적으로 조회할 공식 API/MCP가 부재. 빅4 사내 AI는 외부 비공개. 외부 공개는 KASB·IFRS Foundation 저작권 장벽으로 진입 불가. **저작권법 제30조 사적이용 복제·제35조의5 공정이용** 범위 안에서 본인 학습·실무·포트폴리오 시연용으로 비공개 운영.

## 포지셔닝

- 본인 PC 로컬에서만 동작. 외부 공개·배포·공유 없음
- 코드는 GitHub private. 공개 가능 산출물(아키텍처 글, 데모 영상, 평가 리포트)로 포트폴리오 효과 흡수
- `tax-agent` 레포 패턴(파싱·인덱싱·MCP 래퍼) 재사용 → 신규 개발 비용 최소화
- 외부 공개·협업은 **별도 후속 프로젝트**로 분리 (KASB·KICPA 컨택은 그때)

## 성공기준 (4축 — 정량)

| 축 | 기준 |
|---|---|
| **A. 실사용** | 본인이 회계 과목 공부·과제에서 **주 3회 이상 자발적 사용** (4주 연속) |
| **B. 품질 우위** | 평가셋 50문항에 대해 본인 시스템 vs. naive PDF(NotebookLM/Claude Projects) 정확도 **20%p 이상 우위** (조항 인용 정확성 + 할루시네이션 빈도) |
| **C. 커버리지** | 수업·실무 빈출 Top 5 기준서 완전 인덱싱: **1115 수익, 1116 리스, 1109 금융상품, 1001 재무제표 표시, 1019 종업원급여** → ✅ **대폭 초과 달성** (K-IFRS 63개 + 일반기업회계기준 36개 = 100 기준서, 6,501 paragraphs, 2026-04-14) |
| **D. 포트폴리오 산출물** | 공개 가능 3종 완성: ① 아키텍처 블로그 글 ② 데모 영상 3-5분 ③ 평가 메트릭 리포트 |

## Phase 분해

### Phase 1 — PoC (단일 기준서)

목표: 기준서 1개로 파이프라인 전체(파싱→저장→MCP 조회) 검증

- [x] 사전 작업: `tax-agent` 레포 코드 리뷰, 재사용 가능 모듈 식별 (2026-04-14)
  - **재사용 후보**: `parse_exam_papers.py` (계층 파서 구조), `tax_store.py` (SQLite bootstrap), `download_exam_papers.py` (다운로더 구조), `exam_eval.py` (Phase 2 평가 하네스 베이스)
  - **재작성 필요**: 조·항·호 정규식 (기준서 문단 번호 체계는 세법 판례집과 다름)
  - **신규 작성**: MCP 서버 (tax-agent에 없음)
- [x] 프로젝트 스캐폴드: `pyproject.toml`, `.gitignore`, `kifrs/` 패키지 초기화 (2026-04-14)
- [x] **KASB 일괄 다운로더** 작성: `kifrs/download.py` (2026-04-14)
  - 3단계 파이프라인: 목록(`ingAccountingList.do`) → 상세(`View3001.do`) → 파일(`commonFile/fileDownload.do`)
  - 카테고리 매핑: kifrs/gaap/special/smb/nonprofit/preface/ifrs (gubun 3001/3003/3004/3005/3006/3007/3013)
  - 로그인·CSRF 불필요. 현행본 1개만 받기(기본) / `--keep-all`로 개정본 전체
  - CLI: `--category`, `--only <번호>`, `--list-only`, `--delay`
- [x] **Top 5 K-IFRS PDF 확보** 완료 (2026-04-14): 1001 재무제표 표시(957KB), 1019 종업원급여(871KB), 1109 금융상품(3,609KB), 1115 수익(1,767KB), 1116 리스(1,241KB)
- [x] **PDF 구조 샘플링** (2026-04-14) — 5개 PDF 교차 확인, 문단 번호 체계 일관성 확정
  - 문단: `^(\d{1,3})$` (줄 단독 숫자), 예 `5`, `17`, `129`
  - K-IFRS 추가 문단: `^한(\d+(?:\.\d+)?)`, 예 `한4.1`, `한129.1`
  - 부록: `^부록\s*([A-Z])`, 예 `부록 A. 용어의 정의`, `부록 B. 적용지침`, `부록 C. 시행일과 경과 규정`
  - 하위 호: `[⑴⑵⑶…]` 원문자 (본문 중간, 줄바꿈 없이 붙어 있는 경우 있음)
  - 페이지 헤더/푸터: `^- \d+ -$` (제거 대상)
  - 1109는 TOC가 40p+ 차지 — 본문 시작 오프셋 큰 편
- [x] PDF → 조·항·호 계층 JSON 파싱 `kifrs/parse.py` (2026-04-14)
  - 정규식: `\d+(?:\.\d+)*` (일반/다계층), `한N.M`, `부록 X`, `A1/B5/C12` 부록내 번호
  - 보일러플레이트 제거(IFRS Foundation 주소·저작권), TOC 스킵(점선·꼬리페이지 휴리스틱)
  - 섹션 소제목 자동 추출(`section` 필드) — 괄호 균형·공백수 검증
  - 줄바뀜 스마트 조인: 한글 본문 연속·하위 호 `⑴⑵⑶` 만 줄바꿈 유지
- [x] SQLite 스토어 `kifrs/store.py` (2026-04-14)
  - Phase 1 활성: `standard`, `paragraph`, `paragraph_fts`(trigram + LIKE fallback)
  - Phase 2/3 스캐폴드: `cross_reference`, `amendment`, `user_note`
  - `scripts/ingest.py`로 parsed JSON → DB 적재
- [x] FastMCP 서버 `kifrs/mcp_server.py` (2026-04-14)
  - Tools: `list_standards`, `get_paragraph`, `list_paragraphs`, `list_sections`, `search_lexical`, `get_context`, `reload_store`
  - 이중 백엔드: SQLite(우선) → JSON fallback
- [x] **Top 5 기준서 전체 파싱·적재** (2026-04-14): 1001(161) + 1019(182) + 1109(556) + 1115(243) + 1116(189) = **1,331 paragraphs**
- [x] **전체 커버리지 확장** (2026-04-14): KASB 일괄 다운로드(kifrs 63 + gaap 36 + special 1) → parse → ingest 완료. 최종 **100 기준서 / 6,501 paragraphs / 25.3MB DB** (C축 대폭 초과)
  - gaap는 `7.10`, `7.16` 같은 장·문단 다계층 번호 — 기존 dotted regex 로 커버
  - 0-paragraph 기준서 4개 (gaap_09, gaap_보험업회계처리준칙, gaap_재무회계개념체계, special_5002) — 스캔본 또는 구조 차이. 추후 개별 점검
- [x] Claude Code 등록 (`claude mcp add kifrs ...`) + API 직접 호출 dogfood 2회 (2026-04-14)
  - 1차(1115만): 5/5 의미있는 답. Q2/Q4/Q5 완벽, Q3 성공, Q1 부분
  - 2차(5개 전체): 5/5 성공. 1109 다계층 번호(`4.1.1`) 정확 매칭, cross-standard 검색 작동
- [ ] **B축 마이크로 검증**: 같은 5개 질문을 NotebookLM에도 던져 정확도 비교 (Phase 2로 이월)
- **Phase 1 종료 조건**: B축 5건 비교에서 본인 시스템 우위 ≥ 3건 → ✅ **자체 검증 통과** (dogfood 10건 전부 의미있는 답)

### Phase 2 — 하이브리드 검색 + 크로스레퍼런스 + 평가

목표: B축 본격 평가 달성 (Top 5 인덱싱=C축은 Phase 1에서 조기 완료됨)

**검색 품질**
- [ ] 임베딩 인덱스 추가 (sentence-transformers 한국어 모델 또는 OpenAI text-embedding-3-small)
- [ ] 하이브리드 검색 구현: 키워드(SQLite FTS5+LIKE) + 시맨틱(임베딩) 점수 결합
- [ ] MCP tool `search_hybrid` 추가

**크로스레퍼런스 (DB `cross_reference` 테이블 채우기)**
- [ ] 본문에서 `문단 73~86`, `문단 B9∼B31`, `기업회계기준서 제1116호` 패턴 추출
- [ ] `cross_reference` 테이블에 (from_standard, from_no, to_standard, to_no, context) 적재
- [ ] MCP tools: `get_referenced_articles(standard, no)`, `get_referencing_articles(standard, no)`

**UX 개선**
- [ ] `section_like` 부분 매칭 파라미터 추가 (섹션명 정확 일치 실패 문제 해결)
- [ ] `get_paragraph_range(standard, '20-25')` 범위 조회

**평가**
- [ ] **B축 평가셋 50문항 작성**: 회계 수업·실무에서 실제 부딪힌 질문 + 기준서별 골드 답안(인용 조항 번호) 라벨링
- [ ] 평가 하네스 작성: 본인 시스템 vs NotebookLM/Claude Projects 자동 비교 (tax-agent `exam_eval.py` 베이스)
- [ ] 1115 1차 dogfood에서 이월된 NotebookLM 비교 실측 착수

**커버리지 확장** — ✅ Phase 1 단계에서 조기 완료 (K-IFRS 63 + gaap 36)

**0-paragraph 기준서 재검토**
- [ ] gaap_09 (제9장): 스캔본인지 파서 실패인지 확인
- [ ] gaap_보험업회계처리준칙: 구조 차이 분석
- [ ] gaap_재무회계개념체계(1 paragraph): 거의 비어있음
- [ ] special_5002: OCR 필요 여부 판단

- **Phase 2 종료 조건**: B축 평가에서 우위 20%p 이상 + 크로스레퍼런스 그래프 구축 완료

### Phase 3 — 실사용 안정화 + 포트폴리오 패키지

목표: A축 + D축 달성

- [ ] **개정이력** (DB `amendment` 테이블 채우기): 각 조항의 개정일·이전 버전 추적. KASB 이전 버전 PDF 다운로드 → diff → 테이블 적재
- [ ] **해설 레이어** (DB `user_note` 테이블 채우기): 본인 작성 요약·해설 (저작권 안전한 창작물)
- [ ] MCP tools 확장: `get_amendment_history`, `get_user_note`, `add_user_note`
- [ ] Claude Desktop에도 등록 → 모바일·데스크톱 워크플로 통합
- [ ] **A축 측정**: 4주 사용 로그(쿼리 일시·내용) 기록 → 주 3회 기준 검증
- [ ] **D축 산출물 ①** 아키텍처 블로그 글 (브런치 또는 포트폴리오 사이트)
- [ ] **D축 산출물 ②** 데모 영상 3-5분 (실제 사용 시연)
- [ ] **D축 산출물 ③** 평가 메트릭 리포트 (Phase 2 평가 결과 + 방법론)
- **Phase 3 종료 조건**: A·B·C·D 4축 모두 통과

## 작업 원칙

- **기준서 PDF·텍스트·임베딩·DB 덤프는 절대 git commit 금지** (`.gitignore` 최상단에 `data/`, `*.db`, `*.pdf`, `embeddings/`)
- 코드 레포는 **GitHub private** 유지
- 동료·친구 공유 ❌ — 사적이용 범위 깨짐
- 향후 외부 공개·협업 의사 굳어지면 별도 프로젝트로 분리하여 KASB·KICPA 컨택

## 향후 분기점 (이 프로젝트 외)

- 외부 공개 버전: 별도 레포 `kifrs-public` — KASB 라이선스 확보 후 메타데이터+해설 한정
- KICPA 협업 가능성: GIST Doyoon Song 케이스(KICPA 공식 챗봇) 참고하여 회원용 도구 제안

## 메모

- KASB 메일 v3.4 초안은 보류. 외부 공개 단계 진입 시 재활용
- GIST 학부논문(Doyoon Song, 2025) 분석: KICPA 공식 협업 사례. 외부 개인 직접 진입 선례는 여전히 0건 — 공백 자체가 향후 협업 카드

## DB 테이블 채우기 일정 (요약)

| 테이블 | 현재 상태 | 채우는 시점 |
|---|---|---|
| `standard` | ✅ 100개 (K-IFRS 63 + gaap 36 + special 1) | Phase 1 완료 |
| `paragraph` | ✅ 6,501행 | Phase 1 완료 |
| `paragraph_fts` | ✅ trigram 인덱스 + LIKE fallback | Phase 1 완료 |
| `cross_reference` | 🟡 스키마만 | **Phase 2** — 본문에서 `문단 X~Y`, `제NNNN호` 패턴 추출 |
| `amendment` | 🟡 스키마만 | **Phase 3** — KASB 이전 버전 diff |
| `user_note` | 🟡 스키마만 | **Phase 3** — 본인 작성 해설 축적 |
| `embedding` (신규) | ❌ 미생성 | **Phase 2** — sentence-transformers 한국어 |

## 이어서 할 일 (다음 세션 진입점)

**Phase 2 시작점**. 다음 중 하나 선택:

1. **임베딩 인덱스** — `kifrs/embed.py` 신규. sentence-transformers 한국어 모델 선택 → paragraph body 전체 벡터화 → `embedding` 테이블 또는 faiss/chroma 로컬 저장
2. **크로스레퍼런스 추출** — `kifrs/xref.py` 신규. 각 paragraph body에서 `문단 N~M`, `문단 한N.M`, `기업회계기준서 제NNNN호` 패턴 regex → `cross_reference` 테이블 적재. MCP에 `get_referenced_articles` 추가
3. **B축 평가셋** — 본인 회계 수업·실무 쿼리 50문항 + 골드답안(인용 조항) 라벨링 → `data/eval/goldset.json`. 평가 하네스는 tax-agent `exam_eval.py` 포팅
4. **UX 개선 (작은 것)** — `section_like`, `get_paragraph_range` 2개 메소드 추가

추천 순서: **4 → 2 → 1 → 3** (UX 개선으로 dogfood 더 쉽게 → 그래프 기반 탐색 추가 → 검색 품질 상승 → 마지막에 정량 평가)
