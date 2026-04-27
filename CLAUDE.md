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
