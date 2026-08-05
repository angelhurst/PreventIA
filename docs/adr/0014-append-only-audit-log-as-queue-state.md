# 0014 — The append-only audit log is the queue's state

**Status:** Accepted
**Date:** 2026-08-05
**Deciders:** Felipe Carvajal Brown

## Context

ADR-0006 fixed a triage queue as the escalation surface and described what a row must show. It said
nothing about how a row changes state, who is allowed to change it, or what evidence survives the
change. That gap is not a detail here, because of what the closest Chilean analogue did with it.

`docs/research/felipe/2026-08-05-clinical-dashboard-ui-and-stacks-chile.md` section 6 records it.
SIGTE, the waiting-times platform whose priorisation panels are the nearest existing thing to this
queue, was publicly criticised for manual operation producing serious errors: patients recorded as
attended who were not, and care records against deceased people. MINSAL announced a replacement for
2025. The failure was not a visual one. Queue state could be advanced without the underlying clinical
event having happened, and nothing in the record distinguished the two.

`CLAUDE.md` section 2 already requires that every escalation terminates at a human. The SIGTE record
adds the harder requirement: the queue has to be able to prove that it did.

A judge on the clinical or government side of the Lab panel may know this story. A queue that lets a
case be marked resolved without recording who resolved it and when is the same class of system,
whatever else it does well.

## Decision

**There is no current-state column anywhere in the schema.**

`escalation_audit` is an append-only table. Each row records `patient_code`, `from_state`,
`to_state`, `actor_code`, `occurred_at` and a free-text `note`. A patient's current queue state is
the `to_state` of their most recent entry; a patient with no entries is `pending`.

The four states are `pending`, `in_review`, `contacted` and `closed`, rendered to the nurse in
Chilean Spanish as *pendiente*, *en revisión*, *contactado* and *cerrado*.

`actor_code` is `NOT NULL` and references `clinicians`. Append-only is enforced by `BEFORE UPDATE`
and `BEFORE DELETE` triggers that `RAISE(ABORT)`, so it holds against any writer reaching the
database, not only against the dashboard.

Correcting a mistake means appending a reversing entry. History is never edited.

The trail is shown on the queue row itself, not hidden behind an administrative screen.

## Consequences

- A queue state with no author cannot exist, because there is nowhere to write one. The record is the
  state rather than a log kept beside it, so the two cannot disagree.
- The claim is demonstrable rather than asserted. An `UPDATE` against `escalation_audit` fails at the
  database, in front of anyone who wants to watch.
- Every state change names a clinician, which is what turns "escalation terminates at a human" from a
  policy sentence into a queryable fact.
- Deriving current state costs a correlated subquery per patient rather than a column read. Irrelevant
  at prototype scale and a real consideration if this ever runs at a service's volume, where the
  answer is a materialised projection built from the log, not a mutable column.
- No cheap index on "all pending cases" without a derived view. A view is provided.
- Nobody can quietly fix a typo in a note. Deliberate, and the whole point.

## Alternatives considered

**A current-state column on the escalation row plus a separate audit table**, both written in one
transaction through a single write function. Simpler to read, faster, and one obvious place to look
for the state. Rejected because it stores the same fact twice: the schema itself permits a writer to
update `queue_state` directly and never touch the log, which is precisely the SIGTE class of failure
rather than the cure for it. A convention enforced in one function is not enforced.

**No ADR — build the same append-only trail and note it in the roadmap.** Keeps the ADR set to
architecture and the implementation would be identical. Rejected because the one design choice that
answers the SIGTE question would then be undocumented, and a decision the pitch wants to point at is
worth a file.
