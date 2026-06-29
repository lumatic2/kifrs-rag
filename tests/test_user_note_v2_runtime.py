from pathlib import Path

from kifrs import store


def use_tmp_db(monkeypatch, tmp_path: Path):
    db_path = tmp_path / "kifrs.db"
    monkeypatch.setattr(store, "DB_PATH", db_path)
    store.init_db()
    return db_path


def test_add_user_note_v2_mirrors_legacy_and_runtime_prefers_v2(monkeypatch, tmp_path):
    use_tmp_db(monkeypatch, tmp_path)

    result = store.add_user_note_v2(
        "1113",
        "76",
        "term_bridge",
        "종가",
        "활성시장; 수준 1",
        "test",
        "검색 보강",
        "2026-06-30",
    )

    assert result["inserted"] is True
    assert result["legacy_id"] is not None

    notes = store.get_user_notes("종가 기준 공정가치")
    assert len(notes) == 1
    assert notes[0]["type"] == "term_bridge"
    assert notes[0]["trigger"] == "종가"
    assert notes[0]["legacy_id"] == result["legacy_id"]

    with store._conn() as conn:
        legacy_count = conn.execute("SELECT COUNT(*) FROM user_note").fetchone()[0]
        v2_count = conn.execute("SELECT COUNT(*) FROM user_note_v2").fetchone()[0]
    assert legacy_count == 1
    assert v2_count == 1


def test_get_user_notes_falls_back_to_legacy_when_v2_empty(monkeypatch, tmp_path):
    use_tmp_db(monkeypatch, tmp_path)
    legacy_note = (
        "type=exam_convention; trigger=진행률 반올림; "
        "expansion=중간 반올림과 최종 금액 반올림을 모두 검산한다; "
        "source=test; rationale=시험 관습"
    )
    with store._conn() as conn:
        conn.execute(
            "INSERT INTO user_note (standard, no, note, created_at) VALUES (?, ?, ?, ?)",
            ("1115", "B43", legacy_note, "2026-06-30"),
        )

    notes = store.get_user_notes("진행률 반올림 확인", note_type="exam_convention")
    assert len(notes) == 1
    assert notes[0]["trigger"] == "진행률 반올림"
    assert notes[0]["legacy_id"] == 1


def test_query_expansion_uses_v2_rows(monkeypatch, tmp_path):
    use_tmp_db(monkeypatch, tmp_path)
    store.add_user_note_v2(
        "1113",
        "76",
        "term_bridge",
        "종가",
        "활성시장; 수준 1",
        "test",
        "검색 보강",
        "2026-06-30",
    )

    expanded = store.expand_query("종가로 측정")
    assert "활성시장" in expanded
    assert "수준 1" in expanded
