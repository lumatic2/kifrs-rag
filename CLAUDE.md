# kifrs-rag

> 가상 회계법인 AX 프로젝트(`~/projects/ai-accounting-firm`)의 **K-IFRS 지식 엔진** — 고품질 검색(RAG)과 결정준비 초안(분류판단·분개·검토메모) 산출을 담당한다 (2026-07-12 재정렬 — 비전 전체는 ai-accounting-firm, 상세·결정 이력은 `CLAUDE.md` 「북극성」 절). 새 horizon은 ai-accounting-firm 사용처 결함(issue-back) 기준으로만 연다. 공개 레포에는 코드·아키텍처·평가 하네스만 두고, 기준서 원문·파싱 DB·임베딩·dogfood 자료는 로컬에서만 보관한다.

## 북극성 — 사용자 소유, 승인 없이 수정 금지

> 이 절은 **사용자 소유**다. 에이전트는 문구 후보를 제안하고, 대화에서 확정 문구를 되읽어 **명시 승인을 받은 뒤에만** 그대로 기록한다. 승인 전 자율 수정 금지. 갱신은 **방향 자체가 바뀔 때만** — Milestone 완료는 여기를 바꾸지 않는다.
> 2026-07-23 하네스 재조립(C4)으로 구 OBJECTIVE 문서를 이 절로 흡수했다. 계획 계층이 Objective→Horizon→Milestone→Step 4단에서 **2계층**(이 문서 = 방향+규칙 / 작업 단위 계획서)으로 줄었다.

### 북극성

**가상 회계법인 AX 프로젝트(`~/projects/ai-accounting-firm`)의 K-IFRS 지식 엔진으로서, 실무자 단위 AX
실험이 요구하는 수준의 고품질·고신뢰 검색과 결정준비 초안 산출을 제공한다.**

"회계사 업무를 AI로 어디까지 자동화할 수 있는가"라는 출발 질문과 그 답의 공개 시각화(웹사이트),
법인 모델링, AX 실험은 2026-07-12부터 umbrella 레포 `ai-accounting-firm`의 Objective가 담당한다. 이 레포는
그 시스템의 K-IFRS 축을 맡는다: 기준서 검색(RAG), 결정 엔진(1109/1116 등), review pack 어댑터.
**결정준비 초안**(분류판단·분개·검토메모)까지 자동 산출하되, 최종 검토·서명·법적 책임은 항상
사람에게 남는다(`/accounting` 스킬의 "의사결정을 대신하지 마라" 규칙 불변).

### 성공 모습 (관측 가능한 최종 상태)

**ai-accounting-firm의 실무자 단위 AX 사례들이 이 엔진을 실소비하며, 사용처에서 드러난 결함이
issue-back → 수리 루프로 닫히는 상태** (2026-07-12 재정의).

중간 관문:
1. ai-accounting-firm 첫 실무자 AX(H4)가 kifrs MCP를 실제 입력으로 통과하고, 결함 목록이 이 레포 backlog로 돌아온다.
2. 그 결함 기준으로 retriever promotion(defer 상태)·user_note 확장 등 품질 결정이 재판단된다.
3. 여러 팀/업무의 AX가 반복 소비해도 품질·성능 회귀가 없다.

### 움직이는 축 (현재 → 목표, 측정법)

**축 1 — 업무 지도 커버리지** (신설, 2026-07-04): 회계사 실무 업무 taxonomy 중 자동화 실험이
닿아 "가능/조건부/불가" 판정이 붙은 업무의 비율. 현재 위치: 지도 자체가 없음(0). 첫 목표는
지도 작성 + 기존 자산(1109 엔진 등)의 위치 표기.

**축 2 — 시나리오 완료율** (기존 유지): 도메인별 결정 엔진이 사람 개입 없이 분류판단+분개+
검토메모를 끝까지 산출하는 비율. 현재 위치: 1109 = 6/10(60%), 나머지 도메인 = 엔진 없음(문서만).

축 1이 "어디를 자동화할가"를 고르고, 축 2가 "골라진 곳이 실제로 되는가"를 잰다.

### 긴 arc (지나온 phase → 갈 phase)

- 인프라 → 시험 수준 → 문서 기반 시나리오 → 엔진 hardening → 결정 엔진·RAG 최적화 →
  업무 지도·서비스라인 지도 → F-ACC 기술 확장 → Accounting Intelligence Expansion.
- phase 별 산출물·완료 상태 표는 `docs/BACKLOG.md` 가 소유한다. 현재 horizon 은 `ROADMAP.md` 가 가리킨다.

## 야망 (SoT: OBJECTIVE.md)

현재 법인 AI는 리서치·자료정리 수준 — 이 프로덕트의 차별점은 **결정준비 초안**(분류판단·분개·검토메모)까지 자동 산출. 최종 검토·서명·법적 책임은 항상 사람. 저작권 제약상 "파이프라인은 공유, 데이터는 사용자가 직접 인덱싱" 구조 고정. 성공 모습: 법인 소개/PoC 성사. 세무는 sibling `tax-agent` 담당.

### 단계 분해 (이력 + 현재)

1. **시험 수준** — 2차 기출 정확 인용 + 적용 해설 ✅ (누적 86%)
2. **실무 시나리오 자동화** — 1109 결정 엔진, 완료율 6/10 ✅
3. **업무 지도 / 회계법인 service-line 지도** — 회계사 업무 taxonomy + 회계법인 팀별 workflow + 자동화 가능성 매핑 ✅
4. **F-ACC review pack 구현 → 품질/근거/데모 반복 → 법인 소개** — 회계자문팀 산출물 단위 workpaper pack, 운영 증거, 데모 리허설

각 단계는 **이전 단계가 검증된 후에만** 다음 단계로 진행. 단계 건너뛰기 금지.

### Firm Service Map 빠른 위치

회계법인 조직/팀별 업무 맥락을 다시 물으면 아래 순서로 답한다.

1. `docs/horizons/firm-service-map.md` — 왜 회계법인 service-line 지도를 만들었는지, FM1~FM4의 전체 맥락
2. `docs/practice-map/company-map.md` — 감사, 회계자문/F-S support, 세무, Deal/FAS, Risk/K-SOX, Consulting/ESG/Forensic 등 회계법인 팀 구조
3. `docs/practice-map/team-workflows.md` — 팀별 workflow: 자료수집 → 판단 → 계산/대사 → 문서화 → 리뷰/커뮤니케이션
4. `docs/practice-map/service-line-candidates.md` — AI가 어디에 들어가면 효과가 큰지와 다음 구현 후보

현재 결론: 다음 구현은 **F-ACC(Accounting Advisory / F-S support) review pack**이다. 즉 1116 리스 계약을 입력하면 검토메모, 계산/분개, 주석 초안, 사람 검토 필요 항목을 묶어 회계자문팀 workpaper pack으로 내는 방향이다. 감사팀은 보조 적용처, 세무/D3는 `tax-agent`, Deal/Risk는 내부자료 의존 때문에 후순위다.

## 배경 및 포지셔닝

K-IFRS 기준서를 프로그램적으로 조회할 공식 API/MCP가 부재. 빅4 사내 AI는 외부 비공개. 기준서 원문·파싱 텍스트·DB·임베딩·dogfood 자료는 KASB·IFRS Foundation 저작권 장벽 때문에 공개하지 않는다. 공개 범위는 코드, 아키텍처 설명, 평가 메트릭, 데모/운영 문서로 제한한다.

- 본인 PC 로컬에서만 동작
- 기준서 PDF·파싱 텍스트·DB·임베딩·dogfood 자료는 git 제외
- `tax-agent` 레포 파싱·저장 패턴 재사용 (신규 개발 비용 최소화)
- 외부 공개·협업 시에도 원문 데이터와 기출 자료는 별도 배포하지 않음

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
│   ├── kifrs.db                                  # SQLite DB (17,896 paragraphs)
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

- DB: 100 기준서 / 17,899 paragraphs (SQLite + FTS5 trigram — 2026-07-12 IB2 BC/DO/IN 세분화 + DR2 수정목록 26-1 갱신). KASB 최신성은 `check_drift`(MCP)·`python -m kifrs.drift`로 감시, 개정 감지 시 `--update <id>` 단위 갱신
- 임베딩: bge-m3 (1024d, 17,899 문단 100% 인덱싱), **GPU 인코딩** (RTX 5090 cu128, 2026-06-27 전환 — 한계 #4 참조)
- MCP tools (8): list_standards, get_paragraph, list_paragraphs, list_sections, search_lexical, **search_semantic**, **search_hybrid**, get_context, reload_store
- /accounting 스킬: search_hybrid 1순위 사용. dogfood Round 1+2 검증 완료
- 검색 recall: lexical 60% → hybrid 80% (Phase 2 목표 70%+ 초과)

## 알려진 한계 (dogfood 2 라운드에서 식별)

다음 단계 결정 시 참고:

1. **본문 부재 키워드는 매칭 불가** — 시험 답안 표현이 본문에 어휘로 없으면 임베딩으로도 매칭 안 됨. 예: Q05 "공매도"는 1109에 직접 표현 없음. 우회 — `user_note` 테이블에 "시험 표현 ↔ 본문 표현" 매핑 누적 (Phase 4 작업 일부 당겨오기 권장)

2. **DB 외 도메인** — 한국 상법(자본거래 차손 우선상계, 무상증자 재원, 결산배당 미지급금 인식 시점)은 K-IFRS DB에 없음. Q04 풀이에서 본인 지식으로 채움. 빈도 낮으면 보류, 잦으면 별도 인덱싱 결정 필요

3. **다단 답안 포맷 미스매치** ✅ 해소 (2026-04-28) — SKILL.md §3 `(고정)` → `가치는 고정, 형태는 질문에 맞춘다`로 재구조화. 분기 모드 추가 대신 포맷 자체 완화 → 5 질문 유형 매핑 표 (기본형/시험 다단/cross-standard 비교/워크플로/단답). Round 3 mini 검증: Q01 자료2(계산형) + Q03 (물음 4)(서술형) 두 다른 형태에서 새 가이드가 자연스럽게 작동. 본인 수동 정렬 불필요

4. **CPU 인덱싱 부담** ✅ 해소 (2026-06-27) — Smart App Control은 이미 OFF(레지스트리 state=0) 상태였고, 원인은 단지 CPU 전용 torch 휠(`2.11.0+cpu`)이었음. `uv pip install torch --index-url .../cu128`로 교체 → `2.11.0+cu128`, RTX 5090(sm_120) 인식. 인코딩 ~24배(77→1863 texts/s), 재인덱싱 32분→~1분, per-query 리랭킹 0.44s. sentence-transformers가 CUDA 자동 사용(코드 변경 불필요). 되돌리려면 `+cpu` 휠 재설치
   - **재발 함정 (2026-07-12)**: GPU torch는 **`.venv`에만** 있다 — 임베딩/eval/리랭킹 커맨드는 반드시 `.venv/Scripts/python`으로 실행할 것. bare `python`은 시스템 Python 3.12(`torch +cpu`)라서 조용히 CPU로 돈다 (증상: embed build 수십 분, reranked eval 10분+ 타임아웃).

5. **모범답안 부재 → 정밀 채점 불가** — 회계사 2차 재무회계 학원 가답안은 회원 잠금. 본인 직관 채점만 가능 → "5문제 모두 부분 통과"라는 정성 판정에 그침. B축(80%+ 정확도) 정량 검증은 학원 자료 입수 후로 미뤄짐

6. **MCP stdio 통신 fragility** ✅ 핵심 해소 (2026-06-27) — 무거운 ML 라이브러리 + MCP stdio + 동시성에서 두 종류의 문제가 겹쳐 세션이 끊겼다. 정확한 진단:
   - **(a) C-확장 import 데드락 (진짜 원인 / search_reranked 영구 hang)** — warmup 을 **백그라운드 데몬 스레드**에서 돌리며 거기서 `sentence_transformers→sklearn→scipy.special` C 확장을 **처음 import** → CPython import-lock 교착(scipy#13985 / pybind11#1952 / sklearn#29145). warmup 이 `_model_lock` 을 쥔 채 멈춰 tool 호출까지 락 대기로 같이 hang. **해결: `embed.py:eager_import()` 를 `mcp_server.main()` 의 *메인 스레드*에서 `mcp.run()` 앞에 호출**(무거운 import 를 메인 스레드에서 한 번 끝내 sys.modules 적재 → 이후 스레드 import 는 캐시 적중). 핸드셰이크는 import 시간(~5초)만큼만 늦어지며 타임아웃 한참 이내. 가중치 로딩(느림)은 그대로 warmup 데몬 스레드. **무거운 ML import 는 절대 백그라운드 스레드에서 처음 하지 말 것.**
   - **(b) 터미널 garbage `[I`·`[555;..M` ≠ stdout 오염** — 창 포커스 전환·마우스 hover 시 쏟아지던 깨진 출력은 **터미널 마우스/포커스 리포팅 모드** escape 시퀀스로, **알려진 Claude Code(Windows+VS Code 터미널) 버그**(claude-code#10375·#23581, kilocode#6191). (a) 의 hang 이 세션을 블로킹한 게 주 트리거였고 이제 해소. cosmetic — 깨진 탭은 닫고 새로 열면 모드 리셋. `/terminal-setup`(gpuAcceleration off)·CC 업데이트 권장.
   - **오답 기록(되돌림)**: tqdm progress bar 가설(`predict(show_progress_bar=False)` 만 남김 — 무해), `TOKENIZERS_PARALLELISM` 가설, 그리고 `contextlib.redirect_stdout(sys.stderr)` 가드 — 전역 stdout 을 백그라운드 스레드가 돌려 JSON-RPC 응답이 stderr 로 새 **오히려 hang 유발 → 전부 revert**. 동시성 stdio 서버에서 전역 stdout 리다이렉트 금지.

## 전제 (저작권 — 형태 제약. 2026-07-22 `CLAUDE.md` 「북극성」 절 에서 이관, 문구 원문 그대로)

기준서 원문·파싱 DB·임베딩은 재배포 불가(KASB·IFRS Foundation). 따라서 프로덕트는 어떤 형태든
**"파이프라인은 공유, 데이터는 사용자가 직접 인덱싱"** 구조가 고정 전제다. 1차 형태는
**로컬 도구킷**(Claude Code + kifrs MCP + /accounting 스킬 + 결정 엔진 모듈 — 설치 후
사용자가 자기 기준서 PDF를 인덱싱)으로 확정(2026-07-04 결정). 독립 앱/웹 서비스는 도구킷이
검증된 뒤 별도 판단.

## 경계 (2026-07-22 `CLAUDE.md` 「북극성」 절 에서 이관, 문구 원문 그대로)

- **세무(세법) 영역은 sibling 레포 `tax-agent`가 담당** (2026-07-04 결정). 업무 지도에는 세무
  업무도 *표기*하되, 자동화 실험은 각 레포에서. kifrs-rag은 K-IFRS 회계 중심 유지.
- 기준서 원문·DB·임베딩·dogfood 자료 비공개 원칙 불변 (`CLAUDE.md` 금지 사항).
