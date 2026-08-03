# 0010 — Claude as the Lab runtime, Ollama as the deployment path

**Status:** Accepted. Supersedes 0008
**Date:** 2026-08-03
**Deciders:** Felipe Carvajal Brown

## Context

ADR-0008 made a local model served by Ollama the default runtime, on a stated reading of what the
Impact Lab requires. Its Context says, verbatim:

> The Impact Lab's requirement is satisfied by building with Claude; it does not dictate what the
> deployed agent runs on.

The Lab has since been found to publish the opposite. Its data and AI wiki
(https://longevidad.benditaia.cl/es/wiki-legal, consulted 3 August 2026, archived as
`docs/research/sources/lab-2026-wiki-datos-salud.txt`) states, under "IA en salud, con
responsabilidad", verbatim:

> Claude como motor principal — Sin llamadas reales a la API de Claude → descalificado

"Motor principal" reads as the engine the solution runs on. A narrower reading is available — that
the rule prohibits entering without genuinely using the API at all, which building with Claude Code
would satisfy — and the wiki does not disambiguate. The organisers are not reachable for a
clarification in the time available.

The asymmetry decides it. Under the narrow reading, running the demo on Claude costs nothing. Under
the broad reading, not running it on Claude is disqualification.

ADR-0001 already put every provider behind one seam in `agent/models.py`, selected by
`PREVENTIA_MODEL_PROVIDER`. That seam makes this a configuration decision rather than an
architectural one.

## Decision

**Claude is the runtime for the Lab build, the recorded demo and the pitch.**
`PREVENTIA_MODEL_PROVIDER=anthropic`, `model_id="claude-sonnet-5"`, as already registered in
`agent/models.py`. This is set in `.env` and is what every Phase 1 to Phase 4 activity runs against.

**Ollama remains a first-class registered provider and is the documented deployment path**, for a
health institution that needs patient conversations to stay on hardware it controls. It is presented
in the pitch as the production option, not as the prototype's runtime.

**No module code changes.** The provider seam from ADR-0001 is the whole mechanism. `agent/`,
`clinical/`, `channels/` and `dashboard/` remain provider-agnostic and no module imports a provider
directly.

**`OLLAMA_MODEL` stops blocking Phase 1.** Agreeing it with Angel moves from a blocker to a Phase 4
or post-Lab task, since nothing in the two days depends on it.

**The guardrail and semáforo suites still run against every provider actually used**, per `CLAUDE.md`
section 4. That requirement is unchanged and is now cheaper, because the provider that must pass
before demo day is the hosted one.

## Consequences

- The disqualification risk is removed under either reading of the Lab's rule, for the price of one
  environment variable.
- Per-token cost during the two days, against ADR-0008's zero. Covered by the Lab's per-participant
  API credits.
- The clinical-safety claim gets weaker evidence than ADR-0008 intended. ADR-0008 argued that running
  the deterministic floor and the output filter against an open-weights local model is what stops the
  safety claim depending on a vendor's alignment work. Running them only against Claude does not
  demonstrate that. Mitigation: run both suites against Ollama as well once a model is pinned, and
  say honestly in the pitch which providers the suites have been run against.
- Phase 1 is unblocked immediately, and the build no longer depends on a machine belonging to
  someone else being reachable. That removes the largest availability risk in the schedule after the
  WhatsApp token.
- The data-sovereignty argument survives and arguably improves. "It runs on Claude today and on a
  local open-weights model inside your network tomorrow, behind the same interface, because the
  provider was never in the clinical path" is a stronger adoption statement than either option alone.
- Angel's Mac Studio is no longer on the critical path. He should be told, because ADR-0008 put it
  there.

## Alternatives considered

**Keep Ollama as the demo runtime and argue that building with Claude Code satisfies the rule.**
Costs nothing now and is what ADR-0008 already decided. Rejected because it stakes the entry on an
interpretation of a published rule whose stated penalty is disqualification, with no organiser
available to confirm it and two days to run.

**Make Anthropic the only provider and drop Ollama from the prototype entirely.** Simplest, and it
removes the Mac Studio dependency and the tool-calling reliability risk in one move. Rejected because
it discards the argument that patient conversations never have to leave an institution's own
hardware, which is one of the strongest things this project can say to a health-institution judge,
and because the provider seam costs nothing to keep.
