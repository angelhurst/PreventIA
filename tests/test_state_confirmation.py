import sqlite3
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from preventia.dashboard import audit, auth

SCHEMA = Path(__file__).resolve().parents[1] / "preventia" / "data" / "schema.sql"
GOOD_CODE = "0000"
BAD_CODE = "9999"


def build_database(path):
    connection = sqlite3.connect(str(path))
    connection.executescript(SCHEMA.read_text(encoding="utf-8"))
    connection.executemany(
        "INSERT INTO clinicians (code, display_name, role) VALUES (?, ?, ?)",
        [("CL-01", "Enfermera Rosa", "enfermera"), ("CL-02", "Dr. Ignacio", "medico")],
    )
    connection.execute(
        """
        INSERT INTO patients
            (code, display_name, age, sex, comuna, assigned_clinician, enrolled_on)
        VALUES ('PV-001', 'Prueba Sintetica', 71, 'F', 'Nunoa', 'CL-01', '2026-07-15')
        """
    )
    connection.commit()
    connection.close()


@pytest.fixture
def db(tmp_path, monkeypatch):
    path = tmp_path / "preventia.db"
    build_database(path)
    monkeypatch.setenv("PREVENTIA_DB", str(path))
    monkeypatch.setenv("PREVENTIA_DOCTOR_CODE", GOOD_CODE)
    return path


@pytest.fixture
def client(db):
    from preventia.dashboard.app import app

    session = TestClient(app, follow_redirects=False)
    session.cookies.set(auth.SESSION_COOKIE, auth.session_token())
    return session


def audit_rows(db):
    connection = sqlite3.connect(str(db))
    connection.row_factory = sqlite3.Row
    rows = [dict(row) for row in connection.execute("SELECT * FROM escalation_audit ORDER BY id")]
    connection.close()
    return rows


def sent_messages(db):
    connection = sqlite3.connect(str(db))
    try:
        return connection.execute("SELECT COUNT(*) FROM doctor_messages").fetchone()[0]
    except sqlite3.OperationalError:
        return 0
    finally:
        connection.close()


def test_a_state_change_without_a_code_changes_nothing(client, db):
    response = client.post(
        "/cola/PV-001/estado",
        data={"to_state": "in_review", "actor_code": "CL-01", "note": ""},
    )

    assert response.headers["location"] == "/cola/PV-001?error=confirmacion"
    assert audit_rows(db) == []


def test_a_state_change_with_the_wrong_code_changes_nothing(client, db):
    response = client.post(
        "/cola/PV-001/estado",
        data={
            "to_state": "in_review",
            "actor_code": "CL-01",
            "note": "",
            "confirm_code": BAD_CODE,
        },
    )

    assert response.headers["location"] == "/cola/PV-001?error=confirmacion"
    assert audit_rows(db) == []


def test_a_state_change_with_the_right_code_is_recorded(client, db):
    client.post(
        "/cola/PV-001/estado",
        data={
            "to_state": "in_review",
            "actor_code": "CL-01",
            "note": "",
            "confirm_code": GOOD_CODE,
        },
    )

    rows = audit_rows(db)
    assert len(rows) == 1
    assert rows[0]["to_state"] == "in_review"
    assert rows[0]["confirmed_by"] == "CL-01"


def test_a_doctor_contact_without_a_code_changes_nothing(client, db):
    response = client.post(
        "/cola/PV-001/contacto",
        data={"actor_code": "CL-02", "note": "Llamado telefonico"},
    )

    assert response.headers["location"] == "/cola/PV-001?error=confirmacion"
    assert audit_rows(db) == []


def test_a_doctor_contact_with_the_right_code_records_who_confirmed(client, db):
    client.post(
        "/cola/PV-001/contacto",
        data={
            "actor_code": "CL-02",
            "note": "Llamado telefonico",
            "confirm_code": GOOD_CODE,
        },
    )

    rows = audit_rows(db)
    assert len(rows) == 1
    assert rows[0]["actor_code"] == "CL-02"
    assert rows[0]["confirmed_by"] == "CL-02"


def test_a_message_without_a_code_is_not_sent(client, db):
    response = client.post(
        "/cola/PV-001/mensaje",
        data={"actor_code": "CL-02", "body": "La espero manana."},
    )

    assert response.headers["location"] == "/cola/PV-001?error=confirmacion"
    assert sent_messages(db) == 0


def test_an_unconfirmed_transition_is_marked_as_unconfirmed_in_the_record(tmp_path):
    path = tmp_path / "direct.db"
    build_database(path)
    connection = sqlite3.connect(str(path))
    connection.row_factory = sqlite3.Row

    audit.record_transition(connection, "PV-001", "in_review", "CL-01")

    row = connection.execute("SELECT confirmed_by FROM escalation_audit").fetchone()
    connection.close()
    assert row["confirmed_by"] == ""


def test_the_queue_asks_for_the_code_before_moving_a_case(client):
    page = client.get("/cola")

    assert page.status_code == 200
    assert 'name="confirm_code"' in page.text


def test_the_record_asks_for_the_code_in_every_form_that_writes(client):
    from preventia.dashboard.app import ACTOR_COOKIE

    client.cookies.set(ACTOR_COOKIE, "CL-02")
    page = client.get("/cola/PV-001")

    assert page.status_code == 200
    assert page.text.count('name="confirm_code"') == 4


def test_a_wrong_code_is_explained_on_the_record(client):
    page = client.get("/cola/PV-001?error=confirmacion")

    assert "no coincide" in page.text
