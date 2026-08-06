import sqlite3
from pathlib import Path

import pytest

from preventia.dashboard.repository import queue_rows

SCHEMA = Path(__file__).resolve().parents[1] / "preventia" / "data" / "schema.sql"


def build(tmp_path):
    connection = sqlite3.connect(tmp_path / "test.db")
    connection.row_factory = sqlite3.Row
    connection.executescript(SCHEMA.read_text(encoding="utf-8"))
    connection.execute(
        "INSERT INTO clinicians (code, display_name, role) VALUES ('CL-01', 'Enfermera', 'enfermera')"
    )
    connection.execute(
        "INSERT INTO patients (code, display_name, age, sex, comuna, assigned_clinician, enrolled_on)"
        " VALUES ('PV-001', 'Hilda', 71, 'F', 'Quinta Normal', 'CL-01', '2026-01-01')"
    )
    connection.execute(
        "INSERT INTO escalation_audit (patient_code, from_state, to_state, actor_code, occurred_at, note)"
        " VALUES ('PV-001', 'closed', 'in_review', 'CL-01', '2026-08-06T16:07:00+00:00', '')"
    )
    return connection


def add_check_in(connection, occurred_at, colour, message):
    cursor = connection.execute(
        "INSERT INTO check_ins (patient_code, occurred_at, patient_message, agent_message,"
        " doses_reported_taken, doses_expected, summary_line) VALUES (?, ?, ?, '', 4, 4, ?)",
        ("PV-001", occurred_at, message, message),
    )
    connection.execute(
        "INSERT INTO risk_events (check_in_id, rules_color, rules_reason, model_color,"
        " model_reason, final_color) VALUES (?, ?, '', ?, '', ?)",
        (cursor.lastrowid, colour, colour, colour),
    )
    connection.commit()


def test_a_red_survives_a_later_calm_message(tmp_path):
    connection = build(tmp_path)
    add_check_in(connection, "2026-08-06T16:12:50+00:00", "red", "me acabo de desmayar")
    add_check_in(connection, "2026-08-06T16:13:51+00:00", "green", "me equivoque, estoy bien")

    row = next(r for r in queue_rows(connection) if r.code == "PV-001")

    assert row.color == "red"


def test_the_latest_message_is_still_what_the_clinician_reads(tmp_path):
    connection = build(tmp_path)
    add_check_in(connection, "2026-08-06T16:12:50+00:00", "red", "me acabo de desmayar")
    add_check_in(connection, "2026-08-06T16:13:51+00:00", "green", "me equivoque, estoy bien")

    row = next(r for r in queue_rows(connection) if r.code == "PV-001")

    assert row.summary_line == "me equivoque, estoy bien"


def test_a_clinician_moving_the_case_clears_the_held_red(tmp_path):
    connection = build(tmp_path)
    add_check_in(connection, "2026-08-06T16:12:50+00:00", "red", "me acabo de desmayar")
    connection.execute(
        "INSERT INTO escalation_audit (patient_code, from_state, to_state, actor_code, occurred_at, note)"
        " VALUES ('PV-001', 'in_review', 'contacted', 'CL-01', '2026-08-06T16:20:00+00:00', 'llamada hecha')"
    )
    connection.commit()
    add_check_in(connection, "2026-08-06T16:25:00+00:00", "green", "todo bien")

    row = next(r for r in queue_rows(connection) if r.code == "PV-001")

    assert row.color == "green"


def test_a_yellow_does_not_hide_a_later_red(tmp_path):
    connection = build(tmp_path)
    add_check_in(connection, "2026-08-06T16:10:00+00:00", "yellow", "se me olvido una pastilla")
    add_check_in(connection, "2026-08-06T16:12:00+00:00", "red", "me acabo de desmayar")

    row = next(r for r in queue_rows(connection) if r.code == "PV-001")

    assert row.color == "red"
