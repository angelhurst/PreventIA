# 0016 — A red holds until a clinician moves the case

**Status:** Accepted
**Date:** 2026-08-06
**Deciders:** Felipe Carvajal Brown

## Context

ADR-0004 fixed the rule that matters most to a clinical judge: a deterministic table sets a floor and
the model may raise a colour above it but never lower it. That rule is enforced in the type, in a
`CHECK` constraint on `risk_events`, and in `tests/test_semaforo.py`.

It holds for a single check-in. It said nothing about a case across check-ins, and that gap was found
in live data rather than in review. On 6 August, the patient-role phone produced this sequence in
under two minutes:

| check-in | rules | model | final | message |
|---|---|---|---|---|
| 74 | green | green | green | "me estoy tomando los medicamentos, me siento bien" |
| 75 | yellow | yellow | yellow | "se me olvido una de las pastillas hoy" |
| 76 | yellow | **red** | **red** | "me acabo de desmayar" |
| 77 | green | green | green | "me equivoque, estoy bien, me siento mucho mejor" |

Each classification is individually correct, and check-in 76 shows the model doing exactly what
ADR-0004 permits: raising a colour the rules did not reach. But the triage queue displayed the colour
of the **latest** check-in, so the case was red at 16:12 and green at 16:13. The last human action on
it was a state change at 16:07. Nobody cleared the red; the patient did, by minimising.

`CLAUDE.md` section 2 states that every escalation terminates at a human. This one terminated in
"me equivoqué". A patient who plays down symptoms after a faint is not an edge case in this cohort;
it is the behaviour the product exists to catch.

## Decision

The queue colour for a patient is the **highest final colour recorded since the last clinician state
change**, not the colour of the most recent check-in.

A clinician moving the case — to `contactado`, to `cerrado`, to anything — resets the window, and the
colour then follows subsequent check-ins again. Until they do, a red stays red.

The latest summary line and the latest patient message continue to display underneath, unchanged. The
clinician reads the reassurance; the alarm does not disappear behind it.

`tests/test_queue_red_persistence.py` pins four properties: a red survives a later calm message, the
latest message is still what the clinician reads, a clinician moving the case does clear the hold, and
a yellow cannot mask a later red.

## Consequences

- The rule that the model may only raise a colour now holds at the level a clinician actually works
  at — the case — and not only inside one classification.
- A red row can display alongside a calm latest message, which looks contradictory without
  explanation. The card must say why it is held. That is a display obligation this ADR creates.
- Cases accumulate in red until someone acts on them, which is the intended pressure. In a real
  deployment with a backlog this becomes a workload question rather than a safety question.
- The colour is now derived rather than stored, so nothing in the database contradicts it and there is
  no field for a model to write to.
- A clinician still cannot lower a colour deliberately. That is a separate gap, addressed in ADR-0017.

## Alternatives considered

**Show the latest colour with a badge marking an unreviewed red.** Keeps the queue ordering intact and
still surfaces the information. Rejected: a green row with a small badge is precisely what a busy
clinician scrolls past, and the traffic light exists to prevent that scroll.

**Leave it and explain the design in the pitch.** Defensible on the narrow technical point — each
check-in is independently classified and the full history is one click away in the ficha. Rejected
because it means demonstrating a system where a reported faint removes itself from the queue, which is
the opposite of what the product claims to do.
