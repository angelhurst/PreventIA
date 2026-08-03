# 0004 — Deterministic rule floor for the semáforo, model may only escalate

**Status:** Accepted
**Date:** 2026-08-03
**Deciders:** Felipe Carvajal Brown

## Context

Every interaction is classified green, yellow or red, and that classification decides whether a
human clinician is interrupted. It is the single mechanism a clinical judge will interrogate hardest,
and the single mechanism whose failure hurts a real patient.

Two failure modes matter and they pull in opposite directions. A purely deterministic classifier is
blind to what the README actually promises, which is catching a symptom a patient mentions in
passing rather than in answer to a questionnaire. A purely model-driven classifier is flexible but
cannot be explained to a clinician, cannot be unit-tested meaningfully in the time available, and
can quietly decide a red flag is fine.

## Decision

Two steps, in this order.

**Step 1, rules.** Claude extracts structured facts from the conversation: which doses were reported
taken, which symptoms were mentioned, in what words. A deterministic rule table in `clinical/rules/`
maps hard clinical flags to a **minimum** color. The table is authored and reviewed by the team's
healthcare professional, not by a developer. Its clinical basis is documented in `docs/research/`.

**Step 2, model.** The model may **raise** the color above the floor when it sees something the
table did not anticipate.

**The model can never lower a color the rules set.** This is enforced in code, not requested in a
prompt, and `tests/test_semaforo.py` proves it. Because the model provider is swappable (ADR-0001),
the suite runs against both configured providers.

## Consequences

- One sentence that holds up in front of a clinician: no model output can downgrade a red flag.
- The classifier is testable. The rule table is data, so its behaviour is enumerable and its edge
  cases are fixtures.
- Clinical authorship sits where it belongs. Engineering owns the engine, the healthcare
  professional owns the table.
- The system will over-alert relative to a perfectly tuned classifier, because a floor only ever
  raises. Deliberate: under-alerting is the failure mode that hurts someone.
- **The prototype is not complete without the real flag table.** Engineering can build and test the
  engine against placeholder flags, but shipping placeholder clinical criteria would be worse than
  shipping nothing. This is tracked as a blocker in Phase 0 of the roadmap.

## Alternatives considered

**Deterministic rules only, the model restricted to extraction.** Maximum defensibility, fully
testable, no dependence on model judgement for a clinical decision. Rejected because it is blind to
anything the table did not anticipate, and that blindness is exactly the gap the product claims to
close.

**The model assigns the color directly from a rubric in the prompt.** Simplest to build, most
flexible, adapts to phrasing no rule anticipated. Rejected as indefensible to a clinician and
impossible to test properly in two days. It also makes clinical behaviour a property of the chosen
model, which conflicts with the provider-agnostic decision in ADR-0001.
