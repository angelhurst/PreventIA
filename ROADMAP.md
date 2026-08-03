# PreventIA — Roadmap

Phase-based. The two middle phases are anchored to the Claude Impact Lab on 5-6 August 2026, which
is the only real deadline this project has.

Status values: `Not Started` / `In Progress` / `Blocked` / `Done`.

---

## Phase 0 — Pre-Lab groundwork

**Status:** In Progress

Everything that can be done before the Lab starts, so day 1 is spent on the clinical logic and not
on setup.

- Documentation set: `CLAUDE.md`, `PRD.md`, `ROADMAP.md`, ADRs 0001-0007. **Done**
- Repository skeleton per the layout in `CLAUDE.md`.
- Meta developer app, WhatsApp product, test sender number.
- Five recipient numbers verified by OTP.
- **System User permanent access token.** The console token expires in 60 minutes; this is the
  highest-risk item in the whole build and it is a Phase 0 item for that reason.
- Webhook endpoint plus tunnel, verification handshake completed, one message received end to end.
- Synthetic seed cohort in SQLite: older adults across hypertension, type 2 diabetes, heart failure.
- Adversarial guardrail test suite, written and failing.

Shaped by ADR-0003, ADR-0005, ADR-0007.

**Blocked on the clinical teammate:** the concrete flag table per condition that feeds the semáforo
rules. Engineering can build the rule engine and its tests against placeholder flags, but the
prototype is not complete until a healthcare professional writes the real table.

## Phase 1 — Agent core and semáforo

**Status:** Not Started
**Target:** day 1 morning

- Strands agent assembled, provider-agnostic model layer, Claude configured as default.
- System prompt carrying the clinical boundary.
- Structured extraction of adherence and symptoms from natural conversation.
- Deterministic rule engine setting the color floor.
- Model escalation path, with de-escalation impossible by construction.
- `tests/test_semaforo.py` and `tests/test_extraction.py` green.

Shaped by ADR-0001, ADR-0004, ADR-0005.

## Phase 2 — Clinical record and triage queue

**Status:** Not Started
**Target:** day 1 afternoon

- SQLite schema: patients, medications, daily check-ins, risk events, escalations.
- `FileSessionManager` wired for transcripts.
- Longitudinal adherence and symptom summary, assembled per patient.
- Clinician dashboard: ranked queue, red first, one row readable in seconds.

Shaped by ADR-0002, ADR-0006.

## Phase 3 — Live channel and recorded demo

**Status:** Not Started
**Target:** day 2 morning

- WhatsApp Cloud API adapter behind the channel interface.
- Full round trip on real phones: patient message in, agent reply out, red flag escalating to the
  clinician's queue.
- **Demo video recorded on 5 August**, not on the 6th. Network failure on demo day must cost
  nothing.
- Backup ladder rehearsed at least once: Twilio Sandbox, then local console.

Shaped by ADR-0003.

## Phase 4 — Pitch and hardening

**Status:** Not Started
**Target:** day 2 afternoon

- Pitch built around the five items in the definition of done.
- Guardrail suite runnable live in front of the panel.
- Rule table reviewed and signed off by the clinical teammate.
- Cost and deployability answers ready: what a real pilot would cost per patient per month, what
  changes when the WhatsApp free service window ends on 1 October 2026.
- Scope cut wherever the definition of done is not yet met.

## Phase 5 — AI Health Sandbox track

**Status:** Blocked — only reachable if selected as one of the three winners

- Adapter against real anonymized data from Caja La Araucana.
- Clinical validation of the rule table beyond one professional's review.
- Pilot design inside the health network.
- Whatever the adoption evaluation pathway requires.

Nothing in this phase is planned in detail before selection, because its shape depends on the
institution rather than on us.
