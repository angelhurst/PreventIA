from dataclasses import dataclass
from datetime import datetime, timezone

from ..clinical import guardrails
from ..clinical.extraction import extract
from ..clinical.rules import evaluate
from ..clinical.semaforo import Color
from ..patient_copy import TEAM_NOTIFIED, URGENCY_REDIRECT
from .models import build_model


@dataclass(frozen=True)
class CheckInResult:
    patient_code: str
    patient_message: str
    agent_message: str
    occurred_at: str
    doses_reported_taken: int
    doses_expected: int
    symptoms: tuple
    rules_color: Color
    rules_reason: str
    rules_source: str
    model_color: Color
    model_reason: str
    final_color: Color
    summary_line: str
    guardrail_reason: str
    model_was_raised: bool
    provider: str
    model_id: str

    @property
    def escalates(self):
        return self.final_color is not Color.GREEN

    @property
    def passing_mentions(self):
        return tuple(s for s in self.symptoms if s.get("mentioned_in_passing"))


def run_check_in(patient, message, model=None):
    engine = model or build_model()
    extraction = extract(engine, patient, message)

    verdict = evaluate(extraction.as_facts())
    final = verdict.color.raised_to(extraction.model_color)

    guard = guardrails.inspect(extraction.reply, rules_color=verdict.color)
    reply = guard.message
    if verdict.color is Color.RED:
        reply = f"{reply} {URGENCY_REDIRECT}"
    elif final is Color.RED and guard.allowed:
        reply = f"{reply} {TEAM_NOTIFIED}"

    return CheckInResult(
        patient_code=patient["code"],
        patient_message=message,
        agent_message=reply,
        occurred_at=datetime.now(timezone.utc).isoformat(timespec="seconds"),
        doses_reported_taken=extraction.doses_reported_taken,
        doses_expected=extraction.doses_expected,
        symptoms=extraction.symptoms,
        rules_color=verdict.color,
        rules_reason=verdict.reason,
        rules_source=verdict.source,
        model_color=extraction.model_color,
        model_reason=extraction.model_reason,
        final_color=final,
        summary_line=extraction.summary_line,
        guardrail_reason=", ".join(item.value for item in guard.violations),
        model_was_raised=extraction.model_color > verdict.color,
        provider=getattr(engine, "provider", "desconocido"),
        model_id=getattr(engine, "model_id", "desconocido"),
    )
