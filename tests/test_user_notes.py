from kifrs.user_notes import audit_user_notes, parse_user_note


def test_parse_user_note_structured_fields():
    parsed = parse_user_note(
        "1113",
        "76",
        "type=term_bridge; trigger=종가; expansion=활성시장; 수준 1; source=P4C4; rationale=검색 보강",
        "2026-06-30",
    )
    assert parsed.type == "term_bridge"
    assert parsed.trigger == "종가"
    assert parsed.expansion == "활성시장; 수준 1"
    assert parsed.source == "P4C4"
    assert parsed.rationale == "검색 보강"


def test_audit_user_notes_dead_anchor_and_invalid_type():
    notes = [
        parse_user_note(
            "1113",
            "76",
            "type=term_bridge; trigger=종가; expansion=활성시장; source=P4C4; rationale=검색 보강",
        ),
        parse_user_note(
            "9999",
            "1",
            "type=bad_type; trigger=X; expansion=Y; source=test; rationale=bad",
        ),
    ]
    result = audit_user_notes(notes, paragraph_exists=lambda std, no: std == "1113" and no == "76")
    assert not result["ok"]
    assert len(result["dead_anchor"]) == 1
    assert len(result["invalid_type"]) == 1


def test_audit_user_notes_conflicting_duplicate_trigger():
    notes = [
        parse_user_note("1113", "76", "type=term_bridge; trigger=종가; expansion=A; source=s; rationale=r"),
        parse_user_note("1113", "72", "type=term_bridge; trigger=종가; expansion=B; source=s; rationale=r"),
    ]
    result = audit_user_notes(notes, paragraph_exists=lambda std, no: True)
    assert len(result["duplicate_trigger"]) == 1
    assert len(result["conflicting_trigger"]) == 1
