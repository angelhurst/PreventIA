from .repository import connect


def patient_for_agent(conn, code):
    row = conn.execute(
        "SELECT code, display_name, age, sex, comuna FROM patients WHERE code = ?",
        (code,),
    ).fetchone()
    if row is None:
        return None

    conditions = [
        item["condition"]
        for item in conn.execute(
            "SELECT condition FROM patient_conditions WHERE patient_code = ? ORDER BY condition",
            (code,),
        ).fetchall()
    ]
    medications = [
        {
            "name": item["name"],
            "dose": item["dose"],
            "schedule_text": item["schedule_text"],
            "times_per_day": item["times_per_day"],
        }
        for item in conn.execute(
            "SELECT name, dose, schedule_text, times_per_day FROM medications "
            "WHERE patient_code = ? ORDER BY id",
            (code,),
        ).fetchall()
    ]

    return {
        "code": row["code"],
        "display_name": row["display_name"],
        "age": row["age"],
        "sex": row["sex"],
        "comuna": row["comuna"],
        "conditions": conditions,
        "medications": medications,
    }


def roster_for_intake(conn):
    rows = conn.execute(
        "SELECT code, display_name, age, comuna FROM patients ORDER BY display_name"
    ).fetchall()
    return [dict(row) for row in rows]


def persist(conn, result):
    cursor = conn.execute(
        "INSERT INTO check_ins ("
        " patient_code, occurred_at, patient_message, agent_message,"
        " doses_reported_taken, doses_expected, summary_line"
        ") VALUES (?, ?, ?, ?, ?, ?, ?)",
        (
            result.patient_code,
            result.occurred_at,
            result.patient_message,
            result.agent_message,
            result.doses_reported_taken,
            result.doses_expected,
            result.summary_line,
        ),
    )
    check_in_id = cursor.lastrowid

    for symptom in result.symptoms:
        conn.execute(
            "INSERT INTO symptoms (check_in_id, term, verbatim, mentioned_in_passing)"
            " VALUES (?, ?, ?, ?)",
            (
                check_in_id,
                symptom["term"],
                symptom["verbatim"],
                1 if symptom["mentioned_in_passing"] else 0,
            ),
        )

    conn.execute(
        "INSERT INTO risk_events ("
        " check_in_id, rules_color, rules_reason, model_color, model_reason, final_color"
        ") VALUES (?, ?, ?, ?, ?, ?)",
        (
            check_in_id,
            result.rules_color.value,
            result.rules_reason,
            result.model_color.value,
            result.model_reason,
            result.final_color.value,
        ),
    )

    conn.commit()
    return check_in_id


def persist_crisis(conn, result):
    cursor = conn.execute(
        "INSERT INTO crisis_events ("
        " patient_code, occurred_at, patient_message, agent_message, matched"
        ") VALUES (?, ?, ?, ?, ?)",
        (
            result.patient_code,
            result.occurred_at,
            result.patient_message,
            result.agent_message,
            ", ".join(result.matched),
        ),
    )
    conn.commit()
    return cursor.lastrowid


def open_crises(conn):
    return [
        dict(row)
        for row in conn.execute(
            "SELECT c.*, p.display_name FROM crisis_events c"
            " JOIN patients p ON p.code = c.patient_code"
            " ORDER BY c.occurred_at DESC, c.id DESC"
        ).fetchall()
    ]


__all__ = [
    "connect",
    "patient_for_agent",
    "roster_for_intake",
    "persist",
    "persist_crisis",
    "open_crises",
]
