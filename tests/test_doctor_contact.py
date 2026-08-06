import sqlite3
from pathlib import Path

import pytest

from preventia.dashboard import audit

SCHEMA = Path(__file__).resolve().parents[1] / "preventia" / "data" / "schema.sql"


@pytest.fixture
def conn():
    connection = sqlite3.connect(":memory:")
    connection.row_factory = sqlite3.Row
    connection.executescript(SCHEMA.read_text(encoding="utf-8"))
    connection.executemany(
        "INSERT INTO clinicians (code, display_name, role) VALUES (?, ?, ?)",
        [
            ("CL-01", "Enfermera Rosa Cárdenas", "enfermera"),
            ("CL-02", "Dr. Ignacio Bustamante", "medico"),
        ],
    )
    connection.execute(
        """
        INSERT INTO patients
            (code, display_name, age, sex, comuna, assigned_clinician, enrolled_on)
        VALUES ('PV-001', 'Prueba Sintética', 80, 'F', 'Ñuñoa', 'CL-01', '2026-07-15')
        """
    )
    connection.commit()
    yield connection
    connection.close()


def audit_rows(conn):
    return conn.execute(
        "SELECT * FROM escalation_audit ORDER BY id"
    ).fetchall()


def test_a_doctor_can_record_a_contact(conn):
    audit.record_doctor_contact(conn, "PV-001", "CL-02", "Llamado telefónico, control adelantado")
    rows = audit_rows(conn)
    assert len(rows) == 1
    assert rows[0]["actor_code"] == "CL-02"
    assert rows[0]["to_state"] == "contacted"
    assert rows[0]["from_state"] == "pending"
    assert rows[0]["note"] == "Llamado telefónico, control adelantado"
    assert rows[0]["occurred_at"]


def test_a_nurse_cannot_record_a_doctor_contact(conn):
    with pytest.raises(audit.NotADoctor):
        audit.record_doctor_contact(conn, "PV-001", "CL-01", "Llamado telefónico")
    assert audit_rows(conn) == []


def test_an_unknown_actor_cannot_record_a_doctor_contact(conn):
    with pytest.raises(audit.UnknownActor):
        audit.record_doctor_contact(conn, "PV-001", "CL-99", "Llamado telefónico")
    assert audit_rows(conn) == []


def test_a_contact_without_a_note_is_refused(conn):
    with pytest.raises(audit.MissingContactNote):
        audit.record_doctor_contact(conn, "PV-001", "CL-02", "   ")
    assert audit_rows(conn) == []


def test_the_contact_is_append_only_like_every_other_transition(conn):
    audit.record_doctor_contact(conn, "PV-001", "CL-02", "Llamado telefónico")
    with pytest.raises(sqlite3.IntegrityError):
        conn.execute("UPDATE escalation_audit SET note = 'alterado'")
    with pytest.raises(sqlite3.IntegrityError):
        conn.execute("DELETE FROM escalation_audit")


def test_the_queue_state_follows_the_contact(conn):
    audit.record_doctor_contact(conn, "PV-001", "CL-02", "Llamado telefónico")
    assert audit.current_state(conn, "PV-001") == "contacted"


def test_the_route_refuses_a_nurse_end_to_end(tmp_path, monkeypatch):
    from fastapi.testclient import TestClient

    db = tmp_path / "preventia.db"
    built = sqlite3.connect(str(db))
    built.executescript(SCHEMA.read_text(encoding="utf-8"))
    built.executemany(
        "INSERT INTO clinicians (code, display_name, role) VALUES (?, ?, ?)",
        [("CL-01", "Enfermera Rosa", "enfermera"), ("CL-02", "Dr. Ignacio", "medico")],
    )
    built.execute(
        """
        INSERT INTO patients
            (code, display_name, age, sex, comuna, assigned_clinician, enrolled_on)
        VALUES ('PV-001', 'Prueba', 80, 'F', 'Ñuñoa', 'CL-01', '2026-07-15')
        """
    )
    built.commit()
    built.close()

    monkeypatch.setenv("PREVENTIA_DB", str(db))
    from preventia.dashboard.app import app

    from preventia.dashboard import auth

    client = TestClient(app)
    client.cookies.set(auth.SESSION_COOKIE, auth.session_token())
    refused = client.post(
        "/cola/PV-001/contacto",
        data={"actor_code": "CL-01", "note": "Llamado"},
        follow_redirects=False,
    )
    assert refused.headers["location"] == "/cola/PV-001?error=solo_medico"

    allowed = client.post(
        "/cola/PV-001/contacto",
        data={"actor_code": "CL-02", "note": "Llamado"},
        follow_redirects=False,
    )
    assert allowed.headers["location"] == "/cola/PV-001"

    check = sqlite3.connect(str(db))
    actors = [row[0] for row in check.execute("SELECT actor_code FROM escalation_audit")]
    check.close()
    assert actors == ["CL-02"]
