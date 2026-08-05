import json
import sqlite3
import sys
from datetime import datetime, timedelta
from pathlib import Path

HERE = Path(__file__).resolve().parent
SCHEMA = HERE / "schema.sql"
COHORT = HERE / "cohort.json"
DEFAULT_DB = HERE / "preventia.db"

STATE_FROM_SPANISH = {
    "pendiente": "pending",
    "en_revision": "in_review",
    "contactado": "contacted",
    "cerrado": "closed",
    "pending": "pending",
    "in_review": "in_review",
    "contacted": "contacted",
    "closed": "closed",
}

COLOR_RANK = {"green": 0, "yellow": 1, "red": 2}


def moment(reference, days_ago, seed):
    hour = 8 + (seed % 5)
    minute = (seed * 17) % 60
    day = reference - timedelta(days=days_ago)
    return day.replace(hour=hour, minute=minute, second=0, microsecond=0).isoformat(
        timespec="seconds"
    )


def translate_state(value):
    if value is None:
        return None
    if value not in STATE_FROM_SPANISH:
        raise ValueError(f"unknown queue state {value!r}")
    return STATE_FROM_SPANISH[value]


def check_semaforo(patient_code, check_in):
    floor = max(COLOR_RANK[check_in["rules_color"]], COLOR_RANK[check_in["model_color"]])
    if COLOR_RANK[check_in["final_color"]] < floor:
        raise ValueError(
            f"{patient_code}: final color {check_in['final_color']} is below the floor set by "
            f"rules={check_in['rules_color']} model={check_in['model_color']}"
        )


def build(db_path, cohort_path=COHORT, reference=None):
    reference = reference or datetime.now()
    cohort = json.loads(Path(cohort_path).read_text(encoding="utf-8"))

    db_path = Path(db_path)
    if db_path.exists():
        db_path.unlink()

    conn = sqlite3.connect(str(db_path))
    conn.row_factory = sqlite3.Row
    conn.executescript(SCHEMA.read_text(encoding="utf-8"))

    for clinician in cohort["clinicians"]:
        conn.execute(
            "INSERT INTO clinicians (code, display_name, role) VALUES (?, ?, ?)",
            (clinician["code"], clinician["display_name"], clinician["role"]),
        )

    check_in_total = 0
    for index, patient in enumerate(cohort["patients"]):
        conn.execute(
            """
            INSERT INTO patients
                (code, display_name, age, sex, comuna, assigned_clinician, enrolled_on)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (
                patient["code"],
                patient["display_name"],
                patient["age"],
                patient["sex"],
                patient["comuna"],
                patient["assigned_clinician"],
                moment(reference, patient["enrolled_days_ago"], index)[:10],
            ),
        )

        for condition in patient["conditions"]:
            conn.execute(
                "INSERT INTO patient_conditions (patient_code, condition) VALUES (?, ?)",
                (patient["code"], condition),
            )

        for medication in patient["medications"]:
            conn.execute(
                """
                INSERT INTO medications
                    (patient_code, name, dose, schedule_text, times_per_day)
                VALUES (?, ?, ?, ?, ?)
                """,
                (
                    patient["code"],
                    medication["name"],
                    medication["dose"],
                    medication["schedule_text"],
                    medication["times_per_day"],
                ),
            )

        for position, check_in in enumerate(patient["check_ins"]):
            check_semaforo(patient["code"], check_in)
            cursor = conn.execute(
                """
                INSERT INTO check_ins
                    (patient_code, occurred_at, patient_message, agent_message,
                     doses_reported_taken, doses_expected, summary_line)
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    patient["code"],
                    moment(reference, check_in["days_ago"], index + position),
                    check_in["patient_message"],
                    check_in["agent_message"],
                    check_in["doses_reported_taken"],
                    check_in["doses_expected"],
                    check_in["summary_line"],
                ),
            )
            check_in_id = cursor.lastrowid
            check_in_total += 1

            conn.execute(
                """
                INSERT INTO risk_events
                    (check_in_id, rules_color, rules_reason, model_color, model_reason, final_color)
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (
                    check_in_id,
                    check_in["rules_color"],
                    check_in["rules_reason"],
                    check_in["model_color"],
                    check_in["model_reason"],
                    check_in["final_color"],
                ),
            )

            for symptom in check_in.get("symptoms", []):
                conn.execute(
                    """
                    INSERT INTO symptoms (check_in_id, term, verbatim, mentioned_in_passing)
                    VALUES (?, ?, ?, ?)
                    """,
                    (
                        check_in_id,
                        symptom["term"],
                        symptom["verbatim"],
                        1 if symptom["mentioned_in_passing"] else 0,
                    ),
                )

        entries = sorted(patient.get("audit", []), key=lambda entry: -entry["days_ago"])
        for position, entry in enumerate(entries):
            conn.execute(
                """
                INSERT INTO escalation_audit
                    (patient_code, from_state, to_state, actor_code, occurred_at, note)
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (
                    patient["code"],
                    translate_state(entry.get("from_state")),
                    translate_state(entry["to_state"]),
                    entry["actor"],
                    moment(reference, entry["days_ago"], index + position + 3),
                    entry.get("note", ""),
                ),
            )

    conn.commit()

    declared_mismatches = []
    for patient in cohort["patients"]:
        declared = translate_state(patient.get("queue_state"))
        actual = conn.execute(
            "SELECT state FROM current_queue_state WHERE patient_code = ?", (patient["code"],)
        ).fetchone()["state"]
        if declared and declared != actual:
            declared_mismatches.append((patient["code"], declared, actual))

    summary = {
        "db": str(db_path),
        "clinicians": len(cohort["clinicians"]),
        "patients": len(cohort["patients"]),
        "check_ins": check_in_total,
        "audit_entries": conn.execute("SELECT COUNT(*) FROM escalation_audit").fetchone()[0],
        "queue_colors": dict(
            conn.execute(
                """
                SELECT r.final_color, COUNT(*)
                FROM latest_check_in l
                JOIN risk_events r ON r.check_in_id = l.id
                GROUP BY r.final_color
                """
            ).fetchall()
        ),
        "declared_state_mismatches": declared_mismatches,
    }
    conn.close()
    return summary


if __name__ == "__main__":
    target = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_DB
    report = build(target)
    for key, value in report.items():
        print(f"{key}: {value}")
