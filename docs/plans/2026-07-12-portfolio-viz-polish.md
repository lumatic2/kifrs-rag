# Plan: portfolio-viz-polish

> Created: 2026-07-12
> Horizon: `docs/horizons/portfolio-viz-polish.md` (active)
> 산출물: 전부 changeset

## Step 트리

### PP1 — 비주얼 보강 (P0)

- [ ] PP1-S1: imagegen 매니페스트(`docs/imagegen-manifest.md` — 서가/한지/인주 컨셉, BASE STYLE + 슬롯별 프롬프트) + codex exec 생성 + 육안 검수 (verify: 전 이미지 생성 + 컨셉 톤·무텍스트·무로고 확인)
- [ ] PP1-S2: 사이트 반입 — 히어로/섹션 통합 + 이미지 최적화(용량·lazy) + 4뷰 실브라우저 E2E + gate 재실행 (verify: 렌더 + gate PASS + 빌드 통과)

### PP2 — 인터랙션 + 콘텐츠 + close (P1)

- [ ] PP2-S1: 참조 그래프 UX — 기준서 검색 박스·포커스 모드(선택 노드 이웃만)·필터 개선 (verify: 실브라우저 동작)
- [ ] PP2-S2: 콘텐츠 확장 — drift 감시 루프 스토리 + 수리 루프 연대기(h4→h10, recall 곡선 등 지표만) + ai-accounting-firm 상호 링크 (verify: 신규 데이터 gate PASS — 메타데이터 only)
- [ ] PP2-S3: 재배포 + 라이브 검증 + close report (verify: kifrs.askewly.com 신규 요소 렌더 + dist 재스캔 0건)

## 중단점

- 이미지가 컨셉 톤과 안 맞으면(기업 실사 톤 오염) 프롬프트 재작업 — 어스회계법인과의 차별화가 이 사이트의 정체성.
- gate FAIL 시 즉시 정지 — 본문 비노출은 하드 경계.

## 결정 로그

- 3축 범위·스택 유지(Astro)·milestone 2개 구성은 horizon Decision Log 참조. 잔여 사용자 소유 결정 **없음**.

## planning_gate

```yaml
planning_gate:
  team_validation_mode: manual-pass
  scope_posture: selective
  delegation_decision:
    remote_background_agents: allow
    reason: "imagegen=codex exec 백그라운드, 사이트 구현=로컬 (오늘 확립한 파이프라인 재사용)"
    target_roles: [codex-imagegen]
    execution_path: local_manual
  spec_delta: "사용자 발제 예외 4건째 — horizon/plan doc + ROADMAP marker"
  dod:
    - "PP1: 컨셉 톤 이미지 반입 + 4뷰 E2E + gate PASS"
    - "PP2: 그래프 UX·콘텐츠 신규 섹션 라이브 + dist 재스캔 0건 + close report"
```
