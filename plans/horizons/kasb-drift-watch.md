# Horizon: KASB Drift Watch

> Status: closed (2026-07-12)
> Created: 2026-07-12
> Previous: `docs/horizons/h4-issue-back-repair.md` (closed)
> Objective 링크: `docs/OBJECTIVE.md` — 지식 엔진의 정확성·최신성 유지 (issue-back 규칙의 사용자 승인 예외, 결정 이력 2026-07-12 참조)
> Plan doc: `docs/plans/2026-07-12-kasb-drift-watch.md`

## Goal

KASB(kasb.or.kr)에 공표되는 기준서 제·개정과 로컬 DB(100 기준서, 17,896 문단) 사이의
**drift를 감지하고, 감지된 기준서를 단위 갱신(재다운로드→재파싱→재인제스트→재임베딩)하는
경로까지 닫는다.** 감지는 MCP tool(`check_drift`)로 노출하되 코어 로직은 `kifrs/drift.py`
모듈로 분리해 CLI로도 실행·검증 가능하게 한다.

## Why now

- RAG의 stale 기준서는 **틀린 근거 인용**으로 직결 — ai-accounting-firm 실소비(F-ACC review pack)의
  신뢰성 전제. issue-back이 돌아오기 전에 능동적으로 막을 수 있는 유일한 결함 계열.
- 감지 신호가 실재함: `download.py`가 이미 긁는 KASB 기준서 게시판의 파일 목록(파일명·file_seq)이
  로컬 `standard.source`와 대조 가능한 정본 신호다.
- `amendment` 테이블(스키마만, "실사용 마찰 trigger" 대기)의 첫 실사용처.

## Milestones

### DR1. Drift 감지 코어 + MCP tool (P0)

Status: completed

- Deliverable: `kifrs/drift.py`(KASB 파일 목록 fetch — download.py 재사용 → 로컬 `standard.source`
  + 스냅샷(`data/drift/`) 대조 → drift report) + CLI entry + kifrs MCP tool `check_drift`(얇은
  wrapper, 무거운 import 없음 — 한계 #6 규약 준수).
- Acceptance: 실 KASB 대상 E2E 실행으로 리포트 생성(현재 drift 0건이어도 100 기준서 대조 결과 관측)
  + 네트워크 실패/게시판 포맷 변경 시 graceful 에러(실패 모드) + MCP tool 실호출 관측.

### DR2. 단위 갱신 경로 + 개정 이력 (P1)

Status: completed

- Deliverable: drift 감지된 기준서 1개 단위 갱신 경로(재다운로드→재파싱→재인제스트→임베딩 재색인,
  기존 `scripts/ingest.py` 파이프라인 재사용) + `standard` 테이블 메타 확장(KASB 파일 식별자·감지일)
  + `amendment` 테이블에 갱신 이력 기록.
- Acceptance: drift 1건(실제 개정 없으면 synthetic)으로 갱신 E2E — 갱신 후 문단 수·retrieval eval
  비퇴행 + `amendment` 행 기록 확인.

## Close criteria

- DR1·DR2 완료 + 기존 품질 게이트 비퇴행.
- drift 리포트·커밋 산출물은 public-safe(기준서 번호·제목·파일명 메타만 — 원문·DB 비공개 원칙 불변).
- 스케줄 자동화(cron 등)는 이 horizon 범위 밖 — 수동/MCP 호출로 운영하다 마찰이 생기면 다음 판단.

## Close Result

`kasb_drift_watch_closed` (2026-07-12) — 감지(DR1)·갱신 경로(DR2) 완주, changeset 4개
(#34~#37). **실 성과: KASB 수정목록 26-1 개정 배치 15건을 첫 실행에서 검출**, 그중 2건
(1024 특수관계자공시 — 문단 28A 변경, 2101 — 문단 2건 변경)을 단위 갱신으로 해소하고
amendment 3행에 문단 단위 diff 를 기록. eval 비퇴행(recall@10 0.747 / @20 0.910 / MRR 0.490
유지). 잔여 실 drift 13건은 운영 후속(`python -m kifrs.drift --update <id>`).

## Objective 임팩트

Objective 성공 모습("실소비 결함이 닫히는 상태")을 **예방 축**으로 확장 — stale 기준서가
틀린 인용으로 이어지기 *전에* 감지·갱신하는 수단이 생겼다. 첫 실행에서 실제 개정 15건을
잡았으므로 가설(감지 수단 부재 = 실질 리스크)이 즉시 실증됨. `amendment` 테이블이 스키마
전용에서 첫 실사용으로 전환. ROADMAP 자기평가 재측정 불요 — 다음 horizon 은 여전히
ai-accounting-firm issue-back(또는 사용자 승인 예외)이 연다.

## Decision Log

- 실행 형태 = **MCP tool** (사용자 확정 2026-07-12). stdio 안정성 이력(한계 #6) 때문에 코어는
  모듈+CLI, MCP tool은 얇은 wrapper로.
- 범위 = **감지 + 갱신 경로** (사용자 확정 2026-07-12). 감지만 하고 못 고치면 반쪽.
- issue-back 규칙 예외 = 사용자 명시 승인(2026-07-12)으로 자체 발제 horizon 개설. 규칙 자체는 유지
  — 이후 자체 발제는 다시 예외 승인 필요.
- 감시 신호 = 기준서 게시판 파일 목록 diff(정본). 보도자료/공표 게시판 감시는 부가 신호로 DR1에서
  타당성만 확인, 필수 아님 (구현 재량).
- 스냅샷·리포트 저장 = `data/drift/`(gitignored). 리포트 요약만 필요 시 docs/reports로.
