import json
from pathlib import Path

import pytest

from preventia.clinical.crisis import CrisisDetection, detect

COHORT = Path(__file__).resolve().parent.parent / "preventia" / "data" / "cohort.json"

IDEATION = [
    "Ya no quiero vivir.",
    "A veces pienso en quitarme la vida.",
    "Quiero morirme de una vez.",
    "Me quiero morir.",
    "Estoy pensando en matarme.",
    "No quiero seguir viviendo así.",
    "Para qué sigo viviendo si a nadie le importo.",
    "Estaría mejor muerto.",
    "Quiero terminar con todo.",
]

SELF_HARM = [
    "Anoche estuve por cortarme.",
    "Tengo ganas de hacerme daño.",
    "He pensado en hacerme un daño.",
]

EVERYDAY_IDIOMS = [
    "Me muero de hambre, no alcancé a almorzar.",
    "Me quiero morir de la risa con lo que pasó.",
    "Me muero de frío en esta casa.",
    "Ando muerto de cansancio.",
    "Me muero de ganas de ver a mis nietos.",
    "Tengo que cortarme el pelo, ando hecho un desastre.",
    "Mañana voy a cortarme las uñas.",
]

ORDINARY_CHECK_INS = [
    "Sí, me tomé los siete. Todo tranquilo por acá.",
    "Me faltó la del almuerzo porque salí donde mi hermana.",
    "Ando con un dolor de cabeza en la nuca en las mañanas.",
    "Todo tomado. Sin novedad.",
]


@pytest.mark.parametrize("message", IDEATION)
def test_suicidal_ideation_is_detected(message):
    assert detect(message).detected


@pytest.mark.parametrize("message", SELF_HARM)
def test_self_harm_is_detected(message):
    assert detect(message).detected


@pytest.mark.parametrize("message", EVERYDAY_IDIOMS)
def test_everyday_death_idioms_do_not_fire(message):
    assert not detect(message).detected


@pytest.mark.parametrize("message", ORDINARY_CHECK_INS)
def test_an_ordinary_check_in_does_not_fire(message):
    assert not detect(message).detected


def test_detection_ignores_case_and_accents():
    assert detect("YA NO QUIERO VIVIR").detected
    assert detect("quiero quitarme la vida").detected


def test_an_empty_message_does_not_fire():
    assert not detect("").detected


def test_the_matched_phrase_is_reported():
    result = detect("A veces pienso en quitarme la vida.")
    assert result.matched
    assert "quitarme la vida" in result.matched


def test_the_result_is_a_crisis_detection():
    assert isinstance(detect("Todo bien."), CrisisDetection)


def test_a_crisis_buried_in_a_normal_check_in_is_still_caught():
    message = "Sí, me tomé todos los remedios. La verdad es que ya no quiero vivir."
    assert detect(message).detected


def seeded_patient_messages():
    cohort = json.loads(COHORT.read_text(encoding="utf-8"))
    return [
        (f"{patient['code']}#{position}", check_in["patient_message"])
        for patient in cohort["patients"]
        for position, check_in in enumerate(patient["check_ins"])
    ]


@pytest.mark.parametrize(
    "label,message", seeded_patient_messages(), ids=lambda value: str(value)[:24]
)
def test_no_seeded_patient_message_is_a_false_positive(label, message):
    assert not detect(message).detected, f"{label} wrongly read as a crisis"
