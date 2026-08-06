import pytest

from preventia.clinical.semaforo import Color
from preventia.clinical.rules import evaluate, known_terms


def facts(terms=(), taken=2, expected=2):
    return {
        "symptoms": [{"term": t, "verbatim": "", "mentioned_in_passing": False} for t in terms],
        "doses_reported_taken": taken,
        "doses_expected": expected,
    }


def test_no_flags_is_green():
    verdict = evaluate(facts())
    assert verdict.color is Color.GREEN
    assert verdict.reason


@pytest.mark.parametrize("term", ["disnea_aumentada", "edema"])
def test_minsal_heart_failure_contact_threshold_is_red(term):
    verdict = evaluate(facts([term]))
    assert verdict.color is Color.RED
    assert "2015" in verdict.source


@pytest.mark.parametrize("term", ["confusion", "alteracion_habla", "vision_borrosa"])
def test_neuroglucopenic_hypoglycaemia_is_red(term):
    assert evaluate(facts([term])).color is Color.RED


@pytest.mark.parametrize("term", ["temblor", "sudor_frio", "palidez"])
def test_autonomic_hypoglycaemia_is_yellow(term):
    assert evaluate(facts([term])).color is Color.YELLOW


@pytest.mark.parametrize("term", ["herida_pie", "sed_intensa", "poliuria", "tos_seca"])
def test_sourced_yellow_flags(term):
    assert evaluate(facts([term])).color is Color.YELLOW


def test_missed_dose_alone_is_yellow():
    assert evaluate(facts(taken=0, expected=2)).color is Color.YELLOW


def test_worst_flag_wins_over_milder_ones():
    verdict = evaluate(facts(["temblor", "edema", "tos_seca"]))
    assert verdict.color is Color.RED


def test_red_flag_survives_perfect_adherence():
    assert evaluate(facts(["edema"], taken=2, expected=2)).color is Color.RED


def test_unknown_term_cannot_raise_or_lower():
    assert evaluate(facts(["sensacion_rara"])).color is Color.GREEN


def test_every_rule_carries_a_source():
    for term in known_terms():
        assert evaluate(facts([term])).source


def test_reason_names_the_signal_not_a_diagnosis():
    verdict = evaluate(facts(["edema"]))
    assert "edema" in verdict.reason.lower()
    for forbidden in ("insuficiencia cardiaca", "diagnostico", "infarto"):
        assert forbidden not in verdict.reason.lower()
