# Changeset: 20260712-ib2-parse-bc-sections

## Target

- ROADMAP milestone: IB2 — 파싱 수리 (`docs/horizons/h4-issue-back-repair.md`)
- Plan: `docs/plans/2026-07-12-h4-issue-back-repair.md` IB2-a + IB2-b
  (계획은 changeset 2개였으나 같은 파일(parse.py)·같은 재인제스트 사이클의 응집 변경이라 1개로 통합)

## Scope

- Files: `kifrs/parse.py`, `kifrs/embed.py`(BC 감점 + 후보 풀 확대 — 재인제스트 비퇴행 게이트
  대응), `tests/test_parse_bc_sections.py`(신규), 로컬 재인제스트(`data/` — git 제외)
- Reason (mcp-log #15, #1/#2):
  1. **BC 통짜 문단** — `BC104.1`/`한BC104.1`/`BCE.15`/`DO1` 등 결론도출근거 계열 번호가 어떤
     문단 정규식에도 안 걸려 직전 문단에 통째 흡수 (1001 `1#2`=32k자, 1109 BC7.110 구간 등).
  2. **섹션 제목 잘림** — 두 형태: (a) 진짜 제목이 PDF에서 두 줄로 감기고 앞줄이 30자 제한에
     걸려 뒷조각만 채택("택권") (b) 본문 wrap 마지막 조각이 문단 번호 직전에 와서 제목으로
     오탐("는 금융상품", "체 분류한 …").
- Expected effect: BC/DO/IN 문단 개별 row 분리(1001 +246, 1032 +124, 1109 +1753 등),
  잘린 제목 복원·오탐 차단.

## Contract

- Source of truth: `kifrs/parse.py` (파서), 재생성물은 `data/standards/parsed/*.json` + SQLite +
  임베딩 (전부 git 제외 — 로컬 재인제스트로 파생).
- Compatibility: 기존 본문 문단 번호 체계 불변. BC 분리로 `#N` dedup suffix 문단
  (예: 1001-`1#4`)이 사라지거나 내용이 줄어듦 — BC 인용은 이제 `BC번호` 직접 사용.
  user_note anchor(1001-한138.5, 1032-16)는 본문 문단이라 영향 없음.
- Out of scope: 부록 A/B 대형 문단(1109 B7.2.4 49k자 — 기존과 동일), `--out` 레포 밖 경로 시
  CLI print 크래시(기존 버그, 파일은 정상 생성됨), IE(사례) 별도 세분화.
- Known trade-off: 인접한 두 소제목(상위+하위)에서 상위 제목이 25자 이상이면 드물게
  하나로 join되는 노이즈 잔존 (예: 1109 "2014년 7월에 IFRS 9에 추가된 요구사항IFRS9의
  의무시행일"). 구 동작(상위 제목이 본문 오염)보다 손실이 작다고 판단.

## Verification

- [x] Targeted tests: `test_parse_bc_sections.py` 7건 + `test_store_search.py` = 20 passed
- [x] Reparse 비교: 1001 213→472(BC 246, max body 32k→13.8k) / 1032 88→235(BC 124) /
      1109 563→2373(BC 1753, max body 비악화 49k 유지). 깨진 제목("는 금융상품"/"택권"/
      "체 분류한…") 제거 + 진짜 제목("풋가능 금융상품", "위험회피회계의 적격성과 순포지션의
      지정", 2자 제목 "개요"/"공시" 등) 보존
- [x] 재인제스트: 8,298→17,896 문단 (+9,598 = 정확히 BC/DO/IN 신규분, 감소 기준서 0),
      임베딩 17,896 (100%, orphan 정리 후), GPU(.venv) 재빌드
- [x] Integrated smoke + eval: `get_paragraph(1001,"한BC104.1")` 단독 반환(658자),
      `get_context(1001,"한138.5")` 정상 크기, `list_sections(1032)` 잘림 0.
      **BC 감점 후 hybrid eval 전 지표 개선**: recall@10 0.713→0.747, recall@20 0.887→0.910,
      MRR 0.464→0.490 (감점 전엔 recall@20 0.760 퇴행 → `_BC_DEMOTE=0.5` + 풀 100으로 회복).
      리픽싱 reranked 한BC104.1 rank 1(0.875) 유지. `quality_preflight.py` ok.

## Result

- Status: completed
- Evidence: `docs/reports/2026-07-12-ib2-parse-repair.md` (before/after 표 + eval)
- Notes: MCP 서버 프로세스는 구 코드로 기동 중 — BC 감점은 서버 재시작(세션 재접속) 시 반영.
  reranked의 같은 조건 직전 baseline은 미확보(환경 이슈로 측정 불가) — BC 유무 전후 reranked는
  0.593/0.534 → 0.593/0.538로 평탄.
