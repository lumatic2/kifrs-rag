"""K-IFRS 1109 (금융상품) 분류·측정 결정 엔진 — Phase 3 `data/scenarios/1109_classification/WORKFLOW.md` 이식.

WA1 scope (docs/plans/2026-07-03-wa1-1109-pilot-engine.md): 다음 5개 분류 경로만 결정론적으로
자동화한다 — AC, FVOCI(부채), FVOCI(자본·지분), FVPL(SPPI 실패/제3자 신용연계), FVPL(회계불일치
지정). IFRIC 19 발행자 부채소멸, SPPI 변동금리 재설정 불일치, 보유자 전환사채 미분리, 재분류,
외화 이중트랙 같은 5개 케이스는 각자 별도의 결정 로직이 필요해 이번 범위 밖 — `classify()`가
이런 입력을 만나면 `NeedsHumanReview`를 던진다(회귀 하네스가 완료율 분모에는 포함하되 "사람 개입
필요"로 정직하게 집계).
"""
