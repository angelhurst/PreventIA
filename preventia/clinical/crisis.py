import re
import unicodedata
from dataclasses import dataclass

LIGHT_IDIOM_TAIL = r"(?! de (?:risa|la risa|hambre|frio|sueno|calor|sed|ganas|verguenza|amor))"

GROOMING_TAIL = r"(?! (?:el pelo|las unas|la barba|el pasto|el pan))"

PHRASES = (
    rf"quiero morirme{LIGHT_IDIOM_TAIL}",
    rf"me quiero morir{LIGHT_IDIOM_TAIL}",
    rf"quisiera morirme{LIGHT_IDIOM_TAIL}",
    r"quitarme la vida",
    r"acabar con mi vida",
    r"terminar con mi vida",
    r"terminar con todo",
    r"acabar con todo",
    rf"matarme{LIGHT_IDIOM_TAIL}",
    r"no quiero vivir",
    r"no quiero seguir viviendo",
    r"no vale la pena vivir",
    r"para que sigo viviendo",
    r"estaria mejor muert[oa]",
    r"mejor no despertar",
    r"hacerme dano",
    r"hacerme un dano",
    rf"cortarme{GROOMING_TAIL}",
)

PATTERNS = tuple((re.compile(pattern), pattern) for pattern in PHRASES)


@dataclass(frozen=True)
class CrisisDetection:
    detected: bool
    matched: tuple


def flatten(text):
    decomposed = unicodedata.normalize("NFD", (text or "").lower())
    return "".join(char for char in decomposed if not unicodedata.combining(char))


def detect(message):
    text = flatten(message)
    matched = tuple(
        compiled.search(text).group(0) for compiled, _ in PATTERNS if compiled.search(text)
    )
    return CrisisDetection(detected=bool(matched), matched=matched)
