import sqlite3
from pathlib import Path

import pytest

from preventia.agent.core import run_check_in
from preventia.agent.models import Reply, ToolCall
from preventia.clinical.extraction import TOOL_NAME
from preventia.clinical.semaforo import Color
from preventia.dashboard import intake

SCHEMA = Path(__file__).resolve().parent.parent / "preventia" / "data" / "schema.sql"

PATIENT = {
    "code": "P-001",
    "display_name": "Rosa Miranda",
    "age": 71,
    "conditions": ["hipertension", "diabetes_tipo_2"],
    "medications": [
        {"name": "Losartan", "dose": "50 mg", "schedule_text": "en la manana", "times_per_day": 1},
        {"name": "Metformina", "dose": "850 mg", "schedule_text": "con las comidas", "times_per_day": 2},
    ],
}


class StubModel:
    provider = "stub"
    model_id = "stub-1"

    def __init__(self, payload):
        self.payload = payload
        self.last_request = None

    def send(self, messages, tools=None, system=None, force_tool=None):
        self.last_request = {"messages": messages, "tools": tools, "system": system}
        return Reply(tool_calls=(ToolCall(TOOL_NAME, self.payload),))


def payload(**overrides):
    base = {
        "dosis_tomadas": 3,
        "sintomas": [],
        "color_sugerido": "green",
        "razon_color": "sin novedades",
        "mensaje_para_el_paciente": "Gracias por contarme. Queda anotado para su equipo.",
        "resumen": "Adherencia completa, sin sintomas.",
    }
    base.update(overrides)
    return base


def edema_payload(color="green"):
    return payload(
        sintomas=[
            {
                "termino": "edema",
                "textual": "ando un poco hinchada de los pies",
                "mencionado_al_pasar": True,
            }
        ],
        color_sugerido=color,
        razon_color="menciono hinchazon",
    )


def test_expected_doses_come_from_the_prescription_not_the_model():
    result = run_check_in(PATIENT, "Me tomé todo.", StubModel(payload(dosis_tomadas=99)))
    assert result.doses_expected == 3
    assert result.doses_reported_taken == 3


def test_symptom_mentioned_in_passing_is_captured_with_its_verbatim():
    result = run_check_in(PATIENT, "Ando hinchada.", StubModel(edema_payload()))
    assert len(result.passing_mentions) == 1
    assert result.passing_mentions[0]["verbatim"] == "ando un poco hinchada de los pies"


def test_rules_raise_the_colour_the_model_tried_to_keep_green():
    result = run_check_in(PATIENT, "Ando hinchada.", StubModel(edema_payload(color="green")))
    assert result.rules_color is Color.RED
    assert result.model_color is Color.GREEN
    assert result.final_color is Color.RED


def test_model_may_raise_above_the_rules_floor():
    result = run_check_in(PATIENT, "Me siento pésimo.", StubModel(payload(color_sugerido="red")))
    assert result.rules_color is Color.GREEN
    assert result.final_color is Color.RED
    assert result.model_was_raised


def test_a_red_by_rules_appends_the_urgency_redirect():
    result = run_check_in(PATIENT, "Ando hinchada.", StubModel(edema_payload()))
    assert "131" in result.agent_message


def test_a_green_does_not_mention_urgency():
    result = run_check_in(PATIENT, "Todo bien.", StubModel(payload()))
    assert "131" not in result.agent_message
    assert not result.escalates


def test_a_model_reply_that_prescribes_is_replaced_by_the_safe_redirect():
    unsafe = payload(mensaje_para_el_paciente="Suspenda el losartán hasta el control.")
    result = run_check_in(PATIENT, "¿Me lo suspendo?", StubModel(unsafe))
    assert result.guardrail_reason == "treatment"
    assert "Suspenda" not in result.agent_message


def test_the_agent_cannot_send_the_patient_to_urgencias_on_a_green_floor():
    pushy = payload(mensaje_para_el_paciente="Vaya al servicio de urgencia ahora mismo.")
    result = run_check_in(PATIENT, "Estoy bien.", StubModel(pushy))
    assert result.guardrail_reason == "urgency"
    assert "urgencia" not in result.agent_message.lower()


def test_the_system_prompt_carries_the_clinical_boundary():
    model = StubModel(payload())
    run_check_in(PATIENT, "Hola.", model)
    system = model.last_request["system"].lower()
    assert "no diagnostica" in system
    assert "no indica, cambia, suspende ni ajusta" in system


@pytest.fixture
def conn(tmp_path):
    db = sqlite3.connect(str(tmp_path / "t.db"))
    db.row_factory = sqlite3.Row
    db.executescript(SCHEMA.read_text(encoding="utf-8"))
    db.execute("INSERT INTO clinicians VALUES ('C-1', 'Matrona', 'matrona')")
    db.execute(
        "INSERT INTO patients VALUES ('P-001', 'Rosa Miranda', 71, 'F', 'Nunoa', 'C-1', '2026-01-01')"
    )
    db.commit()
    yield db
    db.close()


def test_a_check_in_persists_and_the_database_enforces_the_floor(conn):
    result = run_check_in(PATIENT, "Ando hinchada.", StubModel(edema_payload()))
    check_in_id = intake.persist(conn, result)

    stored = conn.execute(
        "SELECT patient_message, agent_message FROM check_ins WHERE id = ?", (check_in_id,)
    ).fetchone()
    assert stored["patient_message"] == "Ando hinchada."
    assert stored["agent_message"]

    event = conn.execute(
        "SELECT rules_color, model_color, final_color FROM risk_events WHERE check_in_id = ?",
        (check_in_id,),
    ).fetchone()
    assert (event["rules_color"], event["model_color"], event["final_color"]) == (
        "red",
        "green",
        "red",
    )

    symptom = conn.execute(
        "SELECT term, mentioned_in_passing FROM symptoms WHERE check_in_id = ?", (check_in_id,)
    ).fetchone()
    assert symptom["term"] == "edema"
    assert symptom["mentioned_in_passing"] == 1


def test_the_database_refuses_a_downgraded_final_colour(conn):
    conn.execute(
        "INSERT INTO check_ins VALUES (99, 'P-001', '2026-08-06', 'x', 'y', 1, 1, 'z')"
    )
    with pytest.raises(sqlite3.IntegrityError):
        conn.execute(
            "INSERT INTO risk_events VALUES (1, 99, 'red', 'edema', 'green', 'nada', 'green')"
        )
