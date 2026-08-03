# 0006 — Clinician triage queue as the escalation surface

**Status:** Accepted
**Date:** 2026-08-03
**Deciders:** Felipe Carvajal Brown

## Context

The agent's job ends where a human's begins. Something has to receive an escalation, and the choice
of surface decides whether the product's central promise is true: that the professional reviews a
patient's longitudinal adherence and symptom history in seconds during the next control.

The competing constraint is that the escalation surface has to work on stage, in a recorded video,
in three minutes, in front of judges scoring clinical and management criteria.

## Decision

A **web dashboard with a triage queue**: a list ranked by risk, red first, where each row carries the
patient's longitudinal adherence and symptom summary already assembled.

The design constraint is the professional's time, not the interface's completeness. If a row takes
longer than a few seconds to read, the row is wrong, not the reader.

The queue reads from the SQLite clinical record (ADR-0002). It does not read transcripts.

## Consequences

- The product's own promise becomes something the audience watches happen rather than something the
  pitch asserts.
- The surface is entirely under our control during the demo, with no third-party delivery in the
  path between the red flag and what the judges see.
- It is the natural place to show what the agent decided and why, which is where the semáforo's
  floor logic (ADR-0004) becomes visible to a clinician.
- A dashboard is more to build in two days than a notification would be. Accepted, because the
  longitudinal summary is the part of the product a clinician can evaluate.
- A queue nobody is watching does not interrupt anyone. Real deployment needs a push channel; that
  is a Phase 5 problem, not a prototype one.

## Alternatives considered

**Notification only**, by WhatsApp or email to the clinician. Much cheaper to build and closer to
how an alert would actually reach a busy professional. Rejected as the primary surface because a
notification cannot carry a longitudinal summary in a form anyone reads on a phone, which discards
the specific claim the product makes.

**Dashboard plus a push notification on red.** The correct end state. Rejected for the prototype:
two surfaces means two things to build and two to break across two days, and the queue alone
demonstrates the clinical value.

**Dashboard with the clinician as a sixth WhatsApp recipient**, so the escalation visibly lands on a
second real phone in the video. Attractive for the recording. Rejected for now as scope, and noted
as a cheap addition if Phase 3 finishes early, since the Cloud API test number already supports five
verified recipients.
