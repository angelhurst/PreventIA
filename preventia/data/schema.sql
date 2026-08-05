PRAGMA foreign_keys = ON;

CREATE TABLE clinicians (
    code            TEXT PRIMARY KEY,
    display_name    TEXT NOT NULL,
    role            TEXT NOT NULL
);

CREATE TABLE patients (
    code                TEXT PRIMARY KEY,
    display_name        TEXT NOT NULL,
    age                 INTEGER NOT NULL,
    sex                 TEXT NOT NULL,
    comuna              TEXT NOT NULL,
    assigned_clinician  TEXT NOT NULL REFERENCES clinicians(code),
    enrolled_on         TEXT NOT NULL
);

CREATE TABLE patient_conditions (
    patient_code    TEXT NOT NULL REFERENCES patients(code),
    condition       TEXT NOT NULL,
    PRIMARY KEY (patient_code, condition)
);

CREATE TABLE medications (
    id              INTEGER PRIMARY KEY,
    patient_code    TEXT NOT NULL REFERENCES patients(code),
    name            TEXT NOT NULL,
    dose            TEXT NOT NULL,
    schedule_text   TEXT NOT NULL,
    times_per_day   INTEGER NOT NULL
);

CREATE TABLE check_ins (
    id                      INTEGER PRIMARY KEY,
    patient_code            TEXT NOT NULL REFERENCES patients(code),
    occurred_at             TEXT NOT NULL,
    patient_message         TEXT NOT NULL,
    agent_message           TEXT NOT NULL,
    doses_reported_taken    INTEGER NOT NULL,
    doses_expected          INTEGER NOT NULL,
    summary_line            TEXT NOT NULL
);

CREATE TABLE symptoms (
    id                      INTEGER PRIMARY KEY,
    check_in_id             INTEGER NOT NULL REFERENCES check_ins(id),
    term                    TEXT NOT NULL,
    verbatim                TEXT NOT NULL,
    mentioned_in_passing    INTEGER NOT NULL CHECK (mentioned_in_passing IN (0, 1))
);

CREATE TABLE risk_events (
    id              INTEGER PRIMARY KEY,
    check_in_id     INTEGER NOT NULL UNIQUE REFERENCES check_ins(id),
    rules_color     TEXT NOT NULL CHECK (rules_color IN ('green', 'yellow', 'red')),
    rules_reason    TEXT NOT NULL,
    model_color     TEXT NOT NULL CHECK (model_color IN ('green', 'yellow', 'red')),
    model_reason    TEXT NOT NULL,
    final_color     TEXT NOT NULL CHECK (final_color IN ('green', 'yellow', 'red')),
    CHECK (
        (CASE final_color WHEN 'green' THEN 0 WHEN 'yellow' THEN 1 WHEN 'red' THEN 2 END)
        >=
        (CASE rules_color WHEN 'green' THEN 0 WHEN 'yellow' THEN 1 WHEN 'red' THEN 2 END)
    ),
    CHECK (
        (CASE final_color WHEN 'green' THEN 0 WHEN 'yellow' THEN 1 WHEN 'red' THEN 2 END)
        >=
        (CASE model_color WHEN 'green' THEN 0 WHEN 'yellow' THEN 1 WHEN 'red' THEN 2 END)
    )
);

CREATE TABLE escalation_audit (
    id              INTEGER PRIMARY KEY,
    patient_code    TEXT NOT NULL REFERENCES patients(code),
    from_state      TEXT CHECK (from_state IN ('pending', 'in_review', 'contacted', 'closed')),
    to_state        TEXT NOT NULL CHECK (to_state IN ('pending', 'in_review', 'contacted', 'closed')),
    actor_code      TEXT NOT NULL REFERENCES clinicians(code),
    occurred_at     TEXT NOT NULL,
    note            TEXT NOT NULL DEFAULT ''
);

CREATE TRIGGER escalation_audit_is_append_only_on_update
BEFORE UPDATE ON escalation_audit
BEGIN
    SELECT RAISE(ABORT, 'escalation_audit is append-only, see ADR-0014');
END;

CREATE TRIGGER escalation_audit_is_append_only_on_delete
BEFORE DELETE ON escalation_audit
BEGIN
    SELECT RAISE(ABORT, 'escalation_audit is append-only, see ADR-0014');
END;

CREATE INDEX idx_check_ins_patient ON check_ins(patient_code, occurred_at DESC, id DESC);
CREATE INDEX idx_symptoms_check_in ON symptoms(check_in_id);
CREATE INDEX idx_audit_patient ON escalation_audit(patient_code, occurred_at DESC, id DESC);

CREATE VIEW latest_check_in AS
SELECT c.*
FROM check_ins c
WHERE c.id = (
    SELECT c2.id
    FROM check_ins c2
    WHERE c2.patient_code = c.patient_code
    ORDER BY c2.occurred_at DESC, c2.id DESC
    LIMIT 1
);

CREATE VIEW current_queue_state AS
SELECT
    p.code                              AS patient_code,
    COALESCE(a.to_state, 'pending')     AS state,
    a.actor_code                        AS changed_by,
    a.occurred_at                       AS changed_at,
    a.note                              AS note
FROM patients p
LEFT JOIN escalation_audit a ON a.id = (
    SELECT a2.id
    FROM escalation_audit a2
    WHERE a2.patient_code = p.code
    ORDER BY a2.occurred_at DESC, a2.id DESC
    LIMIT 1
);
