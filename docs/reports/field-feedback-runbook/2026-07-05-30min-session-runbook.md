# 30-Minute Accountant Feedback Session Runbook

> Date: 2026-07-05
> Status: session-ready runbook, not completed feedback evidence
> Target reviewer: accountant familiar with Accounting Advisory / F-S support or audit issue review

## Purpose

이 runbook은 회계사 1명에게 현재 Accounting Intelligence toolkit을 보여주고, 실제 업무에서 쓸 수 있는
부분과 위험한 부분을 기록하기 위한 운영 절차다. 목적은 영업 설득이 아니라 제품 검증이다.

## Inputs

| File | Role |
|---|---|
| `docs/reports/firm-facing-poc/2026-07-05-one-page-brief.md` | 10분 소개의 시작점 |
| `docs/reports/demo-poc/MANIFEST.md` | public-safe demo bundle 순서 |
| `docs/reports/real-transaction-poc/INDEX.md` | 익명화 거래 카드 -> review pack -> queue sample |
| `docs/reports/2026-07-05-af3-feedback-incorporation-report.md` | queue correction이 action plan으로 이어지는 예시 |
| `docs/reports/field-feedback/2026-07-05-feedback-questionnaire.md` | 기본 질문지 |
| `docs/reports/field-feedback/2026-07-05-incorporated-review-questions.md` | 추가 review question 후보 |

## Before Session

1. 아래 명령으로 demo bundle과 sample package를 재생성한다.

```powershell
python scripts\demo_poc.py --scenario revenue-financing --out docs\reports\demo-poc
python scripts\real_transaction_poc.py --out docs\reports\real-transaction-poc
python scripts\feedback_incorporation_report.py --queue docs\reports\real-transaction-poc\feedback-queue.jsonl --out docs\reports\2026-07-05-af3-feedback-incorporation-report.md --questions-out docs\reports\field-feedback\2026-07-05-incorporated-review-questions.md
```

2. 세션 시작 전에 boundary를 먼저 말한다.
   - 최종 회계판단, 감사의견, 세무판단, 법률판단은 사람이 한다.
   - 공개 repo에는 기준서 원문, DB, 임베딩, 고객자료, raw filing body가 없다.
   - 현재 sample은 실제 회계사 검증 완료물이 아니라 public-safe sample이다.

## 30-Minute Timeline

| Time | Segment | Show | Ask |
|---:|---|---|---|
| 0:00-3:00 | Context | one-page brief | "이 대상 팀을 F-ACC로 잡는 설명이 맞는가?" |
| 3:00-8:00 | Demo bundle | demo manifest, 1115 review pack | "판단 흐름이 실제 검토 순서와 맞는가?" |
| 8:00-12:00 | Evidence boundary | evidence-boundary, statement candidates | "근거 경계가 신뢰를 높이는가, 아니면 헷갈리는가?" |
| 12:00-18:00 | Real transaction sample | anonymized input card, 1116 review pack | "실제 익명화 거래라면 어떤 입력이 더 필요할까?" |
| 18:00-22:00 | Feedback loop | feedback queue report, incorporation report | "correction이 eval/backlog/action으로 나뉘는 방식이 맞는가?" |
| 22:00-28:00 | Questionnaire | field feedback questionnaire + supplement | "가장 중요한 개선 1개와 위험 1개는 무엇인가?" |
| 28:00-30:00 | Close | next action options | "다음에 실제 익명화 거래 1건을 제공할 수 있는가?" |

## Required Questions

1. 이 도구가 가장 가까운 팀은 어디인가?
   - F-ACC Accounting Advisory / F-S support
   - F-AUD Audit issue review
   - 결산 지원
   - 기타
2. review pack에서 가장 시간이 줄어들 가능성이 큰 section은 무엇인가?
3. 사람이 반드시 다시 검토해야 하는 section은 명확한가?
4. evidence boundary가 충분히 명확한가?
5. 실제 익명화 거래를 넣는다면 필요한 structured facts는 무엇인가?
6. 다음 demo에서 반드시 추가해야 할 review question은 무엇인가?
7. 자동화되면 가장 위험한 부분은 무엇인가?
8. 이걸 30분 PoC로 다시 본다면 어떤 success criteria를 둘 것인가?

## Recording Template

```markdown
# Field Feedback Notes - YYYY-MM-DD

## Reviewer Context
- Role:
- Service-line:
- Familiar standards:

## Scores
- Workflow fit:
- Evidence boundary clarity:
- Review pack usefulness:
- Human-review boundary clarity:

## Top Positive

## Top Risk

## Required Input Additions

## Review Question Additions

## Queue Candidates
- eval seed:
- backlog:
- no action:

## Next Decision
- real anonymized transaction provided? yes/no
- follow-up session needed? yes/no
```

## After Session

1. 질문지 답변을 별도 notes 파일로 남긴다.
2. correction 후보를 `FeedbackQueueRecord` 형태로 변환할 수 있는지 판단한다.
3. `feedback_incorporation_report.py`로 action plan을 재생성한다.
4. 다음 horizon을 고른다.
   - 실제 익명화 거래를 받았으면 `real-accountant-reviewed-case`.
   - 피드백이 주로 질문/표현 개선이면 `feedback-incorporation-round2`.
   - 도구 설명이 약하면 `firm-introduction-material`.

## Boundary

- 이 runbook은 실제 피드백 완료 증거가 아니다.
- 고객자료, 계약 원문, 기준서 원문, DB, 임베딩을 이 repo에 저장하지 않는다.
- 익명화 거래는 structured facts card로만 받는다.
