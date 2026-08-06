import os
from datetime import datetime

from ..channels import build_channel
from ..channels.base import ChannelError
from .audit import DOCTOR_ROLE, NotADoctor, UnknownActor

MAX_BODY = 900


class MissingRecipient(ValueError):
    pass


class EmptyMessage(ValueError):
    pass


SCHEMA = """
CREATE TABLE IF NOT EXISTS doctor_messages (
    id              INTEGER PRIMARY KEY,
    patient_code    TEXT NOT NULL REFERENCES patients(code),
    actor_code      TEXT NOT NULL REFERENCES clinicians(code),
    occurred_at     TEXT NOT NULL,
    body            TEXT NOT NULL,
    channel         TEXT NOT NULL,
    delivered       INTEGER NOT NULL CHECK (delivered IN (0, 1)),
    reference       TEXT NOT NULL DEFAULT '',
    detail          TEXT NOT NULL DEFAULT ''
)
"""


def ensure_schema(conn):
    conn.execute(SCHEMA)
    columns = {row["name"] for row in conn.execute("PRAGMA table_info(patients)").fetchall()}
    if "phone" not in columns:
        conn.execute("ALTER TABLE patients ADD COLUMN phone TEXT")
    conn.commit()


def recipient_for(conn, patient_code):
    ensure_schema(conn)
    row = conn.execute(
        "SELECT phone FROM patients WHERE code = ?", (patient_code,)
    ).fetchone()
    stored = (row["phone"] if row and row["phone"] else "") or ""
    fallback = os.environ.get("PREVENTIA_DEMO_RECIPIENT", "")
    recipient = stored.strip() or fallback.strip()
    if not recipient:
        raise MissingRecipient(
            "esta persona no tiene telefono registrado y no hay PREVENTIA_DEMO_RECIPIENT en .env"
        )
    return recipient


def _assert_doctor(conn, actor_code):
    actor = conn.execute(
        "SELECT role FROM clinicians WHERE code = ?", (actor_code,)
    ).fetchone()
    if actor is None:
        raise UnknownActor(actor_code)
    if actor["role"] != DOCTOR_ROLE:
        raise NotADoctor(actor_code)


def send_doctor_message(conn, patient_code, actor_code, body, channel=None):
    ensure_schema(conn)
    _assert_doctor(conn, actor_code)

    text = (body or "").strip()
    if not text:
        raise EmptyMessage(patient_code)
    text = text[:MAX_BODY]

    recipient = recipient_for(conn, patient_code)
    transport = channel or build_channel()

    try:
        receipt = transport.send(recipient, text)
    except ChannelError as exc:
        receipt = _failed(transport, str(exc))

    stamp = datetime.now().astimezone().isoformat(timespec="seconds")
    with conn:
        conn.execute(
            "INSERT INTO doctor_messages ("
            " patient_code, actor_code, occurred_at, body, channel, delivered, reference, detail"
            ") VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
            (
                patient_code,
                actor_code,
                stamp,
                text,
                receipt.channel,
                1 if receipt.delivered else 0,
                receipt.reference,
                receipt.detail,
            ),
        )
    return receipt


def _failed(transport, detail):
    from ..channels.base import Receipt

    return Receipt(False, getattr(transport, "name", "desconocido"), detail=detail)


def messages_for(conn, patient_code):
    ensure_schema(conn)
    rows = conn.execute(
        "SELECT m.occurred_at, m.body, m.channel, m.delivered, m.detail, m.reference,"
        " c.display_name AS actor_name"
        " FROM doctor_messages m"
        " JOIN clinicians c ON c.code = m.actor_code"
        " WHERE m.patient_code = ?"
        " ORDER BY m.occurred_at DESC, m.id DESC",
        (patient_code,),
    ).fetchall()
    return [dict(row) for row in rows]
