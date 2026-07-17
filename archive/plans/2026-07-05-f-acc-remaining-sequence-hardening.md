# F-ACC Remaining Sequence Hardening Plan

> Date: 2026-07-05
> Objective: `docs/OBJECTIVE.md`
> Sequence: `docs/horizons/f-acc-technical-expansion.md`
> Current horizon: `docs/horizons/f-acc-financial-statement-draft.md`

## 산문 요약

앞으로 할 일은 새 후보를 고르는 것이 아니라, 이미 조사한 회계법인 service-line map을 따라 남은
자동화 실험을 순서대로 닫는 것이다. 지금 repo의 강점은 F-ACC(Accounting Advisory / F-S support)
산출물이다. 따라서 먼저 review pack output을 재무제표 표시 초안으로 연결하고, 그 다음 F-AUD의
분석적 절차 보조로 확장한 뒤, 마지막에 회계법인 소개용 demo pack으로 묶는다.

## 현재까지 닫힌 것

- [x] 회계법인 service-line map: 감사, 회계자문, 세무, Deal, Risk, Consulting 등 팀 구조와 workflow 정리.
- [x] F-ACC 1116 review pack: 리스 판단, 분개, 검토메모, 주석 초안, checklist.
- [x] F-ACC 1109 review pack: 금융상품 판단 결과를 review pack contract로 정리.
- [x] F-ACC 1115 revenue engine: 수익인식 5단계 판단, 측정, 분개, 검토메모, review pack.
- [x] Disclosure generalization: 1116/1115/1109 주석 checklist skeleton 공통화.
- [x] 1109 hardening: 자동화율 6/10에서 7/10, 남은 NeedsHumanReview의 skeleton/boundary memo 추가.

## 앞으로 닫을 horizon sequence

- [ ] **Horizon 6 — F/S draft**
  - 목적: review pack output을 재무상태표, 손익, OCI, 주석 연결 후보로 바꾼다.
  - Steps:
    - [ ] FS1 — statement draft surface inventory. verify: `docs/reports/2026-07-05-fs1-statement-draft-surface-inventory.md`
    - [ ] FS2 — statement line schema. verify: `python -m pytest tests/test_statement_draft.py`
    - [ ] FS3 — 1109 statement draft pilot. verify: 1109 fixture가 금융자산/손익/OCI 표시 후보를 생성
    - [ ] FS4 — 1115 statement draft pilot. verify: 1115 fixture가 수익/계약부채/금융요소 표시 후보를 생성
    - [ ] FS5 — F/S draft report. verify: `docs/reports/2026-07-05-fs5-statement-draft-report.md`

- [ ] **Horizon 7 — F-AUD analytical procedures**
  - 목적: 감사팀의 분석적 절차를 "계산표 + 이상징후 메모 + 회계이슈 연결" 수준까지 자동화한다.
  - Steps:
    - [ ] AP1 — 공개 F/S 또는 synthetic fixture scope 정의.
    - [ ] AP2 — ratio/trend 계산 schema.
    - [ ] AP3 — anomaly note renderer.
    - [ ] AP4 — review pack/disclosure/F-S draft와 연결되는 audit memo.
    - [ ] AP5 — analytical procedure report.

- [ ] **Horizon 8 — product packaging PoC**
  - 목적: 지금까지 만든 기술 표면을 회계법인에 보여줄 수 있는 10분 demo pack으로 묶는다.
  - Steps:
    - [ ] PK1 — demo scenario selection: 1116, 1109, 1115 중 보여줄 흐름 선택.
    - [ ] PK2 — CLI/demo command surface.
    - [ ] PK3 — sample input/output bundle.
    - [ ] PK4 — README + setup guide: protected K-IFRS assets는 사용자가 직접 인덱싱.
    - [ ] PK5 — 10분 demo brief + 회계사 피드백 질문지.

## 결정 로그

- 결정: 세 후보 중 하나를 고르는 단계가 아니다. F/S draft, audit analytical procedures, product packaging은 모두 해야 한다.
- 결정: 순서는 F-ACC 산출물 완성도 기준으로 정한다. 검토메모/분개/주석 다음은 F/S 표시 초안이다.
- 결정: F-AUD는 보조 적용처로 확장하되, 감사의견·KAM·서명 책임은 자동화 범위 밖으로 둔다.
- 결정: 패키징은 제품 표면이 충분히 쌓인 뒤 한다. 지금 당장 설치 파일부터 만들지 않는다.
- 결정: 기준서 원문, DB, embedding, dogfood 자료는 계속 비공개 자산으로 남긴다.

## 중단점

- protected K-IFRS 원문/DB/embedding을 공개 산출물에 포함해야 하는 요구가 생기면 중단한다.
- DART API key, 외부 credential, 실제 고객자료가 필요해지면 사용자 승인 전 진행하지 않는다.
- 재무제표 전체 자동작성처럼 회사별 TB/mapping table 없이는 성립하지 않는 범위로 커지면 PoC skeleton 범위로 되돌린다.
