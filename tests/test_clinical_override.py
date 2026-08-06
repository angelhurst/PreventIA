import sqlite3
from pathlib import Path

import pytest

from preventia.dashboard import overrides
from preventia.dashboard.repository import queue_rows

SCHEMA = Path(__file__).resolve().parents[1] / "preventia" / "data" / "schema.sql"


@pytest.fixture
def conn(tmp_path):
    connection = sqlite3.connect(tmp_path / "override.db")
    connection.row_factory = sqlite3.Row
    connection.executescript(SCHEMA.read_text(encoding="utf-8"))
    connection.executemany(
        "INSERT INTO clinicians (code, display_name, role) VALUES (?, ?, ?)",
        [("CL-01", "Enfermera Rosa", "enfermera"), ("CL-02", "Dr. Ignacio", "medico")],
    )
    connection.execute(
        "INSERT INTO patients (code, display_name, age, sex, comuna, assigned_clinician, enrolled_on)"
        " VALUES ('PV-001', 'Hilda', 71, 'F', 'Quinta Normal', 'CL-01', '2026-01-01')"
    )
    connection.execute(
        "INSERT INTO escalation_audit (patient_code, from_state, to_state, actor_code, occurred_at, note)"
        " VALUES ('PV-001', 'pending', 'in_review', 'CL-02', '2026-08-06T16:00:00+00:00', '')"
    )
    connection.commit()
    yield connection
    connection.close()


def add_check_in(conn, occurred_at, colour, message="hola"):
    cursor = conn.execute(
        "INSERT INTO check_ins (patient_code, occurred_at, patient_message, agent_message,"
        " doses_reported_taken, doses_expected, summary_line) VALUES (?, ?, ?, '', 4, 4, ?)",
        ("PV-001", occurred_at, message, message),
    )
    conn.execute(
        "INSERT INTO risk_events (check_in_id, rules_color, rules_reason, model_color,"
        " model_reason, final_color) VALUES (?, ?, '', ?, '', ?)",
        (cursor.lastrowid, colour, colour, colour),
    )
    conn.commit()


def colour_of(conn):
    return next(row for row in queue_rows(conn) if row.code == "PV-001").color


def row_of(conn):
    return next(row for row in queue_rows(conn) if row.code == "PV-001")


def test_a_clinician_can_lower_a_colour_the_rules_set(conn):
    add_check_in(conn, "2026-08-06T16:12:00+00:00", "red", "siento dolor en el pecho")
    assert colour_of(conn) == "red"

    overrides.record_override(
        conn,
        "PV-001",
        "yellow",
        "CL-02",
        "baja gravedad por confirmacion de asistencia de SAMU",
        occurred_at="2026-08-06T16:30:00+00:00",
    )

    assert colour_of(conn) == "yellow"


def test_an_override_can_never_suppress_a_later_escalation(conn):
    add_check_in(conn, "2026-08-06T16:12:00+00:00", "red")
    overrides.record_override(
        conn, "PV-001", "green", "CL-02", "revisada en box", occurred_at="2026-08-06T16:30:00+00:00"
    )
    assert colour_of(conn) == "green"

    add_check_in(conn, "2026-08-06T18:00:00+00:00", "red", "volvio el dolor")

    assert colour_of(conn) == "red"


def test_a_calmer_check_in_after_the_override_does_not_raise_the_colour_back(conn):
    add_check_in(conn, "2026-08-06T16:12:00+00:00", "green")
    overrides.record_override(
        conn, "PV-001", "yellow", "CL-02", "control adelantado", occurred_at="2026-08-06T16:30:00+00:00"
    )

    add_check_in(conn, "2026-08-06T18:00:00+00:00", "green", "todo bien")

    assert colour_of(conn) == "yellow"


def test_the_newest_override_is_the_one_that_counts(conn):
    add_check_in(conn, "2026-08-06T16:12:00+00:00", "red")
    overrides.record_override(
        conn, "PV-001", "green", "CL-02", "revisada en box", occurred_at="2026-08-06T16:30:00+00:00"
    )
    overrides.record_override(
        conn, "PV-001", "yellow", "CL-02", "sigue con molestias", occurred_at="2026-08-06T17:00:00+00:00"
    )

    assert colour_of(conn) == "yellow"


def test_an_override_without_a_reason_is_refused_and_writes_nothing(conn):
    add_check_in(conn, "2026-08-06T16:12:00+00:00", "red")

    with pytest.raises(overrides.MissingReason):
        overrides.record_override(conn, "PV-001", "green", "CL-02", "   ")

    assert overrides.for_patient(conn, "PV-001") == []
    assert colour_of(conn) == "red"


def test_only_a_doctor_can_change_the_colour(conn):
    add_check_in(conn, "2026-08-06T16:12:00+00:00", "red")

    with pytest.raises(overrides.NotADoctor):
        overrides.record_override(conn, "PV-001", "green", "CL-01", "me parece que esta bien")

    assert overrides.for_patient(conn, "PV-001") == []
    assert colour_of(conn) == "red"


def test_a_colour_outside_the_semaforo_is_refused(conn):
    with pytest.raises(overrides.UnknownColor):
        overrides.record_override(conn, "PV-001", "azul", "CL-02", "sin sentido")

    assert overrides.for_patient(conn, "PV-001") == []


def test_the_record_of_an_override_cannot_be_edited_or_deleted(conn):
    overrides.record_override(conn, "PV-001", "green", "CL-02", "revisada en box")

    with pytest.raises(sqlite3.IntegrityError):
        conn.execute("UPDATE clinical_overrides SET reason = 'otra cosa'")
    with pytest.raises(sqlite3.IntegrityError):
        conn.execute("DELETE FROM clinical_overrides")


def test_the_model_still_cannot_lower_a_colour_the_rules_set(conn):
    cursor = conn.execute(
        "INSERT INTO check_ins (patient_code, occurred_at, patient_message, agent_message,"
        " doses_reported_taken, doses_expected, summary_line)"
        " VALUES ('PV-001', '2026-08-06T16:12:00+00:00', 'dolor en el pecho', '', 4, 4, '')"
    )

    with pytest.raises(sqlite3.IntegrityError):
        conn.execute(
            "INSERT INTO risk_events (check_in_id, rules_color, rules_reason, model_color,"
            " model_reason, final_color) VALUES (?, 'red', '', 'green', '', 'green')",
            (cursor.lastrowid,),
        )


def test_the_model_cannot_lower_a_colour_a_clinician_set_either(conn):
    add_check_in(conn, "2026-08-06T16:12:00+00:00", "red")
    overrides.record_override(
        conn, "PV-001", "yellow", "CL-02", "evaluada por telefono", occurred_at="2026-08-06T16:30:00+00:00"
    )

    add_check_in(conn, "2026-08-06T18:00:00+00:00", "green", "me equivoque, estoy bien")

    assert colour_of(conn) == "yellow"


def test_the_queue_row_says_the_colour_came_from_a_person(conn):
    add_check_in(conn, "2026-08-06T16:12:00+00:00", "red")
    overrides.record_override(
        conn,
        "PV-001",
        "yellow",
        "CL-02",
        "baja gravedad por confirmacion de asistencia de SAMU",
        occurred_at="2026-08-06T16:30:00+00:00",
    )

    row = row_of(conn)

    assert row.color_set_by_clinician
    assert row.override_by == "Dr. Ignacio"
    assert row.override_reason == "baja gravedad por confirmacion de asistencia de SAMU"


def test_a_row_without_an_override_does_not_claim_one(conn):
    add_check_in(conn, "2026-08-06T16:12:00+00:00", "red")

    row = row_of(conn)

    assert not row.color_set_by_clinician
    assert row.override_reason == ""


def test_a_later_escalation_takes_the_card_off_the_override(conn):
    add_check_in(conn, "2026-08-06T16:12:00+00:00", "red")
    overrides.record_override(
        conn, "PV-001", "green", "CL-02", "revisada en box", occurred_at="2026-08-06T16:30:00+00:00"
    )
    add_check_in(conn, "2026-08-06T18:00:00+00:00", "red", "volvio el dolor")

    row = row_of(conn)

    assert row.color == "red"
    assert not row.color_set_by_clinician


def build_route_database(path):
    connection = sqlite3.connect(str(path))
    connection.executescript(SCHEMA.read_text(encoding="utf-8"))
    connection.executemany(
        "INSERT INTO clinicians (code, display_name, role) VALUES (?, ?, ?)",
        [("CL-01", "Enfermera Rosa", "enfermera"), ("CL-02", "Dr. Ignacio", "medico")],
    )
    connection.execute(
        "INSERT INTO patients (code, display_name, age, sex, comuna, assigned_clinician, enrolled_on)"
        " VALUES ('PV-001', 'Hilda', 71, 'F', 'Quinta Normal', 'CL-01', '2026-01-01')"
    )
    cursor = connection.execute(
        "INSERT INTO check_ins (patient_code, occurred_at, patient_message, agent_message,"
        " doses_reported_taken, doses_expected, summary_line)"
        " VALUES ('PV-001', '2026-08-06T16:12:00+00:00', 'siento dolor en el pecho', '', 4, 4, 'dolor')"
    )
    connection.execute(
        "INSERT INTO risk_events (check_in_id, rules_color, rules_reason, model_color,"
        " model_reason, final_color) VALUES (?, 'red', 'dolor toracico', 'red', '', 'red')",
        (cursor.lastrowid,),
    )
    connection.commit()
    connection.close()


@pytest.fixture
def route(tmp_path, monkeypatch):
    from fastapi.testclient import TestClient

    from preventia.dashboard import auth

    path = tmp_path / "preventia.db"
    build_route_database(path)
    monkeypatch.setenv("PREVENTIA_DB", str(path))
    monkeypatch.setenv("PREVENTIA_DOCTOR_CODE", "0000")

    from preventia.dashboard.app import app

    client = TestClient(app, follow_redirects=False)
    client.cookies.set(auth.SESSION_COOKIE, auth.session_token())
    return client, path


def stored_overrides(path):
    connection = sqlite3.connect(str(path))
    connection.row_factory = sqlite3.Row
    try:
        return [dict(row) for row in connection.execute("SELECT * FROM clinical_overrides")]
    except sqlite3.OperationalError:
        return []
    finally:
        connection.close()


def queue_color(path):
    connection = sqlite3.connect(str(path))
    connection.row_factory = sqlite3.Row
    try:
        return next(row for row in queue_rows(connection) if row.code == "PV-001").color
    finally:
        connection.close()


def test_the_route_lowers_the_colour_and_the_queue_follows(route):
    client, path = route
    assert queue_color(path) == "red"

    response = client.post(
        "/cola/PV-001/color",
        data={
            "color": "yellow",
            "actor_code": "CL-02",
            "reason": "baja gravedad por confirmacion de asistencia de SAMU",
            "confirm_code": "0000",
        },
    )

    assert response.headers["location"] == "/cola/PV-001"
    assert queue_color(path) == "yellow"


def test_the_route_refuses_a_colour_change_without_the_code(route):
    client, path = route

    response = client.post(
        "/cola/PV-001/color",
        data={"color": "green", "actor_code": "CL-02", "reason": "revisada en box"},
    )

    assert response.headers["location"] == "/cola/PV-001?error=confirmacion"
    assert stored_overrides(path) == []
    assert queue_color(path) == "red"


def test_the_route_refuses_an_empty_reason(route):
    client, path = route

    response = client.post(
        "/cola/PV-001/color",
        data={"color": "green", "actor_code": "CL-02", "reason": "   ", "confirm_code": "0000"},
    )

    assert response.headers["location"] == "/cola/PV-001?error=color_sin_razon"
    assert stored_overrides(path) == []
    assert queue_color(path) == "red"


def test_the_route_refuses_a_nurse(route):
    client, path = route

    response = client.post(
        "/cola/PV-001/color",
        data={
            "color": "green",
            "actor_code": "CL-01",
            "reason": "me parece que esta bien",
            "confirm_code": "0000",
        },
    )

    assert response.headers["location"] == "/cola/PV-001?error=color_solo_medico"
    assert stored_overrides(path) == []


def test_the_ficha_shows_who_changed_the_colour_and_why(route):
    from preventia.dashboard.app import ACTOR_COOKIE

    client, path = route
    client.cookies.set(ACTOR_COOKIE, "CL-02")
    client.post(
        "/cola/PV-001/color",
        data={
            "color": "yellow",
            "actor_code": "CL-02",
            "reason": "baja gravedad por confirmacion de asistencia de SAMU",
            "confirm_code": "0000",
        },
    )

    page = client.get("/cola/PV-001").text

    assert "baja gravedad por confirmacion de asistencia de SAMU" in page
    assert "Dr. Ignacio" in page
    assert "Cambio de color" in page


def test_the_queue_card_says_a_person_set_the_colour(route):
    client, path = route
    client.post(
        "/cola/PV-001/color",
        data={
            "color": "green",
            "actor_code": "CL-02",
            "reason": "evaluada en box, sin urgencia",
            "confirm_code": "0000",
        },
    )

    page = client.get("/cola").text

    assert "Este color lo puso el equipo, no las reglas" in page
    assert "evaluada en box, sin urgencia" in page
