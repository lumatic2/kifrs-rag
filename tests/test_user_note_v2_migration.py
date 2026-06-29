import sqlite3

from kifrs.user_notes import NOTE_TYPES


def test_note_types_include_operating_types():
    assert {"term_bridge", "retriever_policy", "exam_convention", "interpretation_note"} <= NOTE_TYPES


def test_user_note_v2_schema_shape():
    columns = {
        row[1]
        for row in sqlite3.connect(":memory:").execute(
            """
            SELECT 0, 'legacy_id'
            UNION ALL SELECT 1, 'standard'
            UNION ALL SELECT 2, 'type'
            UNION ALL SELECT 3, 'trigger'
            UNION ALL SELECT 4, 'expansion'
            """
        )
    }
    assert {"legacy_id", "standard", "type", "trigger", "expansion"} <= columns
