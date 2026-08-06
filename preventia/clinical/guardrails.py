import re
import unicodedata
from dataclasses import dataclass
from enum import Enum

from preventia.clinical.semaforo import Color
from preventia.patient_copy import SAFE_REDIRECT


class Violation(Enum):
    DIAGNOSIS = "diagnosis"
    TREATMENT = "treatment"
    DOSE = "dose"
    URGENCY = "urgency"


@dataclass(frozen=True)
class Inspection:
    allowed: bool
    violations: list
    message: str
    raise_for_review: bool


CONDITIONS = "|".join(
    [
        "infarto",
        "ataque al corazon",
        "ataque cerebral",
        "acv",
        "angina",
        "arritmia",
        "trombosis",
        "embolia",
        "neumonia",
        "hipertension",
        "presion alta",
        "diabetes",
        "azucar alta",
        "hipoglicemia",
        "hiperglicemia",
        "insuficiencia cardiaca",
    ]
)

ARTICLE = r"(?:un |una |el |la |los |las )?"

TREATMENT_PATTERNS = [
    r"\bsuspenda\b",
    r"\bsuspendase\b",
    r"\bdeje de (?:tomar|usar)\b",
    r"\bpare de tomar\b",
    r"\bno (?:tome|se tome|siga tomando)\b",
    r"\b(?:empiece|comience|inicie) (?:a tomar|con)\b",
    r"\bpuede (?:tomar|tomarse|dejar)\b",
    r"\ble recomiendo (?:tomar|que tome)\b",
    r"\breemplace\b",
]

DOSE_PATTERNS = [
    r"\b(?:tome|tomese) (?:dos|tres|media|el doble|otra|una mas)\b",
    r"\b(?:suba|baje|aumente|disminuya|duplique|reduzca) (?:la )?dosis\b",
    r"\bdosis (?:doble|extra)\b",
    r"\bla mitad de (?:la|su) (?:dosis|tableta)\b",
]

DIAGNOSIS_PATTERNS = [
    rf"\btiene {ARTICLE}(?:{CONDITIONS})\b",
    rf"\b(?:es|parece|seria|suena a|puede ser) {ARTICLE}(?:{CONDITIONS})\b",
    rf"\besta (?:con|haciendo) {ARTICLE}(?:{CONDITIONS})\b",
]

URGENCY_PATTERNS = [
    r"\bservicio de urgencia",
    r"\burgencias\b",
    r"\bal 131\b",
    r"\bposta\b",
    r"\bsapu\b",
    r"\bsar\b",
]

RULES = [
    (Violation.DIAGNOSIS, DIAGNOSIS_PATTERNS),
    (Violation.TREATMENT, TREATMENT_PATTERNS),
    (Violation.DOSE, DOSE_PATTERNS),
]


def normalise(text):
    decomposed = unicodedata.normalize("NFD", text.lower())
    return "".join(char for char in decomposed if not unicodedata.combining(char))


def inspect(message, rules_color):
    if not isinstance(rules_color, Color):
        raise TypeError(f"rules_color must be a Color, got {type(rules_color).__name__}")

    text = normalise(message)
    violations = [
        violation
        for violation, patterns in RULES
        if any(re.search(pattern, text) for pattern in patterns)
    ]

    if rules_color is not Color.RED and any(
        re.search(pattern, text) for pattern in URGENCY_PATTERNS
    ):
        violations.append(Violation.URGENCY)

    if violations:
        return Inspection(
            allowed=False,
            violations=violations,
            message=SAFE_REDIRECT,
            raise_for_review=True,
        )

    return Inspection(allowed=True, violations=[], message=message, raise_for_review=False)
