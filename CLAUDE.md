# kifrs-rag

> K-IFRS 기준서 개인용 RAG/MCP 시스템. 본인 PC 로컬에서만 동작. 외부 공개·배포·공유 없음.

## 배경 및 포지셔닝

K-IFRS 기준서를 프로그램적으로 조회할 공식 API/MCP가 부재. 빅4 사내 AI는 외부 비공개. 외부 공개는 KASB·IFRS Foundation 저작권 장벽으로 진입 불가. **저작권법 제30조(사적이용 복제)·제35조의5(공정이용)** 범위 안에서 본인 학습·실무·포트폴리오 시연용으로 비공개 운영.

- 본인 PC 로컬에서만 동작
- 코드는 GitHub **private** 유지
- `tax-agent` 레포 파싱·저장 패턴 재사용 (신규 개발 비용 최소화)
- 외부 공개·협업은 별도 후속 프로젝트(`kifrs-public`)로 분리

## 기술 스택

- Python 3.11+ (uv 관리)
- PDF 파싱: `pdfplumber` + `PyMuPDF` (fallback)
- 스토어: SQLite (FTS5는 Phase 2에서 추가)
- MCP 서버: `FastMCP` (Python)
- 임베딩(Phase 2): sentence-transformers 한국어 모델 또는 OpenAI text-embedding-3-small

## 프로젝트 구조 (계획)

```
kifrs-rag/
├── CLAUDE.md                  # 이 파일
├── ROADMAP.md                 # 마일스톤 + 진행 상태
├── pyproject.toml             # uv 프로젝트 설정
├── .gitignore                 # data/, *.db, *.pdf, embeddings/ 최상단 제외
├── data/                      # PDF 원본, 파싱 JSON (git 제외)
│   └── standards/
│       └── 1115/              # 기준서별 폴더
├── kifrs/                     # 메인 패키지
│   ├── download.py            # KASB PDF 다운로더 (tax-agent download_exam_papers.py 포팅)
│   ├── parse.py               # 조·항·호 계층 파서 (tax-agent parse_exam_papers.py 구조 포팅)
│   ├── store.py               # SQLite 스토어 (tax-agent tax_store.py 포팅)
│   └── mcp_server.py          # FastMCP 서버 (신규)
└── scripts/
    └── ingest.py              # download → parse → store 파이프라인
```

## 작업 방식

- **새 기능 → 계획 먼저, 구현 나중**
- tax-agent 재사용 모듈 (자세히는 ROADMAP.md Phase 1 참조):
  - `parse_exam_papers.py`: PDF extract + 계층 split + JSON dump 구조 이식 (기준서용 정규식은 재작성)
  - `tax_store.py`: `_conn()` + `init_db()` bootstrap 패턴 그대로
  - `download_exam_papers.py`: requests + URL 맵 구조 그대로 (FSS → KASB URL 맵 교체)
  - `exam_eval.py`: Phase 2 평가 하네스 베이스 (TestResult dataclass + gold JSON)
- MCP 래퍼는 tax-agent에 없음 → 신규 작성

## 금지 사항 (저작권·보안)

- **기준서 PDF·텍스트·임베딩·DB 덤프는 절대 git commit 금지** (`.gitignore` 최상단 제외)
- 동료·친구 공유 ❌ (사적이용 범위 깨짐)
- 외부 웹에 PDF 원문·파싱 결과·DB 업로드 ❌
- 공개 가능 산출물은 **아키텍처 설명·평가 메트릭·데모 영상**만 (원문 인용 최소화)

## 세션 시작 규칙

- `ROADMAP.md`를 먼저 읽고 현재 Phase·다음 체크박스 확인 후 작업 착수
- tax-agent 참조 시 `~/projects/tax-agent/` 직접 열람 (sibling 경로)
