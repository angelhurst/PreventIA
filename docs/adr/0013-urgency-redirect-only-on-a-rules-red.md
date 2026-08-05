# 0013 — The urgency redirect is allowed only where a rule fired red

**Status:** Accepted
**Date:** 2026-08-05
**Deciders:** Felipe Carvajal Brown

## Context

`CLAUDE.md` section 2 forbids PreventIA from diagnosing, from indicating or changing a treatment, and
from replacing a control. It also says that when it is unclear whether a message crosses one of those
lines, it crosses it, and the conservative version ships with a test.

A sentence sitting exactly on that edge appeared while building the synthetic cohort: the agent
telling a patient to go to a servicio de urgencia or call 131. It names no condition and it changes
no dose, so it breaks neither of the first two rules on its face. What it does do is make a clinical
judgment about urgency, and the question is whose judgment that is.

ADR-0004 already answers the same question for the semáforo. The deterministic rule table is authored
by the team's healthcare professional; the model may raise a colour above the floor but never lower
it. Authority over clinical criteria sits with the clinician, and the model's contribution is
allowed to be additive only.

The competing consideration is real and points the other way. Removing the sentence entirely means
that in the recorded demo, an older adult describing chest pain receives no safety net on screen. A
clinical judge may reasonably read silence there as the worse failure, not the safer one.

ADR-0005 fixed a deterministic output filter as the second guardrail layer. That filter needs a rule
it can actually test, not a matter of taste.

## Decision

An outbound message may direct a patient to emergency services **only on a check-in whose
deterministic `rules_color` is red.**

Where the rules floor is green or yellow and the model raised the colour, the urgency redirect is
**blocked** by `clinical/guardrails.py` and replaced by the safe redirect, exactly as any other
blocked message is. The case is still raised for review; only the sentence is withheld.

The sentence is therefore issued by the clinician-authored rule table, never by model judgment. It
is the same split as ADR-0004, applied to outbound copy rather than to a colour.

`tests/test_guardrails.py` proves it, so the claim is runnable in front of a panel rather than
asserted.

## Consequences

- The one sentence in the product that comes closest to a clinical instruction is attributable to a
  named healthcare professional's flag table, which is the answer a clinical judge is looking for.
- The guardrail filter gains a rule expressible in code: the message's permitted vocabulary depends
  on `rules_color`, not on `final_color` and not on the model's reasoning.
- A model that spots something the table never anticipated still raises the case and still reaches a
  human. It just does not get to tell the patient to go to urgencias on its own authority.
- The rule table becomes load-bearing for outbound copy as well as for the semáforo, which raises the
  cost of the Phase 0 blocker in ADR-0004. Accepted: the table was already the thing the prototype
  cannot ship without.
- A patient whose danger is genuinely novel and unanticipated by the table hears the softer message.
  This is the residual risk and it is the price of not letting a model decide urgency unsupervised.

## Alternatives considered

**Never, under any circumstances.** The agent says only that it is alerting the care team and asks
the person to stay reachable. Cleanest reading of section 2 and impossible to argue with on the
letter of the rule. Rejected because it removes the safety net at the exact moment it matters, and
because a blanket prohibition is not more conservative than a clinician-governed one — it just moves
the judgment from a reviewed table to nowhere.

**Keep the wording as drafted and refer the question to the clinical teammate after the Lab.** Honest
about who owns clinical copy. Rejected on timing: the demo is recorded from this seed data, and an
unresolved boundary question in the recording is worse than a conservative rule that a clinician can
widen later.
