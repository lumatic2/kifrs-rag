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
| **C. 커버리지** | 수업·실무 빈출 Top 5 기준서 완전 인덱싱: **1115 수익, 1116 리스, 1109 금융상품, 1001 재무제표 표시, 1019 종업원급여** |
| **D. 포트폴리오 산출물** | 공개 가능 3종 완성: ① 아키텍처 블로그 글 ② 데모 영상 3-5분 ③ 평가 메트릭 리포트 |

## Phase 분해

### Phase 1 — PoC (단일 기준서)

목표: 기준서 1개로 파이프라인 전체(파싱→저장→MCP 조회) 검증

- [x] 사전 작업: `tax-agent` 레포 코드 리뷰, 재사용 가능 모듈 식별 (2026-04-14)
  - **재사용 후보**: `parse_exam_papers.py` (계층 파서 구조), `tax_store.py` (SQLite bootstrap), `download_exam_papers.py` (다운로더 구조), `exam_eval.py` (Phase 2 평가 하네스 베이스)
  - **재작성 필요**: 조·항·호 정규식 (기준서 문단 번호 체계는 세법 판례집과 다름)
  - **신규 작성**: MCP 서버 (tax-agent에 없음)
- [ ] 프로젝트 스캐폴드: `pyproject.toml`, `.gitignore`(data/, *.db, *.pdf 최상단 제외), `kifrs/` 패키지 초기화
- [ ] **K-IFRS 1115호 (수익)** PDF KASB 사이트에서 수동 다운로드 → 구조 샘플링 (조항 체계·문단 번호 형식 확인)
- [ ] PDF → 조·항·호 계층 JSON 파싱 (`pdfplumber`/`PyMuPDF` fallback + 조항 정규식, tax-agent 파서 구조 포팅)
- [ ] SQLite 스키마 설계: `standard / article / paragraph / clause / cross_reference / amendment`
- [ ] FastMCP 기반 MCP 서버 — tools: `get_article`, `search_lexical`
- [ ] Claude Code에 등록 → 본인 질문 5개로 동작 확인
- [ ] **B축 마이크로 검증**: 같은 5개 질문을 NotebookLM에도 던져 정확도 비교
- **Phase 1 종료 조건**: B축 5건 비교에서 본인 시스템 우위 ≥ 3건

### Phase 2 — Top 5 커버리지 + 하이브리드 검색 + 크로스레퍼런스

목표: C축 달성 + B축 본격 평가

- [ ] 나머지 4개 기준서(1116, 1109, 1001, 1019) PDF 확보 + 파싱
- [ ] 임베딩 인덱스 추가 (sentence-transformers 한국어 모델 또는 OpenAI text-embedding-3-small)
- [ ] 하이브리드 검색 구현: 키워드(SQLite FTS5) + 시맨틱(임베딩) 점수 결합
- [ ] **크로스레퍼런스 그래프**: 조항 본문에서 "제X조" 패턴 추출 → `cross_reference` 테이블 채움
- [ ] MCP tools 확장: `search_hybrid`, `get_referenced_articles`, `get_referencing_articles`
- [ ] **B축 평가셋 50문항 작성**: 본인이 회계 수업·실무에서 실제 부딪힌 질문 + 기준서별 골드 답안(인용 조항 번호) 라벨링
- [ ] 평가 하네스 작성: 본인 시스템 vs naive PDF 자동 비교 스크립트 (tax-agent `exam_eval.py` 베이스)
- **Phase 2 종료 조건**: C축 완료(Top 5 인덱싱) + B축 평가에서 우위 20%p 이상

### Phase 3 — 실사용 안정화 + 포트폴리오 패키지

목표: A축 + D축 달성

- [ ] **개정이력**: 각 조항의 개정일·이전 버전 추적 (`amendment` 테이블 채움)
- [ ] **해설 레이어**: 본인 작성 요약·해설 별도 테이블에 추가 (저작권 안전한 창작물)
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

## 이어서 할 일 (다음 세션 진입점)

**Phase 1 다음 체크박스**: 프로젝트 스캐폴드(`pyproject.toml`, `.gitignore`, `kifrs/` 패키지) 생성 → KASB 1115호 PDF 수동 다운로드 및 구조 샘플링.
