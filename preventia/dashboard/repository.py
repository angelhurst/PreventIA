import sqlite3
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path

from . import overrides as clinical_overrides
from .audit import ensure_confirmation_column

ADHERENCE_WINDOW = 7

COLOR_RANK = {"red": 0, "yellow": 1, "green": 2}
STATE_RANK = {"pending": 0, "in_review": 1, "contacted": 2, "closed": 3}
OPEN_STATES = ("pending", "in_review", "contacted")


@dataclass
class Symptom:
    term: str
    verbatim: str
    mentioned_in_passing: bool


@dataclass
class Medication:
    name: str
    dose: str
    schedule_text: str


@dataclass
class CheckIn:
    id: int
    occurred_at: str
    patient_message: str
    agent_message: str
    doses_reported_taken: int
    doses_expected: int
    summary_line: str
    rules_color: str
    rules_reason: str
    model_color: str
    model_reason: str
    final_color: str
    symptoms: list = field(default_factory=list)


@dataclass
class AuditEntry:
    from_state: str
    to_state: str
    actor_code: str
    actor_name: str
    occurred_at: str
    note: str
    confirmed_by: str = ""
    kind: str = "state"


@dataclass
class OverrideEntry:
    color: str
    reason: str
    actor_code: str
    actor_name: str
    occurred_at: str
    confirmed_by: str = ""
    kind: str = "color"


@dataclass
class QueueRow:
    code: str
    display_name: str
    age: int
    comuna: str
    conditions: list
    color: str
    summary_line: str
    last_contact_at: str
    doses_taken: int
    doses_expected: int
    state: str
    changed_by: str
    changed_at: str
    symptoms: list
    rules_color: str
    model_color: str
    color_set_by_clinician: bool = False
    override_color: str = ""
    override_reason: str = ""
    override_by: str = ""
    override_at: str = ""

    @property
    def model_raised(self):
        return COLOR_RANK[self.model_color] < COLOR_RANK[self.rules_color]

    @property
    def adherence_percent(self):
        if not self.doses_expected:
            return None
        return round(100 * self.doses_taken / self.doses_expected)


@dataclass
class PatientDetail:
    code: str
    display_name: str
    age: int
    sex: str
    comuna: str
    enrolled_on: str
    clinician_name: str
    conditions: list
    medications: list
    check_ins: list
    state: str
    audit: list
    overrides: list = field(default_factory=list)


class MissingClinicalRecord(RuntimeError):
    pass


def connect(db_path):
    path = Path(db_path)
    if not path.exists():
        raise MissingClinicalRecord(str(path))
    conn = sqlite3.connect(str(path))
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    seeded = conn.execute(
        "SELECT name FROM sqlite_master WHERE type = 'table' AND name = 'patients'"
    ).fetchone()
    if seeded is None:
        conn.close()
        raise MissingClinicalRecord(str(path))
    return conn


def _conditions_by_patient(conn):
    rows = conn.execute("SELECT patient_code, condition FROM patient_conditions").fetchall()
    grouped = {}
    for row in rows:
        grouped.setdefault(row["patient_code"], []).append(row["condition"])
    return grouped


def _symptoms_by_check_in(conn, check_in_ids):
    if not check_in_ids:
        return {}
    placeholders = ",".join("?" for _ in check_in_ids)
    rows = conn.execute(
        f"SELECT check_in_id, term, verbatim, mentioned_in_passing "
        f"FROM symptoms WHERE check_in_id IN ({placeholders}) ORDER BY id",
        tuple(check_in_ids),
    ).fetchall()
    grouped = {}
    for row in rows:
        grouped.setdefault(row["check_in_id"], []).append(
            Symptom(row["term"], row["verbatim"], bool(row["mentioned_in_passing"]))
        )
    return grouped


def _adherence_by_patient(conn):
    rows = conn.execute(
        """
        SELECT patient_code,
               SUM(doses_reported_taken) AS taken,
               SUM(doses_expected) AS expected
        FROM (
            SELECT patient_code,
                   doses_reported_taken,
                   doses_expected,
                   ROW_NUMBER() OVER (
                       PARTITION BY patient_code ORDER BY occurred_at DESC, id DESC
                   ) AS recency
            FROM check_ins
        )
        WHERE recency <= ?
        GROUP BY patient_code
        """,
        (ADHERENCE_WINDOW,),
    ).fetchall()
    return {row["patient_code"]: (row["taken"] or 0, row["expected"] or 0) for row in rows}


def _unreviewed_color_by_patient(conn):
    rows = conn.execute(
        """
        SELECT ci.patient_code AS code, re.final_color AS final_color
        FROM check_ins ci
        JOIN risk_events re ON re.check_in_id = ci.id
        JOIN current_queue_state q ON q.patient_code = ci.patient_code
        WHERE ci.occurred_at >= q.changed_at
        """
    ).fetchall()

    highest = {}
    for row in rows:
        colour = row["final_color"] or "green"
        current = highest.get(row["code"], "green")
        highest[row["code"]] = colour if COLOR_RANK[colour] < COLOR_RANK[current] else current
    return highest


def _more_severe(first, second):
    return first if COLOR_RANK[first] <= COLOR_RANK[second] else second


def _instant(value):
    moment = datetime.fromisoformat(value)
    if moment.tzinfo is None:
        return moment.replace(tzinfo=timezone.utc)
    return moment.astimezone(timezone.utc)


def _highest_color_after_each_override(conn, decided):
    if not decided:
        return {}

    rows = conn.execute(
        """
        SELECT ci.patient_code AS code, ci.occurred_at AS occurred_at, re.final_color AS final_color
        FROM check_ins ci
        JOIN risk_events re ON re.check_in_id = ci.id
        """
    ).fetchall()

    highest = {}
    for row in rows:
        override = decided.get(row["code"])
        if override is None:
            continue
        if _instant(row["occurred_at"]) <= _instant(override["occurred_at"]):
            continue
        colour = row["final_color"] or "green"
        highest[row["code"]] = _more_severe(colour, highest.get(row["code"], "green"))
    return highest


def _resolve_color(base, override, escalated_since):
    if override is None:
        return base, False
    decided = override["color"]
    if escalated_since and COLOR_RANK[escalated_since] < COLOR_RANK[decided]:
        return escalated_since, False
    return decided, True


def queue_rows(conn, only_open=False):
    rows = conn.execute(
        """
        SELECT p.code,
               p.display_name,
               p.age,
               p.comuna,
               l.id AS check_in_id,
               l.occurred_at AS last_contact_at,
               l.summary_line,
               r.rules_color,
               r.model_color,
               r.final_color,
               q.state,
               q.changed_at,
               c.display_name AS changed_by
        FROM patients p
        JOIN current_queue_state q ON q.patient_code = p.code
        LEFT JOIN latest_check_in l ON l.patient_code = p.code
        LEFT JOIN risk_events r ON r.check_in_id = l.id
        LEFT JOIN clinicians c ON c.code = q.changed_by
        """
    ).fetchall()

    conditions = _conditions_by_patient(conn)
    adherence = _adherence_by_patient(conn)
    unreviewed = _unreviewed_color_by_patient(conn)
    decided = clinical_overrides.latest_by_patient(conn)
    escalated_since = _highest_color_after_each_override(conn, decided)
    symptoms = _symptoms_by_check_in(conn, [r["check_in_id"] for r in rows if r["check_in_id"]])

    queue = []
    for row in rows:
        if only_open and row["state"] not in OPEN_STATES:
            continue
        taken, expected = adherence.get(row["code"], (0, 0))
        override = decided.get(row["code"])
        color, held_by_clinician = _resolve_color(
            unreviewed.get(row["code"], row["final_color"] or "green"),
            override,
            escalated_since.get(row["code"]),
        )
        queue.append(
            QueueRow(
                code=row["code"],
                display_name=row["display_name"],
                age=row["age"],
                comuna=row["comuna"],
                conditions=conditions.get(row["code"], []),
                color=color,
                summary_line=row["summary_line"] or "",
                last_contact_at=row["last_contact_at"],
                doses_taken=taken,
                doses_expected=expected,
                state=row["state"],
                changed_by=row["changed_by"],
                changed_at=row["changed_at"],
                symptoms=symptoms.get(row["check_in_id"], []),
                rules_color=row["rules_color"] or "green",
                model_color=row["model_color"] or "green",
                color_set_by_clinician=held_by_clinician,
                override_color=override["color"] if override else "",
                override_reason=override["reason"] if held_by_clinician else "",
                override_by=override["actor_name"] if held_by_clinician else "",
                override_at=override["occurred_at"] if held_by_clinician else "",
            )
        )

    queue.sort(
        key=lambda r: (
            COLOR_RANK[r.color],
            STATE_RANK[r.state],
            r.last_contact_at or "",
        )
    )
    return queue


def patient_detail(conn, code):
    patient = conn.execute(
        """
        SELECT p.*, c.display_name AS clinician_name
        FROM patients p
        JOIN clinicians c ON c.code = p.assigned_clinician
        WHERE p.code = ?
        """,
        (code,),
    ).fetchone()
    if patient is None:
        return None

    medications = [
        Medication(row["name"], row["dose"], row["schedule_text"])
        for row in conn.execute(
            "SELECT name, dose, schedule_text FROM medications WHERE patient_code = ? ORDER BY id",
            (code,),
        )
    ]

    check_in_rows = conn.execute(
        """
        SELECT ci.*, r.rules_color, r.rules_reason, r.model_color, r.model_reason, r.final_color
        FROM check_ins ci
        LEFT JOIN risk_events r ON r.check_in_id = ci.id
        WHERE ci.patient_code = ?
        ORDER BY ci.occurred_at DESC, ci.id DESC
        """,
        (code,),
    ).fetchall()
    symptoms = _symptoms_by_check_in(conn, [row["id"] for row in check_in_rows])

    check_ins = [
        CheckIn(
            id=row["id"],
            occurred_at=row["occurred_at"],
            patient_message=row["patient_message"],
            agent_message=row["agent_message"],
            doses_reported_taken=row["doses_reported_taken"],
            doses_expected=row["doses_expected"],
            summary_line=row["summary_line"],
            rules_color=row["rules_color"] or "green",
            rules_reason=row["rules_reason"] or "",
            model_color=row["model_color"] or "green",
            model_reason=row["model_reason"] or "",
            final_color=row["final_color"] or "green",
            symptoms=symptoms.get(row["id"], []),
        )
        for row in check_in_rows
    ]

    ensure_confirmation_column(conn)
    audit = [
        AuditEntry(
            from_state=row["from_state"],
            to_state=row["to_state"],
            actor_code=row["actor_code"],
            actor_name=row["actor_name"],
            occurred_at=row["occurred_at"],
            note=row["note"],
            confirmed_by=row["confirmed_by"],
        )
        for row in conn.execute(
            """
            SELECT a.*, c.display_name AS actor_name
            FROM escalation_audit a
            JOIN clinicians c ON c.code = a.actor_code
            WHERE a.patient_code = ?
            ORDER BY a.occurred_at DESC, a.id DESC
            """,
            (code,),
        )
    ]

    state = conn.execute(
        "SELECT state FROM current_queue_state WHERE patient_code = ?", (code,)
    ).fetchone()["state"]

    conditions = [
        row["condition"]
        for row in conn.execute(
            "SELECT condition FROM patient_conditions WHERE patient_code = ? ORDER BY condition",
            (code,),
        )
    ]

    return PatientDetail(
        code=patient["code"],
        display_name=patient["display_name"],
        age=patient["age"],
        sex=patient["sex"],
        comuna=patient["comuna"],
        enrolled_on=patient["enrolled_on"],
        clinician_name=patient["clinician_name"],
        conditions=conditions,
        medications=medications,
        check_ins=check_ins,
        state=state,
        audit=audit,
        overrides=[
            OverrideEntry(
                color=item["color"],
                reason=item["reason"],
                actor_code=item["actor_code"],
                actor_name=item["actor_name"],
                occurred_at=item["occurred_at"],
                confirmed_by=item["confirmed_by"],
            )
            for item in clinical_overrides.for_patient(conn, code)
        ],
    )


def clinicians(conn):
    return [dict(row) for row in conn.execute("SELECT * FROM clinicians ORDER BY code")]
