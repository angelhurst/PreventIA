import pytest

from preventia import patient_copy
from preventia.clinical.guardrails import inspect, normalise
from preventia.clinical.semaforo import Color


def public_copy():
    return sorted(
        (name, value)
        for name, value in vars(patient_copy).items()
        if name.isupper() and isinstance(value, str)
    )


def test_the_disclosure_names_itself_a_virtual_assistant():
    assert "asistente virtual" in normalise(patient_copy.ASSISTANT_DISCLOSURE)


def test_the_disclosure_denies_being_a_health_professional():
    assert "no soy" in normalise(patient_copy.ASSISTANT_DISCLOSURE)
    assert "profesional de la salud" in normalise(patient_copy.ASSISTANT_DISCLOSURE)


def test_the_disclosure_says_it_does_not_replace_a_control():
    assert "no reemplazo sus controles" in normalise(patient_copy.ASSISTANT_DISCLOSURE)


def test_the_disclosure_uses_usted_rather_than_tu():
    assert " tu " not in normalise(patient_copy.ASSISTANT_DISCLOSURE)


@pytest.mark.parametrize("name,value", public_copy(), ids=lambda value: str(value)[:32])
def test_every_patient_facing_string_passes_the_guardrail(name, value):
    result = inspect(value, rules_color=Color.GREEN)
    assert result.allowed, f"{name} blocked for {result.violations}"
