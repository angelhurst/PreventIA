import sqlite3
from pathlib import Path

import pytest

from preventia.channels.base import Receipt, normalise_recipient, InvalidRecipient
from preventia.channels.local_console import LocalConsoleChannel
from preventia.dashboard import audit, messaging

SCHEMA = Path(__file__).resolve().parents[1] / "preventia" / "data" / "schema.sql"


class StubChannel:
    name = "stub"

    def __init__(self, delivered=True, detail=""):
        self.delivered = delivered
        self.detail = detail
        self.sent = []

    def send(self, recipient, text):
        self.sent.append((recipient, text))
        return Receipt(self.delivered, self.name, reference="wamid.TEST", detail=self.detail)


@pytest.fixture
def conn(monkeypatch):
    monkeypatch.setenv("PREVENTIA_PATIENT_DIRECTORY", "56911112222=PV-001")
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
        "INSERT INTO patients (code, display_name, age, sex, comuna, assigned_clinician, enrolled_on)"
        " VALUES ('PV-001', 'Prueba Sintética', 80, 'F', 'Ñuñoa', 'CL-01', '2026-07-15')"
    )
    connection.commit()
    yield connection
    connection.close()


def test_a_doctor_can_send_a_message(conn):
    channel = StubChannel()
    receipt = messaging.send_doctor_message(conn, "PV-001", "CL-02", "Hola, la espero mañana.", channel)
    assert receipt.delivered
    assert channel.sent == [("56911112222", "Hola, la espero mañana.")]


def test_a_nurse_cannot_send_a_message(conn):
    channel = StubChannel()
    with pytest.raises(audit.NotADoctor):
        messaging.send_doctor_message(conn, "PV-001", "CL-01", "Hola.", channel)
    assert channel.sent == []


def test_an_empty_message_is_refused(conn):
    with pytest.raises(messaging.EmptyMessage):
        messaging.send_doctor_message(conn, "PV-001", "CL-02", "   ", StubChannel())


def test_a_sent_message_is_persisted_and_readable(conn):
    messaging.send_doctor_message(conn, "PV-001", "CL-02", "La espero mañana.", StubChannel())
    thread = messaging.messages_for(conn, "PV-001")
    assert len(thread) == 1
    assert thread[0]["body"] == "La espero mañana."
    assert thread[0]["delivered"] == 1
    assert thread[0]["actor_name"] == "Dr. Ignacio Bustamante"


def test_a_failed_send_is_recorded_as_not_delivered(conn):
    channel = StubChannel(delivered=False, detail="la ventana de 24 horas esta cerrada")
    receipt = messaging.send_doctor_message(conn, "PV-001", "CL-02", "Hola.", channel)
    assert not receipt.delivered
    thread = messaging.messages_for(conn, "PV-001")
    assert thread[0]["delivered"] == 0
    assert "24 horas" in thread[0]["detail"]


def test_a_failed_send_still_leaves_a_record(conn):
    messaging.send_doctor_message(conn, "PV-001", "CL-02", "Hola.", StubChannel(delivered=False))
    assert len(messaging.messages_for(conn, "PV-001")) == 1


def test_a_patient_outside_the_channel_directory_cannot_be_written_to(conn):
    channel = StubChannel()
    with pytest.raises(messaging.MissingRecipient):
        messaging.send_doctor_message(conn, "PV-003", "CL-02", "Hola.", channel)
    assert channel.sent == []


def test_without_a_directory_the_send_is_refused(conn, monkeypatch):
    monkeypatch.delenv("PREVENTIA_PATIENT_DIRECTORY", raising=False)
    with pytest.raises(messaging.MissingRecipient):
        messaging.send_doctor_message(conn, "PV-001", "CL-02", "Hola.", StubChannel())


def test_the_destination_comes_from_the_channel_directory(conn):
    assert messaging.recipient_for("PV-001") == "56911112222"
    assert messaging.reachable("PV-001")
    assert not messaging.reachable("PV-003")


def test_the_clinical_record_never_stores_a_phone_number(conn):
    messaging.ensure_schema(conn)
    columns = {row["name"] for row in conn.execute("PRAGMA table_info(patients)").fetchall()}
    assert "phone" not in columns


def test_the_schema_migration_is_idempotent(conn):
    messaging.ensure_schema(conn)
    messaging.ensure_schema(conn)
    tables = {
        row["name"]
        for row in conn.execute("SELECT name FROM sqlite_master WHERE type = 'table'").fetchall()
    }
    assert "doctor_messages" in tables


@pytest.mark.parametrize(
    "raw,expected",
    [
        ("+56912345678", "+56912345678"),
        ("56912345678", "+56912345678"),
        ("+56 9 1234 5678", "+56912345678"),
        ("+56-9-1234-5678", "+56912345678"),
    ],
)
def test_recipients_are_normalised_to_e164(raw, expected):
    assert normalise_recipient(raw) == expected


@pytest.mark.parametrize("raw", ["", "hola", "+", "123"])
def test_a_bad_recipient_is_rejected(raw):
    with pytest.raises(InvalidRecipient):
        normalise_recipient(raw)


def test_the_console_channel_writes_the_message_to_the_outbox(tmp_path):
    outbox = tmp_path / "outbox.log"
    receipt = LocalConsoleChannel(outbox=outbox).send("+56911112222", "Hola.")
    assert receipt.delivered
    assert "Hola." in outbox.read_text(encoding="utf-8")
