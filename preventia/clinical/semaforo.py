from dataclasses import dataclass
from enum import Enum
from functools import total_ordering


class EmptyRuleTable(ValueError):
    pass


class UnknownFlag(ValueError):
    pass


@total_ordering
class Color(Enum):
    GREEN = "green"
    YELLOW = "yellow"
    RED = "red"

    @property
    def rank(self):
        return _RANK[self]

    def __lt__(self, other):
        if not isinstance(other, Color):
            return NotImplemented
        return self.rank < other.rank

    def raised_to(self, other):
        return self if self.rank >= other.rank else other

    @classmethod
    def parse(cls, value):
        try:
            return cls(value)
        except ValueError:
            raise ValueError(f"unknown semaforo color {value!r}") from None


_RANK = {Color.GREEN: 0, Color.YELLOW: 1, Color.RED: 2}


@dataclass(frozen=True)
class Classification:
    rules_color: Color
    model_color: Color
    final_color: Color
    fired: list


def classify(flags, table, model_color):
    if not table:
        raise EmptyRuleTable(
            "the clinical flag table is empty, and an empty table is not a green light"
        )

    unknown = [flag for flag in flags if flag not in table]
    if unknown:
        raise UnknownFlag(", ".join(sorted(unknown)))

    rules_color = Color.GREEN
    for flag in flags:
        rules_color = rules_color.raised_to(table[flag])

    return Classification(
        rules_color=rules_color,
        model_color=model_color,
        final_color=rules_color.raised_to(model_color),
        fired=[flag for flag in flags if table[flag] is rules_color],
    )
