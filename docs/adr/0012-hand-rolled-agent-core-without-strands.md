# 0012 — Hand-rolled provider-agnostic agent core, without Strands

**Status:** Accepted
**Date:** 2026-08-05
**Deciders:** Felipe Carvajal Brown

## Context

ADR-0001 adopted the Strands Agents SDK and bought three things with it: the tool-calling loop,
session persistence for raw transcripts, and an MCP client for the Impact Lab's curated dataset
servers. It also recorded, in its own Consequences, the cost it was accepting:

> Neither developer has shipped Strands before. Framework-specific problems will be debugged during
> the Lab, which is the real cost of this decision.

That cost was acceptable when the framework was buying three things. It is no longer buying three
things.

The tools the agent actually needs are local to this repository. Reading a ficha clínica is a query
against the SQLite record from ADR-0002. Reaching the patient is a call into the channel adapter from
ADR-0003. Neither touches MCP, and neither is easier inside a framework than outside one.

MCP enters only through the Lab's dataset servers, and Strands is not the only door to it. The
official `mcp` Python SDK is a standalone package that speaks the same protocol without an agent
framework attached, so keeping Strands is not what keeps MCP available.

What remains is a tool loop bounded at a handful of steps over two local functions. Against roughly a
day and a half of build time, an unfamiliar framework failing at 11pm on day 2 is a larger risk than
code the team wrote and can read.

ADR-0010 is unaffected and is not superseded. Its decision is which provider answers during the Lab,
and that stands unchanged; this ADR replaces the mechanism underneath it. ADR-0002 is likewise not
superseded: its decision was files for transcripts and SQLite for the clinical record, and only the
named implementation of the file half changes here.

## Decision

**Drop the Strands Agents SDK. `agent/` is written by hand and stays provider-agnostic.**

**`agent/models.py` keeps its role and its contract.** One `build_model()` reading
`PREVENTIA_MODEL_PROVIDER`, returning a client that exposes a single uniform send method over
messages and tool definitions. Anthropic, Ollama and the OpenAI-compatible Moonshot endpoint are
reached through their own SDKs behind that seam. No module outside `agent/models.py` imports a
provider, which is the invariant ADR-0001 established and this ADR preserves.

**A deterministic orchestrator owns the turn.** `agent/core.py` exposes `handle_turn(patient_id,
text)` and runs the clinical steps as plain functions in a fixed order. The model does not choose
that order and cannot skip a step.

```python
def handle_turn(patient_id, text):
    reply = tool_loop(history(patient_id), text, TOOLS, max_steps=4)
    facts = extract(text)
    color = raise_only(semaforo(facts), model_hint(facts))
    record.write(patient_id, facts, color)
    if color is Color.RED:
        triage.push(patient_id, color, summary(patient_id))
    return reply
```

**The tool loop is bounded at four steps.** A model that keeps requesting tools past the cap gets the
loop closed and answers with what it has. An unbounded loop is a way for a confused model to burn the
demo window.

**`semaforo`, `raise_only`, `extract`, `record.write` and `triage.push` are not tools.** They are
called by the orchestrator, never exposed to the model, and therefore never subject to the model
deciding to omit one. This is what makes the ADR-0004 claim enforceable at the agent layer as well as
inside the semáforo.

**Two tools at the outset.** `read_ficha`, read-only against the clinical record, and `send_message`.
Further tools are added when a named need appears, not in advance.

**`send_message` is provider-agnostic and runs the guardrail inside itself.**

```python
def send_message(text):
    safe = guardrails.filter(text) or guardrails.REDIRECT
    channel.deliver(safe)
    return "sent"
```

It calls the channel adapter, never a WhatsApp client, so the seam in section 3 of `CLAUDE.md`
holds and the local console channel works unchanged. Because the model may call it more than once in
a turn, the guardrail lives inside the tool rather than around the orchestrator's return value.
Every outbound path to the patient passes `guardrails.filter` exactly once, and
`tests/test_guardrails.py` covers the tool, not only the filter.

**`agent/sessions.py` replaces `FileSessionManager`.** One append-only JSONL file per patient under a
sessions directory, with `append(patient_id, role, text)` and `history(patient_id, limit)`.

```
sessions/patient-0007.jsonl
{"ts": "...", "role": "patient", "text": "..."}
{"ts": "...", "role": "agent", "text": "..."}
```

Transcripts stay out of SQLite, which is ADR-0002's decision and is unchanged.

**MCP is not installed.** The Lab's curated datasets are reached through `data/caja_adapter.py` per
ADR-0007. If a Lab server turns out to expose something a live patient conversation needs, the
official `mcp` Python SDK is added then and registered as one more source of tool definitions in the
same bounded loop.

**The dependency line changes.** `pip install 'strands-agents[ollama,openai,anthropic]'` becomes the
three provider SDKs directly. `CLAUDE.md` sections 3, 4 and 5 are stale as of this ADR and must be
updated to match.

## Consequences

- The largest schedule risk in ADR-0001 is removed. There is no framework whose behaviour has to be
  learned during the two days, and every failure lands in code the team wrote.
- The tool loop, the session store and the provider adapters are now ours to write and ours to debug.
  This is the cost, and it is real, but it is bounded and known rather than unbounded and unknown.
- The clinical claim gets stronger. With the semáforo, the guardrail, extraction and persistence
  outside the tool surface, "no model output can downgrade a red flag" and "every outbound message is
  filtered" are both properties of the control flow rather than properties of the prompt.
- `send_message` being a tool means the model can send more than once per turn. That is deliberate,
  and it is why the guardrail sits inside the tool. It also means a bug in that one function is a bug
  in the only thing standing between the model and the patient, so it is the highest-value test
  target in the repository.
- The deployment story is unchanged and marginally simpler. Provider swap remains one environment
  variable, with three small adapters instead of a framework's provider registry.
- Live consumption of Lab MCP servers is not demonstrated. If the rubric rewards it, the pitch cannot
  claim it, and the honest statement is that the Lab data was ingested offline through an adapter.
- The bounded loop can truncate. A model that needed a fifth step answers with incomplete context
  rather than failing loudly, which is the right trade in front of a patient and the wrong one in a
  test. `tests/` should cover the truncation path explicitly.

## Alternatives considered

**Keep Strands.** Costs nothing to leave in place, and it is what ADR-0001 already decided. Rejected
because it is now paying for one thing rather than three, that thing is a four-step loop over two
local functions, and the framework's unlearned failure modes stay on the critical path through demo
day.

**Keep Strands installed solely for `FileSessionManager`.** No rewrite of the session layer at all.
Rejected because it leaves the dependency, its install weight and its version surface in a project
whose pitch claims a small deployable surface, in exchange for roughly forty lines.

**Let an unbounded tool loop own the whole turn, with `set_color` and `escalate` as tools.** Closest
to ADR-0001's intent and the most flexible. Rejected because it hands control flow to the model at
precisely the points ADR-0004 and ADR-0005 exist to keep deterministic, and because the sentence a
clinical judge is being asked to accept stops being provable by reading `handle_turn`.

**Move transcripts into SQLite and drop the file store entirely.** One store instead of two, and the
longitudinal summary becomes a query. Rejected because ADR-0002 decided against it in terms, and
because it puts free-text patient speech into the database the no-PII rule guards.

**Adopt the `mcp` SDK now and wire it in Phase 1.** Buys certainty that the integration works before
demo day. Rejected because no named tool currently requires it, and the time it costs comes out of
the definition-of-done list in section 12.
