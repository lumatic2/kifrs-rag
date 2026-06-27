# kifrs-rag

> K-IFRS 기준서 + AI 도구체인을 활용해 **회계사 실무의 상당 부분을 본인이 수행할 수 있는 개인용 시스템**. 본인 PC 로컬에서만 동작. 외부 공개·배포·공유 없음.

## 야망

회계사가 아닌 본인이 Claude Code + kifrs MCP + /accounting 스킬을 활용해 **회계사 수준의 결과물**(분개·검토 메모·분류 판단·주석 초안)을 낸다.

### 4단계 분해

1. **시험 수준** — 회계사 2차 기출을 정확한 조항 인용 + 적용 해설로 풀 수 있다 — **현재 진행 단계**
2. **실무 시나리오 1개 자동화** — 금융상품 분류·측정 워크플로 (거래 입력 → 판단 → 분개 → 검토 메모)
3. **시나리오 확장** — 리스, 수익, 공정가치, 연결 등
4. **누적** — 본인 해설·사례가 누적된 Personal AI Accountant

각 단계는 **이전 단계가 검증된 후에만** 다음 단계로 진행. 단계 건너뛰기 금지.

## 배경 및 포지셔닝

K-IFRS 기준서를 프로그램적으로 조회할 공식 API/MCP가 부재. 빅4 사내 AI는 외부 비공개. 외부 공개는 KASB·IFRS Foundation 저작권 장벽으로 진입 불가. **저작권법 제30조(사적이용 복제)·제35조의5(공정이용)** 범위 안에서 본인 학습·실무·포트폴리오 시연용으로 비공개 운영.

- 본인 PC 로컬에서만 동작
- 코드는 GitHub **private** 유지
- `tax-agent` 레포 파싱·저장 패턴 재사용 (신규 개발 비용 최소화)
- 외부 공개·협업은 별도 후속 프로젝트(`kifrs-public`)로 분리

## 기술 스택

- Python 3.11+ (uv 관리)
- PDF 파싱: `pdfplumber` + `PyMuPDF` (fallback)
- 스토어: SQLite (FTS5 trigram + LIKE fallback). **임베딩 인덱스는 Phase 2 dogfood 결과 기반 trigger**
- MCP 서버: `FastMCP` (Python)
- 임베딩(예정): sentence-transformers 한국어 모델 또는 OpenAI text-embedding-3-small
- 답변 LLM: Claude (Claude Code + kifrs MCP + /accounting 스킬)

## 프로젝트 구조 (현재)

```
kifrs-rag/
├── CLAUDE.md                    # 이 파일
├── ROADMAP.md                   # 4단계 야망 + Phase 진행 상태
├── pyproject.toml
├── .gitignore                   # data/, *.db, *.pdf, embeddings/ 최상단 제외
├── data/                        # PDF·파싱 JSON·DB·dogfood 자료 (git 제외)
│   ├── standards/{kifrs,gaap,special,parsed}/   # 100 기준서 PDF + JSON
│   ├── kifrs.db                                  # SQLite DB (8,328 paragraphs)
│   ├── eval/                                     # goldset, 평가 결과
│   └── dogfood/cpa2/                             # 회계사 2차 기출 dogfood
├── kifrs/                       # 메인 패키지
│   ├── download.py              # KASB PDF 다운로더
│   ├── parse.py                 # 조·항·호 계층 파서
│   ├── store.py                 # SQLite 스토어
│   ├── mcp_server.py            # FastMCP 서버
│   └── eval/                    # 평가 하네스 (코드 보존, 옵션 트랙)
└── scripts/
    └── ingest.py                # download → parse → store 파이프라인
```

## 작업 방식

- **단계별 진행** — 4단계 야망 중 한 단계 검증된 뒤에만 다음 단계
- 새 기능 → 계획 먼저, 구현 나중
- tax-agent 재사용 모듈은 ROADMAP.md Phase 1 참조

## 금지 사항 (저작권·보안)

- **기준서 PDF·텍스트·임베딩·DB 덤프는 절대 git commit 금지** (`.gitignore` 최상단)
- **회계사 2차 기출 dogfood 문항도 commit 금지** (저작권 — `data/dogfood/`는 .gitignore 대상)
- 동료·친구 공유 ❌ (사적이용 범위 깨짐)
- 외부 웹에 PDF 원문·파싱 결과·DB·dogfood 자료 업로드 ❌
- 공개 가능 산출물은 **아키텍처 설명·평가 메트릭·데모 영상**만 (원문 인용 최소화)

## 세션 시작 규칙

- `ROADMAP.md` 먼저 읽고 **현재 단계** + 다음 체크박스 확인
- /accounting 스킬은 이미 등록됨 (`mcp__kifrs__*` 통해 즉시 사용 가능)
- tax-agent 참조 시 `~/projects/tax-agent/` 직접 열람 (sibling 경로)

## 현재 상태 (2026-04-28 기준)

**Phase 2 검색 인프라 완성** — 임베딩 + 하이브리드 검색 + dogfood Round 2까지.

- DB: 100 기준서 / 8,328 paragraphs (SQLite + FTS5 trigram)
- 임베딩: bge-m3 (1024d, 100% 인덱싱), **GPU 인코딩** (RTX 5090 cu128, 2026-06-27 전환 — 한계 #4 참조)
- MCP tools (8): list_standards, get_paragraph, list_paragraphs, list_sections, search_lexical, **search_semantic**, **search_hybrid**, get_context, reload_store
- /accounting 스킬: search_hybrid 1순위 사용. dogfood Round 1+2 검증 완료
- 검색 recall: lexical 60% → hybrid 80% (Phase 2 목표 70%+ 초과)

## 알려진 한계 (dogfood 2 라운드에서 식별)

다음 단계 결정 시 참고:

1. **본문 부재 키워드는 매칭 불가** — 시험 답안 표현이 본문에 어휘로 없으면 임베딩으로도 매칭 안 됨. 예: Q05 "공매도"는 1109에 직접 표현 없음. 우회 — `user_note` 테이블에 "시험 표현 ↔ 본문 표현" 매핑 누적 (Phase 4 작업 일부 당겨오기 권장)

2. **DB 외 도메인** — 한국 상법(자본거래 차손 우선상계, 무상증자 재원, 결산배당 미지급금 인식 시점)은 K-IFRS DB에 없음. Q04 풀이에서 본인 지식으로 채움. 빈도 낮으면 보류, 잦으면 별도 인덱싱 결정 필요

3. **다단 답안 포맷 미스매치** ✅ 해소 (2026-04-28) — SKILL.md §3 `(고정)` → `가치는 고정, 형태는 질문에 맞춘다`로 재구조화. 분기 모드 추가 대신 포맷 자체 완화 → 5 질문 유형 매핑 표 (기본형/시험 다단/cross-standard 비교/워크플로/단답). Round 3 mini 검증: Q01 자료2(계산형) + Q03 (물음 4)(서술형) 두 다른 형태에서 새 가이드가 자연스럽게 작동. 본인 수동 정렬 불필요

4. **CPU 인덱싱 부담** ✅ 해소 (2026-06-27) — Smart App Control은 이미 OFF(레지스트리 state=0) 상태였고, 원인은 단지 CPU 전용 torch 휠(`2.11.0+cpu`)이었음. `uv pip install torch --index-url .../cu128`로 교체 → `2.11.0+cu128`, RTX 5090(sm_120) 인식. 인코딩 ~24배(77→1863 texts/s), 재인덱싱 32분→~1분, per-query 리랭킹 0.44s. sentence-transformers가 CUDA 자동 사용(코드 변경 불필요). 되돌리려면 `+cpu` 휠 재설치

5. **모범답안 부재 → 정밀 채점 불가** — 회계사 2차 재무회계 학원 가답안은 회원 잠금. 본인 직관 채점만 가능 → "5문제 모두 부분 통과"라는 정성 판정에 그침. B축(80%+ 정확도) 정량 검증은 학원 자료 입수 후로 미뤄짐

6. **MCP stdio 통신 fragility** ✅ 핵심 해소 (2026-06-27) — 무거운 ML 라이브러리 + MCP stdio + 동시성에서 두 종류의 문제가 겹쳐 세션이 끊겼다. 정확한 진단:
   - **(a) C-확장 import 데드락 (진짜 원인 / search_reranked 영구 hang)** — warmup 을 **백그라운드 데몬 스레드**에서 돌리며 거기서 `sentence_transformers→sklearn→scipy.special` C 확장을 **처음 import** → CPython import-lock 교착(scipy#13985 / pybind11#1952 / sklearn#29145). warmup 이 `_model_lock` 을 쥔 채 멈춰 tool 호출까지 락 대기로 같이 hang. **해결: `embed.py:eager_import()` 를 `mcp_server.main()` 의 *메인 스레드*에서 `mcp.run()` 앞에 호출**(무거운 import 를 메인 스레드에서 한 번 끝내 sys.modules 적재 → 이후 스레드 import 는 캐시 적중). 핸드셰이크는 import 시간(~5초)만큼만 늦어지며 타임아웃 한참 이내. 가중치 로딩(느림)은 그대로 warmup 데몬 스레드. **무거운 ML import 는 절대 백그라운드 스레드에서 처음 하지 말 것.**
   - **(b) 터미널 garbage `[I`·`[555;..M` ≠ stdout 오염** — 창 포커스 전환·마우스 hover 시 쏟아지던 깨진 출력은 **터미널 마우스/포커스 리포팅 모드** escape 시퀀스로, **알려진 Claude Code(Windows+VS Code 터미널) 버그**(claude-code#10375·#23581, kilocode#6191). (a) 의 hang 이 세션을 블로킹한 게 주 트리거였고 이제 해소. cosmetic — 깨진 탭은 닫고 새로 열면 모드 리셋. `/terminal-setup`(gpuAcceleration off)·CC 업데이트 권장.
   - **오답 기록(되돌림)**: tqdm progress bar 가설(`predict(show_progress_bar=False)` 만 남김 — 무해), `TOKENIZERS_PARALLELISM` 가설, 그리고 `contextlib.redirect_stdout(sys.stderr)` 가드 — 전역 stdout 을 백그라운드 스레드가 돌려 JSON-RPC 응답이 stderr 로 새 **오히려 hang 유발 → 전부 revert**. 동시성 stdio 서버에서 전역 stdout 리다이렉트 금지.
