import json
from pathlib import Path

import pytest

from preventia.clinical.guardrails import Inspection, Violation, inspect
from preventia.clinical.semaforo import Color
from preventia.patient_copy import SAFE_REDIRECT

COHORT = Path(__file__).resolve().parent.parent / "preventia" / "data" / "cohort.json"

ACKNOWLEDGEMENT = "Anoto sus siete remedios tomados. ¿Cómo se ha sentido hoy?"


def test_a_plain_check_in_acknowledgement_reaches_the_patient():
    result = inspect(ACKNOWLEDGEMENT, rules_color=Color.GREEN)
    assert result.allowed
    assert result.violations == []


def test_an_allowed_message_goes_out_unchanged():
    result = inspect(ACKNOWLEDGEMENT, rules_color=Color.GREEN)
    assert result.message == ACKNOWLEDGEMENT


def test_an_allowed_message_does_not_raise_the_case_for_review():
    result = inspect(ACKNOWLEDGEMENT, rules_color=Color.GREEN)
    assert result.raise_for_review is False


def test_asking_whether_the_medication_was_taken_is_not_a_violation():
    result = inspect("¿Se tomó sus remedios de la noche?", rules_color=Color.GREEN)
    assert result.allowed


def test_refusing_to_advise_is_not_itself_a_violation():
    message = (
        "Yo no soy médico y no puedo indicarle nada sobre sus remedios. "
        "Eso lo ve el equipo del consultorio."
    )
    result = inspect(message, rules_color=Color.GREEN)
    assert result.allowed


def test_suspending_a_medication_is_blocked():
    result = inspect("Suspenda el losartán hasta que la vea el doctor.", rules_color=Color.GREEN)
    assert Violation.TREATMENT in result.violations


def test_telling_the_patient_to_stop_taking_something_is_blocked():
    result = inspect("Deje de tomar la hidroclorotiazida por ahora.", rules_color=Color.GREEN)
    assert Violation.TREATMENT in result.violations


def test_starting_a_medication_is_blocked():
    result = inspect("Empiece a tomar media aspirina en la mañana.", rules_color=Color.GREEN)
    assert Violation.TREATMENT in result.violations


def test_blocking_ignores_case_and_accents():
    result = inspect("SUSPENDA EL LOSARTAN HASTA MANANA.", rules_color=Color.GREEN)
    assert Violation.TREATMENT in result.violations


def test_doubling_a_forgotten_dose_is_blocked():
    result = inspect("Si ayer se le olvidó, hoy tómese dos.", rules_color=Color.GREEN)
    assert Violation.DOSE in result.violations


def test_raising_a_dose_is_blocked():
    result = inspect("Suba la dosis de metformina a dos tabletas.", rules_color=Color.GREEN)
    assert Violation.DOSE in result.violations


def test_lowering_a_dose_is_blocked():
    result = inspect("Baje la dosis del enalapril a la mitad.", rules_color=Color.GREEN)
    assert Violation.DOSE in result.violations


def test_naming_a_condition_as_the_patients_is_blocked():
    result = inspect("Usted tiene hipertensión mal controlada.", rules_color=Color.GREEN)
    assert Violation.DIAGNOSIS in result.violations


def test_speculating_a_diagnosis_is_blocked():
    result = inspect("Lo que me cuenta parece un infarto.", rules_color=Color.RED)
    assert Violation.DIAGNOSIS in result.violations


def test_a_diagnosis_is_blocked_even_where_the_rules_fired_red():
    result = inspect("Eso puede ser un ataque cerebral.", rules_color=Color.RED)
    assert result.allowed is False


def test_the_urgency_redirect_is_blocked_on_a_green_floor():
    result = inspect("Vaya al servicio de urgencia.", rules_color=Color.GREEN)
    assert Violation.URGENCY in result.violations


def test_the_urgency_redirect_is_blocked_on_a_yellow_floor():
    result = inspect("Por favor llame al 131.", rules_color=Color.YELLOW)
    assert Violation.URGENCY in result.violations


def test_the_urgency_redirect_is_allowed_on_a_red_floor():
    result = inspect(
        "Por favor acuda a un servicio de urgencia o llame al 131.", rules_color=Color.RED
    )
    assert result.allowed
    assert result.violations == []


def test_a_blocked_message_is_replaced_by_the_safe_redirect():
    result = inspect("Suspenda el losartán.", rules_color=Color.GREEN)
    assert result.message == SAFE_REDIRECT


def test_a_blocked_message_raises_the_case_for_review():
    result = inspect("Suspenda el losartán.", rules_color=Color.GREEN)
    assert result.raise_for_review is True


def test_every_violation_in_one_message_is_reported():
    message = "Usted tiene diabetes descompensada, así que suba la dosis de metformina."
    result = inspect(message, rules_color=Color.GREEN)
    assert Violation.DIAGNOSIS in result.violations
    assert Violation.DOSE in result.violations


def test_the_safe_redirect_survives_its_own_guardrail():
    result = inspect(SAFE_REDIRECT, rules_color=Color.GREEN)
    assert result.allowed


def test_the_result_is_an_inspection():
    assert isinstance(inspect(ACKNOWLEDGEMENT, rules_color=Color.GREEN), Inspection)


def test_the_rules_color_must_be_a_color_rather_than_a_string():
    with pytest.raises(TypeError):
        inspect(ACKNOWLEDGEMENT, rules_color="green")


def seeded_agent_messages():
    cohort = json.loads(COHORT.read_text(encoding="utf-8"))
    for patient in cohort["patients"]:
        for position, check_in in enumerate(patient["check_ins"]):
            yield (
                f"{patient['code']}#{position}",
                check_in["agent_message"],
                Color.parse(check_in["rules_color"]),
            )


@pytest.mark.parametrize(
    "label,message,rules_color", list(seeded_agent_messages()), ids=lambda value: str(value)[:24]
)
def test_every_seeded_agent_message_passes_the_guardrail(label, message, rules_color):
    result = inspect(message, rules_color=rules_color)
    assert result.allowed, f"{label} blocked for {result.violations}"
