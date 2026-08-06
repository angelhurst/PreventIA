import sqlite3

import pytest

from preventia.agent.core import CrisisResult, run_check_in
from preventia.dashboard.intake import persist_crisis
from preventia.data.seed_cohort import build
from preventia.patient_copy import CRISIS_DIVERSION

CRISIS_MESSAGE = "Me tomé los remedios. La verdad es que ya no quiero vivir."

PATIENT = {
    "code": "PV-013",
    "display_name": "Hernán Villalobos Sepúlveda",
    "age": 73,
    "conditions": ["hipertension"],
    "medications": [
        {"name": "Losartán", "dose": "50 mg", "schedule_text": "una en la mañana", "times_per_day": 1}
    ],
}


class ExplodingModel:
    provider = "ninguno"
    model_id = "ninguno"

    def send(self, *args, **kwargs):
        raise AssertionError("the model must never be asked about a crisis message")


@pytest.fixture
def conn(tmp_path):
    build(tmp_path / "preventia.db")
    connection = sqlite3.connect(str(tmp_path / "preventia.db"))
    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA foreign_keys = ON")
    yield connection
    connection.close()


def test_a_crisis_never_reaches_the_model():
    result = run_check_in(PATIENT, CRISIS_MESSAGE, model=ExplodingModel())
    assert isinstance(result, CrisisResult)


def test_the_patient_gets_the_crisis_copy():
    result = run_check_in(PATIENT, CRISIS_MESSAGE, model=ExplodingModel())
    assert result.agent_message == CRISIS_DIVERSION


def test_the_matched_phrase_travels_with_the_result():
    result = run_check_in(PATIENT, CRISIS_MESSAGE, model=ExplodingModel())
    assert "no quiero vivir" in result.matched


def test_a_crisis_result_carries_no_semaforo_color():
    result = run_check_in(PATIENT, CRISIS_MESSAGE, model=ExplodingModel())
    assert not hasattr(result, "final_color")
    assert not hasattr(result, "rules_color")


def test_persisting_a_crisis_writes_no_check_in_and_no_risk_event(conn):
    before = conn.execute("SELECT COUNT(*) FROM check_ins").fetchone()[0]
    risk_before = conn.execute("SELECT COUNT(*) FROM risk_events").fetchone()[0]

    persist_crisis(conn, run_check_in(PATIENT, CRISIS_MESSAGE, model=ExplodingModel()))

    assert conn.execute("SELECT COUNT(*) FROM check_ins").fetchone()[0] == before
    assert conn.execute("SELECT COUNT(*) FROM risk_events").fetchone()[0] == risk_before


def test_the_crisis_event_records_the_patients_own_words(conn):
    persist_crisis(conn, run_check_in(PATIENT, CRISIS_MESSAGE, model=ExplodingModel()))
    row = conn.execute("SELECT * FROM crisis_events").fetchone()
    assert row["patient_code"] == "PV-013"
    assert row["patient_message"] == CRISIS_MESSAGE
    assert row["agent_message"] == CRISIS_DIVERSION


def test_crisis_events_cannot_be_updated(conn):
    persist_crisis(conn, run_check_in(PATIENT, CRISIS_MESSAGE, model=ExplodingModel()))
    with pytest.raises(sqlite3.IntegrityError):
        conn.execute("UPDATE crisis_events SET patient_message = 'otra cosa'")


def test_crisis_events_cannot_be_deleted(conn):
    persist_crisis(conn, run_check_in(PATIENT, CRISIS_MESSAGE, model=ExplodingModel()))
    with pytest.raises(sqlite3.IntegrityError):
        conn.execute("DELETE FROM crisis_events")


def test_an_ordinary_message_still_goes_down_the_normal_path():
    class Recorder:
        provider = "prueba"
        model_id = "prueba"
        called = False

        def send(self, *args, **kwargs):
            Recorder.called = True
            raise RuntimeError("stop here")

    with pytest.raises(RuntimeError):
        run_check_in(PATIENT, "Me tomé el remedio, todo bien.", model=Recorder())
    assert Recorder.called
