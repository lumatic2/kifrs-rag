# Reviewer Invite Action Packet

> Scope: copy-ready invite message and post-send ledger command for RS2.

## 한 줄 결론

The invite message is ready to send manually. This file does not send the message and does not update the outreach ledger.

## Send Target

- reviewer alias: `reviewer-001`
- subject: 회계 AI PoC 30분 피드백 요청 초안

## Copy Message

```text
안녕하세요.

제가 만들고 있는 K-IFRS 기반 회계 AI 도구를 회계사 실무 관점에서 30분 정도 보여드리고 피드백을 받고
싶습니다. 목적은 도입 제안이나 영업이 아니라, 실제 회계자문/F-S support 또는 감사 중 회계이슈 검토
업무에서 어떤 부분이 쓸 만하고 어떤 부분이 위험한지 확인하는 것입니다.

보여드릴 것은 아래 정도입니다.

1. 복잡 거래에 대한 review pack 초안
2. 분개 후보와 주석/표시 후보
3. 기준서 근거와 외부 evidence boundary 표시
4. 사람이 반드시 검토해야 하는 질문 목록
5. 피드백이 eval/backlog queue로 반영되는 구조

중요한 경계는 다음과 같습니다.

- 이 도구는 최종 회계판단, 감사의견, 세무판단, 법률판단을 대신하지 않습니다.
- 고객자료, 계약 원문, 회사명, 사업자번호 등 식별정보는 받지 않습니다.
- 실제 거래 예시는 가능하면 조건표 형태로 익명화해서만 다룹니다.
- 공개 repo에는 기준서 원문, DB, 임베딩, 고객자료를 저장하지 않습니다.

30분 세션에서 제가 묻고 싶은 핵심 질문은 세 가지입니다.

1. 이 산출물이 실제 업무 검토 순서와 얼마나 맞는지
2. 검토 시간을 줄일 가능성이 있는 section과 오히려 위험한 section은 무엇인지
3. 다음 PoC에 넣을 만한 익명화 거래 유형은 무엇인지

가능하시면 편한 시간대를 알려주세요. 화면 공유로 30분이면 충분합니다.
```

## Boundary

- Do not ask reviewer to send raw contracts or customer identifiers.
- Use only public-safe notes after the session.
- Update outreach ledger after sending.

## After Manual Send

Run the ledger update only after the invite was actually sent by the operator.

```powershell
python scripts\real_accountant_outreach_update.py --ledger docs/reports/real-accountant-session/outreach-log.sample.jsonl --reviewer-alias reviewer-001 --status sent --channel manual --contacted-at 2026-07-05 --follow-up-by 2026-07-08 --notes "invite sent"
```

## Machine Result

```json
{
  "reviewer_alias": "reviewer-001",
  "subject": "회계 AI PoC 30분 피드백 요청 초안",
  "body": "안녕하세요.\n\n제가 만들고 있는 K-IFRS 기반 회계 AI 도구를 회계사 실무 관점에서 30분 정도 보여드리고 피드백을 받고\n싶습니다. 목적은 도입 제안이나 영업이 아니라, 실제 회계자문/F-S support 또는 감사 중 회계이슈 검토\n업무에서 어떤 부분이 쓸 만하고 어떤 부분이 위험한지 확인하는 것입니다.\n\n보여드릴 것은 아래 정도입니다.\n\n1. 복잡 거래에 대한 review pack 초안\n2. 분개 후보와 주석/표시 후보\n3. 기준서 근거와 외부 evidence boundary 표시\n4. 사람이 반드시 검토해야 하는 질문 목록\n5. 피드백이 eval/backlog queue로 반영되는 구조\n\n중요한 경계는 다음과 같습니다.\n\n- 이 도구는 최종 회계판단, 감사의견, 세무판단, 법률판단을 대신하지 않습니다.\n- 고객자료, 계약 원문, 회사명, 사업자번호 등 식별정보는 받지 않습니다.\n- 실제 거래 예시는 가능하면 조건표 형태로 익명화해서만 다룹니다.\n- 공개 repo에는 기준서 원문, DB, 임베딩, 고객자료를 저장하지 않습니다.\n\n30분 세션에서 제가 묻고 싶은 핵심 질문은 세 가지입니다.\n\n1. 이 산출물이 실제 업무 검토 순서와 얼마나 맞는지\n2. 검토 시간을 줄일 가능성이 있는 section과 오히려 위험한 section은 무엇인지\n3. 다음 PoC에 넣을 만한 익명화 거래 유형은 무엇인지\n\n가능하시면 편한 시간대를 알려주세요. 화면 공유로 30분이면 충분합니다.",
  "send_boundary": [
    "Do not ask reviewer to send raw contracts or customer identifiers.",
    "Use only public-safe notes after the session.",
    "Update outreach ledger after sending."
  ],
  "post_send_update_command": "python scripts\\real_accountant_outreach_update.py --ledger docs/reports/real-accountant-session/outreach-log.sample.jsonl --reviewer-alias reviewer-001 --status sent --channel manual --contacted-at 2026-07-05 --follow-up-by 2026-07-08 --notes \"invite sent\"",
  "report_path": "docs/reports/real-accountant-session/2026-07-05-reviewer-invite-action-packet.md"
}
```
