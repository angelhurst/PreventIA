# 0002 — SQLite for the clinical record, file sessions for transcripts

**Status:** Accepted
**Date:** 2026-08-03
**Deciders:** Felipe Carvajal Brown

## Context

PreventIA holds two kinds of state that look similar and behave differently. One is the raw
conversation: every message exchanged with a patient, needed so the agent has continuity across
days. The other is the clinical record: patients, medications, which doses were reported taken,
which symptoms were extracted, which risk events fired, which escalations were raised. The dashboard
queries the second. An audit would query the second. Nothing queries the first except the agent
itself.

Strands ships `FileSessionManager` and an S3 equivalent. It has no SQLite session manager.

## Decision

**SQLite holds the clinical record.** Patients, medications, daily check-ins, extracted symptoms,
risk events, escalations.

**Strands `FileSessionManager` holds the raw transcripts**, keyed by patient session id.

No custom session manager is written. Transcripts do not go into SQLite.

## Consequences

- Zero custom persistence code, which is the point two days out.
- The clinical tables stay clean: they contain structured, reviewable facts, not conversation. That
  is what makes a row in the triage queue readable in seconds and what makes the schema explicable
  to a clinician.
- Two stores means two things to back up and a demo-day failure mode where one is present and the
  other is not. Accepted; both are local files.
- Reconstructing exactly what a patient said at the moment a red flag fired means joining a risk
  event to a session file by timestamp rather than reading one table. Acceptable for a prototype and
  worth revisiting if the project reaches a pilot.

## Alternatives considered

**Everything in SQLite behind a custom session manager.** One source of truth, easier to reason
about, and a cleaner audit story. Rejected because it means writing and debugging a custom Strands
session manager on day 1, which is time taken directly from the clinical logic the rubric scores.

**SQLite only, no Strands sessions, conversation context rebuilt from the clinical tables each
turn.** Most control and no framework dependency for state. Rejected as the most code for the least
benefit, and it discards the naturalness of the conversation, which is the product's whole premise.
