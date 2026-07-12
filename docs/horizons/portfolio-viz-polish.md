# Horizon: Portfolio Viz Polish

> Status: closed (2026-07-12)
> Created: 2026-07-12
> Previous: `docs/horizons/h10-disclosure-search-repair.md` (closed)
> Objective 링크: `docs/OBJECTIVE.md` — 성공기준 D축(포트폴리오) 심화. **사용자 발제 예외 4건째** (2026-07-12, drift·drift-automation·viz-site에 이어)
> Plan doc: `docs/plans/2026-07-12-portfolio-viz-polish.md`

## Goal

라이브 상태인 kifrs.askewly.com 을 3축으로 polish 한다 (사용자 범위 확정 2026-07-12 —
데이터 갱신 자동화는 미선택/제외):

1. **비주얼 보강** — codex imagegen 파이프라인(ai-accounting-firm 에서 검증됨)으로 사이트
   컨셉(한지·서가·인주·원장청록)에 맞는 실사/질감 이미지를 생성해 히어로·섹션에 반입.
   어스회계법인 사이트(기업 실사 톤)와 차별화 유지.
2. **인터랙션 심화** — **3D 기준서 우주**: `~/projects/obsidian/poc-graph`(brain.askewly.com)
   viewer 이식 — 기준서 star + 절 위성 + 계열 hierarchy, `/universe` 전용 페이지.
   사이트 내 기준서 검색은 저작권(본문 필요) 때문에 제외 — 시각화 전용 (사용자 확정 2026-07-12).
   기존 2D d3 그래프는 개요용 유지.
3. **콘텐츠 확장** — drift 감시 루프 스토리 섹션 + issue-back 수리 루프 연대기(h4→h10) +
   ai-accounting-firm 사이트 상호 링크.

**저작권 하드 경계 유지**: 기준서 본문·문단 텍스트는 어떤 형태로도 반입 금지 — 콘텐츠
확장도 메타데이터(숫자·구조·지표·날짜)만. 배포 전 public-safe gate 재실행 필수.

## Why now

- 어스회계법인 사이트 이미지 작업으로 imagegen 파이프라인·프롬프트 작법이 오늘 확립됨 —
  같은 파이프라인 재사용 비용이 최소인 시점.
- h4~h10 으로 수리 루프 2회전이 완주돼 "살아있는 엔진" 서사(감지→수리→비퇴행)의 실증
  소재가 쌓임 — 콘텐츠 확장의 재료가 완성됨.

## Milestones

### PP1. 비주얼 보강 — imagegen (P0)

Status: completed

- Deliverable: 사이트 컨셉 기반 imagegen 매니페스트(한지 질감·서가·묵향 정물 등) +
  codex exec 생성 + 히어로/섹션 반입. 텍스트 판독 불가·로고 없음 원칙 동일.
- Acceptance: 생성 이미지 육안 검수(컨셉 톤 일치) + 4뷰 실브라우저 렌더 + Lighthouse
  성능 급락 없음(이미지 최적화) + gate 재실행 PASS.

### PP2. 인터랙션 심화 + 콘텐츠 확장 + close gate (P1)

Status: completed

- Deliverable: ① 참조 그래프 UX — 기준서 검색/포커스 모드/가중치 필터 개선 ② drift 루프
  스토리 + 수리 루프 연대기(h4→h10 지표 곡선) 섹션 ③ ai-accounting-firm 상호 링크
  ④ 재배포 + gate 재검증.
- Acceptance: 그래프 신규 인터랙션 실브라우저 동작 확인 + 신규 섹션 메타데이터-only
  (gate PASS) + 라이브 URL 검증.

## Close criteria

- PP1·PP2 완료, kifrs.askewly.com 재배포 라이브.
- public-safe gate 배포 산출물 기준 PASS 유지.

## Close Result

`portfolio_viz_polished` (2026-07-12) — changeset 5개(#47~#51). 히어로·섹션 도판 5(한지/서가
정물 imagegen), **3D 기준서 우주 `/universe/`**(515 노드·1,166 엣지, poc-graph 이식),
drift 스토리·수리 루프 연대기·상호 링크, kifrs.askewly.com 재배포 라이브. gate PASS 유지
(universe graph.json 스캔 편입). 상세: `docs/reports/2026-07-12-portfolio-viz-polish-close-report.md`.

## Objective 임팩트

D축(포트폴리오)이 4뷰 정적 사이트에서 **"살아있는 엔진" 서사(감지→수리→비퇴행 지표) +
3D 지식 우주**로 상향 — brain.askewly.com·account.askewly.com 과 askewly 서브도메인
3부작이 상호 연결됨.

## Decision Log

- 범위 = 비주얼(imagegen)+인터랙션+콘텐츠 3축, 데이터 갱신 자동화 제외 — 사용자 확정 2026-07-12.
- milestone 을 2개로 구성 — h10 크기 회고(§A1: changeset 1개짜리 milestone 금지) 반영,
  인터랙션+콘텐츠+close 를 PP2 로 통합.
- 이미지 스타일은 어스회계법인(기업 실사)과 의도적으로 다르게 — 이 사이트의 기존 서가/
  한지/인주 디자인 시스템을 따르는 정물·질감 계열.
- PP2-S1 = 3D 기준서 우주 (사용자 발제·승인 2026-07-12) — poc-graph viewer 재사용,
  다크 코스믹 톤과 한지 화이트 본 사이트의 충돌은 `/universe` 전용 풀스크린 분리로 해소.
  사이트 내 검색은 저작권 경계로 제외(시각화 전용).
