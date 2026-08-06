# 0015 — The crisis protocol runs outside the semáforo

**Status:** Accepted
**Date:** 2026-08-06
**Deciders:** Felipe Carvajal Brown

## Context

The clinical annex, `docs/research/anexo PreventIA.docx` section 6A, lists four non-negotiable
software safety principles. Three of them were already answered by decisions in this set. The fourth
was not answered anywhere:

> "Protocolo de Crisis Mente/Salud: la detección de palabras clave sobre ideación suicida o
> autolesión desvía de forma inmediata la interacción a un protocolo de emergencia con contacto
> humano, quedando fuera del triaje estandarizado de hipertensión o diabetes."

Two things in that sentence are requirements rather than description. The diversion is *immediate*,
which is a statement about ordering: it happens before whatever else the system would have done. And
the case sits *outside the standardised triage*, which is a statement about destination, not about
urgency.

Everything deterministic the system had was on the wrong side of the conversation for this. ADR-0005's
guardrail inspects messages on the way out. ADR-0004's semáforo runs on facts already extracted from
the patient's words. A crisis has to be caught in the patient's own words, before the model is asked
anything at all, which makes this the first inbound deterministic check in the product.

The cohort makes the "outside the triage" clause sharper rather than softer. Since the cohort was
narrowed to adults aged 65 to 75 with confirmed HTA and/or DM2, every colour the semáforo produces
is a statement about cardiometabolic follow-up, anchored to a MINSAL guideline in
`clinical/rules/flags.py`. A suicidal-ideation case has no reading on that scale. It is not a worse
version of a missed dose.

There is also a false-positive problem specific to Chilean speech, and it runs the opposite way from
the usual detection worry. "Me muero de hambre", "me quiero morir de la risa" and "ando muerto de
cansancio" are ordinary register for the population this product serves. A detector tuned only for
recall would divert conversations that are not crises, teach the care team that the lane is noise,
and by ADR-0006's own logic that is how a queue stops being read.

## Decision

**A crisis is detected on the inbound message and leaves the pipeline before the model is called.**

`clinical/crisis.py` matches phrases on case-folded, accent-stripped text. On a hit,
`agent/core.run_check_in` returns a `CrisisResult` and performs no extraction, no rules evaluation
and no model call of any kind.

**A crisis carries no colour.** `CrisisResult` has no `rules_color`, `model_color` or `final_color`,
and the `crisis_events` table has no colour column. The schema cannot express a crisis as a shade of
the traffic light, which is what makes "fuera del triaje estandarizado" a property of the system
rather than a sentence in a document.

`crisis_events` is append-only, enforced by `BEFORE UPDATE` and `BEFORE DELETE` triggers, on the same
doctrine as ADR-0014.

The patient receives `patient_copy.CRISIS_DIVERSION` and nothing else. It names no condition, gives
no instruction, and promises only what the annex requires: that a person will make contact.

The case surfaces in a lane of its own above the triage queue, headed in the brand navy rather than
in any semáforo colour, carrying the person's verbatim words and the reply they were sent.

`tests/test_crisis.py` and `tests/test_crisis_path.py` prove it. The short-circuit test passes in a
model whose `send()` raises, so the claim is that the model is not in the loop, not that it behaved
well when it was.

## Consequences

- The strongest safety claim in the product is now a structural one rather than a behavioural one. A
  regression that puts the model back on the crisis path fails the build instead of producing a
  fluent, plausible answer to a person in crisis, which is exactly the failure mode
  `docs/research/felipe/2026-08-05-clinician-config-and-human-in-the-loop.md` section 4.4 records as
  the most consequential in clinical LLM use.
- The care team now has two surfaces to watch rather than one. This is the real cost of the decision
  and it was accepted knowingly: a crisis in the same list as the cardiometabolic reds is a crisis
  cleared in the same sweep as a missed dose.
- Detection is tuned against false positives first. Chilean death idioms and grooming phrases are
  guarded explicitly, and all 73 seeded patient messages are asserted not to fire. The residual risk
  runs the other way: a person who signals distress in words the phrase list does not carry is not
  diverted, and reaches the ordinary check-in path instead.
- The phrase list is not clinician-authored. Unlike `clinical/rules/flags.py`, which cites MINSAL
  guidelines per flag, the crisis phrases were written by a developer from ordinary Chilean usage.
  This is the weakest provenance in the clinical layer and it should be reviewed by the healthcare
  professional before any real patient is enrolled.
- **`CRISIS_DIVERSION` carries no helpline number, and this is a deliberate gap rather than an
  oversight.** No verified Chilean crisis line is recorded in this repository, and inventing one is
  not something the project may do. Which number the copy names, if any, is the healthcare
  professional's decision and is the first open question this ADR leaves behind.
- Nothing yet notifies anyone when a crisis event is written. The lane is read when the dashboard is
  read. "Contacto humano inmediato" is currently a promise the interface makes and the system does
  not keep on its own; closing that gap needs the channel layer and a decision about who is paged.

## Alternatives considered

**A dedicated flag in the rule table whose floor is red.** The crisis keyword becomes one more entry
in `clinical/rules/flags.py`, and the case rides the existing semáforo, ranking, queue and audit
machinery with no new schema and no new surface. By a wide margin the cheapest option, and every
piece of it already worked and was already tested. Rejected because it contradicts the annex on its
face: the case would be inside the standardised triage, sorted among cardiometabolic reds, and the
semáforo colour would silently start meaning two different things depending on the row. It also
leaves the model in the loop, since a flag fires only after extraction has already run.

**Divert the conversation, but rank the case in the existing queue above every red.** Keeps the
short-circuit and its safety property while giving the care team one list to watch instead of two,
which is the strongest argument against the option chosen. Rejected because it solves the surface
problem by reintroducing the semantic one: a queue ordered by colour that contains a row which is not
a colour is harder to read correctly under time pressure than two lists, and ADR-0006 fixed that
queue as a thing a clinician reads in seconds.
