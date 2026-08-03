# 0007 — Synthetic seed cohort with an adapter for the Caja dataset

**Status:** Accepted
**Date:** 2026-08-03
**Deciders:** Felipe Carvajal Brown

## Context

The Impact Lab supplies anonymized, aggregated health data from Caja La Araucana through MCP
servers, available when the Lab starts on 5 August. The project needs data before then, because
Phase 0 exists precisely so that day 1 is spent on clinical logic rather than setup.

Neither the shape nor the usefulness of the Lab dataset is known in advance. It may not contain
longitudinal per-patient adherence at all, since it is described as aggregated.

## Decision

Build a **synthetic seed cohort** of older adults across the three target conditions (hypertension,
type 2 diabetes, heart failure) in SQLite, now. It is the data the prototype is developed and
demonstrated against.

Write a **documented adapter**, `data/caja_adapter.py`, that reads the Lab's anonymized dataset over
MCP into the same schema, to be used if the data arrives in a usable shape within the time available.

No real patient data enters this repository under any circumstance. The synthetic cohort is
committed; anything derived from the Lab dataset is not.

## Consequences

- Work starts before the Lab instead of on its first morning.
- The demo is deterministic and reproducible. The same patient, the same conversation, the same red
  flag, every take. This matters more than it sounds when recording video under time pressure.
- The adapter keeps the credibility argument available: the synthetic cohort makes the demo
  reproducible, the adapter makes the projection to real data concrete, and the pitch can say which
  is which without overclaiming.
- Synthetic data can flatter the classifier. Symptoms will be phrased the way we imagined them
  rather than the way a Chilean 80-year-old actually types at 8am. The clinical teammate should
  write or review the patient utterances for exactly this reason.
- If the Lab dataset turns out to be rich and usable, some Phase 0 modelling work is discarded.
  Acceptable price for being able to start.

## Alternatives considered

**Build only on the Lab's anonymized dataset.** Truest to the brief and strongest possible
credibility. Rejected because nothing can be written or tested until the Lab starts, which throws
away the two days before it and gambles the whole prototype on data whose shape is unknown.

**Treat the anonymized dataset as primary with the synthetic cohort as a demo-day fallback.** Better
credibility than the chosen option. Rejected as the same gamble in a milder form: it shapes the
schema around data we have not seen, and the fallback then does not fit the schema it was supposed
to rescue.
