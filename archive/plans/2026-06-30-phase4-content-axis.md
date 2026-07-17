# Phase 4 콘텐츠 축 계획 — RAG 평가 케이스 누적

> 작성일: 2026-06-30
> ROADMAP goal: `phase4-content`
> Active milestone: `P4C1`
> 원칙: 기준서 원문·기출·파싱 데이터는 로컬 사적이용 범위에만 둔다. 공개 산출물은 메트릭·아키텍처·비원문 설명만 허용.

## 1. 목표

검색 파이프라인 M1~M5로 만든 엔진을 실제 회계 판단 태스크에 계속 적용한다. Phase 4의 목적은 시험 문제를 많이 푸는 것이 아니라, 1115·1116·1019·1113 같은 도메인별로 "입력 → 검색 query → 검색 결과 → 인용 검증 → 판단/산식/분개 → 채점 또는 검토 → failure mode → user_note 후보" 루프를 반복해 RAG 품질을 검증하고 개선 근거를 쌓는 것이다.

## 2. 범위

이번 연속 실행의 기본 순서는 다음과 같다.

- P4C1: 1115 수익 q07 RAG eval case + 1115 워크플로 seed
- P4C2: 1116 리스 잔여 시나리오 closeout
- P4C3: q05/q06/q07에서 나온 user_note 후보 운영 시작
- P4C4: 1113 공정가치 도메인 진입 설계
- P4C5: 1019 확정급여(q06) 도메인 workflow 승격

P4C1~P4C5는 완료했다. 다음은 새 engine horizon 정의가 필요한 구간이다.

## 3. 중요한 오염 경계

q07은 `data/dogfood/cpa2/q/q07.md` 안에 문제, 본인 풀이 자리, 모범답안, 채점표가 함께 있다. 본 계획 작성 중 모범답안 숫자 일부가 현재 세션에 노출됐으므로, 이 세션에서 q07 답안을 만들면 "무오염 본인 풀이" 증거가 아니다.

P4C1 실행은 다음 중 하나로 진행한다.

- clean context에서 `q07.md`의 문제 섹션과 본인 풀이 지시만 보고 풀이한다.
- 또는 별도 sanitized 문제 파일을 만들고, fresh agent/session이 그 파일만 읽어 본인 풀이를 작성한다.

## 4. Step 트리

- [x] Step 1 — q07 clean eval input 준비
  - 산출물: `data/dogfood/cpa2/q/q07_problem_only.md` 또는 동등한 clean prompt
  - verify: clean input에 `모범답안`, 정답 금액, 채점표의 모범 값이 없는지 텍스트 검색으로 확인

- [x] Step 2a — q07 retrieval trace 템플릿 준비
  - 산출물: `data/eval/manual/q07_1115_revenue_trace.md`
  - verify: 4개 물음별 query, retriever, top hits, adopted citations, failure mode, user_note 후보 칸 존재

- [x] Step 2b — q07 retrieval trace 작성
  - 산출물: `data/eval/manual/q07_1115_revenue_trace.md`
  - verify: 4개 물음별 query, 사용 retriever, top hits, 채택/폐기 근거, missing 표현이 기록됨

- [x] Step 3 — q07 본인 풀이 작성
  - 산출물: `data/dogfood/cpa2/q/q07.md`의 `# 본인 풀이` 섹션
  - verify: 풀이가 retrieval trace에서 채택한 1115 기준서 인용과 4개 물음별 산식/결론을 포함하는지 확인

- [x] Step 4 — q07 채점 + 인용 검증
  - 산출물: `data/dogfood/cpa2/q/q07.md`의 `# 채점` 섹션
  - verify: 7개 채점 항목이 본인/모범/일치/비고로 채워지고, 직관 점수·해석 인정 점수·인용 정확도가 명시됨

- [x] Step 5 — 1115 수익 워크플로 seed 작성
  - 산출물: `data/scenarios/1115_revenue/WORKFLOW.md`
  - verify: q07 4개 물음이 각각 갱신선택권, 할인권, 유의적 금융요소, 재매입약정 eval/scenario seed로 연결됨

- [x] Step 6 — failure mode + user_note 후보 추출
  - 산출물: `data/scenarios/1115_revenue/user_note_candidates.md` 또는 q07 하단 후보 섹션
  - verify: 검색 실패 표현, 시험 산식 관습, 기준서 본문 표현 차이, 답변 포맷 마찰을 구분해 기록

- [x] Step 7 — P4C1 종료 판정
  - 산출물: ROADMAP P4C1 Status 업데이트 후보 + BACKLOG 요약 후보
  - verify: q07 trace/채점/인용 검증 완료, 1115 WORKFLOW seed 존재, user_note 후보 존재

## 4.1 P4C1 결과

- 채점 결과: 직관 5/7, 해석 인정 6/7, 인용 정확도 13/13.
- RAG pass: q07-2 할인권, q07-3 유의적 금융요소, q07-4 콜옵션 재매입약정.
- RAG partial: q07-1 갱신선택권. citation은 맞았지만 `계약부채`와 `잔여 수행의무` 표시 관점, 진행률 반올림 관습에서 시험 답안과 불일치.
- 새 후보: term_bridge 2건, retriever_policy 1건, metadata_quality 1건, exam_convention 2건.
- 판정: P4C1은 q07 1115 RAG eval case로 완료 가능. 다음 후보는 P4C2 1116 리스 잔여 closeout.

## 5. P4C2 후보 — 1116 리스 잔여 closeout

P4C1 완료 후 바로 이어간 후보. 1116 워크플로는 5/10에서 시작해 잔여 5개를 닫았고, 리스 도메인이 하나의 완성된 Phase 4 사례가 됐다.

- [x] 시나리오 3 — 단기·저가 면제
- [x] 시나리오 4 — 금융리스 제공자 / 금융리스에서 운용리스로 변경
- [x] 시나리오 6 — 금융리스에서 금융리스로 변경
- [x] 시나리오 7 — 리스기간 재평가
- [x] 시나리오 8 — 매수선택권 행사 거의 확실

각 시나리오 산출물은 `transaction.md`, `workflow_log.md`, `entries.md`, `review_memo.md` 네 파일을 기본으로 한다.

P4C2 결과: 1116 시나리오 10/10 완료. 다음 active는 P4C3 user_note 운영 시작.

## 6. P4C3 후보 — user_note 운영 시작

현재 후보는 최소 네 묶음이다.

- q05: 공매도처럼 기준서 본문에 직접 표현이 없는 시험 표현
- q06: 1019 보고기간 중 정산·제도개정 순이자 산식
- q06: 1019 해고급여와 1037 구조조정 충당부채 해석 분기
- q07: 1115 시험 산식과 기준서 표현 차이

완료 기준은 seed 5~10건을 만들고, 검색 또는 답변 작성 시 어떻게 사용할지 최소 운영 규칙을 적는 것이다.

### P4C3 진행 결과

- [x] q05/q06/q07/P4C2 후보를 묶어 seed preview 11건 작성
- [x] `term_bridge`, `exam_convention`, `retriever_policy`, `interpretation_note` 운영 규칙 작성
- [x] seed anchor 10개 문단 DB/PDF 검증 완료
- [x] 실제 SQLite `user_note` insert — `scripts/seed_user_notes.py --apply`
- [x] 검색 전 query expansion 연결 — `type=term_bridge`, `type=retriever_policy`

산출물: `data/user_notes/2026-06-30-p4c3-seed-preview.md`

## 7. P4C4 후보 — 1113 공정가치 진입

1113은 KICPA 적용 부담 1위지만, DCF·옵션모델·시장데이터가 얽혀 있어 바로 문제풀이로 들어가면 범위가 커진다. P4C4는 먼저 경계를 정한다.

- 기준서 본문 판단만 할 것인지
- 숫자 모델까지 할 것인지
- 시장데이터 없이 예제 입력으로만 할 것인지
- 1036 손상·1016 재평가와 묶을 것인지

### P4C4 진행 결과

- [x] 1113 범위 경계 결정
- [x] citation map 14개 DB/PDF 검증
- [x] 수준 1/2/3 concrete scenario 3개 작성
- [x] 1113 term_bridge 3건 SQLite user_note seed 승격

## 7.1 P4C5 후보 — 1019 확정급여(q06) 승격

P4C4 이후 남은 콘텐츠 승격 후보. q06의 확정급여와 구조조정충당부채 풀이·채점·failure mode를 도메인 workflow로 전환한다.

- [x] 1019/1037 범위 경계 결정
- [x] citation map 14개 DB/PDF 검증
- [x] EB-01 확정급여 정산·제도개정 scenario 작성
- [x] EB-02 구조조정충당부채·해고급여 scenario 작성
- [x] `exam_convention`/`interpretation_note`를 답변 작성 단계에서 조회하는 `get_user_notes` 추가

P4C5 결과: 1019 확정급여 entry workflow 완료. Phase 4 콘텐츠 후보는 P4C1~P4C5로 일단 닫힘.

## 8. 멈춤 조건

- q07 clean context 확보에 실패하면 q07 본인 풀이를 진행하지 않는다.
- 기준서 원문·기출 원문·모범답안을 공개 파일이나 git tracked 파일에 옮기지 않는다.
- 한 milestone 완료 후 active가 0개가 되면, 사용자의 "계속" 의사가 유지될 때만 다음 후보 하나를 active로 승격한다.
