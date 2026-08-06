from dataclasses import dataclass

from ..semaforo import Color

MINSAL_IC_2015 = "Minsal/Sochicar, Guia Clinica Insuficiencia Cardiaca 2015, Tabla 28"
MINSAL_DM1_2013 = "Minsal, Guia Clinica Diabetes Mellitus Tipo 1 2013, seccion 8.2"
MINSAL_DM2_2010 = "Minsal, Guia Clinica Diabetes Mellitus tipo 2 2010, seccion 3.5.3"
MINSAL_HTA_2010 = "Minsal, Guia Clinica Hipertension Arterial 2010, p.30 y p.34"
MINSAL_PSCV_2017 = "Minsal, Orientacion Tecnica PSCV 2017, rescate de inasistentes"


@dataclass(frozen=True)
class Flag:
    term: str
    color: Color
    label: str
    source: str


@dataclass(frozen=True)
class Verdict:
    color: Color
    reason: str
    source: str
    fired: tuple


FLAGS = (
    Flag("disnea_aumentada", Color.RED, "aumento de la falta de aire", MINSAL_IC_2015),
    Flag("edema", Color.RED, "edema de extremidades", MINSAL_IC_2015),
    Flag("confusion", Color.RED, "confusion", MINSAL_DM1_2013),
    Flag("alteracion_habla", Color.RED, "alteracion del habla", MINSAL_DM1_2013),
    Flag("vision_borrosa", Color.RED, "vision borrosa", MINSAL_DM1_2013),
    Flag("temblor", Color.YELLOW, "temblor", MINSAL_DM1_2013),
    Flag("sudor_frio", Color.YELLOW, "sudor frio", MINSAL_DM1_2013),
    Flag("palidez", Color.YELLOW, "palidez", MINSAL_DM1_2013),
    Flag("herida_pie", Color.YELLOW, "herida o lesion en el pie", MINSAL_DM2_2010),
    Flag("sed_intensa", Color.YELLOW, "sed intensa", MINSAL_DM2_2010),
    Flag("poliuria", Color.YELLOW, "orinar mucho mas de lo habitual", MINSAL_DM2_2010),
    Flag("baja_de_peso", Color.YELLOW, "baja de peso no explicada", MINSAL_DM2_2010),
    Flag("tos_seca", Color.YELLOW, "tos seca persistente", MINSAL_HTA_2010),
    Flag("mareo_al_pararse", Color.YELLOW, "mareo al ponerse de pie", MINSAL_HTA_2010),
    Flag("nauseas", Color.YELLOW, "nauseas o falta de apetito", MINSAL_IC_2015),
    Flag("palpitaciones", Color.YELLOW, "palpitaciones", MINSAL_IC_2015),
    Flag("cansancio", Color.YELLOW, "cansancio generalizado", MINSAL_IC_2015),
)

_BY_TERM = {flag.term: flag for flag in FLAGS}

ADHERENCE_FLAG = Flag(
    "dosis_no_tomada",
    Color.YELLOW,
    "dosis no tomadas en el ultimo control",
    MINSAL_PSCV_2017,
)

NO_FLAGS_REASON = "sin banderas clinicas; adherencia declarada completa"


def known_terms():
    return tuple(_BY_TERM)


def term_catalogue():
    return {flag.term: flag.label for flag in FLAGS}


def _reported_terms(facts):
    for entry in facts.get("symptoms") or ():
        term = (entry.get("term") or "").strip().lower()
        if term in _BY_TERM:
            yield _BY_TERM[term]


def _adherence_shortfall(facts):
    expected = facts.get("doses_expected") or 0
    taken = facts.get("doses_reported_taken") or 0
    return expected > 0 and taken < expected


def evaluate(facts):
    fired = list(_reported_terms(facts))
    if _adherence_shortfall(facts):
        fired.append(ADHERENCE_FLAG)

    if not fired:
        return Verdict(Color.GREEN, NO_FLAGS_REASON, MINSAL_PSCV_2017, ())

    fired.sort(key=lambda flag: flag.color.rank, reverse=True)
    floor = Color.GREEN
    for flag in fired:
        floor = floor.raised_to(flag.color)

    leading = [flag for flag in fired if flag.color is floor]
    reason = ", ".join(flag.label for flag in leading)
    return Verdict(floor, reason, leading[0].source, tuple(fired))
