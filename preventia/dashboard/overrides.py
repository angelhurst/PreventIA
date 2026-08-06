from datetime import datetime

from .audit import DOCTOR_ROLE, NotADoctor, UnknownActor

COLORS = ("green", "yellow", "red")

SCHEMA = """
CREATE TABLE IF NOT EXISTS clinical_overrides (
    id              INTEGER PRIMARY KEY,
    patient_code    TEXT NOT NULL REFERENCES patients(code),
    actor_code      TEXT NOT NULL REFERENCES clinicians(code),
    occurred_at     TEXT NOT NULL,
    color           TEXT NOT NULL CHECK (color IN ('green', 'yellow', 'red')),
    reason          TEXT NOT NULL,
    confirmed_by    TEXT NOT NULL DEFAULT ''
)
"""

APPEND_ONLY = (
    """
    CREATE TRIGGER IF NOT EXISTS clinical_overrides_is_append_only_on_update
    BEFORE UPDATE ON clinical_overrides
    BEGIN
        SELECT RAISE(ABORT, 'clinical_overrides is append-only');
    END
    """,
    """
    CREATE TRIGGER IF NOT EXISTS clinical_overrides_is_append_only_on_delete
    BEFORE DELETE ON clinical_overrides
    BEGIN
        SELECT RAISE(ABORT, 'clinical_overrides is append-only');
    END
    """,
)


class MissingReason(ValueError):
    pass


class UnknownColor(ValueError):
    pass


def ensure_schema(conn):
    conn.execute(SCHEMA)
    for trigger in APPEND_ONLY:
        conn.execute(trigger)
    conn.commit()


def record_override(
    conn, patient_code, color, actor_code, reason, occurred_at=None, confirmed_by=""
):
    ensure_schema(conn)

    if color not in COLORS:
        raise UnknownColor(color)

    actor = conn.execute(
        "SELECT role FROM clinicians WHERE code = ?", (actor_code,)
    ).fetchone()
    if actor is None:
        raise UnknownActor(actor_code)
    if actor["role"] != DOCTOR_ROLE:
        raise NotADoctor(actor_code)

    written_reason = (reason or "").strip()
    if not written_reason:
        raise MissingReason(patient_code)

    patient = conn.execute(
        "SELECT code FROM patients WHERE code = ?", (patient_code,)
    ).fetchone()
    if patient is None:
        raise ValueError(f"unknown patient {patient_code}")

    stamp = occurred_at or datetime.now().astimezone().isoformat(timespec="seconds")
    with conn:
        conn.execute(
            "INSERT INTO clinical_overrides"
            " (patient_code, actor_code, occurred_at, color, reason, confirmed_by)"
            " VALUES (?, ?, ?, ?, ?, ?)",
            (patient_code, actor_code, stamp, color, written_reason, confirmed_by),
        )
    return color, stamp


def latest_by_patient(conn):
    ensure_schema(conn)
    rows = conn.execute(
        """
        SELECT o.patient_code, o.color, o.occurred_at, o.reason, o.actor_code,
               c.display_name AS actor_name
        FROM clinical_overrides o
        JOIN clinicians c ON c.code = o.actor_code
        WHERE o.id = (
            SELECT o2.id FROM clinical_overrides o2
            WHERE o2.patient_code = o.patient_code
            ORDER BY o2.occurred_at DESC, o2.id DESC
            LIMIT 1
        )
        """
    ).fetchall()
    return {row["patient_code"]: dict(row) for row in rows}


def for_patient(conn, patient_code):
    ensure_schema(conn)
    rows = conn.execute(
        """
        SELECT o.color, o.occurred_at, o.reason, o.actor_code, o.confirmed_by,
               c.display_name AS actor_name
        FROM clinical_overrides o
        JOIN clinicians c ON c.code = o.actor_code
        WHERE o.patient_code = ?
        ORDER BY o.occurred_at DESC, o.id DESC
        """,
        (patient_code,),
    ).fetchall()
    return [dict(row) for row in rows]
