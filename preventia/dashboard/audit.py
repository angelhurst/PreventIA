from datetime import datetime

STATES = ("pending", "in_review", "contacted", "closed")

NEXT_STATE = {
    "pending": "in_review",
    "in_review": "contacted",
    "contacted": "closed",
    "closed": None,
}


class UnknownState(ValueError):
    pass


class UnknownActor(ValueError):
    pass


class NotADoctor(ValueError):
    pass


class MissingContactNote(ValueError):
    pass


DOCTOR_ROLE = "medico"


def current_state(conn, patient_code):
    row = conn.execute(
        "SELECT state FROM current_queue_state WHERE patient_code = ?", (patient_code,)
    ).fetchone()
    if row is None:
        raise ValueError(f"unknown patient {patient_code}")
    return row["state"]


def record_doctor_contact(conn, patient_code, actor_code, note, occurred_at=None):
    actor = conn.execute(
        "SELECT role FROM clinicians WHERE code = ?", (actor_code,)
    ).fetchone()
    if actor is None:
        raise UnknownActor(actor_code)
    if actor["role"] != DOCTOR_ROLE:
        raise NotADoctor(actor_code)
    if not note.strip():
        raise MissingContactNote(patient_code)
    return record_transition(
        conn, patient_code, "contacted", actor_code, note, occurred_at=occurred_at
    )


def record_transition(conn, patient_code, to_state, actor_code, note="", occurred_at=None):
    if to_state not in STATES:
        raise UnknownState(to_state)

    actor = conn.execute(
        "SELECT code FROM clinicians WHERE code = ?", (actor_code,)
    ).fetchone()
    if actor is None:
        raise UnknownActor(actor_code)

    from_state = current_state(conn, patient_code)
    stamp = occurred_at or datetime.now().astimezone().isoformat(timespec="seconds")

    with conn:
        conn.execute(
            """
            INSERT INTO escalation_audit
                (patient_code, from_state, to_state, actor_code, occurred_at, note)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (patient_code, from_state, to_state, actor_code, stamp, note.strip()),
        )
    return from_state, to_state, stamp
